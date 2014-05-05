# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select
from storm.zope.interfaces import IZStorm
from zope.component import getUtility
from datetime import date , datetime, timedelta
<<<<<<< HEAD
from hashlib import md5
from random import choice
=======
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite
>>>>>>> 64b82b56b397644671dc1f36cce1a766b5c789a1

#import sys
#from storm.tracer import debug #debug(True, stream=sys.stdout)

class BaseStore(object):

    def __init__(self, *args, **kwargs):
        self.store = getUtility(IZStorm).get('myvindula')

        #Lazy initialization of the object
        for attribute, value in kwargs.items():
            if not hasattr(self, attribute):
                raise TypeError('unexpected argument %s' % attribute)
            else:
                setattr(self, attribute, value)

        # divide o dicionario 'convertidos'
        for key in kwargs:
            setattr(self,key,kwargs[key])

        try:
            # adiciona a data atual
            self.date_creation = datetime.now()
        except:
            # adiciona a data atual
            self.date_created = datetime.now()
            

# Models de Migração
class BaseStoreMyvindula(BaseStore):

    id = Int(primary=True)
    hash = Unicode(default=u'')
    deleted = Bool(default=False)
    date_created = DateTime(default=datetime.now())
    date_modified = DateTime(default=datetime.now())
    date_excluded = DateTime(default=datetime(1970,1,1,0,0,0))

    @property
    def get_date_created(self):
        time_zone = BaseStoreMyvindula.getVindulaTimeZone()
        date = self.date_created - timedelta(hours=time_zone)
        return date
    
    @property
    def date_creation(self):
<<<<<<< HEAD
        return self.date_created


    @property
    def __hash_vindulapp__(self):
        if not self.id:
            #TODO: Gerar um id aleatorio temporariamente
            id = datetime.now().strftime('%Y-%m-%d|%H:%M:%S')+str(choice(range(100)))
            hash = md5(self.__class__.__name__ + str(id)).hexdigest()
        else:
            hash = md5(self.__class__.__name__ + str(self.id)).hexdigest()
        return unicode(hash, 'utf-8')
=======
        time_zone = BaseStoreMyvindula.getVindulaTimeZone()
        date = self.date_created - timedelta(hours=time_zone)
        return date
    
    @staticmethod
    def getVindulaTimeZone():
        portal_obj = getSite()
        
        #Caso nao exista o registro cadastrado ele ira definir o timezone como 3horas por padrao
        time_zone = 3
        if portal_obj and portal_obj.portal_type == 'Plone Site':
            p_registry = getToolByName(portal_obj, 'portal_registry')
            record_time_zone = p_registry.records.get('vindula.controlpanel.settings.ISettings.timezoneVindula')
            if record_time_zone:
                time_zone = record_time_zone.value
                
        return time_zone
>>>>>>> 64b82b56b397644671dc1f36cce1a766b5c789a1
