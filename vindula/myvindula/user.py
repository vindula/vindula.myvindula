# coding: utf-8
from five import grok
from plone.directives import form

from zope import schema
from z3c.form import button
from plone import namedfile

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.dexterity.utils import createContentInContainer

from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from plone.scale.storage import IImageScaleStorage

from vindula.myvindula import MessageFactory as _

#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc
from zope.component import getUtility
from storm.zope.interfaces import IZStorm
from storm.locals import Store
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.statusmessages.interfaces import IStatusMessage
from vindula.myvindula.validation import valida_form
from datetime import date , datetime 
import pickle




#import sys
#from storm.tracer import debug #debug(True, stream=sys.stdout)

class BaseStore(object):
   
    def __init__(self, *args, **kwargs):
        self.store = getUtility(IZStorm).get('myvindula')
        
        #Lazy initialization of the object
        for attribute, value in kwargs.items():
            if not hasattr(self, attribute):
                raise TypeError('unexpected argument %s' % attribute)
            else:
                setattr(self, attribute, value)        
  
        # divide o dicionario 'convertidos'
        for key in kwargs:
            setattr(self,key,kwargs[key])
        # adiciona a data atual
        self.date_creation = datetime.now()    
  
    
class ModelsFuncDetails(Storm, BaseStore):    
    __storm_table__ = 'vin_myvindula_funcdetails'
    
    id = Int(primary=True)
    name = Unicode()
    phone_number = Unicode()
    cell_phone = Unicode()
    email = Unicode()
    employee_id = Unicode()
    username = Unicode()
    date_birth = Date()
    registration = Unicode()
    enterprise = Unicode()
    position = Unicode()
    admission_date = Date()
    cost_center = Unicode()
    organisational_unit = Unicode()
    reports_to = Unicode()
    location = Unicode() 
    postal_address = Unicode()
    special_roles = Unicode()
    photograph = Unicode()
    nickname = Unicode()
    pronunciation_name = Unicode()
    committess = Unicode()
    projects = Unicode()
    personal_information = Unicode()
    #skills_expertise = Unicode()
    profit_centre = Unicode()
    #languages = Unicode()
    availability = Unicode()
    papers_published = Unicode()
    teaching_research =Unicode()
    delegations = Unicode()
    resume = Unicode()
    blogs = Unicode()
    customised_message = Unicode()
    #vin_myvindula_department_id = Int()
    
    departamento = Reference(username, "ModelsDepartment.vin_myvindula_funcdetails_id")
    
    def set_FuncDetails(self, **kwargs):
        # adicionando...
        funcDetails = ModelsFuncDetails(**kwargs)
        self.store.add(funcDetails)
        self.store.flush()        
        
    def del_FuncDetails(self, username):
        result = self.get_FuncDetails(username)
        if result:
            self.store.remove(result)
            self.store.flush()
            
            return result.photograph 
    
    def get_allFuncDetails(self, ordem='nome'):
        if ordem == 'admicao':
            data = self.store.find(ModelsFuncDetails, ModelsFuncDetails.username!=u'admin').order_by(Desc(ModelsFuncDetails.admission_date))
        
        elif ordem == 'nome':
            data = self.store.find(ModelsFuncDetails, ModelsFuncDetails.username!=u'admin').order_by(ModelsFuncDetails.name)
            
        if data.count() == 0:
            return None
        else:
            return data
    
    def get_FuncDetails(self, user):
        data = self.store.find(ModelsFuncDetails, ModelsFuncDetails.username==user).one()
        if data:
            return data
        else:
            return None
        
    def get_FuncDetails_by_dinamicFind(self, field, text):
        busca = "self.store.find(ModelsFuncDetails, ModelsFuncDetails."+field+".like( '%' + '%'.join(text.split(' ')) + '%' ))"
        data = eval(busca)
        if data.count() > 0:
            return data
        else:
            return None        
        
    def get_FuncDetails_by_DepartamentName(self, text):
        urltool = getSite().portal_url
        caminho = urltool.getPortalPath()
        ctool = getSite().portal_catalog
        data = ctool(portal_type='OrganizationalStructure', 
                      review_state='published',
                      Title=text, path=caminho)   
        
        if len(data) >= 1:
            uid = []
            for item in data:
                obj = item.getObject()
                uid.append(unicode(obj.UID(),'utf-8'))
            
            origin = [ModelsFuncDetails, Join(ModelsDepartment, ModelsDepartment.vin_myvindula_funcdetails_id==ModelsFuncDetails.username)]
            result  = self.store.using(*origin).find(ModelsFuncDetails, ModelsDepartment.uid_plone.is_in(uid))
                
            if result.count() > 0:
                return result
            else:
                return None


        
    def get_FuncBusca(self,name,department_id,phone,filtro=False):
        if department_id == u'0' and name == '' and phone == '':
            data = self.store.find(ModelsFuncDetails).order_by(ModelsFuncDetails.name)
         
        elif department_id != u'0':
            origin = [ModelsFuncDetails, Join(ModelsDepartment, ModelsDepartment.vin_myvindula_funcdetails_id==ModelsFuncDetails.username)]
            data = self.store.using(*origin).find(ModelsFuncDetails,  ModelsFuncDetails.name.like( '%' + '%'.join(name.split(' ')) + '%' ),
                                                                      ModelsFuncDetails.phone_number.like("%" + phone + "%"),                                                                      
                                                                      ModelsDepartment.uid_plone==department_id).order_by(ModelsFuncDetails.name)
        
        elif department_id == u'0' and name != '':
            data = self.store.find(ModelsFuncDetails, ModelsFuncDetails.name.like( '%' + '%'.join(name.split(' ')) + '%' )).order_by(ModelsFuncDetails.name)

        else:
            data = self.store.find(ModelsFuncDetails, ModelsFuncDetails.name.like( '%' + '%'.join(name.split(' ')) + '%' ),
                                                      ModelsFuncDetails.phone_number.like("%" + phone + "%")).order_by(ModelsFuncDetails.name)
                                                      
        if filtro:
            data = data.find(ModelsFuncDetails.phone_number != None)
        
        if data.count() == 0:
            return None
        else:
            return data   

    
    def get_FuncBirthdays(self, date_start, date_end, filtro=''):
        if filtro == 'random':
            data = self.store.execute('SELECT * FROM vin_myvindula_funcdetails WHERE DATE_FORMAT(date_birth, "%m-%d") BETWEEN DATE_FORMAT("'+date_start+'", "%m-%d") AND DATE_FORMAT("'+date_end+'", "%m-%d") ORDER BY RAND();')

        elif filtro == 'proximo':
            data = self.store.execute("SELECT * FROM vin_myvindula_funcdetails WHERE concat_ws('-',year(now()),month(date_birth),day(date_birth)) >= DATE(NOW()) ORDER BY MONTH(date_birth) ASC , DAY(date_birth) ASC;")
        
        else:
            data = self.store.execute('SELECT * FROM vin_myvindula_funcdetails WHERE DATE_FORMAT(date_birth, "%m-%d") BETWEEN DATE_FORMAT("'+date_start+'", "%m-%d") AND DATE_FORMAT("'+date_end+'", "%m-%d") ORDER BY MONTH(date_birth) ASC, DAY(date_birth) ASC;')

        if data.rowcount != 0:
            result=[]
            for obj in data.get_all():
                D={}
                i = 0
                columns = self.store.execute('SHOW COLUMNS FROM vin_myvindula_funcdetails;')
                for column in columns.get_all():
                    if str(column[0]) == 'date_birth':
                        D[str(column[0])] = obj[i].strftime('%d/%m')
                    else:
                        D[str(column[0])] = obj[i]
                    i+=1
            
                result.append(D)       
            
            return result
        else:
            return None

         
