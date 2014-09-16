# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select

from vindula.myvindula.models.base import BaseStoreMyvindula

from vindula.content.models.content import ModelsContent


class ModelsFollow(Storm, BaseStoreMyvindula):
    __storm_table__ = 'vinapp_social_follow'


    id = Int(primary=True)
    username = Unicode()
    content_id = Int()


    @staticmethod
    def get_followers(content):
        content_obj = ModelsContent().getContent_by_uid(content,is_user_object=True)
        
        if content_obj:
            ids = []
            for content in content_obj:
                ids.append(content.id)
        else:
            ids = [0]

        data = ModelsFollow().store.find(ModelsFollow, 
                                         ModelsFollow.content_id.is_in(ids), 
                                         ModelsFollow.deleted==False)
        return data
    
    
    @staticmethod
    def get_followings(content):
        data = ModelsFollow().store.find(ModelsFollow, ModelsFollow.username==content, ModelsFollow.deleted==False)
        
        return data

