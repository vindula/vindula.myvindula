# -*- coding: utf-8 -*-

from plone.app.controlpanel.security import SecurityControlPanelAdapter
from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula
from Products.CMFCore.utils import getToolByName

from zope.component import getUtility
from plone.dexterity.interfaces import IDexterityFTI

from vindula.myvindula.tools.utils import UtilMyvindula

def user_folder(context):
    ctx = context.getSite()
    folder_user = ctx.portal_membership.memberareaCreationFlag
    if not folder_user:
        SecurityControlPanelAdapter(ctx).set_enable_user_folders(True)

    # Creating Migration Users Folder
    if 'control-panel-objects' in ctx.objectIds():
        folder_control_panel = ctx['control-panel-objects']
        if not 'migration-users' in folder_control_panel.objectIds():
            ctx.portal_types.get('Folder').global_allow = True

            folder_control_panel.invokeFactory('Folder',
                                               id='migration-users',
                                               title='Migração de usuários',
                                               description='Pasta que guarda os arquivos CSV da importação de usuários.',
                                               excludeFromNav = True)

            migration = folder_control_panel['migration-users']

            if not 'upload' in folder_control_panel.objectIds():
                migration.invokeFactory('Folder',
                                        id='upload-csv',
                                        title='Upload',
                                        description='Pasta que guarda os arquivos CSV da importação de usuários.',
                                        excludeFromNav = True)

            if not 'errors' in folder_control_panel.objectIds():
                migration.invokeFactory('Folder',
                                        id='errors-import',
                                        title='Erros na Importação',
                                        description='Pasta que guarda os arquivos CSV sobre os erros na importação de usuários.',
                                        excludeFromNav = True)

            ctx.portal_types.get('Folder').global_allow = False

        if not 'list-documents-user' in folder_control_panel.objectIds():
            type = 'vindula.myvindula.vindulalistdocumentuser'
            id = 'list-documents-user'

            if ctx.portal_types.get(type):
                folder_control_panel.setConstrainTypesMode(0)
                ctx.portal_types.get(type).global_allow = True

                # constroi o objeto
                obj = {'type_name':type,'id':id,
                       'title':'Documentos comprobatórios',
                       'excludeFromNav':True,}

                folder_control_panel.invokeFactory(**obj)
                print 'Create %s object.' % id
                ctx.portal_types.get(type).global_allow = False



    portalGroup = context.getSite().portal_groups
    if not 'manage-user' in portalGroup.listGroupIds():
        nome_grupo = 'Gerenciadores dos usuarios'
        portalGroup.addGroup('manage-user', title=nome_grupo)
        #Adiciona o grupo a 'AuthenticatedUsers'
        portalGroup.getGroupById('AuthenticatedUsers').addMember('manage-user')




def set_AllowedType_Members(context):
    portal = context.getSite()
    Types = ['Folder','Image','RTRemoteVideo','RTInternalVideo', 'Document', 'File',]

    if 'Members' in portal.keys():
        folder_members = portal['Members']
        folder_members.setConstrainTypesMode(1) # 1 pasta com restrição de conteudo / 0 sem restrição de conteudo
        folder_members.setImmediatelyAddableTypes(Types)
        folder_members.setLocallyAllowedTypes(Types)

#        if 'index_html' in folder_members.keys():
#            index = folder_members['index_html']
#            #index.write("member_search = '/myvindulalistall'\nreturn container.REQUEST.RESPONSE.redirect(member_search)")


def create_mycontents(context):
    portal = context.getSite()
    portal_workflow = getToolByName(portal, 'portal_workflow')

    # Creating collect Users mycontents
    if not 'myvindula-meus-conteudos' in portal.objectIds():
        portal.portal_types.get('Topic').global_allow = True

        objects = {'type_name':'Topic',
                   'id': 'myvindula-meus-conteudos',
                   'title':'Meus Conteúdos',
                   'description':'Visualização dos meus conteúdos no portal.',
                   'customView':True,
                   'customViewFields':['Title','CreationDate','Description']
                   }

        portal.invokeFactory(**objects)
        portal.portal_types.get('Topic').global_allow = False

        if 'myvindula-meus-conteudos' in portal.keys():
            colection = portal['myvindula-meus-conteudos']

            try:portal_workflow.doActionFor(colection, 'publish')
            except:portal_workflow.doActionFor(colection, 'publish_internally')

            theCriteria = colection.addCriterion('Creator','ATCurrentAuthorCriterion')
            colection.setSortCriterion('created',False)

            colection.manage_setLocalRoles('AuthenticatedUsers', ['Editor', 'Reviewer', 'Reader'])
