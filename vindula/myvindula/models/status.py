# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select

from vindula.myvindula.models.base import BaseStoreMyvindula

from vindula.content.models.content import ModelsContent


class ModelsStatus(Storm, BaseStoreMyvindula):
    __storm_table__ = 'vinapp_social_status'


    id = Int(primary=True)
    username = Unicode()
    content_id = Int()
    text = Unicode()
    
    @staticmethod
    def get_last_status(username):
        if isinstance(username, str):
            username = unicode(username, 'utf-8')
        
        data = ModelsStatus().store.find(ModelsStatus, ModelsStatus.username==username, 
                                         ModelsStatus.deleted==False).order_by(Desc(ModelsStatus.date_created,))
        if data.count():
            return data[0]
        else:
            return None
