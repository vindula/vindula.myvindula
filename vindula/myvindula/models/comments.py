# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore

 

class ModelsMyvindulaComments(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_comments'
    
    _name_class = "ModelsMyvindulaComments"     
    
    id = Int(primary=True)
    username = Unicode()
    ip = Unicode()
    date_creation = DateTime()
    type = Unicode()
    id_obj = Unicode()
    isPlone = Bool()
    text = Unicode()
    
    def set_myvindula_comments(self,**kwargs):
        from vindula.myvindula.user import BaseFunc
        D={}
        base = BaseFunc() 
        D['username'] = base.Convert_utf8(kwargs.get('username',''))
        D['ip'] = base.Convert_utf8(kwargs.get('ip',''))
        D['type'] = base.Convert_utf8(kwargs.get('type',''))
        D['id_obj'] = base.Convert_utf8(kwargs.get('id_obj',''))
        D['isPlone'] = eval(kwargs.get('isPlone','False'))
        D['text'] = base.Convert_utf8(kwargs.get('text',''))
        
        # adicionando...
        comments = ModelsMyvindulaComments(**D)
        self.store.add(comments)
        self.store.flush()
        
        return comments.id        

    def get_myvindula_comments(self,**kwargs):
        id_obj = kwargs.get('id_obj','')
        type_obj = kwargs.get('type','')
        if type(id_obj) != unicode:
            id_obj = unicode(id_obj)
        if type(type_obj) != unicode:
            type_obj = unicode(type_obj)
        data = self.store.find(ModelsMyvindulaComments, ModelsMyvindulaComments.id_obj==id_obj,ModelsMyvindulaComments.type==type_obj)

        if data.count > 0:
            return data
        else:
            return None
        
    def get_comments_byID(self, id):
        data = self.store.find(ModelsMyvindulaComments, ModelsMyvindulaComments.id==id).one()
        
        if data:
            return data
        else:
            return None
    
    def del_myvindula_comments(self, id):
        record = self.store.find(ModelsMyvindulaComments, ModelsMyvindulaComments.id==id).one()
        self.store.remove(record)
        self.store.flush()        
                   