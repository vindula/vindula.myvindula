# coding: utf-8
from Acquisition import aq_inner
from five import grok
from Products.CMFCore.interfaces import ISiteRoot
from zope.interface import Interface
from plone.uuid.interfaces import IUUID

from plone.registry.interfaces import IRegistry
from plone.app.discussion.interfaces import IDiscussionSettings
from zope.component import getUtility, queryUtility
from Products.TinyMCE.interfaces.utility import ITinyMCE

from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

#from plone.directives import form
from vindula.myvindula import MessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

from datetime import date, datetime, timedelta
from DateTime.DateTime import DateTime
import calendar, logging, base64, pickle

from vindula.myvindula.user import BaseFunc, ModelsFuncDetails



from vindula.myvindula.registration import SchemaFunc, SchemaConfgMyvindula
                                   
from vindula.controlpanel.browser.models import ModelsCompanyInformation
from vindula.chat.utils.models import ModelsUserOpenFire

from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.myvindula.models.instance_funcdetail import ModelsInstanceFuncdetails

from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula
from vindula.myvindula.models.department import ModelsDepartment
from vindula.myvindula.models.howareu import ModelsMyvindulaHowareu
from vindula.myvindula.models.comments import ModelsMyvindulaComments
from vindula.myvindula.models.like import ModelsMyvindulaLike
from vindula.myvindula.models.funcdetail_couses import ModelsMyvindulaFuncdetailCouses
from vindula.myvindula.models.courses import ModelsMyvindulaCourses
from vindula.myvindula.models.funcdetail_languages import ModelsMyvindulaFuncdetailLanguages
from vindula.myvindula.models.languages import ModelsMyvindulaLanguages
from vindula.myvindula.models.recados import ModelsMyvindulaRecados

from vindula.myvindula.models.holerite import ModelsFuncHolerite
from vindula.myvindula.models.descricao_holerite import ModelsFuncHoleriteDescricao

from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
from vindula.myvindula.models.instance_funcdetail import ModelsInstanceFuncdetails


from vindula.controlpanel.handlers import userLogged

logger = logging.getLogger('vindula.myvindula')

def por_admicao(item):
    return item.get('admission_date','')


