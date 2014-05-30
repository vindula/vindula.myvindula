# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select

from vindula.myvindula.models.base import BaseStoreMyvindula


class FieldCategory(Storm, BaseStoreMyvindula):
    __storm_table__ = 'vinapp_myvindula_fieldcategory'

    #Campos de edição
    name = Unicode(default=u'')
    label = Unicode(default=u'')
    order_position = Int(default=0)