# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStoreMyvindula

from hashlib import md5
from datetime import datetime


class ModelsConfgMyvindula(Storm, BaseStoreMyvindula):
    #__storm_table__ = 'vin_myvindula_confgfuncdetails'
    __storm_table__ = 'vinapp_myvindula_userschemafields'

    #Campos de edição
    name = Unicode(default=u'')
    label = Unicode(default=u'')
    decription = Unicode(default=u'')
    required = Bool(default=False)
    ativo_edit = Bool(default=True)
    ativo_view = Bool(default=True)
    type = Unicode(default=u'')
    choices =  Unicode(default=u'')
    order_position = Int(default=0)
    mask = Unicode(default=u'')
    profile_category = Reference(id, "FieldCategory.id")


    def set_configuration(self,**kwargs):
        # adicionando...
        str_data = datetime.now().strftime('%Y-%m-%d|%H:%M:%S')
        hash = md5('ModelsConfgMyvindula'+kwargs.get('name','')+str_data).hexdigest()

        kwargs['hash'] = unicode(hash)

        config = ModelsConfgMyvindula(**kwargs)
        self.store.add(config)
        self.store.flush()

    def set_ordemConfiguration(self,campo,ordem):
        record = self.get_configuration_By_fields(campo)
        if record:
            record.ordem = ordem
            self.store.flush()

    def del_configuration(self, campo):
        from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
        from vindula.myvindula.models.photo_user import ModelsPhotoUser

        record = self.store.find(ModelsConfgMyvindula, ModelsConfgMyvindula.name==campo).one()
        if record:
            ModelsDadosFuncdetails().del_DadosFuncdetails_by_field(campo)
            ModelsPhotoUser().del_PhotoUser_byCampo(campo)

            self.store.remove(record)
            self.store.flush()

    #loads data into DataBase
    def get_configuration_By_fields(self, campo):
        try:campo = unicode(campo, 'utf-8')
        except:pass

        data = self.store.find(ModelsConfgMyvindula, ModelsConfgMyvindula.name==campo).one()
        if data:
            return data
        else:
            return None

    def get_configurationAll(self):
        data = self.store.find(ModelsConfgMyvindula).order_by(ModelsConfgMyvindula.order_position)
        return data

    def check_fields(self,campo):
        data = self.store.find(ModelsConfgMyvindula, ModelsConfgMyvindula.name==campo)
        if data.count()>0:
            return False
        else:
            return True

    def getConfig_byArea(self,area):
        data = self.store.find(ModelsConfgMyvindula, ModelsConfgMyvindula.profile_category==area,
                                                     ModelsConfgMyvindula.ativo_view==True).order_by(ModelsConfgMyvindula.order_position)

        if data.count() > 0:
            return data
        else:
            return []


    def getConfig_views(self,campo):
        result = self.get_configuration_By_fields(campo)
        if result:
            return result.ativo_view
        else:
            return True

    def getConfig_edit(self,campo):
        result = self.get_configuration_By_fields(campo)
        if result:
            return result.ativo_edit
        else:
            return True