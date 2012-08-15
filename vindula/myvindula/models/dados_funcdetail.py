# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore


class ModelsDadosFuncdetails(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_dados_funcdetails'
    
    #Campos de edição
    id = Int(primary=True)
    date_creation = DateTime()
    
    valor = Unicode()
    vin_myvindula_confgfuncdetails_fields = Unicode()
    vin_myvindula_instance_id = Int()

    campo = Reference(vin_myvindula_instance_id, "ModelsConfgMyvindula.id")


    def set_DadosFuncdetails(self,**kwargs):
        # adicionando...
        dados = ModelsDadosFuncdetails(**kwargs)
        self.store.add(dados)
        self.store.flush()         

    
    def del_DadosFuncdetails(self,id_instance):
        results = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.vin_myvindula_instance_id==id_instance)
        if results:
            for result in results:
                self.store.remove(result)
                self.store.flush()   
    
    def del_DadosFuncdetails_by_field(self,campo):
        results = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.vin_myvindula_confgfuncdetails_fields==campo)
        if results.count() > 0:
            for result in results:
               self.store.remove(result)
               self.store.flush()          
    
    
    def get_DadosFuncdetails_byInstance(self,id_instance):
        data = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.vin_myvindula_instance_id==id_instance)
        
        if data.count() > 0:
            return data
        else:
            return None
      
    def get_DadosFuncdetails_byInstanceAndField(self,id_instance,fields):
        data = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.vin_myvindula_instance_id==id_instance,
                                                       ModelsDadosFuncdetails.vin_myvindula_confgfuncdetails_fields==fields).one()
        
        if data:
            return data
        else:
            return None
