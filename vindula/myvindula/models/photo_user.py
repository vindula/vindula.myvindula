# coding: utf-8

#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select

from vindula.myvindula.models.base import BaseStore



class ModelsPhotoUser(Storm, BaseStore):    
    __storm_table__ = 'vin_myvindula_photo_user'
    
    id = Int(primary=True)
    date_creation = DateTime()
    username = Unicode()
    
    photograph = Pickle()
    thumb = Pickle()
    
    vin_myvindula_confgfuncdetails_fields = Unicode()
    vin_myvindula_instance_id = Int()
        
    def set_ModelsPhotoUser(self, **kwargs):
        # adicionando...
        setup = ModelsPhotoUser(**kwargs)
        self.store.add(setup)
        self.store.flush()
        return setup.id          
    
    

    def get_ModelsPhotoUser_byFieldAndInstance(self,field, instance):
        data = self.store.find(ModelsPhotoUser, ModelsPhotoUser.vin_myvindula_instance_id == instance,
                                                ModelsPhotoUser.vin_myvindula_confgfuncdetails_fields==field).one()
        if data:
            return data
        else:
            return None
    
    def get_ModelsPhotoUser_byID(self,id):
        data = self.store.find(ModelsPhotoUser, ModelsPhotoUser.id == id).one()
        if data:
            return data
        else:
            return None


# Metodos de Migração temporario
    def get_ModelsPhotoUser_byUsername(self,username,field=u'photograph'):
        from vindula.myvindula.models.instance_funcdetail import ModelsInstanceFuncdetails
        data = self.store.find(ModelsPhotoUser, ModelsPhotoUser.username == username).one()
        if not data:
            instance_user = ModelsInstanceFuncdetails().get_InstanceFuncdetails(username)
            if instance_user:
                data = self.get_ModelsPhotoUser_byFieldAndInstance(field,instance_user.id)
        
        if data:
            return data
        else:
            return None
    
    
    def del_ModelsPhotoUser(self,field, instance):
        result = self.get_ModelsPhotoUser_byFieldAndInstance(field, instance)
        if result:
            self.store.remove(result)
            self.store.flush()