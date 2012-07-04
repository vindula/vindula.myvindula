# coding: utf-8

from vindula.myvindula import MessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage
from datetime import date , datetime
from vindula.myvindula.validation import valida_form

from vindula.myvindula.user import BaseFunc, ModelsDepartment, ModelsFuncDetails,\
                                   ModelsMyvindulaFuncdetailCouses,ModelsMyvindulaCourses,\
                                   ModelsMyvindulaFuncdetailLanguages, ModelsMyvindulaLanguages,\
                                   ModelsConfgMyvindula
               
class SchemaFunc(BaseFunc):
    def to_utf8(value):
        return unicode(value, 'utf-8')

    campos = {'name'                  : {'required': False, 'type' : to_utf8, 'label':'Nome',                   'decription':u'Digite o nome do funcionário',                   'ordem':0},
              'nickname'              : {'required': False, 'type' : to_utf8, 'label':'Apelido',                'decription':u'Digite o apelido do funcionário',                'ordem':1},
              'phone_number'          : {'required': False, 'type' : to_utf8, 'label':'Telefone',               'decription':u'Digite o telefone do funcionário',               'ordem':2},
              'cell_phone'            : {'required': False, 'type' : to_utf8, 'label':'Celular',                'decription':u'Digite o telefone celular do funcionário',       'ordem':3},
              'email'                 : {'required': False, 'type' : 'email', 'label':'E-mail',                 'decription':u'Digite o e-mail do funcionário',                 'ordem':4},
              'employee_id'           : {'required': False, 'type' : to_utf8, 'label':'ID Funcionário',         'decription':u'Digite o ID do funcionário',                     'ordem':5},
              'date_birth'            : {'required': False, 'type' : date,    'label':'Data de Nascimento',     'decription':u'Digite a data de nascimento do funcionário',     'ordem':6},
              'registration'          : {'required': False, 'type' : to_utf8, 'label':'Matrícula',              'decription':u'Digite o número de matrícula do funcionário',    'ordem':7},
              'enterprise'            : {'required': False, 'type' : to_utf8, 'label':'Empresa',                'decription':u'Digite o nome da empresa do funcionário',        'ordem':8},
              'position'              : {'required': False, 'type' : to_utf8, 'label':'Cargo',                  'decription':u'Digite o cargo do funcionário',                  'ordem':9},
              'admission_date'        : {'required': False, 'type' : date,    'label':'Data de Admissão',       'decription':u'Digite a data de admissão do funcionário',       'ordem':10},
              'cost_center'           : {'required': False, 'type' : to_utf8, 'label':'Centro de Custo',        'decription':u'Digite o centro de custo do funcionário',        'ordem':11},
              'organisational_unit'   : {'required': False, 'type' : to_utf8, 'label':'Unidade organizacional', 'decription':u'Digite a unidade organizacional do funcionário', 'ordem':12},
              'reports_to'            : {'required': False, 'type' : to_utf8, 'label':'Reporta-se a',           'decription':u'Digite a quem o funcionário se reporta',         'ordem':13},
              'location'              : {'required': False, 'type' : to_utf8, 'label':'Localização',            'decription':u'Digite a localização do funcionário',            'ordem':14},
              'postal_address'        : {'required': False, 'type' : to_utf8, 'label':'Endereço Postal',        'decription':u'Digite o endereço postal do funcionário',        'ordem':15},
              'special_roles'         : {'required': False, 'type' : to_utf8, 'label':'Funções Especiais',      'decription':u'Digite as funções especiais do funcionário',     'ordem':16},
              'photograph'            : {'required': False, 'type' : 'file',  'label':'Foto',                   'decription':u'Coloque a foto do funcionário',                  'ordem':17},
              'pronunciation_name'    : {'required': False, 'type' : to_utf8, 'label':'Pronuncia do nome',      'decription':u'Como se pronuncia o  nome do funcionário',       'ordem':18},
              'committess'            : {'required': False, 'type' : to_utf8, 'label':'Comissão',               'decription':u'Digite a comissão do funcionário',               'ordem':19},
              'projects'              : {'required': False, 'type' : to_utf8, 'label':'Projetos',               'decription':u'Digite os projetos do funcionário',              'ordem':20},
              'personal_information'  : {'required': False, 'type' : to_utf8, 'label':'Informações pessoais',   'decription':u'Digite as informações pessoais do funcionário',  'ordem':21},
              'skills_expertise'      : {'required': False, 'type' : to_utf8, 'label':'Habilidades'          ,  'decription':u'Digite as habilidades do funcionário',           'ordem':22},
              'profit_centre'         : {'required': False, 'type' : to_utf8, 'label':'Centro de Lucro',        'decription':u'Digite o centro de lucro do funcionário',        'ordem':23},
              'languages'             : {'required': False, 'type' : to_utf8, 'label':'Idioma',                 'decription':u'Digite o idioma do funcionário',                 'ordem':24},
              'availability'          : {'required': False, 'type' : to_utf8, 'label':'Disponibilidade',        'decription':u'Digite a disponibilidade do funcionário',        'ordem':25},
              'papers_published'      : {'required': False, 'type' : to_utf8, 'label':'Artigos Publicados',     'decription':u'Digite os artigo publicados do funcionário',     'ordem':26},
              'blogs'                 : {'required': False, 'type' : to_utf8, 'label':'Blogs',                  'decription':u'Digite os blogs do funcionário',                 'ordem':27},
              'teaching_research'       : {'required': False, 'type' : to_utf8, 'label':'CPF',                  'decription':u'Digite o CPF do funcionário',                    'ordem':28},
              'resume'                  : {'required': False, 'type' : to_utf8, 'label':'Personalizado 2',        'decription':u'Campo para personalizar',                      'ordem':29},
              'delegations'             : {'required': False, 'type' : to_utf8, 'label':'Personalizado 3',        'decription':u'Campo para personalizar',                      'ordem':30},
              'customised_message'      : {'required': False, 'type' : to_utf8, 'label':'Personalizado 4',        'decription':u'Campo para personalizar',                      'ordem':31},
              
              'username'                : {'required': True, 'type' : to_utf8, 'label':'Nome de Usuário',        'decription':u'Digite o CPF do funcionário',                    'ordem':28},}  #Campo Obrigatorio
              #'vin_myvindula_department_id': {'required': False, 'type' : int,     'label':'Departamento'           },} #Campo Obrigatorio

                    
    def registration_processes(self,context,user,manage=False):
        success_url = context.context.absolute_url() + '/@@myvindula'
        success_url_manage = context.context.absolute_url() + '/@@myvindulamanagealluser'
        access_denied = context.context.absolute_url() + '/login'
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        campos = self.campos
        #user = context.context.portal_membership.getAuthenticatedMember()

        if not manage:
            try:
                user_id = unicode(user.getUserName(), 'utf-8')    
            except:
                user_id = user.getUserName()
         
        else:
            if user != 'acl_users':
                user_id = user.username
            else:
                user_id = unicode('acl_users','utf-8')
        
        conf = {}
        for item in campos.keys():
            try: conf[item] = ModelsConfgMyvindula().getConfig_edit(item)
            except:conf[item] = True
        
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,
            'departametos': ModelsDepartment().get_department(),
            'username' : user_id,
            'config_myvindula':conf,
            'manage':manage,}
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            if manage:
                context.request.response.redirect(success_url_manage)
            else:
                context.request.response.redirect(success_url)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            # chama a funcao que valida os dados extraidos do formulario (valida_form) 
            errors, data = valida_form(campos, context.request.form)  

            if not errors:
                # Upload of Photograph
