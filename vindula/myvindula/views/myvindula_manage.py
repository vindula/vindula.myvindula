# coding: utf-8
import logging

from Products.CMFCore.interfaces import ISiteRoot
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot

from vindula.myvindula import MessageFactory as _
from vindula.myvindula.models.funcdetails import FuncDetails
from vindula.myvindula.registration import ImportUser
from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.myvindula.user import BaseFunc


logger = logging.getLogger('vindula.myvindula')


class MyVindulaConfgsView(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindulaconfgs')

    ignoreContext = True

    label = _(u"The Configuration Register myvindula")
    description = _(u"Change the Settings of the Register myvindula.")

    # def load_form(self):
    #     #return SchemaConfgMyvindula().configuration_processes(self)
    #     return ModelsConfgMyvindula().get_configurationAll()

    # def update(self):
    #     self.BlackList = ['vin_myvindula_department','teaching_research',
    #                       'date_birth','email','phone_number','name','photograph']

# class MyVindulaEditConfgsView(grok.View, BaseFunc):
#     grok.context(INavigationRoot)
#     grok.require('cmf.ManagePortal')
#     grok.name('edit_myvindulaconfgs')

#     def load_form(self):
#         return SchemaConfgMyvindula().configuration_processes(self)

#     def update(self):
#         self.BlackList = ['vin_myvindula_department','cpf',
#                           'date_birth','email','phone_number','name','photograph', 'unidadeprincipal']

# class MyVindulaEditOrdemConfgsView(grok.View, BaseFunc):
#     grok.context(INavigationRoot)
#     grok.require('cmf.ManagePortal')
#     grok.name('ordem_myvindulaconfgs')

#     def render(self):
#         return ''

#     def update(self):
#         form = self.request.form

#         if 'list' in form.keys():
#             n = 0
#             list = form.get('list','').split(',')
#             for i in list:
#                 #i = i.split('|')
#                 campo = self.Convert_utf8(i)
#                 #ordem = n
#                 ModelsConfgMyvindula().set_ordemConfiguration(campo,n)
#                 n += 1


# View de migração do banco de dedos para a versão 1.2
# class MyVindulaMigrationFuncdetailsView(grok.View,UtilMyvindula):
#     grok.context(INavigationRoot)
#     grok.require('cmf.ManagePortal')
#     grok.name('migration_funcdetails')

#     def render(self):
#         return 'Migração dos dados do myvindula'


#     def update(self):

#         allUsuarios = ModelsFuncDetails().get_allFuncDetails_migracao()
#         allCampos = ModelsConfgMyvindula().get_configurationAll()
#         tool = UtilMyvindula()

#         for user in allUsuarios:
#             username = user.username
#             user_instance = ModelsInstanceFuncdetails().get_InstanceFuncdetails(username)
#             if not user_instance:
#                 id_instance = ModelsInstanceFuncdetails().set_InstanceFuncdetails(username)
#             else:
#                 id_instance = user_instance.id

#             for campo in allCampos:
#                 valor = None
#                 if campo.fields in ['vin_myvindula_department']:
#                     continue

#                 if campo.fields == 'skills_expertise':
#                     dado_curso = ''
#                     for curso in ModelsMyvindulaCourses().get_allCourses():
#                         dado_curso += curso.title +' - ' +curso.length +'\n'

#                     campo.list_values = self.Convert_utf8(dado_curso)

#                     cursos_user = ModelsMyvindulaFuncdetailCouses().get_funcdetailCouserByUsername(username)
#                     if cursos_user:
#                         L = []
#                         for cursos in cursos_user:
#                             curso = cursos.courses
#                             L.append(curso.title +' - ' +curso.length)

#                         valor = self.encodePickle(L)

#                 elif campo.fields == 'languages':
#                     dado_languages = ''
#                     for language in ModelsMyvindulaLanguages().get_allLanguages():
#                         dado_languages += language.title +' - ' +language.level +'\n'

#                     campo.list_values = self.Convert_utf8(dado_languages)

#                     languages_user = ModelsMyvindulaFuncdetailLanguages().get_funcdetailLanguagesByUsername(username)
#                     if languages_user:
#                         L = []
#                         for languages in languages_user:
#                             language = languages.languages
#                             L.append(language.title +' - ' +language.level)

#                         valor = self.encodePickle(L)

#                 try:
#                     if not valor:
#                         valor = user.__getattribute__(campo.fields)
#                 except:
#                     valor = None

#                 if valor:
#                     if type(valor) == datetime:
#                         valor = valor.strftime('%d/%m/%Y %H:%M:%S')
#                     elif type(valor) == date:
#                        valor = valor.strftime('%d/%m/%Y')

#                     result_campo = ModelsDadosFuncdetails().get_DadosFuncdetails_byInstanceAndField(id_instance,campo.fields)
#                     if result_campo:
#                         result_campo.valor = self.Convert_utf8(valor)
#                         tool.db.store.commit()
#                     else:
#                         D={}
#                         D['vin_myvindula_instance_id'] = id_instance
#                         D['vin_myvindula_confgfuncdetails_fields'] = campo.fields
#                         D['valor'] = self.Convert_utf8(valor)

#                         ModelsDadosFuncdetails().set_DadosFuncdetails(**D)


class MyVindulaCategoryFieldsView(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindulacategoryfields')


class MyVindulaImportUser(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindulaimportuser')

    ignoreContext = True
    label = _(u"users to import the database")
    description = _(u"User import for plone site from mysql database.")

    def load_form(self):
        return ImportUser().databaseUser(self)

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)
        return super(MyVindulaImportUser, self).update()


class MyVindulaDeParaUser(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-compare-user')

    ignoreContext = True

    label = _(u"Usuários orfaos do vindula")
    description = _(u"Excluir usuarios que foram excluidos do plone ou do AD/LDAP.")

class MyVindulaRemoveUser(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-remove-user')

    def render(self):
        pass

    def update(self):
        form = self.request.form
        success_url = self.context.absolute_url() + '/myvindula-compare-user'
        if 'users' in form.keys():
            users = form.get('users','')
            if isinstance(users, str):
                users = [users]
            for user in users:
                username = self.Convert_utf8(user)

#                is_user_vindula = ModelsInstanceFuncdetails().get_InstanceFuncdetails(username)
                is_user_vindula = FuncDetails(username)
                try:
                    if is_user_vindula:
                        is_user_vindula.remove_data_user()
                        self.setStatusMessage("info","Usuário excluído com sucesso.")
                except:
                    self.setStatusMessage("error","Erro ao excluir usuário do Vindula.")

        self.request.response.redirect(success_url)

class AjaxView(grok.View,UtilMyvindula):
    grok.context(ISiteRoot)
    grok.require('cmf.ManagePortal')
    grok.name('ajax_view')

    def defaultMethod(self,form):
        method = form.get('method',None)
        method = getattr(self,method,None)
        if method != None:
            return method(form)
        return None

    def importUser(self,form):
        return ImportUser().importUser(self,form)



class MyVindulaImportHoleriteView(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-import-holerite')

    url_frame = '%s/vindula-api/rh/holerite/manager/%s/%s/?iframe_id=8d60ac741503d50f2970c8ac337e6899'

    def get_url_frame(self):
        url = self.context.portal_url()
        modelo =  self.context.restrictedTraverse('myvindula-conf-userpanel').select_modelo_holerite()
        user_token = self.request.SESSION.get('user_token')

        return self.url_frame %(url,user_token,modelo)

class MyVindulaImportInformeRendimentosView(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-import-ir')

    url_frame = '%s/vindula-api/rh/ir/manager/%s/?iframe_id=8d60ac741503d50f2970c8ac337e6Xc51'

    def get_url_frame(self):
        url = self.context.portal_url()
        user_token = self.request.SESSION.get('user_token')

        return self.url_frame %(url,user_token)




# class MyVindulaImportFirstView(grok.View,UtilMyvindula):
#     grok.context(INavigationRoot)
#     grok.require('cmf.ManagePortal')
#     grok.name('myvindula-import-first')

#     def load_file(self):
#         form = self.request.form
#         if 'load_file' in form.keys():
#             if 'csv_file' in form.keys():
#                 portal = self.context
#                 pasta_control = getattr(portal, 'control-panel-objects')
#                 if pasta_control:
#                     pasta_migracao = getattr(pasta_control, 'migration-users')
#                     if pasta_migracao:
#                         pasta = getattr(pasta_migracao, 'upload-csv')
#                         if pasta:
#                             arquivo = self.request.get('csv_file')
#                             nome = arquivo.filename

#                             normalizer = getUtility(IIDNormalizer)
#                             nome_arquivo = nome_org = normalizer.normalize(unicode(nome, 'utf-8'))

#                             count = 0
#                             while nome_arquivo in pasta.objectIds():
#                                 count +=1
#                                 #if count != 1:
#                                 #    nome_arquivo = nome_arquivo[:-2]
#                                 nome_arquivo = nome_org + '-' + str(count)

#                             pasta.invokeFactory('File',
#                                                 id=nome_arquivo,
#                                                 title=nome_arquivo,
#                                                 description='',
#                                                 file=self.request.get('csv_file')
#                                                 )
#                             campos_csv = pasta.get(nome_arquivo).data.split('\n')[0].replace('"', '').split(';')
#                             arquivo = pasta.get(nome_arquivo).virtual_url_path()
#                             redirect = self.context.absolute_url() + '/myvindula-import-second?url_arquivo=%s' % (arquivo)
#                             return self.request.response.redirect(redirect)
#                         else:
#                             IStatusMessage(self.request).addStatusMessage(_(u"Erro ao carregar arquivo, contate o administrados do portal."), "error")
#                     else:
#                         IStatusMessage(self.request).addStatusMessage(_(u"Erro ao carregar arquivo, contate o administrados do portal."), "error")
#                 else:
#                     IStatusMessage(self.request).addStatusMessage(_(u"Erro ao carregar arquivo, contate o administrados do portal."), "error")

# class MyVindulaImportSecondView(grok.View, UtilMyvindula):
#     grok.context(INavigationRoot)
#     grok.require('cmf.ManagePortal')
#     grok.name('myvindula-import-second')

#     def to_utf8(self, value):
#         return unicode(value, 'utf-8')

#     def load_archive(self):
#         form = self.request.form
#         if 'url_arquivo' in form.keys():
#             path_file = form.get('url_arquivo').split('/')
#             if len(path_file) == 3:
#                 folder = path_file[1]
#                 file = path_file[2]
#             else:
#                 folder = path_file[0]
#                 file = path_file[1]
#             folder = self.context.get(folder)
#             file = folder.get(file)

#             return file.title


#     def load_fields_vindula(self):
#         form = self.request.form
#         fields_vin = []
#         i=0

#         fields = ModelsConfgMyvindula().get_configurationAll() #SchemaFunc().campos
#         FIELD_BLACKLIST = ['vin_myvindula_department',]

#         camposAux = copy(fields)
#         for item in camposAux:
#             if not item.fields in FIELD_BLACKLIST:
#                 fields_vin.append(item.ordem)

#         if fields:
#             for field in fields:
#                 if not field.fields in FIELD_BLACKLIST:
#                     index = field.ordem
#                     D = {}
#                     D['name'] = field.fields
#                     if field.fields != 'username':
#                         D['label'] = field.label  #self.get_label_filed(field)

#                     pos = fields_vin.index(index)
#                     fields_vin.pop(pos)
#                     fields_vin.insert(pos, D)

#                 #fields_vin.append(D)
#         return fields_vin


#     def load_fields_csv(self):
#         form = self.request.form
#         if 'url_arquivo' in form.keys():
#             path_file = form.get('url_arquivo').split('/')
#             folder = getSite()[path_file[0]][path_file[1]][path_file[2]]
#             file = folder.get(path_file[3])

#             return file.data.split('\n')[0].replace('"', '').split(';')

#     def importar_valores(self):
#         form = self.request.form
#         tools = UtilMyvindula()
#         if 'import' in form.keys():
#             path_file = form.get('url_arquivo').split('/')
#             folder = getSite()[path_file[0]][path_file[1]][path_file[2]]
#             arquivo = folder.get(path_file[3])

#             linhas_error =[]
#             lista_erros = []
#             campos = self.get_Dic_Campos()

# #            folder = self.context.get(folder)
# #            arquivo = folder.get(file)
#             ignore_fields = ['import',
#                              'url_arquivo',
#                              'cria-username',
#                              'atualiza-dados',
#                              'ciar-user-plone',
#                              'username',]

#             success = False
#             criar_user = form.get('cria-username', False)
#             merge_user = form.get('atualiza-dados', False)

#             criar_user_plone = form.get('ciar-user-plone', False)

#             error = 0
#             url = ''

#             arquivo.data = arquivo.data.replace('\r', '')

#             for linha in arquivo.data.split('\n')[1:-1]:
#                 if linha:
#                     dados = {}
#                     dados_linha = linha.split(';')
#                     check_user = False
#                     for campo in form.keys():
#                         if form[campo] != '' and campo not in ignore_fields:
#                             indice = int(form[campo])-1
#                             dados[campo] = self.to_utf8(dados_linha[indice].replace('"',''))
#                         else:
#                             if campo == 'username':
#                                 if criar_user:
#                                     name = dados_linha[int(form['name'])-1].replace('"','').lower().split(' ')

#                                     username = name[0] + name[-1]
#                                     cont = 1

#                                     if form.get('registration'):
#                                         matricula = dados_linha[int(form.get('registration'))-1].replace('"','')
#                                         username += str(matricula)
#                                     else:
#                                         matricula = randint(1,pow(10,10))
#                                         username += str(matricula)

#                                     usr = username
#                                     while ModelsInstanceFuncdetails().get_InstanceFuncdetails(self.to_utf8(usr)):
#                                         usr = username + str(cont)
#                                         cont +=1

#                                     dados[campo] = self.to_utf8(usr)
#                                     check_user = True

#                                 else:
#                                     if form.get('username'):
#                                         indice = int(form.get('username'))-1
#                                         user = self.to_utf8(dados_linha[indice].replace('"',''))
#                                         if ModelsInstanceFuncdetails().get_InstanceFuncdetails(user) and merge_user:
#                                             dados[campo] = user
#                                             check_user = True
#                                         else:
#                                             dados[campo] = user
#                                             check_user = True

#                     erros, data_user = valida_form_dinamic(self,campos, dados)
#                     if not erros:
#                         if criar_user_plone:
#                             ImportUser().importUser(self,{},dados)

#                         username = dados['username']
#                         if check_user:
#                             user_instance = ModelsInstanceFuncdetails().get_InstanceFuncdetails(username)
#                             if user_instance:
#                                 id_instance = user_instance.id
#                             else:
#                                 id_instance = ModelsInstanceFuncdetails().set_InstanceFuncdetails(username)

#                             for item in data_user.keys():
#                                 field = self.Convert_utf8(item)
#                                 valor = data_user[item]
#                                 result_campo = ModelsDadosFuncdetails().get_DadosFuncdetails_byInstanceAndField(id_instance,field)
#                                 if result_campo:
#                                     result_campo.valor = valor.strip()
#                                     tools.db.store.commit()
#                                 else:
#                                     if valor:
#                                         D={}
#                                         D['vin_myvindula_instance_id'] = id_instance
#                                         D['vin_myvindula_confgfuncdetails_fields'] = field
#                                         D['valor'] = self.Convert_utf8(valor)

#                                         ModelsDadosFuncdetails().set_DadosFuncdetails(**D)

#                             success = True

#                         else:
#                             error = 1
#                     else:
#                         linhas_error.append(linha)
#                         lista_erros.append(erros)
#                         error = 2
#                         success = False

#                     logger.info("%s - %s "% (erros,data_user))

#             if linhas_error:
#                 success = False
#                 campos = arquivo.data.split('\n')[0].replace('\r','')
#                 text = ''
#                 col = ''
#                 for campo in campos.split(';'):
#                     col += campo+';'

#                 col += 'coluna erro;\n'
#                 text = col
#                 i = 0

#                 for linha in linhas_error:
#                     text += linha.replace('\r','') + ';'+str(lista_erros[i].keys())+'\n'
#                     i +=1

#                 text += '\n'

#                 nome_arquivo = 'error-import-'+ datetime.now().strftime('%Y-%M-%d_%H-%M-%S') +'.csv'
#                 pasta_error = getSite()['control-panel-objects']['migration-users']['errors-import']
#                 pasta_error.invokeFactory('File',
#                                             id=nome_arquivo,
#                                             title=nome_arquivo,
#                                             description='',
#                                             file=text)
#                 url=pasta_error[nome_arquivo].absolute_url()

#             redirect = self.context.absolute_url() + '/myvindula-import-third?success=%s&error=%s&url=%s' % (success,error,url)
#             return self.request.response.redirect(redirect)


# class MyVindulaImportThirdView(grok.View,UtilMyvindula):
#     grok.context(INavigationRoot)
#     grok.require('cmf.ManagePortal')
#     grok.name('myvindula-import-third')

class MyVindulaImportUsers(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-import-users')

class MyVindulaExportUsersView(grok.View,UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-export-users')

class MyVindulaImportProfilePicture(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-import-profile-picture')

