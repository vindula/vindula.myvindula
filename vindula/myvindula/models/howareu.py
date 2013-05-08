# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore


class ModelsMyvindulaHowareu(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_howareu'

    _name_class = "ModelsMyvindulaHowareu"

    id = Int(primary=True)
    username = Unicode()
    date_creation = DateTime()
    visible_area = Unicode()
    text = Unicode()
    upload_image = Pickle()
    upload_image_small = Pickle()

    def set_myvindula_howareu(self,**kwargs):
        D={}

        D['username'] = unicode(kwargs.get('username',''), 'utf-8')
        D['visible_area'] = unicode(kwargs.get('visible_area',''), 'utf-8')
        D['upload_image'] = kwargs.get('upload_image',None)
        D['text'] = unicode(kwargs.get('text',''), 'utf-8')

        # adicionando...
        howareu = ModelsMyvindulaHowareu(**D)
        self.store.add(howareu)
        self.store.flush()


    def set_howareu_image_small(self,obj, image):
        obj.upload_image_small = unicode(image, 'utf-8')
        self.store.commit()
        self.store.flush()


    def get_myvindula_howareu(self,**kwargs):
        if kwargs.get('username',None):
            user = kwargs.get('username','')
            if type(user) != unicode:
                user = unicode(kwargs.get('username',''), 'utf-8')
            data = self.store.find(ModelsMyvindulaHowareu, ModelsMyvindulaHowareu.username==user).order_by(Desc(ModelsMyvindulaHowareu.date_creation))

        elif kwargs.get('visible_area',None):
            visible_area = kwargs.get('visible_area','')
            if type(visible_area) != unicode:
                visible_area = unicode(kwargs.get('visible_area',''), 'utf-8')
            data = self.store.find(ModelsMyvindulaHowareu, ModelsMyvindulaHowareu.visible_area==visible_area)

        else:
            data = self.store.find(ModelsMyvindulaHowareu).order_by(Desc(ModelsMyvindulaHowareu.date_creation))

        if data.count() > 0:
            return data
        else:
            return None

    def get_myvindula_howareu_By_Id(self,id):
        data = self.store.find(ModelsMyvindulaHowareu, ModelsMyvindulaHowareu.id==int(id)).one()

        if data:
            return data
        else:
            return None

    def del_myvindula_howareu(self, id):
        record = self.store.find(ModelsMyvindulaHowareu, ModelsMyvindulaHowareu.id==id).one()
        self.store.remove(record)
        self.store.flush()