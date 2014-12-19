# -*- coding: utf-8 -*-
""" Liberiun Technologies Sistemas de Informação Ltda. """
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from zope.interface import implements

from vindula.myvindula.models.funcdetails import FuncDetails
from vindula.myvindula.tools.utils import UtilMyvindula


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

    show_picture = schema.Bool(title=unicode("Exibir foto", 'utf-8'),
                               description=unicode("Selecione para mostrar a foto dos aniversarientes no portlet.", 'utf-8'),
                               default=True,
                               )

    show_anonymous = schema.Bool(title=unicode("Exibir portlet para anônimos", 'utf-8'),
                               description=unicode("Selecione para mostrar o portlet para usuários anônimos que acessarem o portal.", 'utf-8'),
                               default=True,
                               )

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
    def __init__(self, title_portlet=u'', quantidade_portlet=u'', filtro_user=u'', show_picture=u'',\
                 details_user=u'',details_text=u'', show_anonymous=u''):
       self.title_portlet = title_portlet
       self.quantidade_portlet = quantidade_portlet
       self.filtro_user = filtro_user
       self.show_picture = show_picture
       self.show_anonymous = show_anonymous
       self.details_user = details_user
       self.details_text = details_text

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

    def get_details_user(self,dado_user):
        L = []
        if self.data.details_user:
            lines = self.data.details_user.splitlines()

            for line in lines:
                D = {}
                line = line.replace('[', '').replace(']', '').split(' | ')
                
                D['label'] = line[0]
                if line[1] == 'date_birth':
                    dado = dado_user.get(line[1])
                    dado = dado.split('/')
                    D['content'] = '/'.join(dado[:-1])
                elif line[1] == 'unidadeprincipal':
                    structure = dado_user.get_unidadeprincipal()
                    result = ''
                    if structure:
                        result = structure.getSiglaOrTitle()
                    D['content'] = result
                elif line[1] == 'departamento':
                    texto = ''
                    departamentos = dado_user.get_department()
                    cont_dep = len(departamentos)

                    for cont, item in enumerate(departamentos, start=1):
                        texto += ' %s' % item.get('title')
                        if cont_dep != cont:
                            texto += ' /'

                    D['content'] = texto
                else:
                    D['content'] = dado_user.get(line[1])
                L.append(D)
        return L

    def get_uid_struct_org(self,ctx):
        if ctx.portal_type != 'Plone Site' and ctx.portal_type != 'OrganizationalStructure':
            return self.get_uid_struct_org(ctx.aq_inner.aq_parent)
        elif ctx.portal_type == 'OrganizationalStructure':
            return ctx.UID()
        else:
            return None

    def get_all_uos(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        return catalog(portal_type='OrganizationalStructure',
                       review_state=['published', 'internally_published'])

    def list_departamentos(self):
        # return  ModelsDepartment().get_department()
        return []


    def get_quantidade_portlet(self):
        return self.data.quantidade_portlet

    def get_department(self, user):
        try:
            user_id = unicode(user, 'utf-8')
        except:
            user_id = user
        return 'TODO mudar'


    def getBusca(self):
        form = self.request.form
        campos = self.get_camposFilter()

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

        departamento = form.get('departamento','')

        return form_values, departamento

    def busca_usuarios(self):
        form = self.request.form
        result = None

        if 'SearchSubmit' in form.keys():
            form_values, departamento = self.getBusca()
            self.form_dados = form_values
            check_form = [i for i in form_values if i.values() != [u'']]
            
            if departamento or check_form:
                fields = {}
                for di in check_form:
                    for i in di:
                        fields[i] = '%%%s%%' % (di[i])

                if departamento:
                    fields['unidadeprincipal'] = departamento

                result = FuncDetails.get_FuncDetailsByField(fields, if_empty_return_all=False)
                return [self._username_to_infouser(r) for r in result if r]

    def _username_to_infouser(self, username):
        return FuncDetails(username)

    def getEnd(self,i):
        if i:
            return 'info_boxTipo2'
        else:
            return 'info_boxTipo2 borderDif'

    def check_filter(self):

        form = self.request.form

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