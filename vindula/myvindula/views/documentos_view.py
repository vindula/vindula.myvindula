# coding: utf-8
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from vindula.myvindula.user import BaseFunc
from vindula.myvindula.content.vindulalistdocumentuser import IVindulaListDocumentUser


from vindula.myvindula.document_models import SchemaManageDocument, SchemaDocument
from vindula.myvindula.models.config_documents import ModelsConfigDocuments
from vindula.myvindula.models.user_documents import ModelsUserDocuments

from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails

from vindula.myvindula.tools.utils import UtilMyvindula

from datetime import datetime
import pickle


class MyVindulaManageDocumentView(grok.View):
    grok.context(IVindulaListDocumentUser)
    grok.require('cmf.AddPortalContent')
    grok.name('myvindula-manage-documents')

    def get_Documents(self):
        return ModelsConfigDocuments().get_allConfigDocuments()


class MyVindulaAddDocumentView(grok.View, BaseFunc):
    grok.context(IVindulaListDocumentUser)
    grok.require('cmf.AddPortalContent')
    grok.name('add-documents')

    def load_form(self):
        return SchemaManageDocument().registration_processes(self)


class MyVindulaEditDocumentView(grok.View, BaseFunc):
    grok.context(IVindulaListDocumentUser)
    grok.require('cmf.AddPortalContent')
    grok.name('edit-documents')

    # This may be overridden in ZCML
    index = ViewPageTemplateFile("documentos_view_templates/myvindulaadddocumentview.pt")

    def load_form(self):
        return SchemaManageDocument().registration_processes(self)

    def render(self):
        return self.index()
#
#class MyVindulaAddDocumentView(grok.View, BaseFunc):
#    grok.context(Interface)
#    grok.require('cmf.ManagePortal')
#    grok.name('add-documents')
#
#
#    def load_form(self):
#        return SchemaManageDocument().registration_processes(self)


class MyVindulaExportDocumentView(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.AddPortalContent')
    grok.name('export-documents')

    def render(self):
        pass

    def update(self):
        form = self.request.form
        form_values = []
        if 'export' in form.keys():

            self.request.response.setHeader("Content-Type", "text/csv", 0)
            filename = 'export-search-documents-'+ datetime.now().strftime('%Y-%M-%d_%H-%M') +'.csv'
            self.request.response.setHeader('Content-Disposition','attachment; filename=%s'%(filename))

            if 'filtro' in form.keys() and 'title' in form.keys():

                filtro = form.get('filtro','')
                try:title = unicode(form.get('title',''),'utf-8')
                except:title = form.get('title','')
                status = int(form.get('status',''))
                L=[]

                form_values.append({filtro:title})

                data = ModelsDadosFuncdetails().get_FuncBusca(form_campos=form_values)

                if data:
                    L = []
                    for item in data:
                        D = {}
                        try:user = unicode(item.get('username',''), 'utf-8')
                        except:user = item.get('username','')

                        if status == 0:
                            D['user'] = item
                        elif status == 1:
                            result = ModelsUserDocuments().get_UserDocuments_byUsername(user)
                            if result:
                                D['user'] = item
                        elif status == 2:
                            result = ModelsUserDocuments().get_UserDocuments_byUsername(user)
                            if not result:
                                D['user'] = item
                        if D:
                            L.append(D)


                campos_vin = []
                text = ''
                text = 'Matrícula;Nome;Unidade organizacional;Empresa;\n'

                for item in L:
                    user = item['user']
                    valor = ''
                    valor = str(user.get('registration','')) +';'+ str(user.get('name','')) +';' + str(user.get('organisational_unit','')) +';' + str(user.get('enterprise',''))+';\n'

                    text += valor


                self.request.response.write(str(text))


#-----------------Adição dos documentos peloa usuario---------------------------------------

class MyVindulaDocumentView(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('myvindula-documents')

    def load_form(self):
        return SchemaDocument().registration_processes(self)


    def load_list(self):
        return ModelsConfigDocuments().get_allConfigDocuments()

    def doc_enviado(self, id):
        membership = self.context.portal_membership
        user_login = membership.getAuthenticatedMember()

        try:user = unicode(user_login.id, 'utf-8')
        except:user = user_login.id

        doc_user = ModelsUserDocuments().get_UserDocuments_by_user_and_doc(user,int(id))

        if doc_user:
            return doc_user.id
        else:
            return False

    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')


class MyVindulaListDocumentView(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('list-documents')

    def load_list(self):
        form = self.request.form # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)

        if 'user' in form_keys and 'status' in form_keys:
            try:user = unicode(form.get('user',''), 'utf-8')
            except:user = form.get('user','')
            L =[]
            status = int(form.get('status',''))

            data = ModelsConfigDocuments().get_allConfigDocuments()
            if data:

                for item in data:
                    D = {}
                    D['doc'] = item
                    doc_user = ModelsUserDocuments().get_UserDocuments_by_user_and_doc(user,item.id)

                    D['doc_user'] = doc_user
                    L.append(D)
            return L


    def checaFiltro(self,user_doc):
        form = self.request.form
        form_keys = form.keys()

        if 'status' in form_keys:
            status = int(form.get('status',''))
            if status == 0:
                return True
            elif status == 1:
                if user_doc:
                    return True
                else:
                    return False
            elif status == 2:
                if user_doc:
                    return False
                else:
                    return True
            else:
                return False

    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')


class VindulaDocumentosDownloadView(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('download-document')

    def render(self):
        pass

    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();

        if not open_for_anonymousUser:
            form = self.request.form
            if 'id' in form.keys():
                id = form.get('id','0')
                if id != 'None':
                    campo_doc = ModelsUserDocuments().get_UserDocuments_byID(int(id))
                    if campo_doc:
                        valor_blob = campo_doc.documento
                        x = self.decodePickle(valor_blob)

                        filename = x['filename']
                        self.request.response.setHeader("Content-Type", "type/file", 0)
                        self.request.response.setHeader('Content-Disposition','attachment; filename=%s'%(filename))
                        self.request.response.write(x['data'])

        else:
            self.request.response.redirect(self.context.absolute_url() + '/login')
