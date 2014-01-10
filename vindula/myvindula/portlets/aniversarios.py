# -*- coding: utf-8 -*-
""" Liberiun Technologies Sistemas de Informação Ltda. """
""" Produto:                 """

from zope.interface import implements
from zope.formlib import form
from zope import schema

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from vindula.myvindula.user import BaseFunc
from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
from vindula.myvindula.models.department import ModelsDepartment


from datetime import date
from storm.expr import Desc
#import datetime
from DateTime.DateTime import DateTime
import calendar

from vindula.myvindula.cache import Cache

class TypesSearch():
    """ Cria SimpleVocabulary """

    def __call__(self):
        itens=[(1,'Aniversariantes do dia'), (7,'Aniversariantes da semana'),  (30,'Aniversariantes do mês'), ('prox', 'Próximos Aniversariantes')]
        L=[]
        for i in itens:
            L.append(SimpleTerm(i[0], i[0], unicode(i[1])))

        return SimpleVocabulary(L)

class IPortletAniversarios(IPortletDataProvider):

    """A portlet
    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    title_portlet = schema.TextLine(title=unicode("Título", 'utf-8'),
                                  description=unicode("Título que aparecerá no cabeçalho do portlet.", 'utf-8'),
                                  required=True)

    quantidade_portlet = schema.Int(title=unicode("Quantidade de Itens", 'utf-8'),
                                  description=unicode("Quantidade limite de itens mostrado no portlet.", 'utf-8'),
                                  required=True)

    type_search = schema.Choice(title=unicode("Tipo do filtro", 'utf-8'),
                                description=unicode("Selecione o filtro que será usado no portlet", 'utf-8'),
                                vocabulary=TypesSearch().__call__())

    type_search_list = schema.Choice(title=unicode("Tipo de filtro para a listagem", 'utf-8'),
                                description=unicode("Selecione o fitro que sera usado na lista de aniversariantes", 'utf-8'),
                                vocabulary=TypesSearch().__call__())

    show_picture = schema.Bool(title=unicode("Exibir foto", 'utf-8'),
                               description=unicode("Selecione para mostrar a foto dos aniversariantes no portlet.", 'utf-8'),
                               default=True,
                               )

    show_anonymous = schema.Bool(title=unicode("Exibir portlet para anônimos", 'utf-8'),
                               description=unicode("Selecione para mostrar o portlet para usuarios anônimos que acessarem o portal.", 'utf-8'),
                               default=True,
                               )

    principal_user = schema.TextLine(title=unicode("Destaque do aniversariante", 'utf-8'),
                                     description=unicode("Adicione o campo com a informação princial do aniversariante como 'name' para Nome ou 'nickname' para\
                                                          Apelido ou outros.", 'utf-8'),
                                     default = u'name',
                                     required=True)

    details_user = schema.Text(title=unicode("Detalhes do aniversariante", 'utf-8'),
                                  description=unicode("Adicione detalhes sobre o aniversariante como Empresa, Matricula e outros. \
                                                       Adicione um campo por linha, no formato [Label] | [Campo].", 'utf-8'),
                               default = u'[] | [date_birth]',
                               required=False)

class Assignment(base.Assignment):
    """Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IPortletAniversarios)
    # TODO: Add keyword parameters for configurable parameters here
    def __init__(self, title_portlet=u'', quantidade_portlet=u'',principal_user = u'',show_anonymous=u'',
                type_search=u'',details_user=u'',show_picture=u'',type_search_list=u''):
       self.title_portlet = title_portlet
       self.quantidade_portlet = quantidade_portlet
       self.type_search = type_search
       self.details_user = details_user
       self.principal_user = principal_user
       self.show_anonymous = show_anonymous
       self.show_picture = show_picture
       self.type_search_list = type_search_list

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Portlet Aniversarios"

class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    render = ViewPageTemplateFile('portlet_aniversarios.pt')

    def get_title(self):
        return self.data.title_portlet

    def get_type_search(self):
        return self.data.type_search

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

    def get_type_search_list(self):
        return self.data.type_search_list

    def get_principal_campo(self, obj):
        campo = self.data.principal_user
        if campo:
            try: return obj.get(campo,'')
            except: return obj.get('name',obj.get('username',''))
        else:
            try: return obj.get('name',obj.get('username',''))
            except: return ''

    def nome_filtro(self):
        filtro = self.get_type_search_list()
        if filtro == 1:
            return "Aniversariantes do Dia"
        elif filtro == 7:
            return "Aniversariantes da Semana"
        elif filtro == 30:
            return "Aniversariantes do Mês"
        else:
            return "Próximos Aniversariantes"

    def frase_filtro(self):
        filtro = self.get_type_search()
        if filtro == 1:
            return "hoje"
        elif filtro == 7:
            return "nesta semana"
        elif filtro == 30:
            return "neste mês"
        else:
            return 'nos próximos dias'

    def get_details_user(self, user):
        panel = self.context.restrictedTraverse('@@myvindula-conf-userpanel')
        if self.data.details_user:

            lines = self.data.details_user.splitlines()
            L = []
            for line in lines:
                D = {}
                line = line.replace('[', '').replace(']', '').split(' | ')
                try:
                    D['label'] = line[0]
                    if line[1] == 'date_birth':
                        dado = user.get(line[1])
                        if panel.check_ativa_yearBirth():
                            D['content'] = dado[:5]
                        else:
                            D['content'] = dado

                    else:
                        D['content'] = user.get(line[1])
                    L.append(D)
                except :
                    pass
            return L

        return None

    def get_quantidade_portlet(self):
        return self.data.quantidade_portlet

    def get_department(self, user):
        try:user_id = unicode(user, 'utf-8')
        except:user_id = user

        return ModelsDepartment().get_departmentByUsername(user)


    def get_birthdaysToday(self, type_filter):
        results = None
        if type_filter == 1:
            date_start = date.today().strftime('%Y-%m-%d')
            date_end = date.today().strftime('%Y-%m-%d')

            results = ModelsDadosFuncdetails().get_FuncBirthdays(date_start,date_end,True)

        elif type_filter == 7:
            now = DateTime()
            dow = now.dow()
            date_start = (now + 1 - dow).strftime('%Y-%m-%d')
            date_end = (now + 1 - dow + 6).strftime('%Y-%m-%d')

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


    def birthdaysToday(self):
        type_filter = self.data.type_search
        #quant = self.data.quantidade_portlet
        ch = Cache()
        results = ch.get('PortletAviversarinates_birthdaysToday')

        if not results:
            results = self.get_birthdaysToday(type_filter)
            ch.set('PortletAviversarinates_birthdaysToday',results)

        return results


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
#                #return self.context.absolute_url()+'/'+photo #+ '/image_thumb'
#            else:
#                return self.context.absolute_url()+'/defaultUser.png'
#        else:
#            return self.context.absolute_url()+'/defaultUser.png'


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    form_fields = form.Fields(IPortletAniversarios)

    def create(self, data):
       return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IPortletAniversarios)
