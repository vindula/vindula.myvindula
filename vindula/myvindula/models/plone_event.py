# coding: utf-8
#Imports regarding the connection of the database 'strom'
from storm.locals import *

from vindula.myvindula.models.base import BaseStore
from vindula.myvindula.tools.utils import UtilMyvindula


from datetime import datetime

class PloneEvent(Storm, BaseStore):
    __storm_table__ = 'vinapp_myvindula_plone_event'

    id = Int(primary=True)
    uid = Unicode()
    status = Bool()
    date_created = DateTime()
    
    def set_event(self,uid):
        tool = UtilMyvindula()
       
        D={}
        D['uid'] = tool.Convert_utf8(uid)
        D['status'] = False
        D['date_created'] = datetime.now()
        
        event = PloneEvent(**D)
        self.store.add(event)
        self.store.flush()
