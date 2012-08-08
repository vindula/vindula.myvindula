# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore


class ModelsDadosFuncdetails(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_dados_funcdetails'
    
    #Campos de edição
    id = Int(primary=True)
    date_creation = DateTime()
    type = Unicode()
    valor = Unicode()
    vin_myvindula_confgfuncdetails_fields = Int()
    vin_myvindula_instance_id = Int()





