# coding: utf-8

import pytz
#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStoreMyvindula
from vindula.myvindula.tools.utils import UtilMyvindula

from hashlib import md5
from datetime import datetime

class UserSessionToken(Storm, BaseStoreMyvindula):
    __storm_table__ = 'vinapp_myvindula_usersessiontoken'

    username = Unicode(default=u'')
    token = Unicode(default=u'')
    ip_client = Unicode(default=u'')


    def set_new_token(self,session, user,ip):
        tool = UtilMyvindula()

        username = user.getUserName()
        token = md5(username+session.token+session.id).hexdigest()
        str_data = datetime.now().strftime('%Y-%m-%d|%H:%M:%S')
        hash = md5('UserSessionToken'+username+str_data).hexdigest()
        
        session.set('user_token', token)

        D={}
        D['username'] = tool.Convert_utf8(username)
        D['token'] = tool.Convert_utf8(token)
        D['hash'] = tool.Convert_utf8(hash)
        D['ip_client'] = tool.Convert_utf8(ip)
        D['date_created'] = datetime.now(pytz.utc)

        usersession = UserSessionToken(**D)
        self.store.add(usersession)
        self.store.flush()
