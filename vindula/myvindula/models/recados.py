# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select

from vindula.myvindula.models.base import BaseStore

from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.contentcore.base import BaseFunc

        
class ModelsMyvindulaRecados(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_recados'
    
    _name_class = "ModelsMyvindulaRecados" 
    
    id = Int(primary=True)
    username = Unicode()
    date_creation = DateTime()
    destination = Unicode()
    text = Unicode()
        
    def set_myvindula_recados(self,**kwargs):
        tools = UtilMyvindula()
        D={}
        D['username'] = unicode(kwargs.get('username',''), 'utf-8')
        D['destination'] = unicode(kwargs.get('destination',''), 'utf-8')
        D['text'] = unicode(kwargs.get('text',''), 'utf-8')
        
        user_send = tools.get_prefs_user(D['username'])
        user_destination = tools.get_prefs_user(D['destination'])

        if user_destination and user_destination.get('email',None):
            assunto = 'Novo recado!!!'
            msg = '''<h2>Você tem um novo recado</h2>
                     <p>Você recebeu um novo recado do(a) <a href='%s'> %s</a> </p>
                     <p>Para visualizar o recado acesse <a href="%s"> aqui </a></p>
                   '''%(tools.site.absolute_url() + '/@@myvindulalistuser?user='+D['username'],
                        user_send.get('name',''), tools.site.absolute_url() + '/@@myvindulalistrecados')
            
            BaseFunc().envia_email(tools.site, msg, assunto, user_destination.get('email',''), [])
         
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
                            