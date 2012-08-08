# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore



class ModelsInstanceFuncdetails(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_instance_funcdetails'
    
    #Campos de edição
    id = Int(primary=True)
    username = Unicode()
    date_creation = DateTime()
    ativo_view = Bool()
    label = Unicode()

