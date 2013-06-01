# coding: utf-8

from vindula.myvindula import MessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage
from datetime import date , datetime
from vindula.myvindula.validation import valida_form, valida_form_dinamic

from vindula.myvindula.user import BaseFunc

from vindula.myvindula.models.base import BaseStore

# from vindula.myvindula.models.instance_funcdetail import ModelsInstanceFuncdetails
from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
# from vindula.myvindula.models.photo_user import ModelsPhotoUser

from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula
# from vindula.myvindula.models.department import ModelsDepartment
from zope.app.component.hooks import getSite


from vindula.myvindula.tools.utils import UtilMyvindula


from copy import copy

class SchemaFunc(BaseFunc):


    # TODO: colocar isso em um lugar especifico. Está redundante aqui
    def get_unidade_organizacional_text(self):
        tools = UtilMyvindula()
        caminho = tools.portal_url.getPortalPath()
        data = tools.catalog(portal_type='OrganizationalStructure',
                      sort_on = 'sortable_title',
                      path=caminho)

        if data:
            unidades = []
            for unidade in data:
                unidades.append([unidade.UID,unidade.Title])
            return unidades
        else:
            return []

    def registration_processes(self,context,user,manage=False,delete=False):
        campos = {}
        lista_itens = {}

        if not isinstance(context, dict):
            if not context:
                context = getSite()
            form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
            form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        else:
            form = context
            form['name'] = form.get('fullname', form.get('username', None))
            form['form.submited'] = ['Submited']
            form_keys = form.keys()

        user_id = self.Convert_utf8(user)
#        id_instance = 0

#        if user_id:
#            user_instance = ModelsInstanceFuncdetails().get_InstanceFuncdetails(user_id)
#            if not user_instance:
#                id_instance = ModelsInstanceFuncdetails().set_InstanceFuncdetails(user_id)
#            else:
#                id_instance = user_instance.id

        fields = ModelsConfgMyvindula().get_configurationAll()
        if fields:
            for field in fields:
                M={}
                M['required'] = field.required
                M['type'] = field.type
                M['label'] = field.label
                M['decription'] = field.decription
                M['ordem'] = field.order_position
                M['mascara'] = field.mask

                if  field.type == 'img':
                    M['instance_id'] = user_id

                campos[field.name] = M

                if field.type == 'choice' or\
                   field.type == 'list':

                    items = field.choices.splitlines()
                    valores=[]

                    # TODO: Otimizar este codigo, podemos dizer que estah muito lento e incorreto.
                    for i in items:
                        if i == "###unidadesorganizacionais###":
                            unidades = self.get_unidade_organizacional_text()
                            for unidade in unidades:
                                valores.append([unidade[0],unidade[1]])
                        else:
                            valores.append([i, i])

                    lista_itens[field.name] = valores

        conf = {}
        for item in campos.keys():
            try: conf[item] = ModelsConfgMyvindula().getConfig_edit(item)
            except:conf[item] = True

        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,
            'lista_itens':lista_itens,

            'departametos': ModelsDepartment().get_department(),
            'username' : user_id,
            'config_myvindula':conf,
            'manage':manage,}

        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            if 'id_instance' in form_keys and isForm:
                context.request.response.redirect(success_url+'/view-form')
            else:
                context.request.response.redirect(getSite().portal_url() + '/@@usergroup-userprefs')

        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            if not user_id:
                campos['username'] = {'required': True, 'type' : self.to_utf8, 'label':''}

            #Remove o campos departamento da validação
            if 'vin_myvindula_department' in campos.keys():
                campos.pop('vin_myvindula_department')

            #Remove o campos img da validação
            camposAux = copy(campos)
            for item in camposAux:
                D = camposAux[item]
                if D.get('type') == 'img':
                    campos.pop(item)

            # Inicia o processamento do formulario
            # chama a funcao que valida os dados extraidos do formulario (valida_form)
            if not isinstance(context, dict):
                form = context.request.form
            else:
                form = context

            errors, data = valida_form_dinamic(context, campos, form)

            if not errors:
