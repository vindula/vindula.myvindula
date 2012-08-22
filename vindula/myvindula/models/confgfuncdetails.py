# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore
from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails


class ModelsConfgMyvindula(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_confgfuncdetails'
    
    #Campos de edição
    #id = Int()
    fields = Unicode(primary=True)
    ativo_edit = Bool()
    ativo_view = Bool()
    label = Unicode()
    decription = Unicode()
    required = Bool()
    type = Unicode()
    list_values = Unicode()
    ordem = Int()
    mascara = Unicode()
    area_de_view = Unicode()
    
    def set_configuration(self,**kwargs):
        # adicionando...
        config = ModelsConfgMyvindula(**kwargs)
        self.store.add(config)
        self.store.flush()                

    def set_ordemConfiguration(self,campo,ordem):
        record = self.get_configuration_By_fields(campo)
        if record:
            record.ordem = ordem
            self.store.flush()
        
    def del_configuration(self, campo):
        record = self.store.find(ModelsConfgMyvindula, ModelsConfgMyvindula.fields==campo).one()
        if record:
            ModelsDadosFuncdetails().del_DadosFuncdetails_by_field(campo)
        
            self.store.remove(record)
            self.store.flush()        
        
    #loads data into DataBase    
    def get_configuration_By_fields(self, campo):
        try:campo = unicode(campo, 'utf-8')    
        except:pass 

        data = self.store.find(ModelsConfgMyvindula, ModelsConfgMyvindula.fields==campo).one()
        if data:
            return data
        else:
            return None
        
    def get_configurationAll(self):
        data = self.store.find(ModelsConfgMyvindula).order_by(ModelsConfgMyvindula.ordem)
        if data.count() > 0:
            return data
        else:
            return []
            
    def check_fields(self,campo):
        data = self.store.find(ModelsConfgMyvindula, ModelsConfgMyvindula.fields==campo)
        if data.count()>0:
            return False
        else:
            return True
             
    def getConfig_byArea(self,area):
        data = self.store.find(ModelsConfgMyvindula, ModelsConfgMyvindula.area_de_view==area,
                                                     ModelsConfgMyvindula.ativo_view==True).order_by(ModelsConfgMyvindula.ordem)
                                                             
        if data.count() > 0:
            return data
        else:
            return []
            

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