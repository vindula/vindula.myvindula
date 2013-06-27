# -*- coding: utf-8 -*-

from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula

from vindula.myvindula.tools.utils import UtilMyvindula
from datetime import datetime, date

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
        valor = getattr(self, attribute, default)
        if valor:
            return valor

        return  default


    def getImageIcone(self):
        return '/vindula-api/myvindula/user-picture/photograph/%s/True' %(self.username)

    def getUrlPerfil(self):
        return '/myvindulalistuser?user=%s' %(self.username)


    def getContato(self):
        return '%s<br />%s<br />%s'%(self.get('email',''),
                                     self.get('phone_number',''),
                                     self.get('cell_phone',''))

    def get_unidadeprincipal(self):

        try:
            list_ou = eval(self.get('unidadeprincipal', '[" "]'))
        except SyntaxError:
            try:
                valor = '["%s"]' % self.get('unidadeprincipal')
                list_ou =  eval(valor)
            except: list_ou = ['']

        OU = UtilMyvindula().lookupObject(list_ou[0])
        if OU:
            return {'title':OU.getSiglaunidade() or OU.Title(),
                    'url': OU.absolute_url(),
                    'obj': OU}
        else:
            return {}

    def get_department(self):
        OUs_uid = eval(self.get('vin_myvindula_department') or '[]')
        result = []
        for OU_uid in OUs_uid:
            OU = UtilMyvindula().lookupObject(OU_uid)
            if OU:
                result.append({'title': OU.getSiglaunidade() or OU.Title(),
                                'url' : OU.absolute_url(),
                                'obj': OU })

        return result


    @staticmethod
    def get_AllFuncDetails(filter=None):
        #TODO: Melhorar, colocar o distinct do storm
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



    @staticmethod
    def get_FuncBirthdays(date_start, date_end ):
        L = []
        data = ModelsDadosFuncdetails().store.find(ModelsDadosFuncdetails, ModelsConfgMyvindula.name==u'date_birth',
                                                                           ModelsDadosFuncdetails.field_id==ModelsConfgMyvindula.id)

        for item in data:
            if item.value:

                try:
                    data_usuario = date(date.today().year,
                                        int(datetime.strptime(item.value, "%d/%m/%Y").month),
                                        int(datetime.strptime(item.value, "%d/%m/%Y").day))

                    if data_usuario >= date_start and\
                       data_usuario <= date_end:
                        L.append(item)

                except ValueError:
                    pass

        L = sorted(L, key=lambda row: datetime.strptime(row.value, "%d/%m/%Y").day)
        L = sorted(L, key=lambda row: datetime.strptime(row.value, "%d/%m/%Y").month)

        if L:
            result = [FuncDetails(i.username) for i in L]
            return result
        else:
            return []
