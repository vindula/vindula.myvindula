# -*- coding: utf-8 -*-
""" Liberiun Technologies Sistemas de Informação Ltda. """
""" Produto:                 """

from zope.interface import implements
from zope.formlib import form
from zope import schema

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from vindula.myvindula.user import BaseFunc
from vindula.myvindula.models.department import ModelsDepartment
from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
from vindula.myvindula.models.instance_funcdetail import  ModelsInstanceFuncdetails
from vindula.myvindula.tools.utils import UtilMyvindula

from vindula.myvindula.cache import Cache

class IPortletRamais(IPortletDataProvider):

    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    title_portlet = schema.TextLine(title=unicode("Título", 'utf-8'),
                                  description=unicode("Título que aparecerá no cabeçalho do portlet.", 'utf-8'),
                                  required=True)

    quantidade_portlet = schema.Int(title=unicode("Quantidade de Itens", 'utf-8'),
                                  description=unicode("Quantidade limite de item mostrado no portlet.", 'utf-8'),
                                  required=True)

    filtro_user = schema.Text(title=unicode("Bancos para busca de pessoas", 'utf-8'),
                              description=unicode("Adicione os campos que serão possiveis realizar a busca dos usuários como Nome, Empresa, Matricula e outros. \
                                                   Adicione um campo por linha, no formato [Label] | [Campo].", 'utf-8'),
                              default=u'[Nome] | [name]\n[Ramal] | [phone_number]',
                              required=True)


    filtro_departamento = schema.TextLine(title=unicode("Dados do campo departamento", 'utf-8'),
                                  description=unicode("Adicione qual dado do banco de dados será usado para filtro dos usuários,\
                                                      (Valor Padrão: 'departamentos')", 'utf-8'),
                                  default=unicode('departamentos','utf-8'),
                                  required=True)

    show_picture = schema.Bool(title=unicode("Exibir foto", 'utf-8'),
                               description=unicode("Selecione para mostrar a foto dos aniversarientes no portlet.", 'utf-8'),
                               default=True,
                               )

    show_anonymous = schema.Bool(title=unicode("Exibir portlet para anônimos", 'utf-8'),
                               description=unicode("Selecione para mostrar o portlet para usuários anônimos que acessarem o portal.", 'utf-8'),
                               default=True,
                               )

    active_vindula_contato_geral = schema.Bool(title=unicode("Altera o comportamento do portlet para buscar os contatos do portal", 'utf-8'),
                               description=unicode("Selecione para buscar os contados presente no portal.", 'utf-8'),
                               default=False,
                               )


    principal_user = schema.TextLine(title=unicode("Destaque do usuário", 'utf-8'),
                                     description=unicode("Adicione o campo com a informação principal do usuário como 'name' para Nome ou 'nickname' para\
                                                          Apelido, entre outros.", 'utf-8'),
                                     default = u'name',
                                     required=True)

    details_user = schema.Text(title=unicode("Detalhes do ramais", 'utf-8'),
                                  description=unicode("Adicione detalhes sobre os usuários como Empresa, Matricula e outros. \
                                                       Adicione um campo por linha, no formato [Label] | [Campo].", 'utf-8'),
                                  required=False)

    details_text = schema.Text(title=unicode("Texto do portlet", 'utf-8'),
                                  description=unicode("Adicione o texto que será mostrado no final da busca de ramais.", 'utf-8'),
                                  required=False)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IPortletRamais)

    # TODO: Add keyword parameters for configurable parameters here
    def __init__(self, title_portlet=u'', quantidade_portlet=u'', filtro_departamento=u'',filtro_user=u'',\
                 show_picture=u'', details_user=u'',details_text=u'',principal_user='',show_anonymous=u'',active_vindula_contato_geral=False):
       self.title_portlet = title_portlet
       self.quantidade_portlet = quantidade_portlet
       self.filtro_departamento = filtro_departamento
       self.filtro_user = filtro_user
       self.show_picture = show_picture
       self.show_anonymous = show_anonymous
       self.details_user = details_user
       self.details_text = details_text
       self.principal_user = principal_user
       self.active_vindula_contato_geral = active_vindula_contato_geral

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Portlet Busca de Pessoas"

