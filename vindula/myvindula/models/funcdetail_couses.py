# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore


class ModelsMyvindulaFuncdetailCouses(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_funcdetail_couses'
    __storm_primary__ = "vin_myvindula_funcdetail_username", "vin_myvindula_courses_id"
    
    #id = Int(primary=True)
    vin_myvindula_funcdetail_username = Unicode()
    vin_myvindula_courses_id = Int()
    
    def get_funcdetailCouserByUsername(self, user):
        data = self.store.find(ModelsMyvindulaFuncdetailCouses, ModelsMyvindulaFuncdetailCouses.vin_myvindula_funcdetail_username==user)
        
        if data:
            return data
        else:
            return None
    
    def set_funcdetailCouser(self,**kwargs):
        D={}
        D['vin_myvindula_funcdetail_username']= kwargs.get('username','')
        D['vin_myvindula_courses_id'] = int(kwargs.get('id_courses',''))
    
        # adicionando...
        funcdetailCouser = ModelsMyvindulaFuncdetailCouses(**D)
        self.store.add(funcdetailCouser)
        self.store.flush()   
        
    
    def del_funcdetailCouser(self, user):
        results = self.store.find(ModelsMyvindulaFuncdetailCouses, ModelsMyvindulaFuncdetailCouses.vin_myvindula_funcdetail_username==user)
        if results:
            for result in results:
                self.store.remove(result)
                self.store.flush()