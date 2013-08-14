# -*- coding: utf-8 -*-

from storm.locals import Select
from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula

from vindula.myvindula.tools.utils import UtilMyvindula
from plone.app.uuid.utils import uuidToObject
from datetime import datetime, date
from vindula.myvindula.cache import *

from storm.expr import Or, And

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

        redis_conn = get_redis_connection()
        key = 'vindula:user-profile:%s' % username
        if redis_conn.hmget(key,'username')[0] != None:
            for field in redis_conn.hkeys(key):
                setattr(self,field,redis_conn.hmget(key,field)[0])
            del(redis_conn)
        else:
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
        except:
            try:
                valor = '["%s"]' % self.get('unidadeprincipal')
                list_ou =  eval(valor)
            except: list_ou = ['']
        
        OU = uuidToObject(list_ou[0])
#        OU = UtilMyvindula().lookupObject(list_ou[0])
        
        if OU:
            return OU

    def get_sigla_unidadeprincipal(self):
        structure = self.get_unidadeprincipal()
        sigla = ''
        if structure:
            sigla = structure.getSiglaOrTitle()
        return sigla

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
    def get_AllFuncFakeList(filter=None):
        L_username = []
        data = ModelsDadosFuncdetails().store.find(ModelsDadosFuncdetails)
        if filter:
            data = data.find(ModelsDadosFuncdetails.value.like('%'+filter+'%',case_sensitive=False))
        return range(data.count())

    @staticmethod
    def get_AllFuncUsernameList(filter=None,b_size=None,b_start=None,sorted_by=por_name):
        #Nao usar o b_size, b_start
        #TODO: Consertar a forma que esta sendo ordenada a lista
        #TODO: Melhorar, ainda nao está bom, tempo melhorado de 11 para 2 sec
        key = generate_cache_key(domain='FuncDetails:get_AllFuncUsernameList',filter=filter,b_size=b_size,b_start=b_start,sorted_by=str(sorted_by))
        L_username = get_redis_cache(key)
        if not L_username:
            L_username = []
            L_retorno = []
            if b_size != None and b_start != None:
                b_start = int(b_start)
                b_size = b_start + int(b_size)
            else:
                b_start = None
                b_size = None
            
            if filter:
                #Ajustando filtro para o caso de busca
                #por mais de uma palavra Ex: '%palavra1%palavra2%'
                filter = filter.split(' ')
                filter = '%'.join(filter)
                data = ModelsDadosFuncdetails().store.find(ModelsDadosFuncdetails, 
                                                           ModelsDadosFuncdetails.deleted==False,
                                                           ModelsDadosFuncdetails.value.like('%'+filter+'%',case_sensitive=False))
                if data.count() > 0:
                    for item in data:
                        if not item.username in L_username:
                            L_username.append(item.username)
            else:
                #Pegando os usuarios com distinct
                select = Select(ModelsDadosFuncdetails.username,
                                ModelsDadosFuncdetails.deleted==False,
                                distinct=True)
                data = ModelsDadosFuncdetails().store.execute(select)
                for item in data:
                    L_username.append(item[0])

            
            for user in L_username[b_start:b_size]:
                L_retorno.append(FuncDetails(user))
            
            L_username  = [i.username for i in sorted(L_retorno, key=sorted_by)]
            set_redis_cache(key,'FuncDetails:get_AllFuncUsernameList:keys',L_username,600)
        
        return L_username

    @staticmethod
    def get_AllFuncDetails(filter=None,b_size=None,b_start=None):
        L_retorno = []
        L_username = FuncDetails.get_AllFuncUsernameList(filter=filter,b_size=b_size,b_start=b_start)
        for user in L_username[b_start:b_size]:
            L_retorno.append(FuncDetails(user))

        return L_retorno

    @staticmethod
    def get_FuncDetailsByField(fields={}):
        L_username = []
        L_retorno = []
        
        expressions = []
        expression_name = []
        campos = []
        
        data = []
        data_username = []
        
        username_term = ''
        
        for item in fields.items():
            field, value = item[0], item[1]
            if value:
                if field == 'name':
                    value = unicode(value, 'utf-8')
                    username_term = value
                    expression_name += [ModelsDadosFuncdetails.value.like(value,case_sensitive=False)]
                    expression_name += [ModelsDadosFuncdetails.username.like(value,case_sensitive=False)]
                else:
                    if isinstance(value, list):
                        for val in value:
                            expressions += [ModelsDadosFuncdetails.value.like(unicode(val, 'utf-8'),case_sensitive=False)]
                    else:
                        expressions += [ModelsDadosFuncdetails.value.like(unicode(value, 'utf-8'),case_sensitive=False)]
                    campos += [unicode(field, 'utf-8')]
        
        if campos and expressions:
            data = ModelsDadosFuncdetails().store.find(ModelsDadosFuncdetails,
                                                       ModelsConfgMyvindula.name.is_in(campos), 
                                                       ModelsDadosFuncdetails.field_id==ModelsConfgMyvindula.id,
                                                       ModelsDadosFuncdetails.deleted==False,
                                                       Or(*expressions),)

        
        
        
        if expression_name:
            data_username = ModelsDadosFuncdetails().store.find(ModelsDadosFuncdetails,
                                                       ModelsConfgMyvindula.name==u'name',
                                                       ModelsDadosFuncdetails.field_id==ModelsConfgMyvindula.id,
                                                       ModelsDadosFuncdetails.deleted==False,
                                                       Or(*expression_name),)
            
        if (data and data.count() > 0) or (data_username and data_username.count() > 0):
            L_username_aux = []
            L_username_aux2 = []
            
            for item in data:
                if not item.username in L_username:
                    L_username_aux.append(item.username)
                    
            for item in data_username:
                if not item.username in L_username:
                    L_username_aux2.append(item.username)
                    
            #verifica se a busca foi feita tanto por nome quando pelos outros filtros
            if expressions and expression_name:
                if L_username_aux and L_username_aux2:
                    for i in L_username_aux:
                        if (i in L_username_aux2) and (i not in L_username):
                            L_username.append(i)
            #verifica se a busca foi feita apenas por filtro
            elif expressions:
                L_username = L_username_aux
            #verifica se a busca foi feita apenas por nome e username
            else:
                L_username = L_username_aux2
                
        else:
            #Pegando os usuarios com distinct
            select = Select(ModelsDadosFuncdetails.username,
                            ModelsDadosFuncdetails.deleted==False,
                            distinct=True)
            
            data = ModelsDadosFuncdetails().store.execute(select)
            for item in data:
                L_username.append(item[0])

        key = generate_cache_key('FuncDetails:get_FuncDetailsByField::',str(L_retorno))
        sorted_user_list = get_redis_cache(key)
        if not sorted_user_list:
            for user in L_username:
                L_retorno.append(FuncDetails(user))
            
            sorted_user_list = sorted(L_retorno, key=por_name)
            set_redis_cache(key,'FuncDetails:get_FuncDetailsByField:keys',sorted_user_list,600)

        return sorted_user_list

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
