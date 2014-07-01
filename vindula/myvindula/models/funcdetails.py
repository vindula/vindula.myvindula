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
        self.fields = ModelsConfgMyvindula().get_configurationAll()
        self.fields_private = self.fields.find(ativo_onlyuser=True)
        
        redis_conn = get_redis_connection()
        key = 'vindula:user-profile:%s' % username
        if redis_conn.hmget(key,'username')[0] != None:
            for field in redis_conn.hkeys(key):
                setattr(self,field,redis_conn.hmget(key,field)[0])
            del(redis_conn)
        else:
            if  self.fields.count() > 0:
                user_data = ModelsDadosFuncdetails().get_DadosFuncdetails_byInstance(self.username)

                for field in self.fields:

                    value = user_data.get(field.name)

                    if field.type == 'BooleanField':
                        if value == 'on':
                            value = True
                        else:
                            value = False

                    setattr(self, field.name,value)
                    continue
                    

        #TODO: Verificar pq isso esta acontecendo
        if not isinstance(self.username,unicode) and not isinstance(self.username,str):
            self.username = self.username.username
        

    def get(self,attribute,default=''):
        valor = getattr(self, attribute, default)
        if valor:
            return valor

        return  default

    def getImageIcone(self):
        url_foto_user = UtilMyvindula().getURLFotoUser(username=self.username,with_root=False)
        return url_foto_user

    def getUrlPerfil(self):
        return '/myvindulalistuser?user=%s' %(self.username)

    def getContato(self):
        info = '%s<br />' % (self.get('email',''))
        show_phone = self.get('show_phone', 'off')
        ramal = self.get('ramal', '')
        
        if ramal:
            info += ramal
        
        if self.get('phone_number', False) and show_phone == 'on':
            if ramal:
                info += ' | '
            info += self.get('phone_number', '') + '<br />'
        
        return info

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
    
    def is_deleted(self):
        username = self.username
        if username and isinstance(username, str):
            username = self.username.decode('utf-8')
            
        data = ModelsDadosFuncdetails().store.find(ModelsDadosFuncdetails, 
                                                   ModelsDadosFuncdetails.deleted==True,
                                                   ModelsDadosFuncdetails.username==self.username.decode('utf-8'))
        if data.count() > 0:
            return True
        else:
            return False

    @staticmethod
    def get_AllFuncFakeList(filter=None):
        L_username = []
        data = ModelsDadosFuncdetails().store.find(ModelsDadosFuncdetails)
        if filter:
            data = data.find(ModelsDadosFuncdetails.value.like('%'+filter+'%',case_sensitive=False))
        return range(data.count())

    @staticmethod
    def get_AllFuncUsernameList(filter=None,b_size=None,b_start=None,sorted_by=por_name,reverse=False,search_all_fields=True):
        #Nao usar o b_size, b_start
        #TODO: Consertar a forma que esta sendo ordenada a lista
        #TODO: Melhorar, ainda nao está bom, tempo melhorado de 11 para 2 sec
        key = generate_cache_key(domain='FuncDetails:get_AllFuncUsernameList', 
                                 filter=filter,
                                 b_size=b_size,
                                 b_start=b_start,
                                 sorted_by=str(sorted_by),
                                 search_all_fields=str(search_all_fields))
        
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
                
                data = []
                
                if search_all_fields:
                    data = ModelsDadosFuncdetails().store.find(ModelsDadosFuncdetails, 
                                                               ModelsDadosFuncdetails.deleted==False,
                                                               ModelsDadosFuncdetails.value.like('%'+filter+'%',case_sensitive=False))
                else:
                    #Faz a busca só pelos campos de NOME, EMAIL E APELIDO!
                    fields = ModelsConfgMyvindula().store.find(ModelsConfgMyvindula, 
                                                               ModelsConfgMyvindula.deleted==False,
                                                               ModelsConfgMyvindula.name.is_in([u'nickname', u'name', u'email']))
                    id_fields = []
                    for field in fields:
                        id_fields.append(field.id) 
                    if id_fields:
                        data = ModelsDadosFuncdetails().store.find(ModelsDadosFuncdetails, 
                                                                   ModelsDadosFuncdetails.deleted==False,
                                                                   ModelsDadosFuncdetails.field_id.is_in(id_fields),
                                                                   ModelsDadosFuncdetails.value.like('%'+filter+'%',case_sensitive=False))
                if data and data.count() > 0:
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
            
            #O reverse é utilizado para quando se trata de um campo de DATA
            L_username  = [i.username for i in sorted(L_retorno, key=sorted_by, reverse=reverse)]
            set_redis_cache(key,'FuncDetails:get_AllFuncUsernameList:keys',L_username,1800)
        
        return L_username

    @staticmethod
    def get_AllFuncDetails(filter=None, b_size=None, b_start=None, search_all_fields=True):
        """Retorna todos os usuarios e seus atributos
        :param filter: Adiciona um filtro na busca dos usuarios
        :param b_size: Passa o tamanho da lista para retornar (usado para paginação)
        :param b_start: Passa de onde vai continuar a paginar (usado para paginação)
        :param search_all_fields: Variável que define se o filtro vai ser aplicado a todos os campos do perfil ou apenas para nome, apelido e email
        """
        
        L_retorno = []
        L_username = FuncDetails.get_AllFuncUsernameList(filter=filter, b_size=b_size, b_start=b_start, search_all_fields=search_all_fields)
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
                                                                ModelsConfgMyvindula.name.is_in([u'name', u'nickname']),
                                                                ModelsDadosFuncdetails.field_id==ModelsConfgMyvindula.id,
                                                                ModelsDadosFuncdetails.deleted==False,
                                                                Or(*expression_name),)
            
        if (data and data.count() > 0) or (data_username and data_username.count() > 0):
            L_username_aux = []
            L_username_aux2 = []
            
            for item in data:
                if not item.username in L_username_aux:
                    L_username_aux.append(item.username)
            
            for item in data_username:
                if not item.username in L_username_aux2:
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

        key = generate_cache_key('FuncDetails:get_FuncDetailsByField',
                                 L_retorno=str(L_username),
                                 fields=str(fields))
        sorted_user_list = get_redis_cache(key)
        if not sorted_user_list:
            for user in L_username:
                L_retorno.append(FuncDetails(user))
            
            sorted_user_list = sorted(L_retorno, key=por_name)
            try:
                set_redis_cache(key,'FuncDetails:get_FuncDetailsByField:keys',sorted_user_list,600)
            except:
                sorted_user_list = [i.username for i in L_retorno]
                set_redis_cache(key,'FuncDetails:get_FuncDetailsByField:keys',sorted_user_list,600)

        return sorted_user_list

    @staticmethod
    def get_FuncBirthdays(date_start, date_end ):
        key = generate_cache_key('FuncDetails:get_FuncBirthdays',date_start=str(date_start),date_end=str(date_end))
        L = get_redis_cache(key)
        if not L:  
            L = []
            data = ModelsDadosFuncdetails().store.find(ModelsDadosFuncdetails, 
                                                       ModelsConfgMyvindula.name==u'date_birth',
                                                       ModelsDadosFuncdetails.field_id==ModelsConfgMyvindula.id,
                                                       ModelsDadosFuncdetails.value != u'',
                                                       ModelsDadosFuncdetails.deleted==False,)

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
                sorted_user_list = []
                result = []
                for user in L:
                    profile = FuncDetails(user.username)
                    if not profile.get('hide_birthday') or profile.get('hide_birthday') == 'off':
                        UO = profile.get_unidadeprincipal()
                        if UO:
                            UO = UO.UID()
                        else:UO = ''
                        sorted_user_list.append({'username':user.username,'UO':UO})
                        result.append(profile)
                set_redis_cache(key,'FuncDetails:get_FuncBirthdays:keys',sorted_user_list,7200)                
                return result
            else:
                return []
        return L