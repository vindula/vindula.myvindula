# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore

        
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
