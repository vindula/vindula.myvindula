# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore


    
class ModelsUserDocuments(Storm, BaseStore):    
    __storm_table__ = 'vin_myvindula_user_documents'
    
    id = Int(primary=True)
    documento = Pickle()
    date_creation = DateTime()
    vin_myvindula_funcdetails_username = Unicode()
    vin_myvindula_config_documents_id = Int()
    
    funcionario = Reference(vin_myvindula_funcdetails_username, "ModelsFuncDetails.username")
    nome_documento = Reference(vin_myvindula_config_documents_id, "ModelsConfigDocuments.id")
    
    def set_UserDocuments(self, **kwargs):
        # adicionando...
        userDoc = ModelsUserDocuments(**kwargs)
        self.store.add(userDoc)
        self.store.flush()
        
    def del_UserDocuments(self, user,doc):
        results = self.get_UserDocuments_by_user_and_doc(user, doc)
        if results:
            self.store.remove(results)
            self.store.flush()
        
    def get_UserDocuments(self):
        data = self.store.find(ModelsUserDocuments)
        if data.count() > 0:
            return data
        else:
            return None                

    def get_UserDocuments_byUsername(self, username):
        data = self.store.find(ModelsUserDocuments, ModelsUserDocuments.vin_myvindula_funcdetails_username == username)
        if data.count() > 0:
            return data
        else:
            return None

    def get_UserDocuments_byID(self, id):
        data = self.store.find(ModelsUserDocuments, ModelsUserDocuments.id == id).one()
        if data:
            return data
        else:
            return None    
    
    
    def get_UserDocuments_by_user_and_doc(self, user, doc):
        data = self.store.find(ModelsUserDocuments, ModelsUserDocuments.vin_myvindula_funcdetails_username == user,
                                                    ModelsUserDocuments.vin_myvindula_config_documents_id == doc).one()
        if data:
            return data
        else:
            return None