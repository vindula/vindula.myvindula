# coding: utf-8
import StringIO
import calendar, logging, pickle
import os
from datetime import date, datetime

from Acquisition import aq_inner
from DateTime.DateTime import DateTime
from PIL import Image
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.statusmessages.interfaces import IStatusMessage
from five import grok
from plone.app.discussion.interfaces import IDiscussionSettings
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from vindula.content.models.content import ModelsContent
from vindula.controlpanel.browser.models import ModelsCompanyInformation
from vindula.controlpanel.handlers import userLogged
from zExceptions import NotFound
from zope.app.component.hooks import getSite
from zope.component import getUtility, queryUtility
from zope.interface import Interface

from vindula.myvindula import MessageFactory as _
from vindula.myvindula.models.comments import ModelsMyvindulaComments
from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula
from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
from vindula.myvindula.models.fieldcategory import FieldCategory
from vindula.myvindula.models.follow import ModelsFollow
from vindula.myvindula.models.funcdetails import FuncDetails
from vindula.myvindula.models.howareu import ModelsMyvindulaHowareu
from vindula.myvindula.models.like import ModelsMyvindulaLike
from vindula.myvindula.models.notification import ModelsMyvindulaNotificacao
from vindula.myvindula.models.recados import ModelsMyvindulaRecados
from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.myvindula.user import BaseFunc


logger = logging.getLogger('vindula.myvindula')

def por_admicao(item):
    return item.get('admission_date','')