#                if not user_id:
#                    id_instance = ModelsInstanceFuncdetails().set_InstanceFuncdetails(data.get('username'))
#                    user_id = data.get('username')
#                    data.pop('username')

                if 'vin_myvindula_department' in form_keys or 'departaments_old' in form_keys:
                    L = []
                    portalGroup = getSite().portal_groups
                    portalCatalog = getSite().portal_catalog

                    if form.get('vin_myvindula_department', None):
                        if not type(form.get('vin_myvindula_department', None)) == list:
                            L.append(form.get('vin_myvindula_department', None))
                        else:
                            L = form.get('vin_myvindula_department', None)
                    deparataments_old = form.get('departaments_old', [])

                    #Adiciona o usuario do grupo da estrutura organizacional
                    dep_adicionados = set(L) - set(deparataments_old)
                    for departament in dep_adicionados:
                        D={}
                        D['UID'] = unicode(departament,'utf-8')
                        D['funcdetails_id'] = user_id
                        ModelsDepartment().set_department(**D)

                        obj_org = portalCatalog(portal_type='OrganizationalStructure', UID=departament)
                        if obj_org:
                            obj_org = obj_org[0].getObject()

                            #Adiciona o usuário no campo Employees
                            if user_id not in obj_org.getEmployees():
                                tuple_employees = list(obj_org.employees)
                                tuple_employees.append(user_id)
                                obj_org.employees = tuple(tuple_employees)

                            #Adiciona o usuário no campo Permissao de Visualizacao
                            if user_id not in obj_org.getGroups_view():
                                tuple_Groups_view = list(obj_org.Groups_view)
                                tuple_Groups_view.append(user_id)
                                obj_org.Groups_view = tuple(tuple_Groups_view)

                        if user_id not in portalGroup.getGroupById(departament+'-view').getAllGroupMemberIds():
                            portalGroup.getGroupById(departament+'-view').addMember(user_id)

                    #Exclui o usuario do grupo da estrutura organizacional
                    dep_excluidos = set(deparataments_old) - set(L)
                    for departament in dep_excluidos:
                        ModelsDepartment().del_department(user=unicode(user_id), depUID=unicode(departament,'utf-8'))

                        obj_org = portalCatalog(portal_type='OrganizationalStructure', UID=departament)
                        if obj_org:
                            obj_org = obj_org[0].getObject()
                            if user_id != obj_org.getManager():
                                #Removendo o usuário no campo Employees
                                if user_id in obj_org.getEmployees():
                                    tuple_employees = list(obj_org.employees)
                                    tuple_employees.remove(user_id)
                                    obj_org.employees = tuple(tuple_employees)

                                #Removendo o usuário no campo Permissao de Visualizacao
                                if user_id in obj_org.getGroups_view():
                                    tuple_Groups_view = list(obj_org.Groups_view)
                                    tuple_Groups_view.remove(user_id)
                                    obj_org.Groups_view = tuple(tuple_Groups_view)

                                if user_id in portalGroup.getGroupById(departament+'-view').getAllGroupMemberIds():
                                    portalGroup.getGroupById(departament+'-view').removeMember(user_id)

                            else:
                                self.setStatusMessage("error","O usuário é gestor do departamento %s, ele não pode ser removido." % obj_org.Title())
                                self.setRedirectPage('/@@user-information?userid='+user_id)
                                form_data['errors'] = errors
                                form_data['data'] = data
                                return form_data

                for item in data.keys():
                    field_name = self.Convert_utf8(item)
                    valor = data[item]
                    result_campo = ModelsDadosFuncdetails().get_DadosFuncdetails_byInstanceAndFieldName(user_id,field_name)
                    if result_campo:
                        result_campo.value = valor.strip()
                        result_campo.date_modified = datetime.now()
                        self.db.store.commit()
                    else:
                        if valor:
                            D={}
                            #D['vin_myvindula_instance_id'] = id_instance
                            D['username'] = user_id
                            D['field'] = field_name
                            D['value'] = self.Convert_utf8(valor)

                            ModelsDadosFuncdetails().set_DadosFuncdetails(**D)

                #Redirect back to the front page with a status message
                self.setStatusMessage("info","Perfil editado com sucesso.")
                if manage:
                    self.setRedirectPage('/@@usergroup-userprefs')
                else:
                    self.setRedirectPage('/myvindulalistuser')

            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data

        # se for um formulario de edicao
        elif user_id:# and id_instance:

            #data_value = ModelsInstanceFuncdetails().get_InstanceDadosFuncdetails(user_id)

            data_value = self.get_prefs_user(user_id)