#                if 'photograph' in form_keys:
#                    if type(form['photograph']) == str:
#                        data['photograph'] = unicode(form['photograph'], 'utf-8')
#                        
#                    else:
#                        if form['photograph'].filename != '':
#                            path = context.context.portal_membership.getHomeFolder()
#                            file = data['photograph']
#                            if path:
#                                photo = BaseFunc().uploadFile(context,path,file)
#                                if photo:
#                                    data['photograph'] = photo
#                                else:
#                                    access_denied = context.context.absolute_url() + '/@@myvindulaprefs?error=1'
#                                    return context.request.response.redirect(access_denied)
#                            else:
#                                access_denied = context.context.absolute_url() + '/@@myvindulaprefs?error=2'
#                                return context.request.response.redirect(access_denied)
#                            
#                        else:
#                            data['photograph'] = None      
                
                if 'vin_myvindula_department' in form_keys:
                    L = []
                    ModelsDepartment().del_department(user_id)
                    
                    if not type(form['vin_myvindula_department']) == list:
                        L.append(form['vin_myvindula_department'])
                    else:
                        L = form['vin_myvindula_department']
                    
                    for departament in L:
                        D={}
                        D['UID'] = unicode(departament,'utf-8')
                        D['funcdetails_id'] = user_id
                        ModelsDepartment().set_department(**D)
                        
                        #context.context.addUserGroup(user_id,departament)
                            
                if 'skills_expertise' in form_keys:
                    ModelsMyvindulaFuncdetailCouses().del_funcdetailCouser(user_id)
                    for curso in form['skills_expertise']:
                        D={}
                        D['username'] = user_id
                        D['id_courses'] = int(curso)
                        ModelsMyvindulaFuncdetailCouses().set_funcdetailCouser(**D)
        
                
                if 'languages' in form_keys:
                    ModelsMyvindulaFuncdetailLanguages().del_funcdetailLanguages(user_id)
                    for languages in form['languages']:
                        D={}
                        D['username'] = user_id
                        D['id_courses'] = int(languages)
                        ModelsMyvindulaFuncdetailLanguages().set_funcdetailLanguages(**D)
                
                if user_id != 'acl_users':
                    # editando...
                    result = self.store.find(ModelsFuncDetails, ModelsFuncDetails.username == user_id).one()
                    if result:
#                        if data['photograph'] is None:
#                            data['photograph'] = result.photograph
                        
                        for campo in campos.keys():
                            value = data.get(campo, None)
                            setattr(result, campo, value)

                    else:
                        #adicionando...
                        database = ModelsFuncDetails(**data)
                        self.store.add(database)
                        self.store.flush()
                        
                    #dicionario para edição do usuario do plone
                    user_plone = {'fullname':data.get('name',''),
                                  'email':data.get('email',''),
                                  'home_page':data.get('blogs',''),
                                  'location':data.get('location',''),
                                  'description':data.get('customised_message','')}
                    
                    if not manage:
                        user.setMemberProperties(user_plone)
                        
                elif user_id == 'acl_users':
                    diff = False
                    path_user = u''
                    if form.get('username', None) !=\
                        form.get('username-old', None): 
                        
                        try:user_del = unicode(form.get('username-old'),'utf-8')
                        except:user_del = form.get('username-old')
                        
                        path_user = ModelsFuncDetails().del_FuncDetails(user_del)
                        diff = True
                    
                    #Adicionando...
                    result = self.store.find(ModelsFuncDetails, ModelsFuncDetails.username == data.get('username','')).one()
                    if not result:
                        #data['photograph'] = path_user
                        
                        database = ModelsFuncDetails(**data)
                        self.store.add(database)
                        self.store.flush()
                        
                    elif not diff:
#                        if data['photograph'] is None:
#                            data['photograph'] = result.photograph
                        
                        for campo in campos.keys():
                            value = data.get(campo, None)
                            setattr(result, campo, value)

                    else:
                       errors['username'] = 'Ja existem um usuário com este username, por favor escolha outro usernome'
                       
                       form_data['errors'] = errors
                       form_data['data'] = data
                       return form_data 
                
                #Redirect back to the front page with a status message
                IStatusMessage(context.request).addStatusMessage(_(u"Seu perfil foi editado com sucesso!!"), "info")
                if manage:
                    context.request.response.redirect(success_url_manage)
                else:
                    context.request.response.redirect(success_url)
                                   
            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data
          
        # se clicou em excluir
        elif 'form.excluir' in form_keys:
            if user_id == 'acl_users':
                if form.get('username', None) !=\
                    form.get('username-old', None): 
                
                    try: user_id = unicode(form.get('username-old'))
                    except: user_id = form.get('username-old')
                else:
                    try: user_id = unicode(form.get('username'))
                    except: user_id = form.get('username')
                    
            record = self.store.find(ModelsFuncDetails, ModelsFuncDetails.username == user_id).one()

            self.store.remove(record)
            self.store.flush()
            
            IStatusMessage(context.request).addStatusMessage(_(u'Removido com sucesso.'),"erro")
            context.request.response.redirect(success_url_manage)
          
        # se for um formulario de edicao 
        elif user_id != 'acl_users':
            data = self.store.find(ModelsFuncDetails, ModelsFuncDetails.username == user_id).one()
            
            if data:
                departaments = ModelsDepartment().get_departmentByUsername(user_id)
                D = {}
                
                for campo in campos.keys():
                    D[campo] = getattr(data, campo, '')
              
                D['vin_myvindula_department'] = departaments
                
                form_data['data'] = D
                return form_data
            else:
               return form_data
              
        # se o usuario não estiver logado
        else:
            #IStatusMessage(context.request).addStatusMessage(_(u'Erro ao salvar o registro.'),"erro")
            #context.request.response.redirect(access_denied)
            
            return form_data
        