class MyVindulaView(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula')

    action_social = {'Like': ' curtiu ',
                     'Comment': ' comentou ',
                     'Share' : ' compartilhou ',
                     'Follow' : ' assinou ',
                     'History' : ' atualizou ',}

    def get_howareu(self, user):
        D={}
        D['username'] = user
        return ModelsMyvindulaHowareu().get_myvindula_howareu(**D)

    def count_recados_new(self, username):
        return ModelsMyvindulaRecados().cont_recados_new(username)

    def get_recados(self,username):
        return ModelsMyvindulaRecados().get_myvindula_recados(receiver=username,destination=username)[:5]
    
    def count_notificacao_new(self, username):
        return ModelsMyvindulaNotificacao().cont_notificacao_new(username)

    def get_notificacoes(self,username, limit=5):
        query = 'result = ModelsMyvindulaNotificacao().get_myvindula_notificacao(username=username)'
        if limit:
            query += '[:5]'
        
        exec(query)
        if result.count():
            return self.rs_to_list(result)
        else:
            return []

    def name_user_top(self,full_name):
        limit = 12
        str = full_name

        while str > limit and len(str.split(' ')) > 1:
            str = ' '.join(str.split(' ')[:-1])

        return str
    
    def getOnlySubjectMessag(self,text):
        if (text.find('<br />') != -1):
            return text[:text.find('<br />')]
        return text

    def checkHomeFolder(self):
        """ Check if exist homeFolder """
        homefolder = self.context.portal_membership.getHomeFolder()
        if homefolder:
            return True
        else:
            return False

    def getConfTyneMCE(self):
        utility = getUtility(ITinyMCE)
        conf = utility.getConfiguration(context=self.context,
                                        field='text',
                                        request=self.request)
        return conf


    def update(self):
        """ Receive itself from request and do some actions """
        form = self.request.form
        submitted = form.get('form.submitted', False)
        excluir = eval(form.get('form_excluir', 'False'))

        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();

        if not open_for_anonymousUser:
            if submitted:
                #visible_area = form.get('visible_area')
                text = form.get('text')

                #if not eval(visible_area):
                #    form['visible_area'] = form.get('departamento','0')
                if text == '':
                    IStatusMessage(self.request).addStatusMessage(_(u'Não é possível postar um pensamento em branco.'),"info")
                    return False
                upload_foto = form.get('upload_image')
                if upload_foto:
                    data = upload_foto.read()
                    if len(data) != 0 :
                        form['upload_image'] = pickle.dumps(data)
                    else:
                        form['upload_image'] = ''
                else:
                    form['upload_image'] = ''
                ModelsMyvindulaHowareu().set_myvindula_howareu(**form)

            elif excluir:
                id_howareu = int(form.get('id_howareu','0'))
                ModelsMyvindulaHowareu().del_myvindula_howareu(id_howareu)

        else:
            self.request.response.redirect(self.context.absolute_url() + '/login')
            
    def convertResultSetToList(self, result_set):
        return [i for i in result_set]

#Views de renderização das imagem do howareu ---------------------------------------------------
class VindulahowareuImage(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('howareu-image')

    def render(self):
        pass

    def update(self):
        form = self.request.form
        buffer = ''

        if 'id' in form.keys():
            id = form.get('id','0')
            if id != 'None':
                campo_image = ModelsMyvindulaHowareu().get_myvindula_howareu_By_Id(id)

                valor = campo_image.upload_image_small

                if not valor:
                    image_origin = campo_image.upload_image
                    data = self.decodePickle(image_origin)

                    img_org = Image.open(StringIO.StringIO(data))
                    # verifica se a imagem é maior que o máximo permitido
                    tamMax = (640.0,440.0)
                    imgSize = img_org.size
                    if (imgSize[0] > tamMax[0]) or (imgSize[1] > tamMax[1]):
                        #verifica se a largura é maior que a altura
                        if (imgSize[0] > imgSize[1]):
                            novaLargura = tamMax[0]
                            novaAltura = round((novaLargura / imgSize[0]) * imgSize[1])
                        elif (imgSize[1] > imgSize[0]):
                            #se a altura for maior que a largura
                            novaAltura = tamMax[1]
                            novaLargura = round((novaAltura / imgSize[1]) * imgSize[0])
                        else:
                            #altura == largura
                            novaAltura = novaLargura = max(tamMax)

                        img_org.thumbnail((novaLargura, novaAltura), Image.ANTIALIAS)

                    imagefile = StringIO.StringIO()
                    img_org.save(imagefile,'JPEG')
                    buffer = imagefile.getvalue()

                    new_image = self.encodePickle(buffer)
                    ModelsMyvindulaHowareu().set_howareu_image_small(campo_image,new_image)

                else:
                    buffer = self.decodePickle(valor)

        self.request.response.setHeader("Content-Type", "image/jpeg", 0)
        self.request.response.write(buffer)

class VindulaHowAreUListAll(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('howareu-list-all')

    def load_dados(self):
         result =  ModelsMyvindulaHowareu().get_myvindula_howareu()

         if result:
             return self.rs_to_list(result)
         else:
             return []

    def update(self):
        """ Receive itself from request and do some actions """
        form = self.request.form
        excluir = form.get('form.excluir', False)

        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();

        if not open_for_anonymousUser:
            if excluir:
                id_howareu = int(form.get('id_howareu','0'))
                ModelsMyvindulaHowareu().del_myvindula_howareu(id_howareu)

                IStatusMessage(self.request).addStatusMessage(_(u'Registro removido com sucesso.'),"info")

        else:
            self.request.response.redirect(self.context.absolute_url() + '/login')


class MyVindulaPanelView(grok.View,UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindulapanel')

    def _checkPermission(self, permission, context):
        mt = getToolByName(context, 'portal_membership')
        return mt.checkPermission(permission, context)

    def checkEveron(self,variavel):
        environ = os.environ
        return environ.get(variavel,False)


    def getPersonalInfoLink(self):
        """ Get the link for vindula home """

        context = aq_inner(self.context)
        template = None
        if self._checkPermission('Set own properties', context):
            template = '@@myvindulapanel?section=myvindula'
        return template

    def getPersonalPrefsLink(self):
        """ Get the link for user preferences """

        context = aq_inner(self.context)
        template = None
        if self._checkPermission('Set own properties', context):
            template = '@@myvindulapanel?section=myvindulaprefs'
        return template


class MyVindulaRecursosHumanosView(grok.View, UtilMyvindula):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('myvindula-recursos-humanos')

    def getMacro(self,link='myvindula-documents'):
        if 'id' in self.request.keys():
            set_macro = self.request['id']
            return 'context/'+ set_macro +'/macros/page'
        else:
            return 'context/'+link+'/macros/page'

    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();

        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')

class MyVindulaPrefsView(grok.View, BaseFunc):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('myvindulaprefs')

    ignoreContext = True
    label = _(u"Personal Information")
    description = _(u"Change your available information below.")

    def check_edit_manager(self,username):
        check_permission =  self.context.restrictedTraverse('vindula-object-user').checkPermission(username)
        if 'rh' in check_permission.get('groups') or check_permission.get('has_manager'):
            return True
        return False

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)
        #return super(MyVindulaPrefsView, self).update()
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')

class MyVindulaListUser(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindulalistuser')

    black_list = ['name','vin_myvindula_department','photograph',\
                  'about','unidadeprincipal','atividades','biografia','hide_birthday','show_phone']

    def __init__(self,context,request):
        super(MyVindulaListUser, self).__init__(context,request)


    def get_ConfugCampos(self, campo):
        configuracao= ModelsConfgMyvindula().getConfig_views(campo)
        return configuracao

    def check_edit_manager(self,username):
        check_permission =  self.context.restrictedTraverse('vindula-object-user').checkPermission(username)
        if 'rh_' in str(check_permission.get('groups')) or check_permission.get('has_manager'):
            return True
        return False

    def load_list(self):
        member =  self.context.restrictedTraverse('@@plone_portal_state').member().getUserName();
        user = self.Convert_utf8(self.request.form.get('user', str(member)))

        p_membership = getToolByName(self.context, 'portal_membership')
        user = p_membership.getMemberById(user)

        if not user:
            raise NotFound, 'Usuário nao encontrado'

        return self.get_prefs_user(user.getUserName())

    def get_follow(self, username, followers=True):
        items = []
        result = []

        if followers:
            items = ModelsFollow.get_followers(self.Convert_utf8(username))
        else:
            items = ModelsFollow.get_followings(self.Convert_utf8(username))
                        
        for item in  items:
            user = None
            if followers:
                user = FuncDetails(item.username)
            else:
                content = self.get_content_by_id(item.content_id)
                if content:
                    if content.type == 'UserObject':
                        user = FuncDetails(content.uid)
                        item = content
            
            if user and not user.is_deleted():
                result.append(item)
        return result
        
    def get_content_by_id(self,content_id):
        content_obj = ModelsContent().getContent_by_id(content_id)
        if content_obj:
            return content_obj

    def format_follow(self, obj_list, qtd=9):
        lista = []
        L = None
        for count, obj in enumerate(obj_list):
            if count == 0 or count % qtd == 0:
                L = []

            L.append(obj)

            if (count + 1) % qtd == 0:
                lista.append(L)
                L = None

        if L:
            lista.append(L)

        return lista
    
    def get_projects(self, user):
        p_catalog = getToolByName(self.context, 'portal_catalog')
        p_object = self.context.portal_url.getPortalObject()
        departaments = user.get_department()
        result = []

        if departaments:
            departaments = [i.get('obj').UID() for i in departaments if i.get('obj', None)]
            projects = p_catalog({'path': {'query': '/'.join(p_object.getPhysicalPath()), 'depth': 99},
                                  'portal_type': ['OrganizationalStructure'],
                                  'tipounidade': ['projeto', 'Projeto']})
            for project in projects:
                if project.UID in departaments:
                    result.append(project.getObject())

        return result
    
    def getProfileLayout(self):
        portal = self.context.portal_url.getPortalObject()
        cpanel_objects = portal.get('control-panel-objects')
        if cpanel_objects:
            v_categories = cpanel_objects.get('vindula_categories')
            if v_categories:
                return v_categories.profile_layout
        
    def get_fields_category(self):
        data = FieldCategory().store.find(FieldCategory).order_by(FieldCategory.order_position)
        return data

    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();

        if not open_for_anonymousUser:
            form = self.request.form
            submitted = form.get('form.submitted', False)

            excluir_howareu = form.get('form.excluir.howareu', False)
            excluir_recados = form.get('form.excluir.recados', False)

            if submitted:
                return  ModelsMyvindulaRecados().set_myvindula_recados(**form)

            elif excluir_howareu:
                id_howareu = int(form.get('id_howareu','0'))
                ModelsMyvindulaHowareu().del_myvindula_howareu(id_howareu)

                IStatusMessage(self.request).addStatusMessage(_(u'Registro removido com sucesso.'),"info")

            elif excluir_recados:
                id_recado = int(form.get('id_recado','0'))
                ModelsMyvindulaRecados().del_myvindula_recados(id_recado)

                IStatusMessage(self.request).addStatusMessage(_(u'Registro removido com sucesso.'),"info")
        else:
            self.request.response.redirect(self.context.absolute_url() + '/login')


class MyVindulalistAll(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindulalistall')

    def load_list(self):
        form = self.request.form
        result = None
        config_muit_user = self.context.restrictedTraverse('@@myvindula-conf-userpanel').config_muit_user()
        filtro_busca = self.context.restrictedTraverse('@@myvindula-conf-userpanel').check_filtro_busca_user()

        if 'SearchSubmit' in form.keys():
            title = form.get('title','').strip()
            campos = eval(form.get('campos',"[{'name':title}]"))
            campo_departamento = form.get('filtro','departamentos').strip()
            departamento = form.get('departamento','')

            form_values = []
            for item in campos:
                D = {}
                name = item.keys()[0]
                value = item.values()[0].strip()
                D[name] = self.Convert_utf8(value)

                form_values.append(D)

            if campo_departamento != "departamentos":
                D = {}
                D[campo_departamento] = self.Convert_utf8(departamento)

                form_values.append(D)
                departamento = None
            else:
                departamento = self.Convert_utf8(departamento)

            check_form = [i for i in form_values if i.values()]
            if departamento or check_form:
                result = ModelsDadosFuncdetails().get_FuncBusca(departamento,form_values,filtro_busca)
                #result = self.rs_to_list(result)

        elif not config_muit_user or 'all' in form.keys():
            result = ModelsInstanceFuncdetails().get_AllFuncDetails()
#            if result_set:
#                    result = self.rs_to_list(result_set)

        return result

    def check_no_result(self):
        form = self.request.form
        if 'title' in form.keys():
            title = form.get('title','').strip()
            departamento= form.get('departamento','0')
            ramal = form.get('ramal','').strip()
            if title or departamento !='0' or ramal:
                return 'Não há resultados.'
        if 'SearchSubmit' in form.keys():
            return 'Digite um filtro para a busca.'
        else:
            return ''

    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')

class MyVindulaNewsEmployeeView(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-news-employee')

    def load_list(self):
        result = ModelsInstanceFuncdetails().get_AllFuncDetails()

        return sorted(result, key=por_admicao)


    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')


class MyVindulaFirstRegistreView(grok.View, UtilMyvindula):
    grok.context(ISiteRoot)
    grok.require('vindula.UserLogado')
    grok.name('myvindula-first-registre')

    def to_utf8(self,value):
        return unicode(value, 'utf-8')

    def load_list(self):
        form = self.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)

        continuar_url = self.context.absolute_url() + '/myvindulaprefs'
        voltar_url = self.context.absolute_url() + '/'

        if 'continuar' in form_keys:
            self.request.response.redirect(continuar_url)

        elif 'voltar' in form_keys:
            userLogged(self,False)

        else:
            result = ModelsCompanyInformation().get_CompanyInformation()
            if result:
                return result[0]
            else:
                return {}

    def checkCampoVazio(self,campo):
          member = getSite().portal_membership
          data = self.get_prefs_user(member.getAuthenticatedMember().getUserName())
          if data:
              if campo == 'name':
                  if data.get('name') == member.getAuthenticatedMember().getUserName():
                      return True

              elif data.__getattribute__(campo):
                  # Campo Não Esta vazio
                  return False

              else:
                  # Campo Esta vazio
                  return True
          else:
              # Campo Esta vazio
              return True

    def checkUserXMPP(self):
        member = getSite().portal_membership
        # try: user = self.to_utf8(member.getAuthenticatedMember().getUserName())
        # except: user =  member.getAuthenticatedMember().getUserName()
        # data = ModelsUserOpenFire().get_UserOpenFire_by_username(user)
        # if data:
        #     return True
        # else:
        return False


    def get_saldacao(self):
        hora = datetime.now().strftime('%H')
        if hora > '17':
            return 'Boa noite, '
        elif hora > '12':
            return 'Boa tarde, '
        else:
            return 'Bom dia, '

    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')


class MyVindulaListBirthdays(grok.View,UtilMyvindula):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('myvindulalistbirthdays')

    def nome_filtro(self):
        filtro = self.request.form.get('filtro',1)
        if filtro == '1':
            return "do Dia"
        elif filtro == '7':
            return "da Semana"
        elif filtro == '30':
            return "do Mês"
        else:
            return ''

    def get_department(self, user):
        try:
            user_id = unicode(user, 'utf-8')
        except:
            user_id = user

        return 'TODO mudar'
        # return ModelsDepartment().get_departmentByUsername(user)

    def get_campos_list_user(self):
        if 'control-panel-objects' in  getSite().keys():
            control = getSite()['control-panel-objects']
            if 'vindula_aniversariantesconfig' in control.keys():
                list = control['vindula_aniversariantesconfig']
            else:
                list = None

        if list:
            lines = list.list_campos_user.splitlines()
            L = []

            for line in lines:
                D = {}
                line = line.replace('[', '').replace(']', '').split(' | ')
                try:D['label'] = line[0]
                except:D['label'] = ''

                try:D['content'] = line[1]
                except:D['content'] = ''

                L.append(D)
            return L

    def get_birthdaysToday(self, type_filter):
        results = []
        if type_filter == 1:
            date_start = date.today().strftime('%Y-%m-%d')
            date_end = date.today().strftime('%Y-%m-%d')

            results = ModelsDadosFuncdetails().get_FuncBirthdays(date_start,date_end)

        elif type_filter == 7:
            now = DateTime()
            dow = now.dow()
            date_start = (now - dow).strftime('%Y-%m-%d')
            date_end = (now - dow + 6).strftime('%Y-%m-%d')

            results = ModelsDadosFuncdetails().get_FuncBirthdays(date_start,date_end)

        elif type_filter == 30:
            now = DateTime()

            dia = calendar.monthrange(now.year(),now.month())[1]
            date_start = now.strftime('%Y-%m-1')
            date_end = now.strftime('%Y-%m-'+str(dia))

            results = ModelsDadosFuncdetails().get_FuncBirthdays(date_start,date_end)

        elif type_filter == 'prox':
            results = ModelsDadosFuncdetails().get_FuncBirthdays('','','proximo')

        if results:
            return results #results[:int(quant)]
        else:
            return []

    def load_list(self):
        form = self.request.form
#        ch = Cache()
        filtro = form.get('filtro',1)
        if filtro == 'prox':

            results = self.get_birthdaysToday(filtro)
        else:
            results = self.get_birthdaysToday(int(filtro))

        if results:
            return results
        else:
            return []


    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')


class MyVindulaLike(grok.View,UtilMyvindula):
    grok.context(ISiteRoot)
    grok.require('vindula.UserLogado')
    grok.name('myvindula-like')

    def render(self):
        membership = getSite().portal_membership
        form = self.request.form
        member = membership.getAuthenticatedMember()
        view_like = self.context.restrictedTraverse('@@myvindula-comments')

        data_like = view_like.get_like(form['id_obj'],form['type']);
        like_user = data_like.find(username=unicode(member.getUserName())).count()
        html = ''

        if eval(form.get('isPlone','False')):
            html += '<div id="%s">' %(form.get('id_obj'))
            html += '<input type="hidden" value="True" id="isPlone" name="isPlone:boolean">'
            html += '<input type="hidden" value="%s" id="type" name="type"></div>' %(form.get('type',''))

        if like_user:
            if data_like.count()>2:
                html += '<span > Você e mais '+str(data_like.count()-1)+' pessoas já curtiram isso.</span>'

            elif data_like.count()==2:
                html += '<span >Você e mais uma pessoa curtiram isso.</span>'

            elif data_like.count()==1:
                html += '<span >Você curtiu isso.</span>'

            html += '<span class="link" id="'+form['id_obj']+'" src="True">(Desfazer Curtir)</span>'

        else:
            if data_like.count()>1:
                html += '<span>'+str(data_like.count())+' pessoas já curtiram isso.</span>'

            elif data_like.count()==1:
                html +=  '<span>'+ str(data_like.count())+' pessoa curtiu isso.</span>'

            html += '<span class="link" id="'+form['id_obj']+'">(Curtir)</span>'

        return html

    def update(self):
        """ Receive itself from request and do some actions """
        member = getSite().portal_membership
        form = self.request.form
        dislike = form.get('dislike','False')
        self.id_like = 0
        self.excluir = False

        if not member.isAnonymousUser():
            form['username'] = member.getAuthenticatedMember().getUserName()
            if eval(dislike):
                ModelsMyvindulaLike().del_myvindula_like(**form)

            else:
                ModelsMyvindulaLike().set_myvindula_like(**form)


class MyVindulaComments(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-comments')

    def get_UID(self):
        return IUUID(self.context)

    def discussionAllowed(self,conf_global, replies,conf_context):
        if conf_global:
            if replies:
                return True
            elif conf_context:
                return True
            else:
                return False
        else:
            if replies:
                return True
            else:
                return conf_global


    def is_discussion_allowed(self):
        # Fetch discussion registry
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings, check=False)

        # Check if discussion is allowed globally
        if not settings.globally_enabled:
            return False

        return True


    def get_comments(self,id,type):
        D={}
        D['id_obj'] = id
        D['type'] = type
        return ModelsMyvindulaComments().get_myvindula_comments(**D)

    def get_like(self,id,type_obj):
        D={}
        D['id_obj'] = id
        D['type'] = type_obj
        return ModelsMyvindulaLike().get_myvindula_like(**D)

    def get_sigle_comments(self):
        try:
            id = self.id_comment
            return ModelsMyvindulaComments().get_comments_byID(id)
        except:
            return None

    def is_discussion_allowed(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings, check=False)
        return settings.globally_enabled

    def update(self):
        """ Receive itself from request and do some actions """
        form = self.request.form
        submitted = eval(form.get('form_submitted_comment', 'False'))
        excluir = eval(form.get('form_excluir', 'False'))

        request = self.request.environ

        if 'HTTP_REFERER' in request:
            redirect = request.get('HTTP_REFERER',self.context.absolute_url())
        else:
            redirect = self.context.absolute_url()

        if submitted:
            member = getSite().portal_membership
            if not member.isAnonymousUser():
                form['username'] = member.getAuthenticatedMember().getUserName()
                form['ip'] = self.get_ip(self.request)

                self.id_comment = ModelsMyvindulaComments().set_myvindula_comments(**form)

        elif excluir:
            id_comments = int(form.get('id_comments','0'))
            ModelsMyvindulaComments().del_myvindula_comments(id_comments)



class MyVindulaHoleriteView(grok.View, UtilMyvindula):
    grok.context(ISiteRoot)
    grok.require('vindula.UserLogado')
    grok.name('myvindula-holerite')

    url_frame = '%s/vindula-api/rh/holerite/%s/%s/?iframe_id=2942e8d4dc2af485405cb70f936847df'

    def get_url_frame(self):
        url = self.context.portal_url()
        modelo =  self.context.restrictedTraverse('myvindula-conf-userpanel').select_modelo_holerite()
        user_token = self.request.SESSION.get('user_token')

        return self.url_frame %(url,user_token,modelo)
    
