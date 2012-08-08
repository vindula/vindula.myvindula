# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore



class ModelsConfgMyvindula(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_confgfuncdetails'
    
    #Campos de edição
    #id = Int()
    fields = Unicode(primary=True)
    ativo_edit = Bool()
    ativo_view = Bool()
    label = Unicode()
    decription = Unicode()
    ordem = Int()

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