# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore
from vindula.myvindula.tools.utils import UtilMyvindula

from hashlib import md5 
from datetime import datetime

class UserSessionToken(Storm, BaseStore):
    __storm_table__ = 'vinapp_myvindula_usersessiontoken'

    id = Int(primary=True)
    username = Unicode()
    token = Unicode()
    ip_client = Unicode()
    hash = Unicode()
    date_created = DateTime()
    date_modified = DateTime()
    date_excluded = DateTime()
    
    
    def set_new_token(self,session, user,ip):
        tool = UtilMyvindula()
        
        username = user.getUserName()
        token = md5(username+session.token+session.id).hexdigest()
        hash = md5('UserSessionToken'+username).hexdigest()
          
        session.set('user_token', token)
        
        D={}
        D['username'] = tool.Convert_utf8(username)
        D['token'] = tool.Convert_utf8(token)
        D['hash'] = tool.Convert_utf8(hash)
        D['ip_client'] = tool.Convert_utf8(ip)
        D['date_created'] = datetime.now()
        
        usersession = UserSessionToken(**D)
        self.store.add(usersession)
        self.store.flush()
        