class ModelsDepartment(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_department'
 
    __storm_primary__ = "uid_plone", "vin_myvindula_funcdetails_id"
    
    #id = Int(primary=True)
    uid_plone = Unicode()
    vin_myvindula_funcdetails_id = Unicode()

    def set_department(self, **kwargs):
        D={}
        D['uid_plone'] = kwargs.get('UID','')
        D['vin_myvindula_funcdetails_id'] = kwargs.get('funcdetails_id')
        
        # adicionando...
        department = ModelsDepartment(**D)
        self.store.add(department)
        self.store.flush()        
    
    #loads data into the combo "departamento_id"    
    def get_department(self):
        urltool = getSite().portal_url
        caminho = urltool.getPortalPath() #+'/jornal-da-caixa/banners-do-jornal';
        ctool = getSite().portal_catalog
        data = ctool(portal_type='OrganizationalStructure', 
                      review_state=['published','internal'],
                      sort_on = 'sortable_title',
                      path=caminho)   
        
        #data = self.store.find(ModelsDepartment)
        if data: 
            return data
        else:
            return []
        
    def get_departmentByUsername(self,user):
        catalog = getToolByName(getSite(), 'portal_catalog')
        datas = self.store.find(ModelsDepartment, ModelsDepartment.vin_myvindula_funcdetails_id==user)
        if datas.count() != 0:
            L=[]
            for data in datas:
                obj = catalog({'UID':data.uid_plone})
                if obj:
                    L.append(obj[0])
            if L:
                return L
            else:
                return []
        else:
            return []

#    def get_departmentByID(self,id):
#        data = self.store.find(ModelsDepartment, ModelsDepartment.id==int(id)).one()
#        if data:
#            return data
#        else:
#            return None
        
    def del_department(self, user):
        results = self.store.find(ModelsDepartment, ModelsDepartment.vin_myvindula_funcdetails_id==user)
        if results:
            for result in results:
                self.store.remove(result)
                self.store.flush()


class ModelsFuncHolerite(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_holerite'
    
    id = Int(primary=True)
    nome = Unicode()
    cpf = Unicode()
    matricula = Unicode() 
    cargo= Unicode()
    cod_cargo = Unicode()
    date_creation = DateTime()
    competencia = Unicode()
    empresa = Unicode()
    cod_empresa = Unicode()
    endereco_empresa = Unicode()
    cidade_empresa = Unicode()
    estado_empresa = Unicode()
    cnpj_empresa = Unicode()
    total_vencimento = Unicode()
    total_desconto = Unicode()
    observacao = Unicode()
    valor_liquido = Unicode()
    salario_base = Unicode()
    base_Inss = Unicode()
    base_fgts = Unicode()
    fgts_mes = Unicode()
    base_irrf = Unicode()
    
    descricao = Reference(id, "ModelsFuncHoleriteDescricao.vin_myvindula_holerite_id")
       
    def set_FuncHolerite(self, **kwargs):
        # adicionando...
        funcHolerite = ModelsFuncHolerite(**kwargs)
        self.store.add(funcHolerite)
        self.store.flush()
        
        return funcHolerite.id       
    
    def get_FuncHolerites_byCPF(self, cpf):
        #Checando se atributo é None, se for já não retorna nenhum holerite
        #Por seguranca retorna None quando CPF = None, pois na importacao, 
        #pode ser improtado algum holerite com cpf vazio 
        if cpf == None: return None
        data = self.store.find(ModelsFuncHolerite, ModelsFuncHolerite.cpf==cpf).order_by(ModelsFuncHolerite.competencia)
        if data.count() > 0:
            return data
        else:
            return None    
    
    def get_FuncHolerites_byCPFAndID(self, cpf,id):
        #Checagem de seguranca
        if cpf == None: return None
        
        data = self.store.find(ModelsFuncHolerite, ModelsFuncHolerite.cpf==cpf, ModelsFuncHolerite.id==id).one()
        if data:
            return data
        else:
            return None    

    def get_FuncHolerites_byData(self, data):
        data = self.store.find(ModelsFuncHolerite, ModelsFuncHolerite.date_creation==data)
        if data.count() > 1:
            return data
        else:
            return None        
    
    def get_FuncHolerites_Import(self):        
        result = self.store.execute("SELECT count(*),DATE_FORMAT(date_creation,'%d/%m/%Y %H:%i') as data,\
                                    date_creation, empresa FROM vin_myvindula_holerite group by data,empresa")
        L = []        
        for i in result:
            L.append({'contador':i[0],
                      'date_creation':i[1],
                      'date_excluir':i[2], 
                      'empresa':i[3],                      
                      })        
        return L    

    def del_HoleritesLote(self, date,empresa):
        #import pdb;pdb.set_trace()
        results = self.store.find(ModelsFuncHolerite, ModelsFuncHolerite.date_creation>=date,
                                                      ModelsFuncHolerite.date_creation<=date.replace(second=59),
                                                      ModelsFuncHolerite.empresa==empresa)
        if results:
            for result in results:
                ModelsFuncHoleriteDescricao().del_HoleritesDescricao(result.id)
                self.store.remove(result)
                self.store.flush()        
    
    
    
class ModelsFuncHoleriteDescricao(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_descricao_holerite'
    
    id = Int(primary=True)    
    codigo = Unicode()
    descricao = Unicode()
    ref = Unicode()
    vencimentos = Unicode()
    descontos = Unicode()
    vin_myvindula_holerite_id = Int()
    
    def set_FuncHoleriteDescricao(self, **kwargs):
        # adicionando...
        funcHoleriteDescricao = ModelsFuncHoleriteDescricao(**kwargs)
        self.store.add(funcHoleriteDescricao)
        self.store.flush()          
    
    def get_FuncHoleriteDescricoes_byid(self, id):
        data = self.store.find(ModelsFuncHoleriteDescricao, ModelsFuncHoleriteDescricao.vin_myvindula_holerite_id==id)
        if data.count() > 0:
            return data
        else:
            return None        
    
    def del_HoleritesDescricao(self, holerite_id):
        results = self.store.find(ModelsFuncHoleriteDescricao, ModelsFuncHoleriteDescricao.vin_myvindula_holerite_id==holerite_id)
        if results:
            for result in results:
                self.store.remove(result)
                self.store.flush()
        

class ModelsConfgMyvindula(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_confgfuncdetails'
    
    #Campos de edição
    #id = Int()
    fields = Unicode(primary=True)
    ativo_edit = Bool()
    ativo_view = Bool()
    label = Unicode()

    #loads data into DataBase    
    def get_configuration_By_fields(self, campo):
        try:campo = unicode(campo, 'utf-8')    
        except:pass 

        data = self.store.find(ModelsConfgMyvindula, ModelsConfgMyvindula.fields==campo).one()
        if data:
            return data
        else:
            return None
    
    def set_configuration(self,**kwargs):
        # adicionando...
        config = ModelsConfgMyvindula(**kwargs)
        self.store.add(config)
        self.store.flush()                

    def getConfig_views(self,campo):
        result = self.get_configuration_By_fields(campo)
        if result:
            return result.ativo_view
        else:
            return True

    def getConfig_edit(self,campo):
        result = self.get_configuration_By_fields(campo)
        if result:
            return result.ativo_edit
        else:
            return True

    
class ModelsMyvindulaHowareu(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_howareu'
    
    _name_class = "ModelsMyvindulaHowareu" 
    
    id = Int(primary=True)
    username = Unicode()
    date_creation = DateTime()
    visible_area = Unicode()
    text = Unicode()
    upload_image = Pickle()
        
    def set_myvindula_howareu(self,**kwargs):
        D={}
        
        D['username'] = unicode(kwargs.get('username',''), 'utf-8')
        D['visible_area'] = unicode(kwargs.get('visible_area',''), 'utf-8')
        D['upload_image'] = kwargs.get('upload_image',None)
        D['text'] = unicode(kwargs.get('text',''), 'utf-8')
        
        # adicionando...
        howareu = ModelsMyvindulaHowareu(**D)
        self.store.add(howareu)
        self.store.flush()
    
    def get_myvindula_howareu(self,**kwargs):
        if kwargs.get('username',None):
            user = kwargs.get('username','')
            if type(user) != unicode:
                user = unicode(kwargs.get('username',''), 'utf-8')
            data = self.store.find(ModelsMyvindulaHowareu, ModelsMyvindulaHowareu.username==user).order_by(Desc(ModelsMyvindulaHowareu.date_creation))
        
        elif kwargs.get('visible_area',None):
            visible_area = kwargs.get('visible_area','')
            if type(visible_area) != unicode:
                visible_area = unicode(kwargs.get('visible_area',''), 'utf-8')
            data = self.store.find(ModelsMyvindulaHowareu, ModelsMyvindulaHowareu.visible_area==visible_area)
        
        else:
            data = self.store.find(ModelsMyvindulaHowareu).order_by(Desc(ModelsMyvindulaHowareu.date_creation))    
        
        if data.count() > 0:
            return data
        else:
            return None    
    
    def get_myvindula_howareu_By_Id(self,id):
        data = self.store.find(ModelsMyvindulaHowareu, ModelsMyvindulaHowareu.id==int(id)).one()
        
        if data:
            return data
        else:
            return None
        
    def del_myvindula_howareu(self, id):
        record = self.store.find(ModelsMyvindulaHowareu, ModelsMyvindulaHowareu.id==id).one()
        self.store.remove(record)
        self.store.flush()        
        
        
class ModelsMyvindulaRecados(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_recados'
    
    _name_class = "ModelsMyvindulaRecados" 
    
    id = Int(primary=True)
    username = Unicode()
    date_creation = DateTime()
    destination = Unicode()
    text = Unicode()
        
    def set_myvindula_recados(self,**kwargs):
        from vindula.contentcore.base import BaseFunc as Tools
        
        tools = BaseFunc()
        D={}
        D['username'] = unicode(kwargs.get('username',''), 'utf-8')
        D['destination'] = unicode(kwargs.get('destination',''), 'utf-8')
        D['text'] = unicode(kwargs.get('text',''), 'utf-8')
        
        user_send = ModelsFuncDetails().get_FuncDetails(tools.Convert_utf8(D['username']))
        user_destination = ModelsFuncDetails().get_FuncDetails(tools.Convert_utf8(D['destination']))

        if user_destination and user_destination.email:
            assunto = 'Novo recado!!!'
            msg = '''<h2>Você tem um novo recado</h2>
                     <p>Você recebeu um novo recado do(a) <a href='%s'> %s</a> </p>
                     <p>Para visualizar o recado acesse <a href="%s"> aqui </a></p>
                   '''%(getSite().absolute_url() + '/@@myvindulalistuser?user='+user_send.username ,
                        user_send.name, getSite().absolute_url() + '/@@myvindulalistrecados')
            
            Tools().envia_email(getSite(),msg,assunto,user_destination.email,[])

        # adicionando...
        recados = ModelsMyvindulaRecados(**D)
        self.store.add(recados)
        self.store.flush()

    
    def get_myvindula_recados(self,**kwargs):
        if kwargs.get('destination',None):
            user = kwargs.get('destination','')
            if type(user) != unicode:
                user = unicode(kwargs.get('destination',''), 'utf-8')
            data = self.store.find(ModelsMyvindulaRecados, ModelsMyvindulaRecados.destination==user).order_by(Desc(ModelsMyvindulaRecados.date_creation))
        
            if data.count() > 0:
                return data
            else:
                return None
        else:
            return None            

    def del_myvindula_recados(self, id):
        record = self.store.find(ModelsMyvindulaRecados, ModelsMyvindulaRecados.id==id).one()
        self.store.remove(record)
        self.store.flush()        
                            

class ModelsMyvindulaComments(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_comments'
    
    _name_class = "ModelsMyvindulaComments"     
    
    id = Int(primary=True)
    username = Unicode()
    ip = Unicode()
    date_creation = DateTime()
    type = Unicode()
    id_obj = Unicode()
    isPlone = Bool()
    text = Unicode()
    
    def set_myvindula_comments(self,**kwargs):
        D={}
        base = BaseFunc() 
        D['username'] = base.Convert_utf8(kwargs.get('username',''))
        D['ip'] = base.Convert_utf8(kwargs.get('ip',''))
        D['type'] = base.Convert_utf8(kwargs.get('type',''))
        D['id_obj'] = base.Convert_utf8(kwargs.get('id_obj',''))
        D['isPlone'] = eval(kwargs.get('isPlone','False'))
        D['text'] = base.Convert_utf8(kwargs.get('text',''))
        
        # adicionando...
        comments = ModelsMyvindulaComments(**D)
        self.store.add(comments)
        self.store.flush()
        
        return comments.id        

    def get_myvindula_comments(self,**kwargs):
        id_obj = kwargs.get('id_obj','')
        type_obj = kwargs.get('type','')
        if type(id_obj) != unicode:
            id_obj = unicode(id_obj)
        if type(type_obj) != unicode:
            type_obj = unicode(type_obj)
        data = self.store.find(ModelsMyvindulaComments, ModelsMyvindulaComments.id_obj==id_obj,ModelsMyvindulaComments.type==type_obj)

        if data.count > 0:
            return data
        else:
            return None
        
    def get_comments_byID(self, id):
        data = self.store.find(ModelsMyvindulaComments, ModelsMyvindulaComments.id==id).one()
        
        if data:
            return data
        else:
            return None
    
    def del_myvindula_comments(self, id):
        record = self.store.find(ModelsMyvindulaComments, ModelsMyvindulaComments.id==id).one()
        self.store.remove(record)
        self.store.flush()        
                   

class ModelsMyvindulaLike(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_like'
    
    id = Int(primary=True)
    username = Unicode()
    date_creation = DateTime()
    type = Unicode()
    id_obj = Unicode()
    isPlone = Bool()
     
    def set_myvindula_like(self,**kwargs):
        D={}
        base = BaseFunc() 
        D['username'] =  base.Convert_utf8(kwargs.get('username',''))
        D['type'] =  base.Convert_utf8(kwargs.get('type',''))
        D['id_obj'] =  base.Convert_utf8(kwargs.get('id_obj',''))
        D['isPlone'] = eval(kwargs.get('isPlone','False'))
        
        # adicionando...
        comments = ModelsMyvindulaLike(**D)
        self.store.add(comments)
        self.store.flush()        

    def get_myvindula_like(self,**kwargs):
        id_obj = kwargs.get('id_obj','')
        type_obj = kwargs.get('type','')
        if type(id_obj) != unicode:
            id_obj = unicode(id_obj)
        if type(type_obj) != unicode:
            type_obj = unicode(type_obj)
        data = self.store.find(ModelsMyvindulaLike, ModelsMyvindulaLike.id_obj==id_obj,ModelsMyvindulaLike.type==type_obj)

        if data.count > 0:
            return data
        else:
            return None   

    def del_myvindula_like(self, **kwargs):
        id_obj = kwargs.get('id_obj','')
        username = kwargs.get('username','')
        type_obj = kwargs.get('type','')
        
        if type(id_obj) != unicode:
            id_obj = unicode(id_obj)
        if type(username) != unicode:
            username = unicode(username)
        if type(type_obj) != unicode:
            type_obj = unicode(type_obj)
        
        record = self.store.find(ModelsMyvindulaLike, ModelsMyvindulaLike.id_obj==id_obj,
                                                      ModelsMyvindulaLike.type==type_obj,
                                                      ModelsMyvindulaLike.username==username).one()
        self.store.remove(record)
        self.store.flush()


class ModelsMyvindulaCourses(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_courses'
    
    id = Int(primary=True)
    title = Unicode()
    length = Unicode()
    
    def get_allCourses(self):
        data = self.store.find(ModelsMyvindulaCourses)
        if data:
            return data
        else:
            return None
    
    def set_courses(self,**kwargs):
        # adicionando...
        couses = ModelsMyvindulaCourses(**kwargs)
        self.store.add(couses)
        self.store.flush() 
        
    def get_courses_byID(self,id):
        data = self.store.find(ModelsMyvindulaCourses, ModelsMyvindulaCourses.id==id).one()
        if data:
            return data
        else:
            return None
        
        
class ModelsMyvindulaLanguages(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_languages'
    
    id = Int(primary=True)
    title = Unicode()
    level = Unicode()
    
    def get_allLanguages(self):
        data = self.store.find(ModelsMyvindulaLanguages)
        if data:
            return data
        else:
            return None

    def set_languages(self,**kwargs):
        # adicionando...
        languages = ModelsMyvindulaLanguages(**kwargs)
        self.store.add(languages)
        self.store.flush()         

    def get_languages_byID(self,id):
        data = self.store.find(ModelsMyvindulaLanguages, ModelsMyvindulaLanguages.id==id).one()
        if data:
            return data
        else:
            return None        

class ModelsMyvindulaFuncdetailCouses(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_funcdetail_couses'
    __storm_primary__ = "vin_myvindula_funcdetail_username", "vin_myvindula_courses_id"
    
    #id = Int(primary=True)
    vin_myvindula_funcdetail_username = Unicode()
    vin_myvindula_courses_id = Int()
    
    def get_funcdetailCouserByUsername(self, user):
        data = self.store.find(ModelsMyvindulaFuncdetailCouses, ModelsMyvindulaFuncdetailCouses.vin_myvindula_funcdetail_username==user)
        
        if data:
            return data
        else:
            return None
    
    def set_funcdetailCouser(self,**kwargs):
        D={}
        D['vin_myvindula_funcdetail_username']= kwargs.get('username','')
        D['vin_myvindula_courses_id'] = int(kwargs.get('id_courses',''))
    
        # adicionando...
        funcdetailCouser = ModelsMyvindulaFuncdetailCouses(**D)
        self.store.add(funcdetailCouser)
        self.store.flush()   
        
    
    def del_funcdetailCouser(self, user):
        results = self.store.find(ModelsMyvindulaFuncdetailCouses, ModelsMyvindulaFuncdetailCouses.vin_myvindula_funcdetail_username==user)
        if results:
            for result in results:
                self.store.remove(result)
                self.store.flush()        


class ModelsMyvindulaFuncdetailLanguages(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_funcdetail_languages'
    __storm_primary__ = "vin_myvindula_funcdetail_username", "vin_myvindula_languages_id"

    #id = Int(primary=True)
    vin_myvindula_funcdetail_username = Unicode(primary=True)
    vin_myvindula_languages_id = Int()
    
    def get_funcdetailLanguagesByUsername(self, user):
        data = self.store.find(ModelsMyvindulaFuncdetailLanguages, ModelsMyvindulaFuncdetailLanguages.vin_myvindula_funcdetail_username==user)
        
        if data:
            return data
        else:
            return None
    
    
    def set_funcdetailLanguages(self,**kwargs):
        D={}
        D['vin_myvindula_funcdetail_username']= kwargs.get('username','')
        D['vin_myvindula_languages_id'] = int(kwargs.get('id_courses',''))
    
        # adicionando...
        funcdetaillanguages = ModelsMyvindulaFuncdetailLanguages(**D)
        self.store.add(funcdetaillanguages)
        self.store.flush()   
    
    def del_funcdetailLanguages(self, user):
        results = self.store.find(ModelsMyvindulaFuncdetailLanguages, ModelsMyvindulaFuncdetailLanguages.vin_myvindula_funcdetail_username==user)
        if results:
            for result in results:
                self.store.remove(result)
                self.store.flush()         
    
        
class BaseFunc(BaseStore):
    #default class for standard functions

    # define se aparece ou nao as mensagens e marcacoes de erros  
    def field_class(self, errors, field_name):
        if errors is not None:
            if errors.get(field_name, None) is not None:
                return 'field error'                   
            else:
                 return 'field'
        else:
              return 'field'
          
    #pega o valor entre dois campos
    def checaValor(self, x, y):
        if not x and not y:
            return ''
        elif x:
             return x
        elif y:
             return y
        else:
             return '' 
          
    def checaEstado(self,config, campo):
        if config:
            try:
                return config.get(campo)
            except:
                return True
        else:
            return True

    def decodePickle(self,valor):
        if valor:
            return pickle.loads(str(valor))
        else:
            return ''    
    
    def Convert_utf8(self,valor):
        try: return unicode(valor,'utf-8')
        except: return valor
    
    def rs_to_list(self, rs):
        if rs:
            return [i for i in rs]
   
    def get_ip(self, request):
        """ Extract the client IP address from the HTTP request in a proxy-compatible way.
        
        @return: IP address as a string or None if not available
        """
        if "HTTP_X_FORWARDED_FOR" in request.environ:
            # Virtual host
            ip = request.environ["HTTP_X_FORWARDED_FOR"]
        elif "HTTP_HOST" in request.environ:
            # Non-virtualhost
            ip = request.environ["REMOTE_ADDR"]
        else:
            # Unit test code?
            ip = None
        
        return ip
   
   
    def getValue(self,campo,request,data):
        if campo in request.keys():
            if request.get(campo, None):
                return request.get(campo,'')
            else:
                return ''
        elif campo in data.keys():
            if data.get(campo, None):
                return data.get(campo,'')
            else:
                return ''
        else:
            return ''
    
    def getValueList(self,campo,request,data):
        if campo in request.keys():
            if request.get(campo, None):
                return request.get(campo,[])
            else:
                return []
        elif data:
            L = []
            for i in data:
                if campo == 'languages':
                    L.append(i.vin_myvindula_languages_id)
                elif campo == 'skills_expertise':
                    L.append(i.vin_myvindula_courses_id)
                else:
                    L.append(i.id)
                    
            return L
        else:
            return []    
        
    def getParametersFromURL(self, ctx):
        traverse = ctx.context.REQUEST.get('traverse_subpath')
        vars = {}
        if traverse != None:
            size = len(traverse)
            counter = 0
            for i in range(size/2):
                position = i+counter
                vars.update({traverse[position]:traverse[position+1]})
                counter+=1
        return vars
                
    
    def getPhoto(self,campo,request,data):
        if campo in request.keys():
#            if request.get(campo, None):
#                return self.context.absolute_url()+'/'+request.get(campo, '').filename + '/image_thumb'
#            else:
                return self.context.absolute_url()+'/'+'defaultUser.png'
        elif campo in data.keys():
            if data.get(campo, None) and not ' ' in data.get(campo,None) and not data.get(campo,None) == '':
                #return self.context.absolute_url()+'/'+data.get(campo,'') + '/image_thumb'
                return BaseFunc().get_imageVindulaUser(data.get(campo,''))
                
            else:
                return self.context.absolute_url()+'/'+'defaultUser.png'
        else:
            return self.context.absolute_url()+'/'+'defaultUser.png'        
        
    def checked(self,campo,request,data,ativa='edit'):
        if campo in request.keys():
            if request.get(campo, '') == True:
                return "checked"
            else:
                return ""
        elif campo in data.keys():
            D = data.get(campo,None)
            if D:
                if ativa == 'edit':
                    if D.get('edit',False):
                        return "checked"
                    else:
                        return ""
                elif ativa == 'view':
                    if D.get('view',False):
                        return "checked"
                    else:
                        return ""
                else:
                    return ""
            else:
                return ""
        else:
            return ""    
    
    # retorna dado convertido para o campo de valor monetario   
    def converte_valor(self, valor):
        if valor is not None:
            if type(valor) == Decimal:
                valor = str(valor)
                valor = valor.replace('R$ ','')
                valor = valor.replace('.', ',')
                #valor = 'R$ ' + valor
                return valor
            else: 
                return None  
        else:
            return None        
    
    #retorno a data de competencia no ordem coreta
    def converte_competencia(self, valor):
        if valor is not None:
            tmp = valor.split('/')
            return tmp[1]+'/'+tmp[0]
        else:
            return None
        
    # retorna dado convertido para o campos de data 
    def converte_data(self, data, data_atual=False):
        if data is not None and data != '':
            if type(data) == date:
                return data.strftime('%d/%m/%Y')
            else:
                return data
        else:
            if data_atual == True:
                data = date.today()
                dia = data.day
                mes = data.month
                ano = data.year
        
                if dia < 10:
                    dia = '0' + str(dia)
                else:
                    dia = str(dia)
                    
                if mes < 10:
                    mes = '0' + str(mes)
                else:
                    mes = str(mes)
                    
                datastr = dia + '/' + mes + '/' + str(ano)
        
                return datastr  
            else:
                return data

    #Retorna o label dos campos dinamicos
    def get_label_filed(self, campo):
        from vindula.myvindula.registration import SchemaConfgMyvindula
        result = ModelsConfgMyvindula().get_configuration_By_fields(campo)
        default = SchemaConfgMyvindula().campos.get(campo)
        
        if result:
            label = result.__getattribute__('label') 
            if not label:
                return default.get('label')
            else:
                return label
            
        else:
            return default.get('label')

            
    def converte_dadosByDB(self, D):
        keys = D.keys()
        for item in keys:
            if item == 'itens_holerite' or\
               item == 'itens_holerite_check' or\
               item == 'completo':
                D.pop(item)
            else: 
                valor = D[item]
                if type(valor) == str: 
                    valor = valor.strip()
                    try:
                        D[item] = unicode(valor, 'utf-8')
                    except:
                        D[item] = unicode(valor, 'ISO-8859-1')
                else:
                    D[item] = valor
        
        return D
                 
    def geraCampos(self,form_data):
        if type(form_data) == dict:
            errors = form_data.get('errors',None)
            data = form_data.get('data',None)
            campos = form_data.get('campos',None)
            config_myvindula = form_data.get('config_myvindula',None)
            manage = form_data.get('manage',False)
            
            languages = ModelsMyvindulaLanguages().get_allLanguages()
            cursos = ModelsMyvindulaCourses().get_allCourses()
            user = form_data.get('username','')
            
            funcdetailLanguages = ModelsMyvindulaFuncdetailLanguages().get_funcdetailLanguagesByUsername(user)
            funcdetailCourse = ModelsMyvindulaFuncdetailCouses().get_funcdetailCouserByUsername(user)
            
            html=[]
            i=0
            while i < len(campos.keys())-1:
                html.append(i)
                i+=1
            for campo in campos.keys():
                if campo != 'vin_myvindula_department' and campo != 'username':
                    
                    index = campos[campo].get('ordem',0)
                    tmp = ""
                    tmp += "<!-- Campo %s -->"%(campo)
                    tmp += "<div class='%s'>"%(self.field_class(errors, campo))
                    if self.checaEstado(config_myvindula,campo) or manage:
                        tmp += "   <label for='%s'>%s</label>"%(campo,self.get_label_filed(campo))
                        if campos[campo]['required'] == True:
                            tmp += "   <span class='fieldRequired' title='Obrigatório'>(Obrigatório)</span>"
    
                        tmp += "   <div class='formHelp'>%s.</div>"%(campos[campo]['decription'])   
                        tmp += "   <div >%s</div>"%(errors.get(campo,''))
                        
                        if campo == 'photograph':
#                            if errors:
#                                if data:
#                                    tmp += "<img src='%s' style='width:100px;height:100px;' /><br />"%(self.getPhoto(campo,self.request,data))
#                            else: 
#                                 tmp += "<img src='%s' style='width:100px;height:100px;' /><br />"%(self.getPhoto(campo,self.request,data))
#                            tmp += "<input id='photograph' type='file' value='%s' name='photograph' size='25' />"%(self.getPhoto(campo,self.request,data))
                            url = getSite().portal_url()
                            from vindula.myvindula.user_photo import ModelsPhotoUser
                            user_foto = ModelsPhotoUser().get_ModelsPhotoUser_byUsername(user)
                            
                            tmp +="<div id='%s'><a href='%s/myvindula-user-crop' class='crop-foto'>Editar Foto</a>" %(campo,url)
                            if user_foto:
                                tmp += "<div id='preview-user'><img height='150px' src='%s/user-image?username=%s' /></div>" %(url,user)
                                tmp += "<a href='%s/myvindula-user-delcrop' class='excluir-foto'>Excluir Foto</a>" %(url)
                            else:
                                tmp += "<div id='preview-user'></div>"
                                tmp += "<a href='%s/myvindula-user-delcrop' style='display:none' class='excluir-foto'>Excluir Foto</a>" %(url)
                            
                            tmp += "</div>"
                        
                        elif campo == 'date_birth' or campo == 'admission_date':
                            tmp += """<input id='%s' type='text' maxlength='10' onKeyDown='Mascara(this,Data);' onKeyPress='Mascara(this,Data);' onKeyUp='Mascara(this,Data);'
                                             value='%s' name='%s' size='25'/>"""%(campo,self.converte_data(self.getValue(campo,self.request,data),False),campo)

                        elif campo == 'customised_message':
                            tmp += "<textarea id='%s' name='%s' style='width: 100; height: 81px;'>%s</textarea>"%(campo, campo, self.getValue(campo,self.request,data)) 
                        
                        
                        elif campo == 'languages':
                            tmp += "<div class='boxSelecao' name='languages'>"
                            for language in languages:
                                if language.id in self.getValueList(campo,self.request,funcdetailLanguages):
                                    lable_language = language.title +' - '+ language.level
                                    tmp += "<input value='%s' type='checkbox' checked name='languages'/><label>%s</label><br/>"%(language.id,lable_language)
                                else:
                                    lable_language = language.title +' - '+ language.level
                                    tmp += "<input value='%s' type='checkbox' name='languages'/><label>%s</label><br/>"%(language.id,lable_language)
                            tmp += "</div>" 
                            
                        elif campo == 'skills_expertise':
                            tmp += "<div class='boxSelecao' name='skills_expertise'>"
                            for curso in cursos:
                                if curso.id in self.getValueList(campo,self.request,funcdetailCourse):
                                    lable_curso = curso.title +' - '+ curso.length
                                    tmp += "<input value='%s' type='checkbox' checked name='skills_expertise'/><label>%s</label><br/>"%(curso.id,lable_curso)
                                else:
                                    lable_curso = curso.title +' - '+ curso.length
                                    tmp += "<input value='%s' type='checkbox' name='skills_expertise'/><label>%s</label><br/>"%(curso.id,lable_curso)
                            
                            tmp += "</div>" 
                            
                        else:
                            tmp += "<input id='%s' type='text' value='%s' name='%s' size='25'/>"%(campo,self.getValue(campo,self.request,data),campo)
                    else:
                        if campo == 'date_birth' or campo == 'admission_date':
                            tmp += "<input id='%s' type='hidden' value='%s' name='%s' size='25'/>"%(campo,self.converte_data(self.getValue(campo,self.request,data),False),campo)
                        
                        elif campo == 'skills_expertise':
                            for i in self.getValueList(campo,self.request,funcdetailCourse):
                                tmp += "<input id='%s' type='hidden' value='%s' name='%s' size='25'/>"%(campo,i,campo)
                            
                        elif campo =='languages':
                            for i in self.getValueList(campo,self.request,funcdetailLanguages):
                                tmp += "<input id='%s' type='hidden' value='%s' name='%s' size='25'/>"%(campo,i,campo)
                        
                        else:
                            tmp += "<input id='%s' type='hidden' value='%s' name='%s' size='25'/>"%(campo,self.getValue(campo,self.request,data),campo)
                        
                    tmp += "</div>"
                    html.pop(index)
                    html.insert(index, tmp)    
            
            return html

    def geraConfCampos(self,form_data,start=True):
        if type(form_data) == dict:
            errors = form_data.get('errors',None)
            data = form_data.get('data',None)
            campos = form_data.get('campos',None)
#            notCampos = []
#                                    
#            if start:
#                for i in campos.keys():
#                    if 'view' in i:
#                        notCampos.append(i)
#            else:
#                for i in campos.keys():
#                    if not 'view' in i:
#                        notCampos.append(i)
                
            html = []
            i=0
            
            #cont = len(campos) - len(notCampos)
            while i < len(campos):
                html.append(i)
                i+=1
             
            for campo in campos.keys():
                if campo != 'id' and campo != 'username': #and not campo in notCampos:
                    index = campos[campo].get('ordem',0)
                    tmp = ""
                    tmp += "<!-- Campo %s -->"%(campo)
                    tmp += "<div class='%s'>"%(self.field_class(errors, campo))
                    tmp += "   <label for='%s'>%s</label>"%(campo,data[campo]['label'])
                    tmp += "   <div >%s</div>"%(errors.get(campo,''))
                    tmp += "   <div class='formHelp'>"
                    tmp += "   <input id='%s' type='checkbox' value='%s' name='%s' size='25' %s/>"%('edit_'+campo,'true','edit_'+campo,self.checked(campo,self.request,data,'edit'))
                    tmp += "   Habilita a edição do campo '%s' pelo funcionário</div>"%(data[campo]['label'])   
                    tmp += "   <div class='formHelp'>"
                    tmp += "   <input id='%s' type='checkbox' value='%s' name='%s' size='25' %s/>"%('view_'+campo,'true','view_'+campo,self.checked(campo,self.request,data,'view'))
                    tmp += "    Habilita a visualização do campo '%s' pelo funcionário</div>"%(data[campo]['label'])   

                    tmp += "   <div class='formHelp'>Digite o nome de visualização do campo '%s' pelo funcionário</div>"%(data[campo]['label'])
                    value = self.getValue(campo,self.request,data)
                    try: valor = value.get('label','')
                    except: valor = value
                       
                    tmp += "   <input id='%s' type='text' value='%s' name='%s' size='25' />"%('label_'+campo,valor,'label_'+campo,)
                    
                    tmp += "</div>" 
                    
                    html.pop(index)
                    html.insert(index, tmp)      
            
            return html
        
    def geraExtraCampos(self,form_data):
        if type(form_data) == dict:
            errors = form_data.get('errors',None)
            data = form_data.get('data',None)
            campos = form_data.get('campos',None)
            
            html=[]
            i=0
            while i < len(campos.keys()):
                html.append(i)
                i+=1
            for campo in campos.keys():
                type_campo = campos[campo]['type']
                index = campos[campo].get('ordem',0)
                tmp = ""
                tmp += "<!-- Campo %s -->"%(campo)
                tmp += "<div class='%s'>"%(self.field_class(errors, campo))
                tmp += "   <label for='%s'>%s</label>"%(campo,campos[campo]['label'])
                
                if campos[campo]['required'] == True:
                    tmp += "   <span class='fieldRequired' title='Obrigatório'>(Obrigatório)</span>"

                tmp += "   <div class='formHelp'>%s.</div>"%(campos[campo]['decription'])   
                tmp += "   <div >%s</div>"%(errors.get(campo,''))
                if type_campo == 'file':
                    if campo == 'logo_corporate' and data:
                        tmp += "<img src='%s' height='60px'/><br />" %( getSite().portal_url() +'/company-logo?cnpj='+data.get('cnpj',''))
                    
                    tmp += "<input id='%s' type='file' value='%s' name='%s' size='25'  accept='image/*'/>"%(campo,'',campo)
                else:
                    tmp += "<input id='%s' type='text' value='%s' name='%s' size='25'/>"%(campo,self.getValue(campo,self.request,data),campo)
                
                tmp += "</div>"
                html.pop(index)
                html.insert(index, tmp)    
            
            return html
        
#    def uploadFile(self,ctx, path, file):
#        """ function used to upload the file to the Plone site, 
#           with the parameter where the file will be saved and the file will be saved
#        """
#        portal_workflow = getToolByName(getSite(), 'portal_workflow')
#        normalizer = getUtility(IIDNormalizer)
#        name_file = normalizer.normalize(file.filename)    #unicode(file.filename, 'utf-8')) #takes the name of the file
#        count = 0
#        file2 = file
#        while name_file in path.objectIds():
#            name_file = name_file + '-' + str(count)
#            count +=1
#        
#        #starts the upload process     
#        else:
#            try:
#                img = file.xreadlines().read()
#                imagem = namedfile.NamedImage(img, filename=unicode(file.filename))
#                objects = {'type_name':'vindula.myvindula.vindulaphotouser',
#                          'id': name_file,
#                          'title':name_file,
#                          'photograph':imagem}
#
##                ctx.context.portal_membership.changeMemberPortrait(file, path.id)
#                    
#                path.invokeFactory(**objects)              
#                #takes the url of the file to save the database  
#                content = getattr(path, name_file, None)
#
#                url = ''
#                if content is not None:
#                    url = '/'.join(content.getPhysicalPath()[2:])  
#                
#                return unicode(url)
#                
#            except:
#                return None

#    def get_imageVindulaUser(self,caminho):
#        local = caminho.split('/')
#        try:
#            ctx= getSite()[local[0]][local[1]][local[2]]
#            obj = ctx.restrictedTraverse('@@images').scale('photograph', height=150, width=120)
#        
#            return obj.url
#        except:
#            return ''

