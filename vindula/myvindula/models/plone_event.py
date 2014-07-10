# coding: utf-8
#Imports regarding the connection of the database 'strom'
from storm.locals import *

from vindula.myvindula.models.base import BaseStore, BaseStoreMyvindula
from vindula.myvindula.tools.utils import UtilMyvindula


from datetime import datetime, timedelta

class PloneEvent(Storm, BaseStore):
    __storm_table__ = 'vinapp_myvindula_plone_event'

    id = Int(primary=True)
    uid = Unicode()
    type = Unicode()
    actor = Unicode()
    status = Bool()
    error = Bool()
    date_created = DateTime()
    
    def set_event(self,uid,portal_type,actor):
        tool = UtilMyvindula()
       
        D={}
        D['uid'] = tool.Convert_utf8(uid)
        D['type'] = tool.Convert_utf8(portal_type)
        D['status'] = False
        D['error'] = False
        D['actor'] = tool.Convert_utf8(actor)
        
        time_zone = BaseStoreMyvindula.getVindulaTimeZone()
        D['date_created'] = datetime.now() + timedelta(hours=time_zone)
        
        event = PloneEvent(**D)
        self.store.add(event)
        self.store.flush()
