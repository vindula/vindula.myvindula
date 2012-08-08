# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select

from vindula.myvindula.models.base import BaseStore



class ModelsPhotoUser(Storm, BaseStore):    
    __storm_table__ = 'vin_myvindula_photo_user'
    
    id = Int(primary=True)
    username = Unicode()
    date_creation = DateTime()
    photograph = Pickle()
    thumb = Pickle()
        
    def set_ModelsPhotoUser(self, **kwargs):
        # adicionando...
        setup = ModelsPhotoUser(**kwargs)
        self.store.add(setup)
        self.store.flush()
        return setup.id          
    
    def del_ModelsPhotoUser(self, username):
        result = self.get_ModelsPhotoUser_byUsername(username)
        if result:
            self.store.remove(result)
            self.store.flush()

    
    def get_ModelsPhotoUser_byID(self,id):
        data = self.store.find(ModelsPhotoUser, ModelsPhotoUser.id == id).one()
        if data:
            return data
        else:
            return None

    def get_ModelsPhotoUser_byUsername(self,username):
        data = self.store.find(ModelsPhotoUser, ModelsPhotoUser.username == username).one()
        if data:
            return data
        else:
            return None