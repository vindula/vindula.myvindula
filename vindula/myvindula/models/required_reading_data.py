# coding: utf-8

#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select

from vindula.myvindula.models.base import BaseStoreMyvindula

from hashlib import md5
from datetime import datetime


class RequiredReadingData(Storm, BaseStoreMyvindula):
    __storm_table__ = 'vinapp_social_required_reading_data'

    username = Unicode()
    content_id = Int()
    is_read = Bool()
    
    content = Reference(content_id, "ModelsContent.id")
    
    def setReadingData(self, **kwargs):
        str_data = datetime.now().strftime('%Y-%m-%d|%H:%M:%S:%f')
        hash = md5('RequiredReadingData'+kwargs.get('username','') + str_data).hexdigest()
        kwargs['hash'] = unicode(hash)
        
        if kwargs.get('username','') and isinstance(kwargs.get('username',''), str):
            kwargs['username'] = kwargs.get('username','').decode('utf-8')
        
        data = RequiredReadingData(**kwargs)
        self.store.add(data)
        self.store.flush()
        
        return self
    
    @staticmethod
    def getData(username, content, is_read=True):
        if isinstance(username, str):
            username = unicode(username, 'utf-8')
         
        data = RequiredReadingData().store.find(RequiredReadingData, 
                                                RequiredReadingData.username==username,
                                                RequiredReadingData.content==content,
                                                RequiredReadingData.is_read==is_read,
                                                RequiredReadingData.deleted==False)
        if data.count():
            return data
        else:
            return None