class SchemaConfgMyvindula(BaseFunc):
    
    campos = {#Campos Edição
              'vin_myvindula_department': {'required': False, 'type' : bool, 'label':'Departamento',      'ordem':0},
              'name'                    : {'required': False, 'type' : bool, 'label':'Nome',              'ordem':1},
              'nickname'                : {'required': False, 'type' : bool, 'label':'Apelido',           'ordem':2},
              'phone_number'            : {'required': False, 'type' : bool, 'label':'Telefone',          'ordem':3},
              'cell_phone'              : {'required': False, 'type' : bool, 'label':'Celular',           'ordem':4},
              'email'                   : {'required': False, 'type' : bool, 'label':'E-mail',            'ordem':5},
              'employee_id'             : {'required': False, 'type' : bool, 'label':'ID Funcionário',    'ordem':6},
              'date_birth'            : {'required': False, 'type' : bool, 'label':'Data de Nascimento',     'ordem':7},
              'registration'          : {'required': False, 'type' : bool, 'label':'Matrícula',              'ordem':8},
              'enterprise'            : {'required': False, 'type' : bool, 'label':'Empresa',                'ordem':9},
              'position'              : {'required': False, 'type' : bool, 'label':'Cargo',                  'ordem':10},
              'admission_date'        : {'required': False, 'type' : bool, 'label':'Data de Admissão',       'ordem':11},
              'cost_center'           : {'required': False, 'type' : bool, 'label':'Centro de Custo',        'ordem':12},
              'organisational_unit'   : {'required': False, 'type' : bool, 'label':'Unidade organizacional', 'ordem':13},
              'reports_to'            : {'required': False, 'type' : bool, 'label':'Reporta-se a',           'ordem':14},
              'location'              : {'required': False, 'type' : bool, 'label':'Localização',            'ordem':15},
              'postal_address'        : {'required': False, 'type' : bool, 'label':'Endereço Postal',        'ordem':16},
              'special_roles'         : {'required': False, 'type' : bool, 'label':'Funções Especiais',      'ordem':17},
              'photograph'            : {'required': False, 'type' : bool, 'label':'Foto',                   'ordem':18},
              'pronunciation_name'    : {'required': False, 'type' : bool, 'label':'Pronuncia do nome',      'ordem':19},
              'committess'            : {'required': False, 'type' : bool, 'label':'Comissão',               'ordem':20},
              'projects'              : {'required': False, 'type' : bool, 'label':'Projetos',               'ordem':21},
              'personal_information'  : {'required': False, 'type' : bool, 'label':'Informações pessoais',   'ordem':22},
              'skills_expertise'      : {'required': False, 'type' : bool, 'label':'Habilidades'          ,  'ordem':23},
              'profit_centre'         : {'required': False, 'type' : bool, 'label':'Centro de Lucro',        'ordem':24},
              'languages'             : {'required': False, 'type' : bool, 'label':'Idioma',                 'ordem':25},
              'availability'          : {'required': False, 'type' : bool, 'label':'Disponibilidade',        'ordem':26},
              'papers_published'      : {'required': False, 'type' : bool, 'label':'Artigos Publicados',     'ordem':27},
              'blogs'                 : {'required': False, 'type' : bool, 'label':'Blogs',                  'ordem':28},
              'teaching_research'     : {'required': False, 'type' : bool, 'label':'CPF',                    'ordem':29},
              'resume'                : {'required': False, 'type' : bool, 'label':'Personalizado 2',        'ordem':30},
              'delegations'           : {'required': False, 'type' : bool, 'label':'Personalizado 3',        'ordem':31},
              'customised_message'    : {'required': False, 'type' : bool, 'label':'Personalizado 4',        'ordem':32},
              
              }
   
    def configuration_processes(self,context):
        success_url = context.context.absolute_url() + '/@@vindula-control-panel'
        access_denied = context.context.absolute_url() + '/@@overview-controlpanel'
        form = context.request # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        campos = self.campos
        config = False #ModelsConfgMyvindula().get_configuration()
       
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,}
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            context.request.response.redirect(success_url)
        
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
              # Inicia o processamento do formulario
              # chama a funcao que valida os dados extraidos do formulario (valida_form) 
              errors, data = valida_form(campos, context.request.form)  
              
              if not errors:
                  
                  for campo in campos.keys():
                      edit = False
                      L = []
                      for i in form_keys:
                          if campo in i:
                              L.append(i)  
                      
                      
                      result = ModelsConfgMyvindula().get_configuration_By_fields(campo)
                      if result:
                          edit = True
                              
                      D = {}
                      for item in L:
                        if 'edit' in item:
                            if form.get(item):
                                D['ativo_edit'] = True
                            else:
                                D['ativo_edit'] = False
                               
                        elif 'view' in item:
                            if form.get(item):
                                D['ativo_view'] = True 
                            else:
                                D['ativo_view'] = False
                            
                        elif 'label' in item:
                            try: valor = unicode(form.get(item),'utf-8')
                            except: valor = form.get(item)
                            
                            D['label'] = valor
                      
                      if not 'ativo_edit' in D.keys():
                          D['ativo_edit'] = False
                      
                      if not 'ativo_view' in D.keys():
                          D['ativo_view'] = False
                      
                      if edit:
                          for data in D.keys():
                              setattr(result, data, D.get(data))
                              self.store.flush()
                      else:
                          try: field = unicode(campo,'utf-8')
                          except: field = campo
                          D['fields'] = field
                          ModelsConfgMyvindula().set_configuration(**D)  
                  
                  
