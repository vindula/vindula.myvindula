# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore


class ModelsMyvindulaFuncdetailLanguages(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_funcdetail_languages'
    __storm_primary__ = "vin_myvindula_funcdetail_username", "vin_myvindula_languages_id"

    #id = Int(primary=True)
    vin_myvindula_funcdetail_username = Unicode(primary=True)
    vin_myvindula_languages_id = Int()
    
    languages = Reference(vin_myvindula_languages_id, "ModelsMyvindulaLanguages.id")
    
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