class MyVindulaView(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula')

    
    def get_howareu(self, user):
        D={}
        D['username'] = user
        return ModelsMyvindulaHowareu().get_myvindula_howareu(**D)

    def get_department(self):
        return ModelsDepartment().get_department()

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

#Views de renderização das imagem do howareu ---------------------------------------------------   
class VindulahowareuImage(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('howareu-image')
    
    def render(self):
        pass
    
    def update(self):
        form = self.request.form
        if 'id' in form.keys():
            id = form.get('id','0')
            if id != 'None':
                campo_image = ModelsMyvindulaHowareu().get_myvindula_howareu_By_Id(id)
                valor = campo_image.upload_image
                x = self.decodePickle(valor)
                
                self.request.response.setHeader("Content-Type", "image/jpeg", 0)
                self.request.response.write(x)                

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
    
    def load_form(self):
        form = self.request.form
        membership = self.context.portal_membership
        user_login = membership.getAuthenticatedMember().getUserName()
        permissao = self.checa_login()
        
        if 'user' in form.keys() and not'newuser' in form.keys() and permissao:
            user_cod = self.Convert_utf8(self.decodeUser(form.get('user','')))
            return SchemaFunc().registration_processes(self, user_cod, True)
        
        elif 'newuser' in form.keys() and self.checa_login():
            return SchemaFunc().registration_processes(self, '', True)    
        
        else:    
            return SchemaFunc().registration_processes(self, user_login, False)

    
    def get_ConfugCampos(self, campo):
        configuracao= ModelsConfgMyvindula().getConfig_edit(campo)
        return configuracao
    
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
    
    def get_ConfugCampos(self, campo):
        configuracao= ModelsConfgMyvindula().getConfig_views(campo)
        return configuracao
        
    def get_department(self, user):
        return ModelsDepartment().get_departmentByUsername(self.Convert_utf8(user))     

    def load_list(self):
        member =  self.context.restrictedTraverse('@@plone_portal_state').member().getUserName();
        user = self.Convert_utf8(self.request.form.get('user',str(member)))
        #return ModelsFuncDetails().get_FuncDetails(unicode(user, 'utf-8'))
        return ModelsInstanceFuncdetails().get_InstanceFuncdetails(user)


    def geraDadosAreas(self,area,instanceUser):
        campos = ModelsConfgMyvindula().getConfig_byArea(self.Convert_utf8(area))
        L = []
        for campo in campos:
            D = {}
            D['label'] = campo.label
            try:
                valor = self.getDadoUser_byField(instanceUser, campo.fields)
                if type(valor) == list:
                    valor_list = ''
                    for i in valor:
                        if i :valor_list += (i + ' / ') 
                    
                    valor = "<span>"+valor_list+"</span>"
                
                elif campo.type == 'img':
                    site = self.context.portal_url.getPortalObject()
                    valor = "<img height='150px' src='%s/user-image?field=%s&instance_id=%s' />"%(site.absolute_url(),campo.fields,instanceUser.id)
                
                D['data']  = valor
            except:
                D['data'] = ''
        
            L.append(D)
        
        return L 

    def getAreasDinamicas(self):
        areas = [{'id':'contact',
                  'title':'Contato',
                  'url_image': self.static()+'/images/user_contact.png'},
                  {'id':'corporate',
                   'title':'Corporativo',
                   'url_image': self.static()+'/images/user_business.png'},
                  {'id':'other',
                   'title':'Outras Informações',
                   'url_image': self.static()+'/images/user_others.png'}
                 ]
        
        site = self.context.portal_url.getPortalObject()
        pw = site.portal_workflow
        if 'control-panel-objects' in  site.keys():
            control = site['control-panel-objects']
            if 'fieldset-myvindula' in control.keys():
                folder_Areas = control['fieldset-myvindula']
                for item in folder_Areas.objectValues():
                     
                    if pw.getInfoFor(item,'review_state') == 'published':
                        D={}
                        D['id'] = item.getId()
                        D['title'] = item.Title()
                        if item.getLogo():
                            D['url_image'] = item.getLogo().absolute_url()
                        else:
                            D['url_image'] = ''
                    
                        areas.append(D)
                        
                return areas
            else:
                return areas
        else:
            return areas
    
    
    def get_campos(self):
        fields = ModelsConfgMyvindula().get_configurationAll()
        conf = {}
        for campos in fields:
            item = campos.fields
            dado = ModelsConfgMyvindula().getConfig_edit(item)
            conf[item] = dado
       
        return conf
    

    def get_howareu(self, user):
        member =  self.context.restrictedTraverse('@@plone_portal_state').member().getUserName();
        user = self.request.form.get('user',str(member))
        D={}
        D['username'] = user
        return ModelsMyvindulaHowareu().get_myvindula_howareu(**D)
    
    
    def get_recados(self, user):
        D={}
        D['destination'] = user
        return ModelsMyvindulaRecados().get_myvindula_recados(**D)
    
    

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


class MyVindulaListRecados(grok.View,UtilMyvindula):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('myvindulalistrecados')

    def get_recados(self, user):
        D={}
        D['destination'] = user
        return ModelsMyvindulaRecados().get_myvindula_recados(**D)

    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        
        if not open_for_anonymousUser:
            form = self.request.form
            excluir = form.get('form.excluir', False)
        
            if excluir:
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
   

#class MyVindulaListMyContent(grok.View):
#    grok.context(Interface)
#    grok.require('zope2.View')
#    grok.name('myvindula-meus-conteudos')
#    
#    def load_list(self):        
#        membership = self.context.portal_membership
#        user_login = membership.getAuthenticatedMember()
#        
#        if user_login.getUserName():
#            ctool = getSite().portal_catalog
#            items = ctool(path = {'query': '/', 'depth': 99},
#                          Creator=user_login.getId())        
#        
#            return items
#            
#        else:
#            self.request.response.redirect(self.context.absolute_url() + '/login')


    
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
                  if data.__getattribute__('name') == member.getAuthenticatedMember().getUserName():
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
        try: user = self.to_utf8(member.getAuthenticatedMember().getUserName())
        except: user =  member.getAuthenticatedMember().getUserName()
        data = ModelsUserOpenFire().get_UserOpenFire_by_username(user)
        if data:
            return True
        else:
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
        
        return ModelsDepartment().get_departmentByUsername(user)     
        
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

        if like_user:
            if data_like.count()>2:
                html = '<span > Você e mais '+str(data_like.count()-1)+' pessoas já curtiram isso.</span>'
            
            elif data_like.count()==2:
                html = '<span >Você e mais uma pessoa curtiram isso.</span>'
             
            elif data_like.count()==1:
                html = '<span >Você curtiu isso.</span>'
            
            html += '<span class="link" id="'+form['id_obj']+'" src="True">(Desfazer Curtir)</span>'
                
        else:
            if data_like.count()>1:
                html = '<span>'+str(data_like.count())+' pessoas já curtiram isso.</span>'
            
            elif data_like.count()==1:
                html =  '<span>'+ str(data_like.count())+' pessoa curtiu isso.</span>'
        
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
               


class MyVindulaFindHoleriteView(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('vindula.UserLogado')
    grok.name('myvindula-find-holerite')
    
    def get_descricao_holerite(self, id_holerite):
        result = ModelsFuncHoleriteDescricao().get_FuncHoleriteDescricoes_byid(id_holerite)
        if result: 
            return result
        else:
            return [] 
    
    def load_list(self):
        form = self.request.form
        session = self.context.REQUEST.SESSION
        if 'cpf' in session.keys() and 'id' in form.keys():
            try:cpf = unicode(session.get('cpf', ''),'utf-8')
            except:cpf = session.get('cpf', '')
            
            id = int(form.get('id','0'))
            
            return ModelsFuncHolerite().get_FuncHolerites_byCPFAndID(cpf, id)
        
class MyVindulaHoleriteView(grok.View, UtilMyvindula):
    grok.context(ISiteRoot)
    grok.require('vindula.UserLogado')
    grok.name('myvindula-holerite')
    
    def get_descricao_holerite(self, id_holerite):
        result = ModelsFuncHoleriteDescricao().get_FuncHoleriteDescricoes_byid(id_holerite)
        if result: 
            return result
        else:
            return [] 
    
    def load_list(self):
        session = self.context.REQUEST.SESSION
        result = []
        if 'cpf' in session.keys():
            cpf = session.get('cpf')
        else:
            membership = self.context.portal_membership
            user_login = membership.getAuthenticatedMember()
            user = str(user_login.getUserName())
            prefs_user = self.get_prefs_user(user)
            if prefs_user:
                cpf = prefs_user.get('cpf','')
        
        if cpf:
            holerites = ModelsFuncHolerite().get_FuncHolerites_byCPF(cpf)
            D = {}
            if holerites:
                if holerites.count() > 1:
                    D['select'] = holerites 
                    D['data'] = holerites.last() 
                    result =  D
                else:
                    D['select'] = []
                    D['data'] = holerites.one() 
                    result = D

        return result
    
    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')
            
    def validateUser(self):
        cpf_valid = False
        request = self.context.REQUEST
        
        if 'cpf' not in request.SESSION.keys():
            if 'cpf_validate' in request.keys():
                cpf_valid = self.CPFValid(request)
                if not cpf_valid:
                    IStatusMessage(self.request).addStatusMessage(_(u'CPF não é valido.'),"error")
        elif 'cpf_time' in request.SESSION.keys():
            if request.SESSION.get('cpf_time') < datetime.now() - timedelta(minutes=10):
                if 'cpf_validate' in request.keys():
                    cpf_valid = self.CPFValid(request)
                    if not cpf_valid:
                        IStatusMessage(self.request).addStatusMessage(_(u'CPF não é valido.'),"error")
            else:
                cpf_valid = True
        else:
            cpf_valid = True

        return cpf_valid
    
    def CPFValid(self, request):
        membership = self.context.portal_membership
        user_login = membership.getAuthenticatedMember()
        user = str(user_login.getUserName())
        prefs_user = self.get_prefs_user(user)
        if prefs_user:
            cpf = prefs_user.get('cpf')
            cpf_validate = request.get('cpf_validate').replace('.', '').replace('-', '')
            if cpf == cpf_validate:
                request.SESSION['cpf'] = cpf
                request.SESSION['cpf_time'] = datetime.now()
                return True
            
        return False
        
            
class MyVindulaPrintHoleriteView(grok.View, UtilMyvindula):
    grok.context(ISiteRoot)
    grok.require('vindula.UserLogado')
    grok.name('imprimir-holerite')
    
    def get_descricao_holerite(self, id_holerite):
        result = ModelsFuncHoleriteDescricao().get_FuncHoleriteDescricoes_byid(id_holerite)
        if result: 
            return result
        else:
            return [] 
    
    def load_list(self):
        form = self.request.form
        
        membership = self.context.portal_membership
        user_login = membership.getAuthenticatedMember()
        prefs_user = self.get_prefs_user(user_login.getUserName())
        
        if prefs_user and 'id' in form.keys():

            try:cpf = unicode(prefs_user.get('cpf',''),'utf-8')
            except:cpf = prefs_user.get('cpf','')
            
            id = int(form.get('id','0'))
                
            return ModelsFuncHolerite().get_FuncHolerites_byCPFAndID(cpf, id)      
        
    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')
        
