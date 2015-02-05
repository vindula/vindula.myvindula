# coding: utf-8


#Imports regarding the connection of the database 'strom'
from datetime import datetime
from hashlib import md5

from storm.locals import *

from vindula.myvindula.models.base import BaseStoreMyvindula
from vindula.myvindula.tools.utils import UtilMyvindula


class UserSessionToken(Storm, BaseStoreMyvindula):
    __storm_table__ = 'vinapp_myvindula_usersessiontoken'

    username = Unicode()
    token = Unicode()
    ip_client = Unicode()

    def set_new_token(self, session, user, ip):
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
        D['date_created'] = datetime.now()

        usersession = UserSessionToken(**D)
        self.store.add(usersession)
        self.store.flush()
        
    
    def invalidateToken(self):
        self.deleted = True
        
        #TODO: Arrumar isso, foi comentada essa linha pois em BD com postgres o storm está dando conflito
        #self.date_excluded = datetime.now()

    @staticmethod
    def get_tokenobj_by_token(token):
        if isinstance(token, str):
            token = token.decode('utf-8')

        rs = UserSessionToken().store.find(UserSessionToken,
                UserSessionToken.token==token,
                UserSessionToken.deleted==False)

        if rs and rs.count():
            return rs[0]
        return None

    @staticmethod
    def token_exits(token):
        obj_token = UserSessionToken.get_tokenobj_by_token(token)
        if obj_token:
            return True
        return False
