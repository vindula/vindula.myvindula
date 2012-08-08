# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore


class ModelsMyvindulaLike(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_like'
    
    id = Int(primary=True)
    username = Unicode()
    date_creation = DateTime()
    type = Unicode()
    id_obj = Unicode()
    isPlone = Bool()
     
    def set_myvindula_like(self,**kwargs):
        D={}
        base = BaseFunc() 
        D['username'] =  base.Convert_utf8(kwargs.get('username',''))
        D['type'] =  base.Convert_utf8(kwargs.get('type',''))
        D['id_obj'] =  base.Convert_utf8(kwargs.get('id_obj',''))
        D['isPlone'] = eval(kwargs.get('isPlone','False'))
        
        # adicionando...
        comments = ModelsMyvindulaLike(**D)
        self.store.add(comments)
        self.store.flush()        

    def get_myvindula_like(self,**kwargs):
        id_obj = kwargs.get('id_obj','')
        type_obj = kwargs.get('type','')
        if type(id_obj) != unicode:
            id_obj = unicode(id_obj)
        if type(type_obj) != unicode:
            type_obj = unicode(type_obj)
        data = self.store.find(ModelsMyvindulaLike, ModelsMyvindulaLike.id_obj==id_obj,ModelsMyvindulaLike.type==type_obj)

        if data.count > 0:
            return data
        else:
            return None   

    def del_myvindula_like(self, **kwargs):
        id_obj = kwargs.get('id_obj','')
        username = kwargs.get('username','')
        type_obj = kwargs.get('type','')
        
        if type(id_obj) != unicode:
            id_obj = unicode(id_obj)
        if type(username) != unicode:
            username = unicode(username)
        if type(type_obj) != unicode:
            type_obj = unicode(type_obj)
        
        record = self.store.find(ModelsMyvindulaLike, ModelsMyvindulaLike.id_obj==id_obj,
                                                      ModelsMyvindulaLike.type==type_obj,
                                                      ModelsMyvindulaLike.username==username).one()
        self.store.remove(record)
        self.store.flush()