#            D = {}
#            if data_value:
#                for campo in campos.keys():
#                    for data in data_value:
#                        if data.vin_myvindula_confgfuncdetails_fields == campo:
#                            D[campo] = data.valor

            data_value['vin_myvindula_department'] = ModelsDepartment().get_departmentByUsername(user_id)
            form_data['data'] = data_value
            return form_data

        else:
            return form_data

    def deleteUser(self, user):
        user = self.Convert_utf8(user)
        is_user_vindula = ModelsInstanceFuncdetails().get_InstanceFuncdetails(user)
        try:
            if is_user_vindula:
                ModelsInstanceFuncdetails().del_InstanceDadosFuncdetails(user)
        except:
            self.setStatusMessage("error","Erro ao excluir usuário do Vindula.")
            self.setRedirectPage('/@@usergroup-userprefs')

class SchemaConfgMyvindula(BaseFunc):

    def configuration_processes(self,context):
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)

        campos = {'name'     : {'required': True,  'type':'key',          'label':'Nome do Campo',               'decription':'Nome unico do campo',                                                   'ordem':0},
                  'ativo_edit' : {'required': False, 'type':'bool',         'label':'Habilitado para edição',      'decription':'Habilita a edição do campo pelo funcionário',                           'ordem':1},
                  'ativo_view' : {'required': False, 'type':'bool',         'label':'Habilitado para visualização','decription':'Habilita a visualização do campo pelo funcionário',                     'ordem':2},
                  'label'      : {'required': True,  'type':self.to_utf8,   'label':'Título',                      'decription':'Digite o nome de visualização do campo pelo funcionário',               'ordem':3},
                  'decription' : {'required': False, 'type':'textarea',     'label':'Descrição',                   'decription':'Descrição para o preenchimento do campo',                                'ordem':4},
                  'required'   : {'required': False, 'type':'bool',         'label':'Campo Obrigatório',           'decription':'Este campo sera de preenchimento obrigátorio',                           'ordem':5},
                  'type'       : {'required': True,  'type':'choice',       'label':'Tipo do Campo',               'decription':'Escolha o tipo do campo ',                                              'ordem':6},
                  'choices'    : {'required': False, 'type':'textarea',     'label':'Lista de dados para o select','decription':u'Caso o campo seja um select ou list digite os valores para o campo\
                                                                                                                                  <br /> Digite um item por linha',                                      'ordem':7},
                  'mask'    : {'required': False, 'type':'choice',       'label':'Tipo da Máscara',             'decription':'Escolha um tipo de máscara para o campo ',                              'ordem':8},
                  'profile_category' : {'required': True,  'type':'choice',       'label':'Área de Visualização',        'decription':'Escolha um área para este campo ser visualizado no perfil do usúario',  'ordem':9},
                  'order_position'      : {'required': False, 'type':'hidden',       'label':'Ordenação',                   'decription':'',                                                                      'ordem':10},
                  }

        lista_itens = {'type':[['text','Campo de Texto'],['textarea','Campo Texto Múltiplas Linhas'],
                               ['img','Campo de Upload de Imagem'], ['list','Campo de Seleção Multipla'],
                               ['choice','Campo de Escolha']],

                       'mask':[['Telefone','Telefone'],['Data','Data'],['Integer','Números Inteiros'],
                                  ['Cpf','CPF'],['Cep','CEP'],['Cnpj','CNPJ']],

                       'profile_category':[['personal','Pessoal'],['contact','Contato'],
                                       ['corporate','Corporativo'],['other','Outros']
                                       ]
                       }

        site = context.context.portal_url.getPortalObject()
        pw = site.portal_workflow
        if 'control-panel-objects' in  site.keys():
            control = site['control-panel-objects']
            if 'fieldset-myvindula' in control.keys():
                folder_Areas = control['fieldset-myvindula']
                for item in folder_Areas.objectValues():

                    if pw.getInfoFor(item,'review_state') == 'published':
                        lista_itens['profile_category'].append([item.getId(),item.Title()])

        result_form = ModelsConfgMyvindula().get_configurationAll()

        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,
            'lista_itens':lista_itens}

        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:

            self.setRedirectPage('/myvindulaconfgs')

        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            # chama a funcao que valida os dados extraidos do formulario (valida_form)
            errors, data = valida_form_dinamic(context, campos, context.request.form)

            if not errors:
                if 'name' in form_keys and 'form.edit' in form_keys:
                    # editando...
                    fields = form.get('name','')
                    result_fields = ModelsConfgMyvindula().get_configuration_By_fields(fields)
                    if result_fields:
                        for campo in campos.keys():
                            value = data.get(campo, None)
                            setattr(result_fields, campo, value)

                        self.setStatusMessage("info","Campo editado com com sucesso")
                        self.setRedirectPage('/myvindulaconfgs')

                else:
                    if ModelsConfgMyvindula().check_fields(data['name']):
                        #adicionando...
                        ModelsConfgMyvindula().set_configuration(**data)
                        self.setStatusMessage("info","Campo adicionado com sucesso")
                        self.setRedirectPage('/myvindulaconfgs')

                    else:
                        self.setStatusMessage("error","Já existe um campo com este nome")
                        self.setRedirectPage('/edit_myvindulaconfgs')

            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data

        # se clicou em excluir
        elif 'form.excluir' in form_keys:
            field = self.Convert_utf8(form.get('fields',''))
            ModelsConfgMyvindula().del_configuration(field)

            self.setStatusMessage("info","Campo removido com sucesso")
            self.setRedirectPage('/myvindulaconfgs')

        # se for um formulario de edicao
        elif 'fields' in form_keys: #'forms_id'in form_keys and :
            fields = form.get('fields','')
            if fields in context.BlackList:
                campos['name']['type'] = 'hidden'
                campos['type']['type'] = 'hidden'
                campos['profile_category']['type'] = 'hidden'

            data = ModelsConfgMyvindula().get_configuration_By_fields(fields)
           # campos['name_field'] = {'required': True,  'type':'hidden','label':'Nome do Campo', 'decription':u'', 'ordem':0}
            if data:
                D = {}
                for campo in campos.keys():
                    D[campo] = getattr(data, campo, '')

                form_data['data'] = D
                return form_data
            else:
               return form_data

        #se for um formulario de adição
        else:
            data = {}

            if result_form:
                data['order_position'] = result_form.count()
            else:
                 data['order_position'] = 0
            form_data['data'] = data
            return form_data


