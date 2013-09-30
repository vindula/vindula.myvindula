# coding: utf-8

from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.interfaces import ISiteRoot

from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer

from zope.app.component.hooks import getSite

from vindula.myvindula import MessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

from datetime import date, datetime 
from random import randint
import logging, base64
from copy import copy 

from vindula.myvindula.validation import valida_form,valida_form_dinamic
from vindula.myvindula.user import BaseFunc
from vindula.myvindula.registration import SchemaFunc, SchemaConfgMyvindula, ImportUser
from vindula.chat.utils.models import ModelsUserOpenFire

from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.myvindula.models.instance_funcdetail import ModelsInstanceFuncdetails
from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails


#Import Necessario spara a migração dos dados
from vindula.myvindula.models.courses import ModelsMyvindulaCourses
from vindula.myvindula.models.languages import ModelsMyvindulaLanguages
from vindula.myvindula.models.funcdetail_couses import ModelsMyvindulaFuncdetailCouses
from vindula.myvindula.models.funcdetail_languages import ModelsMyvindulaFuncdetailLanguages


from vindula.myvindula.models.funcdetails import ModelsFuncDetails
from vindula.myvindula.models.holerite import ModelsFuncHolerite
from vindula.myvindula.models.descricao_holerite import ModelsFuncHoleriteDescricao
from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula

from vindula.myvindula.models.holerites2 import ModelsFuncHolerite02, ModelsFuncHoleriteDescricao02

from vindula.myvindula.models.photo_user import ModelsPhotoUser

logger = logging.getLogger('vindula.myvindula')



