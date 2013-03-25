# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore
from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
from vindula.myvindula.models.department import ModelsDepartment


class ModelsInstanceFuncdetails(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_instance_funcdetails'
    
    #Campos de edição
    id = Int(primary=True)
    username = Unicode()
    date_creation = DateTime()
    
    dadosUses = ReferenceSet(id, "ModelsDadosFuncdetails.vin_myvindula_instance_id")
    
    def departamentos(self):
        result = ModelsDepartment().get_departmentByUsername(self.username)
        return result

    def set_InstanceFuncdetails(self,username):
        D={}
        D['username'] = username
        
        # adicionando...
        instance = ModelsInstanceFuncdetails(**D)
        self.store.add(instance)
        self.store.flush()
        return instance.id
    
    def get_InstanceFuncdetails(self,username):
        data = self.store.find(ModelsInstanceFuncdetails, ModelsInstanceFuncdetails.username==username).one()
        
        if data:
            return data
        else:
            return None
    
    def get_InstanceDadosFuncdetails(self,username):
        data = self.get_InstanceFuncdetails(username)
        if data:
            valores = ModelsDadosFuncdetails().get_DadosFuncdetails_byInstance(data.id)
            if valores and valores.count() > 0:
                return valores

        return []
    
    def del_InstanceDadosFuncdetails(self,username):
        results = self.store.find(ModelsInstanceFuncdetails, ModelsInstanceFuncdetails.username==username).one()
        if results:
            ModelsDadosFuncdetails().del_DadosFuncdetails(results.id)
            
            self.store.remove(results)
            self.store.flush()   
    
    
    def get_AllFuncDetails(self):
        L = []
        data = self.store.find(ModelsInstanceFuncdetails)
        if data.count() > 0:
            for item in data:
                L.append(item.id)
        
        return ModelsDadosFuncdetails().geraDic_DadosUser(L)
    