#                  if config:
#                      
#                          value = data.get(campo, None)
#                          setattr(config, campo, value)
#
#                  else:
#                      # adicionando...
#                      configuration = ModelsConfgMyvindula(**data)
#                      self.store.add(configuration)
#                      self.store.flush()
                  
                  context.request.response.redirect(success_url)        
                       
              else:
                  form_data['errors'] = errors
                  form_data['data'] = data
                  return form_data
          
        # se for um formulario de edicao
#        elif config:    
#            D = {}
#            for campo in campos.keys():
#                D[campo] = getattr(config, campo, '')
#            
#            form_data['data'] = D
#            return form_data
              
        # se for um formulario de adicao
        else:
            D = {}
            for campo in campos.keys():
                result = ModelsConfgMyvindula().get_configuration_By_fields(campo)
                dados = {}
                if result:
                    label = result.label
                    if label:
                        dados['label'] = label
                    else:
                        dados['label'] = campos[campo].get('label')
                    dados['edit'] = result.ativo_edit
                    dados['view'] = result.ativo_view

                else:
                    dados['label'] = campos[campo].get('label')
                    dados['edit'] = True
                    dados['view'] = True
            
            
                D[campo] = dados
            form_data['data'] = D
            return form_data

 
 
class ImportUser(BaseFunc):
    
    def databaseUser(self,ctx):
        db_user = ModelsFuncDetails().get_allFuncDetails()
        plone_user = ctx.context.acl_users.getUserIds()
        cont = 0 
        D={}
        for user in db_user:
            if not user.username in plone_user: 
                cont += 1
               
        D['user_new'] = cont
        D['user_all'] = db_user.count()
        D['user_plone'] = len(plone_user) 

        return D
        
    def importUser(self,ctx,form):
        db_user = ModelsFuncDetails().get_allFuncDetails()
        plone_user = ctx.context.acl_users.getUserIds()
        portal_member = ctx.context.portal_membership
        D={}
        index = int(form.get('numb_user','0'))
        user = db_user[index]
        
        user_properties = {'fullname':user.name,
                           'email':user.email,
                           'home_page':user.blogs,
                           'location':user.location,
                           'description':user.customised_message,}
       
        if portal_member.getMemberById(user.username):
            portal_member.getMemberById(user.username).setMemberProperties(user_properties)
            
        else:
            
            if user.username != '':
                user_properties['username'] = user.username
                user_properties['password'] = user.username
                
                portal_member.addMember(id=user.username,
                                        password=user.username,
                                        roles=("Member",),
                                        domains="",
                                        properties=user_properties)
        
        D['username'] = user.username
        D['fullname'] = user.name
        D['email'] = user.email
        
        return D

    