class MyVindulaConfgsView(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindulaconfgs')
    
    ignoreContext = True
    
    label = _(u"The Configuration Register myvindula")
    description = _(u"Change the Settings of the Register myvindula.")   
    
    def load_form(self):
        #return SchemaConfgMyvindula().configuration_processes(self)
        return ModelsConfgMyvindula().get_configurationAll()
    
    def update(self):
        self.BlackList = ['vin_myvindula_department','teaching_research',
                          'date_birth','email','phone_number','name','photograph']
    
class MyVindulaEditConfgsView(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('edit_myvindulaconfgs')
    
    def load_form(self):
        return SchemaConfgMyvindula().configuration_processes(self)

    def update(self):
        self.BlackList = ['vin_myvindula_department','cpf',
                          'date_birth','email','phone_number','name','photograph']

class MyVindulaEditOrdemConfgsView(grok.View, BaseFunc):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('ordem_myvindulaconfgs')

    def render(self):
        return ''

    def update(self):
        form = self.request.form
        
        if 'list' in form.keys():
            n = 0
            list = form.get('list','').split(',')
            for i in list:
                #i = i.split('|')
                campo = self.Convert_utf8(i)
                #ordem = n
                ModelsConfgMyvindula().set_ordemConfiguration(campo,n)
                n += 1
            

# View de migração do banco de dedos para a versão 1.2
class MyVindulaMigrationFuncdetailsView(grok.View,UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('migration_funcdetails')
    
    def render(self):
        return 'Migração dos dados do myvindula'
    
    
    def update(self):
       
        allUsuarios = ModelsFuncDetails().get_allFuncDetails_migracao()
        allCampos = ModelsConfgMyvindula().get_configurationAll()
        tool = UtilMyvindula()
        
        for user in allUsuarios:
            username = user.username
            user_instance = ModelsInstanceFuncdetails().get_InstanceFuncdetails(username)
            if not user_instance:
                id_instance = ModelsInstanceFuncdetails().set_InstanceFuncdetails(username)
            else:
                id_instance = user_instance.id
            
            for campo in allCampos:
                valor = None
                if campo.fields in ['vin_myvindula_department']:
                    continue
                
                if campo.fields == 'skills_expertise':
                    dado_curso = ''
                    for curso in ModelsMyvindulaCourses().get_allCourses():
                        dado_curso += curso.title +' - ' +curso.length +'\n' 
                     
                    campo.list_values = self.Convert_utf8(dado_curso)
                    
                    cursos_user = ModelsMyvindulaFuncdetailCouses().get_funcdetailCouserByUsername(username)
                    if cursos_user:
                        L = []
                        for cursos in cursos_user:
                            curso = cursos.courses
                            L.append(curso.title +' - ' +curso.length)
                        
                        valor = self.encodePickle(L)

                elif campo.fields == 'languages':
                    dado_languages = ''
                    for language in ModelsMyvindulaLanguages().get_allLanguages():
                        dado_languages += language.title +' - ' +language.level +'\n' 
                     
                    campo.list_values = self.Convert_utf8(dado_languages)
                    
                    languages_user = ModelsMyvindulaFuncdetailLanguages().get_funcdetailLanguagesByUsername(username)
                    if languages_user:
                        L = []
                        for languages in languages_user:
                            language = languages.languages
                            L.append(language.title +' - ' +language.level)
                        
                        valor = self.encodePickle(L)
               
                try:
                    if not valor:
                        valor = user.__getattribute__(campo.fields)
                except: 
                    valor = None
                
                if valor:
                    if type(valor) == datetime:
                        valor = valor.strftime('%d/%m/%Y %H:%M:%S')
                    elif type(valor) == date:
                       valor = valor.strftime('%d/%m/%Y')
                
                    result_campo = ModelsDadosFuncdetails().get_DadosFuncdetails_byInstanceAndField(id_instance,campo.fields)
                    if result_campo: 
                        result_campo.valor = self.Convert_utf8(valor)
                        tool.db.store.commit()
                    else:
                        D={}
                        D['vin_myvindula_instance_id'] = id_instance
                        D['vin_myvindula_confgfuncdetails_fields'] = campo.fields
                        D['valor'] = self.Convert_utf8(valor)
                        
                        ModelsDadosFuncdetails().set_DadosFuncdetails(**D)
                

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
    
    
    def update(self):
        db_user = ModelsInstanceFuncdetails().get_AllFuncDetails()
        plone_user = self.context.acl_users.getUserIds()
        
        self.user = []
        for user in db_user:
            if not user.get('username') in plone_user and\
                user.get('username') != 'admin':
                self.user.append(user)   

class MyVindulaRemoveUser(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-remove-user')
    
    def render(self):
        pass
    
    def update(self):
        form = self.request.form 
        success_url = self.context.absolute_url() + '/myvindula-compare-user'
        
        if 'user' in form.keys():
            username = self.Convert_utf8(form.get('user',''))
                    
            is_user_vindula = ModelsInstanceFuncdetails().get_InstanceFuncdetails(username)
            try:
                if is_user_vindula:
                    ModelsInstanceFuncdetails().del_InstanceDadosFuncdetails(username)
                    self.setStatusMessage("info","Usuário excluído com sucesso.")
            except:
                self.setStatusMessage("error","Erro ao excluir usuário do Vindula.")
                self.setRedirectPage('/@@usergroup-userprefs')
    
        
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


class MyVindulaDelHoleriteView(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-del-holerite')
    
    def select_modelo(self):
        modelo =  self.context.restrictedTraverse('myvindula-conf-userpanel').select_modelo_holerite()
        return modelo
    
    
    def update(self):
        form = self.request.form
        success_url = self.context.absolute_url() + '/myvindula-import-holerite'
        if 'date' in form.keys() and 'empresa' in form.keys():
            data_lote = form['date']
            
            try:empresa = unicode(form['empresa'],'utf-8')
            except:empresa = form['empresa']

            data_lote = datetime.strptime(data_lote,'%Y-%m-%d %H:%M')
            
            if self.select_modelo() == '01':
                ModelsFuncHolerite().del_HoleritesLote(data_lote,empresa)
            elif self.select_modelo() == '02':  
                ModelsFuncHolerite02().del_HoleritesLote(data_lote,empresa)
            
        self.request.response.redirect(success_url)
    
    def render(self):
        pass
       
class MyVindulaImportHoleriteView(grok.View, UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-import-holerite')
    
    def select_modelo(self):
        modelo =  self.context.restrictedTraverse('myvindula-conf-userpanel').select_modelo_holerite()
        return modelo
    
    
    def get_lastImport(self):
        if self.select_modelo() == '01':
            result = ModelsFuncHolerite().get_FuncHolerites_Import()
        elif self.select_modelo() == '02':
            result = ModelsFuncHolerite02().get_FuncHolerites_Import()
        
        if result: 
            return result
        else:
            return []
        
    def load_file(self):
        if self.select_modelo() == '01':
            return self.mecanismo01() 
        elif self.select_modelo() == '02':
            return self.mecanismo02() 
        
    def mecanismo01(self):
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
        
     
    def mecanismo02(self):
        form = self.request.form
        erro = False
        holerite_erro = None
        holerites = []
        holerite_observacao = ''
        modelo_holerite = {'empresa':None,
                           'cnpj_empresa':None,
                           'competencia':None,
                           'matricula':None,
                           'nome':None,
                           'data_admissao':None,    
                           'cargo':None,
                           'setor':None,
                           'carteira_trabalho':None,
                           'secao':None,
                           'dep_ir':None,
                           'dep_sf':None,
                           'cpf':None,
                           'indentidade':None,
                           'pis':None,
                           'salario_base':None,
                           'cod_pagamento':None, 
                           'banco_pag':None,
                           'agencia':None,
                           'conta_corrente':None,
                           'date_creation':None,
                           'base_Inss':None,
                           'base_fgts':None,
                           'base_irrf':None,
                           'salario_contribuicao':None,
                           'total_proventos':None,
                           'total_desconto':None,
                           'fgts_mes':None,
                           'valor_liquido':None,
                           'observacao':None,
                           
                           'completo':False,
                           'itens_holerite':[],}
        
        holerite = copy(modelo_holerite)
        
        if 'load_file' in form.keys():            
            if 'txt_file' in form.keys():
                file = form.get('txt_file','')
                if file:
                    texto = file.read()
                    texto = texto.replace('\r','')
                    cont = 1
                    
                    for linha in texto.split('\n'):
                        #Checando linhas vazias, se a linha for vazia ou só espaço, vai retornar uma lista vazia e nao entrar no if.
                        check_linha = [i for i in linha.split(' ') if i != '']
                        #import pdb;pdb.set_trace()
                        #Pulando linhas vazias
                        if check_linha != []:
                             
                             #Buscando Registro Funcionário
                            if linha[0:2] == '03':
                                holerite['empresa'] = linha[2:42]
                                holerite['cnpj_empresa'] = linha[42:61]
                                holerite['matricula'] = linha[61:72]
                                holerite['nome'] = linha[72:112]
                                holerite['data_admissao'] = linha[112:122]
                                holerite['cargo'] = linha[122:147]
                                holerite['setor'] = linha[147:172]
                                holerite['carteira_trabalho'] = linha[172:188]
                                holerite['secao'] = linha[188:193]
                                holerite['dep_ir'] = linha[193:195]
                                holerite['dep_sf'] = linha[195:197]
                                holerite['cpf'] = linha[197:211]
                                holerite['indentidade'] = linha[211:231]
                                holerite['pis'] = linha[231:245]
                            
                                holerite['observacao'] = holerite_observacao
                                holerite['completo'] = True
                            
                            #Buscando Registro de Totais
                            elif linha[0:2] == '02':    
                                holerite['competencia'] = linha[2:8]
                                holerite['cod_pagamento'] = linha[8:10]
                                holerite['banco_pag'] = linha[10:35]
                                holerite['agencia'] = linha[35:50]
                                holerite['conta_corrente'] = linha[50:65]
                                
                                holerite['salario_base'] = linha[65:75]
                                holerite['base_fgts'] = linha[75:85]
                                holerite['fgts_mes'] = linha[85:95]
                                
                                holerite['base_Inss'] = None
                                
                                holerite['base_irrf'] = linha[95:105]
                                holerite['salario_contribuicao'] = linha[105:115]
                                holerite['total_proventos'] = linha[115:125]
                                holerite['total_desconto'] = linha[125:135]
                                holerite['valor_liquido'] = linha[135:145]
                                   
                            #Buscando Registro das Verbas
                            elif linha[0:2] == '01':    

                                itens_holerite = {'codigo':None,
                                                  'descricao':None,
                                                  'valor':None,
                                                  'status':None,
                                                  'referencial':None,}
                                    
                                itens = copy(itens_holerite)
                                
                                itens['codigo'] = linha[2:5]
                                itens['descricao'] = linha[5:35]
                                itens['valor'] = linha[35:45]
                                itens['status'] = linha[45:46]
                                itens['referencial'] = linha[46:56]

                                #holerite['itens_holerite_check'] = True
                                    
                                holerite['itens_holerite'].append(itens)
                                  
                            #Buscando Registro Cabeçalho
                            elif linha[0:2] == '00':                                          
                                holerite_observacao = linha[2:102]
                               
                            if holerite['completo'] == True:
                                holerites.append(holerite)
                                holerite = copy(modelo_holerite)
                                holerite['itens_holerite'] = []
                                
                            
                    if holerites:
                        for holerite in holerites:
                            itens = copy(holerite['itens_holerite'])
                            convertido = self.converte_dadosByDB(holerite)
                            id = ModelsFuncHolerite02().set_FuncHolerite(**convertido)
                            
                            for item in itens:
                                item['vin_myvindula_holerite02_id'] = id
                                desc_convertido = self.converte_dadosByDB(item)
                                ModelsFuncHoleriteDescricao02().set_FuncHoleriteDescricao(**desc_convertido)
                    
        else:
            return None
   
       
   
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
                            nome_arquivo = nome_org = normalizer.normalize(unicode(nome, 'utf-8'))
                            
                            count = 0
                            while nome_arquivo in pasta.objectIds():
                                count +=1
                                #if count != 1:
                                #    nome_arquivo = nome_arquivo[:-2]
                                nome_arquivo = nome_org + '-' + str(count)         
                            
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
        
        fields = ModelsConfgMyvindula().get_configurationAll() #SchemaFunc().campos
        FIELD_BLACKLIST = ['vin_myvindula_department',]

        camposAux = copy(fields)
        for item in camposAux:
            if not item.fields in FIELD_BLACKLIST:
                fields_vin.append(item.ordem)
        
        if fields:
            for field in fields:
                if not field.fields in FIELD_BLACKLIST:
                    index = field.ordem
                    D = {}
                    D['name'] = field.fields
                    if field.fields != 'username':
                        D['label'] = field.label  #self.get_label_filed(field)
    
                    pos = fields_vin.index(index)
                    fields_vin.pop(pos)
                    fields_vin.insert(pos, D) 
                
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
        tools = UtilMyvindula()
        if 'import' in form.keys():
            path_file = form.get('url_arquivo').split('/')
            folder = getSite()[path_file[0]][path_file[1]][path_file[2]]
            arquivo = folder.get(path_file[3])
            
            linhas_error =[]
            lista_erros = []
            campos = self.get_Dic_Campos()
            
#            folder = self.context.get(folder)
#            arquivo = folder.get(file)
            ignore_fields = ['import',
                             'url_arquivo',
                             'cria-username',
                             'atualiza-dados',
                             'ciar-user-plone',
                             'username',]
            
            success = False
            criar_user = form.get('cria-username', False)
            merge_user = form.get('atualiza-dados', False)
            
            criar_user_plone = form.get('ciar-user-plone', False)
            
            error = 0
            url = ''
            
            arquivo.data = arquivo.data.replace('\r', '')
            
            for linha in arquivo.data.split('\n')[1:-1]:
                if linha:
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
     
                                    if form.get('registration'):
                                        matricula = dados_linha[int(form.get('registration'))-1].replace('"','')    
                                        username += str(matricula)
                                    else:
                                        matricula = randint(1,pow(10,10))
                                        username += str(matricula)
                                    
                                    usr = username
                                    while ModelsInstanceFuncdetails().get_InstanceFuncdetails(self.to_utf8(usr)): 
                                        usr = username + str(cont)
                                        cont +=1
                                      
                                    dados[campo] = self.to_utf8(usr)
                                    check_user = True
                                        
                                else:
                                    if form.get('username'):
                                        indice = int(form.get('username'))-1
                                        user = self.to_utf8(dados_linha[indice].replace('"',''))
                                        if ModelsInstanceFuncdetails().get_InstanceFuncdetails(user) and merge_user:    
                                            dados[campo] = user
                                            check_user = True
                                        else:
                                            dados[campo] = user
                                            check_user = True
                                            
                    erros, data_user = valida_form_dinamic(self,campos, dados)
                    if not erros:
                        if criar_user_plone:
                            ImportUser().importUser(self,{},dados)   
                        
                        username = dados['username']
                        if check_user:
                            user_instance = ModelsInstanceFuncdetails().get_InstanceFuncdetails(username)
                            if user_instance:
                                id_instance = user_instance.id
                            else:
                                id_instance = ModelsInstanceFuncdetails().set_InstanceFuncdetails(username)
                                    
                            for item in data_user.keys():
                                field = self.Convert_utf8(item)
                                valor = data_user[item]
                                result_campo = ModelsDadosFuncdetails().get_DadosFuncdetails_byInstanceAndField(id_instance,field)
                                if result_campo: 
                                    result_campo.valor = valor.strip()
                                    tools.db.store.commit()
                                else:
                                    if valor:
                                        D={}
                                        D['vin_myvindula_instance_id'] = id_instance
                                        D['vin_myvindula_confgfuncdetails_fields'] = field
                                        D['valor'] = self.Convert_utf8(valor)
                                        
                                        ModelsDadosFuncdetails().set_DadosFuncdetails(**D)
                                            
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
            
            fields_orig = ModelsConfgMyvindula().get_configurationAll()  #ModelsFuncDetails()._storm_columns.values()

            campos_vin = []
            text = ''
            
            if fields_orig:
                campos_vin.append('username')    
                text += 'username;'
                
                for field in fields_orig:
                    campos_vin.append(field.fields)
                    text += field.fields + ';'
            
                text = text[:-1] + '\n'
            
            users = ModelsInstanceFuncdetails().get_AllFuncDetails()

            for user in users:
                for campo in campos_vin:
                    if campo == 'photograph':
                        username = user.get('username','')
                        instance_id = ModelsInstanceFuncdetails().get_InstanceFuncdetails(username)

                        campo_image_instance = ModelsPhotoUser().get_ModelsPhotoUser_byFieldAndInstance(campo,instance_id.id)

                        if campo_image_instance:
                            text += '%s;' %('True')

                        else:
                            try:
                                campo_image_username = ModelsPhotoUser().get_ModelsPhotoUser_byUsername(username,campo)    

                                if campo_image_username:
                                    text += '%s;' %('True')
                                else:
                                    text += '%s;' %('False')
                            except:
                                text += '%s;' %('False')

                    if campo == 'vin_myvindula_department':
                        valor = user.get(campo,'')
                        try:
                            text += '%s;' %(valor[1])
                        except:
                            text += ';' 

                    else:
                        valor = user.get(campo,'')
                        
                        if type(valor) == list:
                            valor_list = ''
                            for i in valor:
                                if i :valor_list += (i + ' / ') 
                            
                            valor = valor_list
                            
                        text += '%s;' % (str(valor).replace('\n', '').replace('\r', '').replace(';', ''))

                text += '\n'
                 
            self.request.response.write(str(text))
        
        
        
        
class MyVindulaSchemaLdapView(grok.View,UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-list-schemaldap')


    def update(self):
        acl_users = getToolByName(self.context, 'acl_users')
        itens = [item for item in acl_users.objectValues()\
                       if item.meta_type == 'Plone Active Directory plugin' or\
                          item.meta_type == 'Plone LDAP plugin']

        self.connectors = itens

class MyVindulaManageSchemaLdapView(grok.View,UtilMyvindula):
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    grok.name('myvindula-manager-schemaldap')

    block_fields = ['name','vin_myvindula_department','photograph']
    schema_map_ldap = {}

    def tuple2dict(self, schema_tupla):
        D = {}
        for key, value in schema_tupla:
            D[value] = key
        return D

    def update(self):
        acl_users = getToolByName(self.context, 'acl_users')
        self.fields_myvindula = ModelsConfgMyvindula().get_configurationAll() 

        id_connectors = self.request.form.get('id','')
        try:
            connector = acl_users[id_connectors]
        except:
            connector = False


        form = self.request.form
        if form.get('submitted', False) and connector:
            
            for field in form.keys():
                if 'my_' in field:

                    valor = form.get(field.replace('my_', 'ad_'),'')
                    campo_myvindula =  field.replace('my_', '')

                    if valor:
                        connector.acl_users.manage_addLDAPSchemaItem(ldap_name=valor,
                                                                     friendly_name=campo_myvindula,
                                                                     public_name=campo_myvindula,)

                    else:
                        ldap_names = form.get(field.replace('my_', 'del_ad_'),'')
                        connector.acl_users.manage_deleteLDAPSchemaItems(ldap_names=[ldap_names])

            IStatusMessage(self.request).addStatusMessage(_(u'O mapeamento foi realizado com sucesso.'),"info") 
            self.request.response.redirect(self.context.absolute_url() + '/myvindula-list-schemaldap')


        if connector:
            self.schema_map_ldap = self.tuple2dict(connector.acl_users.getMappedUserAttrs())
             