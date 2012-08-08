# coding: utf-8

from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.interfaces import ISiteRoot

from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer

from zope.app.component.hooks import getSite

from vindula.myvindula import MessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

from datetime import date, datetime 
import logging, base64

from vindula.myvindula.validation import valida_form

from vindula.myvindula.user import BaseFunc, ModelsFuncDetails,\
                                   ModelsFuncHolerite, ModelsFuncHoleriteDescricao

from vindula.myvindula.registration import SchemaFunc, SchemaConfgMyvindula, ImportUser, ManageCourses, ManageLanguages
from vindula.chat.utils.models import ModelsUserOpenFire
from vindula.myvindula.utils import UtilMyvindula

logger = logging.getLogger('vindula.myvindula')



class MyVindulaConfgsView(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindulaconfgs')
    
    ignoreContext = True
    
    label = _(u"The Configuration Register myvindula")
    description = _(u"Change the Settings of the Register myvindula.")   
    
    def load_form(self):
        return SchemaConfgMyvindula().configuration_processes(self)



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
    





class MyVindulaManageAllUser(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindulamanagealluser')
    
    def checa_login(self):
        membership = self.context.portal_membership
        groups = self.context.portal_groups
        
        user_login = membership.getAuthenticatedMember()
        user_groups = groups.getGroupsByUserId(user_login.getId())
        
        checa = False
        if 'Manager' in user_login.getRoles():
            checa = True
        else:
            for i in user_groups:
                if i.id == 'manage-user':
                    checa = True
                    break 
        
        return checa            
    
    def load_list(self):
        form = self.request.form
        config_muit_user = self.context.restrictedTraverse('@@myvindula-conf-userpanel').config_muit_user()
        
        if self.checa_login():
            #vars = BaseFunc().getParametersFromURL(self)
            if 'title' in form.keys() and not 'all' in form.keys():
                title = form.get('title','').strip()
                departamento= form.get('departamento','0')
                ramal = form.get('ramal','').strip()
                result = self.rs_to_list(ModelsFuncDetails().get_FuncBusca(unicode(title, 'utf-8'),
                                                           unicode(departamento,'utf-8'),
                                                           unicode(ramal, 'utf-8')))
            
            elif not config_muit_user:
                result = self.rs_to_list(ModelsFuncDetails().get_FuncBusca('','0',''))
                
            elif 'all' in form.keys():
                result = self.rs_to_list(ModelsFuncDetails().get_FuncBusca('','0',''))
            
            else:
                result = None
            
            return result
        else:
            self.request.response.redirect(self.context.absolute_url() + '/login')



class MyVindulaDelHoleriteView(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-del-holerite')
    
    def update(self):
        form = self.request.form
        success_url = self.context.absolute_url() + '/myvindula-import-holerite'
        if 'date' in form.keys() and 'empresa' in form.keys():
            data_lote = form['date']
            
            try:empresa = unicode(form['empresa'],'utf-8')
            except:empresa = form['empresa']

            data_lote = datetime.strptime(data_lote,'%Y-%m-%d %H:%M')
            ModelsFuncHolerite().del_HoleritesLote(data_lote,empresa)
            
        self.request.response.redirect(success_url)
    
    def render(self):
        pass
    
    
    
    
class MyVindulaImportHoleriteView(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-import-holerite')
    
    def get_lastImport(self):
        result = ModelsFuncHolerite().get_FuncHolerites_Import()
        if result: 
            return result
        else:
            return []
        
    def load_file(self):
        from pprint import pprint
        from copy import copy
        form = self.request.form
        erro = False
        holerite_erro = None
        holerites = []
        modelo_holerite = {'cod_empresa':None,
                           'empresa':None,
                           'endereco_empresa':None,
                           'estado_empresa':None,
                           'cnpj_empresa':None,
                           'competencia':None,
                           'matricula':None,
                           'nome':None,
                           'cpf':None,
                           'completo':False,
                           'itens_holerite':[],
                           'itens_holerite_check':False,
                           'total_vencimento':None,
                           'total_desconto':None,
                           'valor_liquido':None,
                           'salario_base':None,
                           'base_Inss':None,
                           'base_fgts':None,
                           'fgts_mes':None,
                           'base_irrf':None}
        
        holerite = copy(modelo_holerite)
        
        if 'load_file' in form.keys():            
            if 'txt_file' in form.keys():
                file = form.get('txt_file','')
                if file:
                    texto = file.read()
                    texto = texto.replace('\r','').replace('\x1b2','') #.replace('#','')
                    cont = 1
                    
                    for linha in texto.split('\n'):
                        #Checando linhas vazias, se a linha for vazia ou só espaço, vai retornar uma lista vazia e nao entrar no if.
                        check_linha = [i for i in linha.split(' ') if i != '']
                        
                        #Pulando linhas vazias
                        if check_linha != []:
                            #Buscando cod_empresa e empresa
                            if holerite['cod_empresa'] == None:                                
                                holerite['cod_empresa'] = linha[:4]
                                holerite['empresa'] = linha[5:]
                            
                            #Buscando dados de endereço
                            elif holerite['endereco_empresa'] == None: 
                                linha_list = [i for i in linha.lstrip().rstrip().split('  ') if i != '']
                                holerite['endereco_empresa'] = ' '.join(linha_list[:-1])
                                holerite['estado_empresa'] = linha[len(linha_list)-1].lstrip()
                                                        
                            elif holerite['cnpj_empresa'] == None:
                                linha_list = [i for i in linha.lstrip().rstrip().split(' ') if i != '']
                                holerite['cnpj_empresa'] = linha_list[0]
                                holerite['competencia'] = linha_list[1]
                                
                            elif holerite['matricula'] == None:
                                holerite['matricula'] = linha.split(' ')[0]
                                linha_list = [i for i in linha.split(' ')[+1:] if i != '']
                                holerite['nome'] = ' '.join(linha_list[:-1]) 
                                holerite['cpf'] = linha_list[len(linha_list)-1]
                            
                            #Importando itens do holerite
                            elif holerite['matricula'] != None and holerite['itens_holerite_check'] == False:
                                    itens_holerite = {'codigo':None,
                                                      'descricao':None,
                                                      'ref':None,
                                                      'vencimentos':None,
                                                      'descontos':None,}
                                    
                                    itens = copy(itens_holerite)
                                    
                                    itens['codigo'] = linha.split('  ')[0].split(' ')[0] 
                                    itens['descricao'] = ' '.join(linha.split('  ')[0].split(' ')[+1:])
                                    
                                    if itens['codigo'] != '' and itens['codigo'].isdigit() and cont <= 15:
                                        linha_valores = [i for i in linha.split('  ')[+1:] if i != '']
                                        
                                        if len(linha_valores) > 1:
                                            itens['ref'] = linha_valores[0]
                                            valor_indefinido = linha_valores[1]
                                        else:
                                            valor_indefinido = linha_valores[0]
            
                                        if linha[linha.find(valor_indefinido):].count(' ') >= 26:                                    
                                            itens['vencimentos'] = valor_indefinido
                                        else:
                                            itens['descontos'] = valor_indefinido
                                        
                                        holerite['itens_holerite'].append(itens)
                                        cont = cont + 1    
                                    else:
                                        holerite['itens_holerite_check'] = True
                                        
                            #Separando valores da linha, para distinguir observacao de valor liquido e valor desconto
                            linha_obervacao = [i for i in linha.split('  ') if i != '' and i != ' ']
                            
                            if linha.lstrip().rstrip() == '##########':                    
                                #Marca o holerite como completo e vai para o proximo
                                holerite['completo'] = True   
                            
                            elif holerite['total_vencimento'] == None and holerite['itens_holerite_check'] == True:
                                linha_list = [i for i in linha.lstrip( ).rstrip().split('  ') if i != '']
                                if len(linha_list) == 3:
                                    # Linha[0] mensagem ignorada
                                    holerite['observacao'] = linha_list[0]
                                    holerite['total_vencimento'] = linha_list[1]
                                    holerite['total_desconto'] = linha_list[2]
                                elif len(linha_list) == 2:
                                    holerite['total_vencimento'] = linha_list[0]
                                    holerite['total_desconto'] = linha_list[1]
                                
                                elif len(linha_list) == 1:
                                    holerite['observacao'] = linha_list[0]
                                #else:
                                #    #Marca o holerite como completo e vai para o proximo
                                #    holerite['completo'] = True
                            elif holerite.has_key('observacao') and len(linha_obervacao) == 1 and linha[0] != ' ' and holerite['valor_liquido'] == None:
                                holerite['observacao'] = holerite['observacao'] +' '+ linha_obervacao[0]
                                

                            elif holerite['total_desconto'] != None and holerite['valor_liquido'] == None:
                                linha_list = [i for i in linha.lstrip().rstrip().split(' ') if i != '']
                                holerite['valor_liquido'] = linha_list[0] 
                            
                            elif holerite['valor_liquido'] != None and  holerite['salario_base'] == None:
                                linha_list = [i for i in linha.lstrip().rstrip().split(' ') if i != '']
                                holerite['salario_base'] = linha_list[0]
                                holerite['base_Inss'] = linha_list[1]
                                holerite['base_fgts'] = linha_list[2]
                                holerite['fgts_mes'] = linha_list[3]
                                holerite['base_irrf'] = linha_list[4]
                               
                                holerite['completo'] = True

                                
                            if holerite['completo'] == True:
                                holerites.append(holerite)
                                holerite = copy(modelo_holerite)
                                holerite['itens_holerite'] = []
                                cont = 1
                            
                    if holerites:
                        for holerite in holerites:
                            itens = copy(holerite['itens_holerite'])
                            convertido = self.converte_dadosByDB(holerite)
                            id = ModelsFuncHolerite().set_FuncHolerite(**convertido)
                            
                            for item in itens:
                                item['vin_myvindula_holerite_id'] = id
                                desc_convertido = self.converte_dadosByDB(item)
                                ModelsFuncHoleriteDescricao().set_FuncHoleriteDescricao(**desc_convertido)
                            
                    
        else:
            return None
        
     
#    def load_file_old(self):
#        form = self.request.form
#        if 'load_file' in form.keys():
#            
#            if 'txt_file' in form.keys():
#                file = form.get('txt_file','')
#                if file:
#                    texto = file.read()
#                    texto = texto.replace('\r','')
#                    registros = texto.split('\x1b2\n')
#                    for reg in registros:
#                        D = {}
#                        L = []
#                        linhas = reg.split('\n')
#                        max = len(linhas)-1
#                        cont = 0
#                        entra = False
#                        #while cont <= max:
#                        
#                        for linha in linhas:
#                            
#                            #linha = linhas[cont]
#                            if len(linha) == 80:
#                                entra = True
#                                if cont == 0:
#                                    D['cod_empresa'] = linha[0:3] 
#                                    D['empresa'] = linha[5:51]
#                                    #D['cnomeidade_empresa'] = linha[] 
#                                
#                                elif cont == 1:
#                                    D['endereco_empresa'] = linha[5:60]                    
#                                    D['estado_empresa'] = linha[60:62]
#                                
#                                elif cont == 2:    
#                                    D['cnpj_empresa'] = linha[5:23]
#                                    tmp = linha[56:63]
#                                    tmp = tmp.strip()
#                                    tmp = tmp.split('/')
#                                    D['competencia'] = tmp[1]+'/'+tmp[0] 
#                                
#                                elif cont == 4:
#                                    
#                                    D['matricula'] = linha[0:5]
#                                    D['nome'] = linha[6:51]
#                                    D['cpf']  = linha[69:80]
#                    
#                                elif cont >= 8 and cont <= 23:
#                                    E = {}
#                                    E['codigo'] = linha[0:3]
#                                    E['descricao'] = linha[4:33]
#                                    E['ref'] = linha[34:43]
#                                    E['vencimentos'] = linha[44:57]
#                                    E['descontos'] = linha[58:70]
#                                    
#                                    L.append(E)
#                                elif cont == 24:
#                                    D['total_vencimento'] = linha[42:55]
#                                    D['total_desconto'] = linha[56:70]
#                                
#                                elif cont == 26:
#                                    D['valor_liquido'] = linha[56:70]
#                                    
#                                elif cont == 28:
#                                    D['salario_base'] = linha[0:13]
#                                    D['base_Inss'] = linha[14:25]
#                                    D['base_fgts'] = linha[26:38]
#                                    D['fgts_mes'] = linha[40:50]
#                                    D['base_irrf'] = linha[52:70]
#                            if entra:    
#                                cont += 1
#                        if D:
#                            convertido = self.converte_dadosByDB(D)
#                            id = ModelsFuncHolerite().set_FuncHolerite(**convertido)
#                            for item in L:
#                                try:
#                                    item['vin_myvindula_holerite_id'] = id
#                                    desc_convertido = self.converte_dadosByDB(item)
#                                    ModelsFuncHoleriteDescricao().set_FuncHoleriteDescricao(**item)
#                                except:
#                                    item['vin_myvindula_holerite_id'] = id
#                                    desc_convertido = self.converte_dadosByDB(item)
#                                    ModelsFuncHoleriteDescricao().set_FuncHoleriteDescricao(**item)
#        
#        else:
#            return None
                
        
        
class MyVindulaCoursesView(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-courses')
    
    def load_list(self):
        return ManageCourses().load_courses(self)

        
class MyVindulaManageCoursesView(grok.View, UtilMyvindula):        
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-manage-courses')    

    def load_form(self):
        return ManageCourses().registration_processes(self)      

class MyVindulaLanguagesView(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-languages')
    
    def load_list(self):
        return ManageLanguages().load_languages(self)
        
class MyVindulaManageLanguagesView(grok.View, UtilMyvindula):        
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-manage-languages')    

    def load_form(self):
        return ManageLanguages().registration_processes(self)
    
class MyVindulaImportFirstView(grok.View,UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-import-first')
    
    def load_file(self):
        form = self.request.form               
        if 'load_file' in form.keys():
            if 'csv_file' in form.keys():
                portal = self.context
                pasta_control = getattr(portal, 'control-panel-objects')
                if pasta_control:
                    pasta_migracao = getattr(pasta_control, 'migration-users')
                    if pasta_migracao:
                        pasta = getattr(pasta_migracao, 'upload-csv')
                        if pasta:
                            arquivo = self.request.get('csv_file')
                            nome = arquivo.filename
                            
                            normalizer = getUtility(IIDNormalizer)
                            nome_arquivo = normalizer.normalize(unicode(nome, 'utf-8'))
                            
                            count = 0
                            while nome_arquivo in pasta.objectIds():
                                count +=1
                                if count != 1:
                                    nome_arquivo = nome_arquivo[:-2]
                                nome_arquivo = nome_arquivo + '-' + str(count)         
                            
                            pasta.invokeFactory('File', 
                                                id=nome_arquivo,
                                                title=nome_arquivo,
                                                description='',
                                                file=self.request.get('csv_file')
                                                )
                            campos_csv = pasta.get(nome_arquivo).data.split('\n')[0].replace('"', '').split(';')
                            arquivo = pasta.get(nome_arquivo).virtual_url_path()
                            redirect = self.context.absolute_url() + '/myvindula-import-second?url_arquivo=%s' % (arquivo)
                            return self.request.response.redirect(redirect)          
                        else:
                            IStatusMessage(self.request).addStatusMessage(_(u"Erro ao carregar arquivo, contate o administrados do portal."), "error")
                    else:
                        IStatusMessage(self.request).addStatusMessage(_(u"Erro ao carregar arquivo, contate o administrados do portal."), "error")
                else:
                    IStatusMessage(self.request).addStatusMessage(_(u"Erro ao carregar arquivo, contate o administrados do portal."), "error")
                
class MyVindulaImportSecondView(grok.View, UtilMyvindula): 
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-import-second')
    
    def to_utf8(self, value):
        return unicode(value, 'utf-8')    
    
    def load_archive(self):
        form = self.request.form
        if 'url_arquivo' in form.keys():
            path_file = form.get('url_arquivo').split('/')
            if len(path_file) == 3:
                folder = path_file[1]
                file = path_file[2]
            else:
                folder = path_file[0]
                file = path_file[1]
            folder = self.context.get(folder)
            file = folder.get(file)
            
            return file.title
            
    
    def load_fields_vindula(self):
        form = self.request.form
        fields_vin = []
        i=0
        fields = SchemaFunc().campos
        while i < len(fields.keys())-1:
              fields_vin.append(i)
              i+=1
        
        if fields:
            for field in fields:
                index = fields[field].get('ordem',0)
                D = {}
                D['name'] = field
                if field != 'username':
                    D['label'] = self.get_label_filed(field)

                fields_vin.pop(index)
                fields_vin.insert(index, D)    
                
                #fields_vin.append(D)
        return fields_vin
        
            
    def load_fields_csv(self):
        form = self.request.form
        if 'url_arquivo' in form.keys():
            path_file = form.get('url_arquivo').split('/')
            folder = getSite()[path_file[0]][path_file[1]][path_file[2]]
            file = folder.get(path_file[3])
            
            return file.data.split('\n')[0].replace('"', '').split(';')
            
    def importar_valores(self):
        form = self.request.form
        if 'import' in form.keys():
            path_file = form.get('url_arquivo').split('/')
            folder = getSite()[path_file[0]][path_file[1]][path_file[2]]
            arquivo = folder.get(path_file[3])
            
            linhas_error =[]
            lista_erros = []
            
#            folder = self.context.get(folder)
#            arquivo = folder.get(file)
            ignore_fields = ['import',
                             'url_arquivo',
                             'cria-username',
                             'atualiza-dados',
                             'username',]
            
            success = False
            criar_user = form.get('cria-username', False)
            merge_user = form.get('atualiza-dados', False)
            error = 0
            url = ''
            
            for linha in arquivo.data.split('\n')[1:-1]:
                dados = {}
                dados_linha = linha.split(';')
                check_user = False
                for campo in form.keys():
                    if form[campo] != '' and campo not in ignore_fields:
                        indice = int(form[campo])-1
                        dados[campo] = self.to_utf8(dados_linha[indice].replace('"',''))
                    else: 
                        if campo == 'username':
                            if criar_user:
                                name = dados_linha[int(form['name'])-1].replace('"','').lower().split(' ')

                                username = name[0] + name[-1]
                                cont = 1
 
                                if form['registration']:
                                    matricula = dados_linha[int(form['registration'])-1].replace('"','')    
                                    username += str(matricula)
                                
                                usr = username
                                while ModelsFuncDetails().get_FuncDetails(self.to_utf8(usr)):
                                    usr = username + str(cont)
                                    cont +=1
                                  
                                dados[campo] = self.to_utf8(usr)
                                check_user = True
                                                                   
                                    
                            elif merge_user:
                                if form[campo] != '':
                                    indice = int(form[campo])-1
                                    user = self.to_utf8(dados_linha[indice].replace('"',''))
                                    if ModelsFuncDetails().get_FuncDetails(user):    
                                            dados[campo] = user
                                            check_user = True
                            
                            else:                            
                                if form[campo] != '':
                                    indice = int(form[campo])-1
                                    user = self.to_utf8(dados_linha[indice].replace('"',''))
                                    if not ModelsFuncDetails().get_FuncDetails(user):    
                                        dados[campo] = user
                                        check_user = True

                        else:
                            dados[campo] = u''
                 
                erros, data_user = valida_form(SchemaFunc().campos, dados)
                if not erros:
                    if check_user:
                        if criar_user:
                            ModelsFuncDetails().set_FuncDetails(**data_user)
                            success = True
                        elif merge_user:
                            result = ModelsFuncDetails().get_FuncDetails(user)
                            if result:
                                success = True
                                campos = SchemaFunc().campos
                                for campo in campos.keys():
                                    value = data_user.get(campo, None)
                                    if value:
                                        setattr(result, campo, value)
                        else:
                            ModelsFuncDetails().set_FuncDetails(**data_user)
                            success = True
                    else:
                        error = 1
                else:
                    linhas_error.append(linha)
                    lista_erros.append(erros)
                    error = 2
                    success = False
                
                logger.info("%s - %s "% (erros,data_user))
                    
            if linhas_error:
                success = False
                campos = arquivo.data.split('\n')[0].replace('\r','')
                text = ''
                col = ''
                for campo in campos.split(';'):
                    col += campo+';'
                
                col += 'coluna erro;\n'
                text = col
                i = 0
                
                for linha in linhas_error:
                    text += linha.replace('\r','') + ';'+str(lista_erros[i].keys())+'\n'   
                    i +=1
                    
                text += '\n'
                
                nome_arquivo = 'error-import-'+ datetime.now().strftime('%Y-%M-%d_%H-%M-%S') +'.csv'
                pasta_error = getSite()['control-panel-objects']['migration-users']['errors-import']
                pasta_error.invokeFactory('File', 
                                            id=nome_arquivo,
                                            title=nome_arquivo,
                                            description='',
                                            file=text)
                url=pasta_error[nome_arquivo].absolute_url()
                             
            redirect = self.context.absolute_url() + '/myvindula-import-third?success=%s&error=%s&url=%s' % (success,error,url)
            return self.request.response.redirect(redirect)   
            
                
class MyVindulaImportThirdView(grok.View,UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-import-third')
                
class MyVindulaExportUsersView(grok.View,UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-export-users')
    
    def export_users(self):
        form = self.request.form
        if 'export' in form.keys():
            self.request.response.setHeader("Content-Type", "text/csv", 0)
            filename = 'myvindula-export-users.csv'
            self.request.response.setHeader('Content-Disposition','attachment; filename=%s'%(filename))
            
            fields_orig = ModelsFuncDetails()._storm_columns.values()

            campos_vin = []
            text = ''
            
            if fields_orig:
                for field in fields_orig:
                    campos_vin.append(field.name)
                    text += field.name + ';'
                text = text[:-1] + '\n'

            users = ModelsFuncDetails().get_allFuncDetails()

            for user in users:
                for campo in campos_vin:
                    if campo not in ('skills_expertise', 'languages'):
                        valor = user.__getattribute__(campo)
                        if valor == None:
                            valor = ''
                        
                        if campo == 'customised_message':
                            valor = str(valor).replace('\n', '').replace('\r', '').replace(';', '')
                        
                        text += '%s;' % (valor)
                text += '\n'
                 
            self.request.response.write(str(text))
        
        
        
        