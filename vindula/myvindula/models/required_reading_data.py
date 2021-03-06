# -*- coding: utf-8 -*-
from datetime import datetime
from hashlib import md5

import requests
from storm.locals import *
from zope.component.hooks import getSite

from vindula.myvindula.config import HA_VINDULAPP_HOST,HA_VINDULAPP_PORT
from vindula.myvindula.models.base import BaseStoreMyvindula


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

        kwargs['date_created'] = datetime.now()
        kwargs['date_modified'] = datetime.now()

        data = RequiredReadingData(**kwargs)
        self.store.add(data)
        self.store.commit()
        self.store.flush()

        #Criando o registro de log para o analytics
        site = getSite()
        session = site.REQUEST.SESSION
        token = session.get('user_token')

        uri = 'vindula-api/myvindula/run-log/%s/%s/%s' % (token, self.__class__.__name__, data.hash)
        url = 'http://%s:%s/%s' %(HA_VINDULAPP_HOST,HA_VINDULAPP_PORT,uri)
        requests.get(url)
        
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