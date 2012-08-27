# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore

        
class ModelsMyvindulaRecados(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_recados'
    
    _name_class = "ModelsMyvindulaRecados" 
    
    id = Int(primary=True)
    username = Unicode()
    date_creation = DateTime()
    destination = Unicode()
    text = Unicode()
        
    def set_myvindula_recados(self,**kwargs):
        D={}
        D['username'] = unicode(kwargs.get('username',''), 'utf-8')
        D['destination'] = unicode(kwargs.get('destination',''), 'utf-8')
        D['text'] = unicode(kwargs.get('text',''), 'utf-8')
        
        # adicionando...
        recados = ModelsMyvindulaRecados(**D)
        self.store.add(recados)
        self.store.flush()
    
    def get_myvindula_recados(self,**kwargs):
        if kwargs.get('destination',None):
            user = kwargs.get('destination','')
            if type(user) != unicode:
                user = unicode(kwargs.get('destination',''), 'utf-8')
            data = self.store.find(ModelsMyvindulaRecados, ModelsMyvindulaRecados.destination==user).order_by(Desc(ModelsMyvindulaRecados.date_creation))
        
            if data.count() > 0:
                return data
            else:
                return None
        else:
            return None            

    def del_myvindula_recados(self, id):
        record = self.store.find(ModelsMyvindulaRecados, ModelsMyvindulaRecados.id==id).one()
        self.store.remove(record)
        self.store.flush()        
                            