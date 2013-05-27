# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select

from vindula.myvindula.models.base import BaseStore

from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.contentcore.base import BaseFunc


class ModelsMyvindulaRecados(Storm, BaseStore):
    __storm_table__ = 'vinapp_social_message'

    _name_class = "ModelsMyvindulaRecados"

    id = Int(primary=True)
    username = Unicode()
    receiver = Unicode()
    text = Unicode()
    viewed = Bool()

    date_created = DateTime()


    # def set_myvindula_recados(self,**kwargs):
    #     tools = UtilMyvindula()
    #     D={}
    #     D['username'] = unicode(kwargs.get('username',''), 'utf-8')
    #     D['destination'] = unicode(kwargs.get('destination',''), 'utf-8')
    #     D['text'] = unicode(kwargs.get('text',''), 'utf-8')

    #     user_send = tools.get_prefs_user(D['username'])
    #     user_destination = tools.get_prefs_user(D['destination'])

    #     if user_destination and user_destination.get('email',None):
    #         assunto = 'Novo recado!!!'
    #         msg = '''<h2>Você tem um novo recado</h2>
    #                  <p>Você recebeu um novo recado do(a) <a href='%s'> %s</a> </p>
    #                  <p>Para visualizar o recado acesse <a href="%s"> aqui </a></p>
    #                '''%(tools.site.absolute_url() + '/@@myvindulalistuser?user='+D['username'],
    #                     user_send.get('name',''), tools.site.absolute_url() + '/@@myvindulalistrecados')

    #         BaseFunc().envia_email(tools.site, msg, assunto, user_destination.get('email',''), [])

    #     # adicionando...
    #     recados = ModelsMyvindulaRecados(**D)
    #     self.store.add(recados)
    #     self.store.flush()


    def cont_recados_new(self,user):
        data = self.get_myvindula_recados(destination=user)
        #if data:
        data = data.find(ModelsMyvindulaRecados.viewed==False)
        return data.count()

        return 0

    def get_myvindula_recados(self,**kwargs):
        #Todo: colocar um limite de itens retornados
        if kwargs.get('destination',None):
            user = kwargs.get('receiver',None)
            if user == None:
                user = kwargs.get('destination',None)

            if type(user) != unicode:
                user = unicode(user, 'utf-8')

            data = self.store.find(ModelsMyvindulaRecados,
                                   ModelsMyvindulaRecados.receiver==user).order_by(Desc(ModelsMyvindulaRecados.date_created))
            return data
            #if data.count() > 0:
            #    return data
            #else:
            #    return []
        else:
            return None

    def del_myvindula_recados(self, id):
        record = self.store.find(ModelsMyvindulaRecados, ModelsMyvindulaRecados.id==id).one()
        self.store.remove(record)
        self.store.flush()
