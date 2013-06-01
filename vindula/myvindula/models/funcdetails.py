# -*- coding: utf-8 -*-

from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula

from vindula.myvindula.tools.utils import UtilMyvindula

def por_name(item):
    return item.get('name','')

class FuncDetails(object):
    '''
        Objeto dos dados do usuario
    '''
    username = None
    fields = []

    def __unicode__(self,):
        return 'Objeto do Usuario - %s' % (self.username)

    def __init__(self, username, *args, **kwargs):
        self.username = username

        self.fields = ModelsConfgMyvindula().get_configurationAll()
        if  self.fields.count() > 0:
            user_data = ModelsDadosFuncdetails().get_DadosFuncdetails_byInstance(self.username)

            for field in self.fields:
                value = user_data.get(field.name)
                setattr(self, field.name,value)


    def get(self,attribute,default=''):
        return getattr(self, attribute, default)


    def getImageIcone(self):
        return '/vindula-api/myvindula/user-picture/photograph/%s/True' %(self.username)

    def getContato(self):
        return '%s<br />%s<br />%s'%(self.get('email',''),
                                     self.get('phone_number',''),
                                     self.get('cell_phone',''))

    def get_unidadeprincipal(self):
        OU = UtilMyvindula().lookupObject(self.get('unidadeprincipal'))
        if OU:
            return OU.getSiglaunidade() or OU.Title()
        else:
            return ''


    @staticmethod
    def get_AllFuncDetails(filter=None):
        L_username = []
        L_retorno = []
        data = ModelsDadosFuncdetails().store.find(ModelsDadosFuncdetails)
        if filter:
            data = data.find(ModelsDadosFuncdetails.value.like('%'+filter+'%'))

        if data.count() > 0:
            for item in data:
                if not item.username in L_username:
                    L_username.append(item.username)
                    L_retorno.append(FuncDetails(item.username))

        return sorted(L_retorno, key=por_name)