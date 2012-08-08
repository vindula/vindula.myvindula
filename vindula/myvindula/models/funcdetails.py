# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore
from vindula.myvindula.models.department import ModelsDepartment


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


        
    def get_FuncBusca(self,name='',department_id=u'0',phone='',filtro=False):
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
        
        
    def get_FuncBusca_dinamic(self,department_id='',form_campos=[],filtro=False):
        origin = [ModelsFuncDetails, Join(ModelsDepartment, ModelsDepartment.vin_myvindula_funcdetails_id==ModelsFuncDetails.username)]
        busca = "self.store.using(*origin).find(ModelsFuncDetails,"
        for item in form_campos:
            if item.values()[0]:
                busca += "ModelsFuncDetails."+item.keys()[0]+".like( '%' + '%'.join(u'"+item.values()[0]+"'.split(' ')) + '%' ),"
        
        if department_id:
            busca += "ModelsDepartment.uid_plone==department_id,"
            
        busca += ").order_by(ModelsFuncDetails.name)"
        data = eval(busca)
        
#        
#        if department_id == u'0' and name == '' and phone == '':
#            data = self.store.find(ModelsFuncDetails).order_by(ModelsFuncDetails.name)
#         
#        elif department_id != u'0':
#            origin = [ModelsFuncDetails, Join(ModelsDepartment, ModelsDepartment.vin_myvindula_funcdetails_id==ModelsFuncDetails.username)]
#            data = self.store.using(*origin).find(ModelsFuncDetails,  ModelsFuncDetails.name.like( '%' + '%'.join(name.split(' ')) + '%' ),
#                                                                      ModelsFuncDetails.phone_number.like("%" + phone + "%"),                                                                      
#                                                                      ModelsDepartment.uid_plone==department_id).order_by(ModelsFuncDetails.name)
#        
#        elif department_id == u'0' and name != '':
#            data = self.store.find(ModelsFuncDetails, ModelsFuncDetails.name.like( '%' + '%'.join(name.split(' ')) + '%' )).order_by(ModelsFuncDetails.name)
#
#        else:
#            data = self.store.find(ModelsFuncDetails, ModelsFuncDetails.name.like( '%' + '%'.join(name.split(' ')) + '%' ),
#                                                      ModelsFuncDetails.phone_number.like("%" + phone + "%")).order_by(ModelsFuncDetails.name)
                                                      
        if filtro:
            data = data.find(ModelsFuncDetails.phone_number != None)
        
        if data.count() == 0:
            return None
        else:
            return data.group_by(ModelsFuncDetails.username)        
           

    
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