class Renderer(base.Renderer, UtilMyvindula):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    render = ViewPageTemplateFile('portlet_ramais.pt')

    def get_title(self):
        return self.data.title_portlet

    def show_picture(self):
        return self.data.show_picture

    def show_anonymous(self):
        return self.data.show_anonymous

    @property
    def available(self):
        membership = self.context.portal_membership
        if membership.isAnonymousUser():
            if self.show_anonymous():
                return True
            else:
                return False
        else:
            return True


    def filtro_departamento(self):
        return self.data.filtro_departamento

    def get_details_text(self):
        return self.data.details_text


    def get_url_mais(self, form_dados):
        view = self.data
        context = self.context
        request = self.request

        return '%s/myvindulalistall?campos=%s&departamento=%s&filtro=%s&SearchSubmit=""' %(context.portal_url(),
                                                                                           form_dados,
                                                                                           request.get('departamento',''),
                                                                                           (view.filtro_departamento or 'departamentos'))

    def get_url_mais_contatos(self, form_dados):
        context = self.context

        return '%s/myvindulalistcontatos?campos=%s&SearchSubmit=' %(context.portal_url(),
                                                                   form_dados)

            

    def get_principal_campo(self, obj):
        campo = self.data.principal_user
        if campo:
            try: return obj.get(campo)
            except: return obj.get('name')
        else:
            try: return obj.get('name')
            except: return ''

    def get_camposFilter(self):
        L = []
        if self.data.filtro_user:
            lines = self.data.filtro_user.splitlines()

            for line in lines:
                D = {}
                line = line.replace('[', '').replace(']', '').split(' | ')
                try:
                    D['label'] = line[0]
                    D['content'] = line[1]
                    L.append(D)
                except:
                    pass

        return L

    def get_details_user(self, user):
        if self.data.details_user:
            lines = self.data.details_user.splitlines()
            L = []

            for line in lines:
                D = {}
                line = line.replace('[', '').replace(']', '').split(' | ')
                try:
                    D['label'] = line[0]
                    
                    content = user.get(line[1])

                    if not content and len(line) == 3:
                        content = user.get(line[2])

                    D['content'] = content

                    L.append(D)
                except:
                    pass
            return L

        return None

    def get_uid_struct_org(self,ctx):
        if ctx.portal_type != 'Plone Site' and ctx.portal_type != 'OrganizationalStructure':
            return self.get_uid_struct_org(ctx.aq_inner.aq_parent)
        elif ctx.portal_type == 'OrganizationalStructure':
            return ctx.UID()
        else:
            return None

    def list_filtro(self):
        campo = self.data.filtro_departamento
        
        ch = Cache()
        L = ch.get('PortletRamais_list_filtro')

        if not L:
            result = ModelsInstanceFuncdetails().get_AllFuncDetails()
            L = []
            if result:
                for i in result:
                    if not i.get(campo,'') in L :
                        L.append(i.get(campo))
        
                L.sorted()

            ch.set('PortletRamais_list_filtro',L)
        
        return L 



    def list_departamentos(self):
        return  ModelsDepartment().get_department()

    def get_quantidade_portlet(self):
        return self.data.quantidade_portlet

    def get_department(self, user):
        try:
            user_id = unicode(user, 'utf-8')
        except:
            user_id = user

        return ModelsDepartment().get_departmentByUsername(user_id)

    def getBusca(self):
        form = self.request.form
        campos = self.get_camposFilter()
        campo_departamento = self.filtro_departamento()

        form_values = []
        for item in campos:
            D = {}
            name = item.get('content')
            value = form.get(name).strip()
            if type(value) != unicode:
                D[name] = unicode(value, 'utf-8')
            else:
                D[name] = value
            form_values.append(D)

        #title = form.get('title','').strip()
        #ramal = form.get('ramal','').strip()
        departamento = form.get('departamento','')
        if campo_departamento != "departamentos":
            D = {}
            if type(departamento) != unicode:
                D[campo_departamento] = unicode(departamento, 'utf-8')
            else:
                D[campo_departamento] = departamento
            form_values.append(D)
            departamento = None
        else:
            if type(departamento) != unicode:
                departamento = unicode(departamento, 'utf-8')

        return form_values, departamento

