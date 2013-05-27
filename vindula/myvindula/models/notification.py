# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select

from vindula.myvindula.models.base import BaseStore

from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.contentcore.base import BaseFunc


class ModelsMyvindulaNotificacao(Storm, BaseStore):
    __storm_table__ = 'vinapp_social_notification'

    _name_class = "ModelsMyvindulaNotificacao"

    id = Int(primary=True)
    username = Unicode()
    actor = Unicode()
    action = Unicode()
    viewed = Bool()

    date_created = DateTime()


    def cont_notificacao_new(self,user):
        data = self.get_myvindula_notificacao(username=user)
        if data:
            data = data.find(ModelsMyvindulaNotificacao.viewed==False)
            return data.count()

        return 0

    def get_myvindula_notificacao(self,**kwargs):
        if kwargs.get('username',None):
            user = kwargs.get('username','')

            if type(user) != unicode:
                user = unicode(kwargs.get('username',''), 'utf-8')

            data = self.store.find(ModelsMyvindulaNotificacao,
                                   ModelsMyvindulaNotificacao.username==user,
                                   ModelsMyvindulaNotificacao.viewed==False).order_by(Desc(ModelsMyvindulaNotificacao.date_created,))

            return data
            #if data.count() > 0:
            #    return data
            #else:
            #    return None
        else:
            return None

