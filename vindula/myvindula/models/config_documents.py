# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore


class ModelsConfigDocuments(Storm, BaseStore):    
    __storm_table__ = 'vin_myvindula_config_documents'
    
    id = Int(primary=True)
    name_document = Unicode()
    date_creation = DateTime()
    flag_ativo = Bool()
    
    
    def set_ConfigDocuments(self, **kwargs):
        # adicionando...
        confDoc = ModelsConfigDocuments(**kwargs)
        self.store.add(confDoc)
        self.store.flush()        
    
    def get_allConfigDocuments(self):
        data = self.store.find(ModelsConfigDocuments).order_by(ModelsConfigDocuments.name_document)
        if data.count() == 0:
            return None
        else:
            return data
        
    
    def get_ConfigDocuments_byID(self,id):
        data = self.store.find(ModelsConfigDocuments, ModelsConfigDocuments.id == id).one()
        if data:
            return data
        else:
            return None