#    @view.memoize
    def busca_usuarios(self):
        form = self.request.form
        result = None
        filtro_busca = self.context.restrictedTraverse('@@myvindula-conf-userpanel').check_filtro_busca_user()

        if 'SearchSubmit' in form.keys():

            form_values, departamento = self.getBusca()
            self.form_dados = form_values
            check_form = [i for i in form_values if i.values() != [u'']]

            active_vindula_contato = form.get('active_vindula_contato', False)

            if active_vindula_contato:
                context = self.context
                path = context.portal_url.getPortalObject()
                
                query = {'portal_type': ('VindulaContato',),
                         'path': {'query':'/'.join(path.getPhysicalPath()),'depth':99},
                         'sort_on':'sortable_title', 'sort_order':'ascending'}

                SearchableText = []
                for item in check_form:

                    if item.has_key('name'):
                        query['Title'] = item['name']+'*'

                    else:
                        SearchableText.append(item.values()[0]+'*')
    
                if len(SearchableText):
                    query['SearchableText'] = SearchableText

                busca = self.portal_catalog(**query)

                result = [i.getObject() for i in busca]

            else:
                if departamento or check_form:
                    #import pdb;pdb.set_trace()
    #                if type(title) != unicode:
    #                    title = unicode(title, 'utf-8')
    #
    #                if type(departamento) != unicode:
    #                    departamento = unicode(departamento, 'utf-8')
    #
    #                if type(ramal) != unicode:
    #                    ramal = unicode(ramal, 'utf-8')

                    
                    result = ModelsDadosFuncdetails().get_FuncBusca(departamento,form_values,filtro_busca)
                    result = self.rs_to_list(result)
    #                if result:
    #                    for item in form_values:
    #                        if item.values():
    #                            busca = "result.find("+item.keys()[0] + ".like( '%' + '%'.join('"+item.values()[0]+"'.split(' ')) + '%'))"
    #                            result = eval(busca)
    #                    if departamento != '0' and self.data.filtro_departamento != 'departamentos':
    #                        busca = "result.find("+self.data.filtro_departamento + "=u'" + departamento+"')"
    #                        data = eval(busca)
    #                        if data.count() != 0:
    #                            result = data
    #                        else:
    #                            result = None
    #                    elif self.data.filtro_departamento == 'departamentos':
    #                        data = ModelsFuncDetails().get_FuncBusca(title,departamento,ramal,filtro_busca)
    #                        if data:
    #                            result = data
    #                        else:
    #                            result = None





        return result


    def getEnd(self,i):
        if i:
            return 'info_boxTipo2'
        else:
            return 'info_boxTipo2 borderDif'

#    def getPhoto(self,photo):
#        if photo is not None and not ' ' in photo:
#            url_foto = BaseFunc().get_imageVindulaUser(photo)
#            if url_foto:
#                return url_foto
#                #return self.context.absolute_url()+'/'+photo # + '/image_thumb'
#            else:
#                return self.context.absolute_url()+'/defaultUser.png'
#        else:
#            return self.context.absolute_url()+'/defaultUser.png'

    def check_filter(self):

        form = self.request.form
        campos = self.get_camposFilter()
        campo_departamento = self.filtro_departamento()

        if 'SearchSubmit' in form.keys():
            form_values, departamento = self.getBusca()

            check_form = [i for i in form_values if i.values() != [u'']]
            if departamento or check_form:
                return 'Não há resultados.'
            else:
                return 'Nenhum campo foi preenchido, por favor preencha algum campo e efetue a busca novamente.'


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    form_fields = form.Fields(IPortletRamais)

    def create(self, data):
       return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IPortletRamais)
