# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore


class ModelsMyvindulaCourses(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_courses'
    
    id = Int(primary=True)
    title = Unicode()
    length = Unicode()
    
    def get_allCourses(self):
        data = self.store.find(ModelsMyvindulaCourses)
        if data:
            return data
        else:
            return None
    
    def set_courses(self,**kwargs):
        # adicionando...
        couses = ModelsMyvindulaCourses(**kwargs)
        self.store.add(couses)
        self.store.flush() 
        
    def get_courses_byID(self,id):
        data = self.store.find(ModelsMyvindulaCourses, ModelsMyvindulaCourses.id==id).one()
        if data:
            return data
        else:
            return None