class ImportUser(BaseFunc):

    def databaseUser(self,ctx):
        db_user = ModelsInstanceFuncdetails().get_AllFuncDetails() #ModelsFuncDetails().get_allFuncDetails()
        plone_user = ctx.context.acl_users.getUserIds()

        cont = 0
        D={}
        for user in db_user:
            if not user.get('username') in plone_user and\
                   user.get('username') != 'admin':
                cont += 1

        D['user_new'] = cont
        D['user_all'] = len(db_user)
        D['user_plone'] = len(plone_user)

        return D

    def importUser(self,ctx,form,user={}):
        db_user = ModelsInstanceFuncdetails().get_AllFuncDetails() #ModelsFuncDetails().get_allFuncDetails()
        plone_user = ctx.context.acl_users.getUserIds()
        #db_user = ModelsFuncDetails().get_allFuncDetails()
        #plone_user = ctx.context.acl_users.getUserIds()

        portal_member = ctx.context.portal_membership
        D={}
        index = int(form.get('numb_user','0'))
        if not user:
            user = db_user[index]

        user_properties = {'fullname':user.get('name',''),
                           'email':user.get('email',''),
                           #'home_page':user.blogs,
                           #'location':user.location,
                           #'description':user.customised_message,
                           }

        username = user.get('username','')
        if portal_member.getMemberById(username):
            portal_member.getMemberById(username).setMemberProperties(user_properties)

        else:
            if username != '':
                user_properties['username'] = username
                user_properties['password'] = username

                portal_member.addMember(id=username,
                                        password=username,
                                        roles=("Member",),
                                        domains="",
                                        properties=user_properties)

        D['username'] = username
        D['fullname'] = user.get('name','')
        D['email'] = user.get('email','')

        return D