class ManageCourses(BaseFunc):
    def to_utf8(value):
        return unicode(value, 'utf-8')
    
    campos = {'title'  : {'required': True,  'type' : to_utf8, 'label':'Nome do Curso',     'decription':u'Digite o nome do curso',    'ordem':0},
              'length' : {'required': False, 'type' : to_utf8, 'label':'Duração do Curso',  'decription':u'Digite a duração do curso', 'ordem':1},}
    
    def load_courses(self,ctx):
        data = ModelsMyvindulaCourses().get_allCourses()
        
        if data:
            return data
        else:
            return []
        
    
    def registration_processes(self,ctx):
        success_url = ctx.context.absolute_url() + '/myvindula-courses'
        access_denied = ctx.context.absolute_url() + '/@@vindula-control-panel'
        form = ctx.request.form # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        campos = self.campos
        
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,}
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            ctx.request.response.redirect(success_url)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            # chama a funcao que valida os dados extraidos do formulario (valida_form) 
            errors, data = valida_form(campos, form)  

            if not errors:
                
                if 'id' in form_keys:
                    # editando...
                    id = int(form.get('id'))
                    result = self.store.find(ModelsMyvindulaCourses, ModelsMyvindulaCourses.id == id).one()
                    if result:
                        for campo in campos.keys():
                            value = data.get(campo, None)
                            setattr(result, campo, value)

                else:
                    #adicionando...
                    database = ModelsMyvindulaCourses(**data)
                    self.store.add(database)
                    self.store.flush()
                        
                #Redirect back to the front page with a status message
                #IStatusMessage(ctx.request).addStatusMessage(_(u"Thank you for your order. We will contact you shortly"), "info")
                ctx.request.response.redirect(success_url)
                                   
            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data
          
        # se for um formulario de edicao 
        elif 'id' in form_keys:

            id = int(form.get('id'))
            data = self.store.find(ModelsMyvindulaCourses, ModelsMyvindulaCourses.id == id).one()
            
            D = {}
            for campo in campos.keys():
                D[campo] = getattr(data, campo, '')
              
            if data:
               form_data['data'] = D
               return form_data
            else:
               return form_data
              
        # se o usuario não estiver logado
        else:
            return form_data
    
    
class ManageLanguages(BaseFunc):
    def to_utf8(value):
        return unicode(value, 'utf-8')
    
    campos = {'title'  : {'required': True,  'type' : to_utf8, 'label':'Nome do Idioma',   'decription':u'Digite o nome do idioma',  'ordem':0},
              'level'  : {'required': False, 'type' : to_utf8, 'label':'Nível do Idioma',  'decription':u'Digite o nível do idioma', 'ordem':1},}
    
    def load_languages(self,ctx):
        data = ModelsMyvindulaLanguages().get_allLanguages()
        
        if data:
            return data
        else:
            return []
        
    
    def registration_processes(self,ctx):
        success_url = ctx.context.absolute_url() + '/myvindula-languages'
        access_denied = ctx.context.absolute_url() + '/@@vindula-control-panel'
        form = ctx.request.form # var tipo 'dict' que guarda todas as informacoes do formulario (keys,items,values)
        form_keys = form.keys() # var tipo 'list' que guarda todas as chaves do formulario (keys)
        campos = self.campos
        
        # divisao dos dicionarios "errors" e "convertidos"
        form_data = {
            'errors': {},
            'data': {},
            'campos':campos,}
        
        # se clicou no botao "Voltar"
        if 'form.voltar' in form_keys:
            ctx.request.response.redirect(success_url)
          
        # se clicou no botao "Salvar"
        elif 'form.submited' in form_keys:
            # Inicia o processamento do formulario
            # chama a funcao que valida os dados extraidos do formulario (valida_form) 
            errors, data = valida_form(campos, form)  

            if not errors:
                
                if 'id' in form_keys:
                    # editando...
                    id = int(form.get('id'))
                    result = self.store.find(ModelsMyvindulaLanguages, ModelsMyvindulaLanguages.id == id).one()
                    if result:
                        for campo in campos.keys():
                            value = data.get(campo, None)
                            setattr(result, campo, value)

                else:
                    #ModelsMyvindulaLanguages().set_languages(**data)
                    #adicionando...
                    database = ModelsMyvindulaLanguages(**data)
                    self.store.add(database)
                    self.store.flush()
                        
                #Redirect back to the front page with a status message
                #IStatusMessage(ctx.request).addStatusMessage(_(u"Thank you for your order. We will contact you shortly"), "info")
                ctx.request.response.redirect(success_url)
                                   
            else:
                form_data['errors'] = errors
                form_data['data'] = data
                return form_data
          
        # se for um formulario de edicao 
        elif 'id' in form_keys:
            id = int(form.get('id'))
            data = self.store.find(ModelsMyvindulaLanguages, ModelsMyvindulaLanguages.id == id).one()
            
            D = {}
            for campo in campos.keys():
                D[campo] = getattr(data, campo, '') 
              
            if data:
               form_data['data'] = D
               return form_data
            else:
               return form_data
              
        # se o usuario não estiver logado
        else:
            return form_data
