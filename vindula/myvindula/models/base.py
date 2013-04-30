# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select
from storm.zope.interfaces import IZStorm
from zope.component import getUtility
from datetime import date , datetime


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
#
        try:
            # adiciona a data atual
            self.date_creation = datetime.now()
        except:
            # adiciona a data atual
            self.date_created = datetime.now()

