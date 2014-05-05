# coding: utf-8

#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select

from vindula.myvindula.models.base import BaseStoreMyvindula


class RequiredReadingData(Storm, BaseStoreMyvindula):
    __storm_table__ = 'vinapp_social_required_reading_data'

    username = Unicode()
    content_id = Int()
    is_read = Bool()
    
    content = Reference(content_id, "ModelsContent.id")
    
    @staticmethod
    def getData(username, content):
        if isinstance(username, str):
            username = unicode(username, 'utf-8')
         
        data = RequiredReadingData().store.find(RequiredReadingData, 
                                                RequiredReadingData.username==username,
                                                RequiredReadingData.content==content,
                                                RequiredReadingData.deleted==False)
        if data.count():
            return data
        else:
            return None