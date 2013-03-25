# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select

from vindula.myvindula.models.base import BaseStore

from vindula.myvindula.tools.utils import UtilMyvindula
         
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
        tools = UtilMyvindula()
        caminho = tools.portal_url.getPortalPath()
        data = tools.catalog(portal_type='OrganizationalStructure', 
                      sort_on = 'sortable_title',
                      path=caminho)   
        
        #data = self.store.find(ModelsDepartment)
        if data: 
            return data
        else:
            return []
        
    def get_departmentByUsername(self,user):
        tools = UtilMyvindula()
        datas = self.store.find(ModelsDepartment, ModelsDepartment.vin_myvindula_funcdetails_id==user)
        if datas.count() != 0:
            L=[]
            for data in datas:
                obj = tools.catalog({'UID':data.uid_plone})
                if obj:
                    L.append(obj[0])
            if L:
                return L


        return []

#    def get_departmentByID(self,id):
#        data = self.store.find(ModelsDepartment, ModelsDepartment.id==int(id)).one()
#        if data:
#            return data
#        else:
#            return None


    def del_department(self, user, depUID=None):
        if depUID:
            results = self.store.find(ModelsDepartment, ModelsDepartment.vin_myvindula_funcdetails_id==user, ModelsDepartment.uid_plone==depUID)
        else:
            results = self.store.find(ModelsDepartment, ModelsDepartment.vin_myvindula_funcdetails_id==user)
        if results:
            for result in results:
                self.store.remove(result)
                self.store.flush()
