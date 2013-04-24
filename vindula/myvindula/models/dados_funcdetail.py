# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore
from vindula.myvindula.models.department import ModelsDepartment
from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula

from vindula.myvindula.tools.utils import UtilMyvindula

from datetime import datetime, date
from hashlib import md5

class ModelsDadosFuncdetails(Storm, BaseStore):
    #__storm_table__ = 'vin_myvindula_dados_funcdetails'
    __storm_table__ = 'vinapp_myvindula_userschemadata'

    #Campos de edição
    id = Int(primary=True)
    hash = Unicode()
    username = Unicode()
    field_id = Int()
    value = Unicode()
    date_created = DateTime()
    date_modified = DateTime()

    #vin_myvindula_confgfuncdetails_fields = Unicode()
    #vin_myvindula_instance_id = Int()

    campo = Reference(field_id, "ModelsConfgMyvindula.id")
#    instance = Reference(vin_myvindula_instance_id, "ModelsInstanceFuncdetails.id")

    def createUserProfile(self,data):
        tool = UtilMyvindula()
        username = data.get(u'username')
        created = False
        #Removendo valor do dicionario para criar os valores
        data.pop(u'username')
        #Recebe o dicionario de dados do usuario e cria o perfil
        for field in data.keys():
            field_config = ModelsConfgMyvindula().get_configuration_By_fields(field)
            if field_config:
                field_id = field_config.id
            else:
                #Caso nao exista o field chamado, loga o erro e deixa passar
                tool.setLogger('info',"User schema field unkown: %s" % field)
                continue

            value = tool.Convert_utf8(data[field])

            str_data = datetime.now().strftime('%Y-%m-%d|%H:%M:%S')

            hash = md5('ModelsDadosFuncdetails'+str(username)+str(field_id)+str_data).hexdigest()

            value_object = ModelsDadosFuncdetails(**{'username':username,
                                                     'field_id':field_id,
                                                     'value':value,
                                                     'hash' : unicode(hash),
                                                     'date_created':datetime.now(),
                                                     'date_modified':datetime.now()})
            tool.setLogger('info',"User data stored: %s - %s - %s" % (username,
                                                                      field,
                                                                      value))
            self.store.add(value_object)
            created = True

        if created:
            self.store.flush()
            tool.setLogger('info',"User created on myvindula: %s" % username)

    def set_DadosFuncdetails(self,**kwargs):
        # adicionando...
        field_config = ModelsConfgMyvindula().get_configuration_By_fields(kwargs.get(u'field'))
        if field_config:
            kwargs.pop(u'field')

            str_data = datetime.now().strftime('%Y-%m-%d|%H:%M:%S')
            kwargs[u'field_id'] = field_config.id

            hash = md5('ModelsDadosFuncdetails'+str(kwargs.get('username',u''))+str(kwargs.get(u'field_id',u''))+str_data).hexdigest()
            kwargs[u'hash'] = unicode(hash)
            kwargs[u'date_created'] = datetime.now()
            kwargs[u'date_modified'] = datetime.now()

            dados = ModelsDadosFuncdetails(**kwargs)
            self.store.add(dados)
            self.store.flush()


    def del_DadosFuncdetails(self,id_instance):
        results = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.username==id_instance)
        if results.count() > 0:
            for result in results:
                self.store.remove(result)
                self.store.flush()


    def del_DadosFuncdetails_by_field(self,campo):
        results = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.field_id==campo)
        if results.count() > 0:
            for result in results:
               self.store.remove(result)
               self.store.flush()


    def get_DadosFuncdetails_byInstance(self,id_instance):
        data = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.username==id_instance)

        if data.count() > 0:
            return data
        else:
            return None

    def get_DadosFuncdetails_byInstanceAndField(self,username,field_id):
        data = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.username==username,
                                                       ModelsDadosFuncdetails.field_id==field_id).one()
        if data:
            return data

        return None

    def get_DadosFuncdetails_byInstanceAndFieldName(self,username,field):
        field_config = ModelsConfgMyvindula().get_configuration_By_fields(field)
        if field_config:
            field_id = field_config.id

            data = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.username==username,
                                                           ModelsDadosFuncdetails.field_id==field_id).one()
            if data:
                return data

        return None

    def geraDic_DadosUser(self,ids_instances):
        from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula
        tools = UtilMyvindula()
        L = []
        campos = ModelsConfgMyvindula().get_configurationAll()

        for ids in ids_instances:
            dados = self.get_DadosFuncdetails_byInstance(ids)

            D = {}
            if dados:

                # ToDo: Estas duas chaves estao legadas para o resto da aplicação
                D['instance_user'] = ids
                D['username'] = ids #dados[0].instance.username

                for campo in campos:
                    tmp = dados.find(field_id=campo.id).one()
                    if tmp:
                        try:
                            data = tools.decodePickle(tmp.value)
                        except:
                            data = tmp.value

                        D[campo.name] = data

                L.append(D)
        return L


    #Metodos de busca de usuario para o portal
    def get_FuncBusca(self,department_id='',form_campos=[],filtro=False):
        #from vindula.myvindula.models.instance_funcdetail import ModelsInstanceFuncdetails
        ids_instances = []

        if filtro:
            form_campos.append({'phone_number':'None'})


        origin = [ModelsDadosFuncdetails,
                  Join(ModelsConfgMyvindula, ModelsConfgMyvindula.id==ModelsDadosFuncdetails.field_id)]

        if department_id:
            origin.append(Join(ModelsDepartment, ModelsDepartment.vin_myvindula_funcdetails_id==ModelsDadosFuncdetails.username))

        for item in form_campos:
            busca = "self.store.using(*origin).find(ModelsDadosFuncdetails,"
            if item.values()[0]:

                if item.keys()[0] == 'phone_number':
                    busca += "ModelsConfgMyvindula.name==u'phone_number',\
                             ModelsDadosFuncdetails.value, "
                else:
                    busca += "ModelsConfgMyvindula.name==u'"+item.keys()[0]+"',\
                             ModelsDadosFuncdetails.value.like( '%' + '%'.join(u'"+item.values()[0]+"'.split(' ')) + '%' ),"

                if ids_instances:
                    busca += "ModelsDadosFuncdetails.username.is_in(ids_instances),"

                if department_id:
                    busca += "ModelsDepartment.uid_plone==department_id,"

                busca += ')'

                #import pdb;pdb.set_trace()
                data = eval(busca)

                #if data.count()>0:
                ids_instances = []
                for i in data:
                    id = i.username
                    if not id in ids_instances:
                        ids_instances.append(i.username)



#            import pdb;pdb.set_trace()
#            busca = "self.store.using(*origin).find(ModelsDadosFuncdetails,"
#            busca += "ModelsDadosFuncdetails.vin_myvindula_confgfuncdetails_fields==u'phone_number',\
#                     ModelsDadosFuncdetails.valor != u'',"
#
#            if ids_instances:
#                busca += "ModelsDadosFuncdetails.vin_myvindula_instance_id.is_in(ids_instances),"
#
#            if filtro:
#                 busca += "ModelsDadosFuncdetails.vin_myvindula_confgfuncdetails_fields==u'phone_number',\
#                            ModelsDadosFuncdetails.valor,"

#
#            if department_id:
#                busca += "ModelsDepartment.uid_plone==department_id,"
#
#            busca += ')'
#
#            data = eval(busca)
#
#            if data.count()>0:
#                ids_instances = []
#                for i in data:
#                    id = i.vin_myvindula_instance_id
#                    if not id in ids_instances:
#                        ids_instances.append(i.vin_myvindula_instance_id)

        #busca += ").order_by(ModelsFuncDetails.name)"

        return self.geraDic_DadosUser(ids_instances)

    def get_FuncBirthdays(self, date_start, date_end, filtro=''):

        L = []
        data = []

        field_config = ModelsConfgMyvindula().get_configuration_By_fields(u'date_birth')
        if field_config:
            data = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.field_id==field_config.id)

        for item in data:

            data_usuario = date(date.today().year,
                        int(datetime.strptime(item.value, "%d/%m/%Y").month),
                        int(datetime.strptime(item.value, "%d/%m/%Y").day))

            if filtro == 'proximo':
                if data_usuario >= date.today():
                    L.append(item)
            else:

                date_start = date(int(date_start.split('-')[0]),
                          int(date_start.split('-')[1]),
                          int(date_start.split('-')[2]))

                date_end = date(int(date_end.split('-')[0]),
                                int(date_end.split('-')[1]),
                                int(date_end.split('-')[2]))

                if data_usuario >= date_start and\
                   data_usuario <= date_end:
                    L.append(item)

        L = sorted(L, key=lambda row: datetime.strptime(row.value, "%d/%m/%Y").day)
        L = sorted(L, key=lambda row: datetime.strptime(row.value, "%d/%m/%Y").month)

        if L:
            result = [i.username for i in L]
            return self.geraDic_DadosUser(result)
        else:
            return None


#            sql = """SELECT vin_myvindula_instance_id FROM vin_myvindula_dados_funcdetails WHERE vin_myvindula_confgfuncdetails_fields='date_birth' and
#                     concat_ws('-',year(now()),month(STR_TO_DATE(valor,"%d/%m/%Y")),day(STR_TO_DATE(valor,"%d/%m/%Y"))) >= DATE(NOW()) ORDER BY MONTH(STR_TO_DATE(valor,"%d/%m/%Y"))
#                     ASC , DAY(STR_TO_DATE(valor,"%d/%m/%Y")) ASC;
#            """
#        else:
#            sql = '''
#                 SELECT vin_myvindula_instance_id FROM vin_myvindula_dados_funcdetails WHERE vin_myvindula_confgfuncdetails_fields='date_birth' and
#                 DATE_FORMAT(STR_TO_DATE(valor,"%d/%m/%Y"), "%m-%d") BETWEEN DATE_FORMAT('{0}', "%m-%d") AND DATE_FORMAT('{1}', "%m-%d")
#                '''.format(date_start,date_end)
#
#            if filtro == 'random':
#                sql += ' ORDER BY RAND();'
#
#            else:
#                sql +='ORDER BY MONTH(STR_TO_DATE(valor,"%d/%m/%Y")) ASC, DAY(STR_TO_DATE(valor,"%d/%m/%Y")) ASC;'
#
            #data = self.store.execute('SELECT * FROM vin_myvindula_funcdetails WHERE DATE_FORMAT(date_birth, "%m-%d") BETWEEN DATE_FORMAT("'+date_start+'", "%m-%d") AND DATE_FORMAT("'+date_end+'", "%m-%d") ORDER BY RAND();')
            #data = self.store.execute("SELECT * FROM vin_myvindula_funcdetails WHERE concat_ws('-',year(now()),month(date_birth),day(date_birth)) >= DATE(NOW()) ORDER BY MONTH(date_birth) ASC , DAY(date_birth) ASC;")

#        else:
#            data = self.store.execute('SELECT * FROM vin_myvindula_funcdetails WHERE DATE_FORMAT(date_birth, "%m-%d") BETWEEN DATE_FORMAT("'+date_start+'", "%m-%d") AND DATE_FORMAT("'+date_end+'", "%m-%d") ORDER BY MONTH(date_birth) ASC, DAY(date_birth) ASC;')

#        data = self.store.execute(sql)
#        if data.rowcount != 0:
#            result=[]
#            for obj in data.get_all():
#                result.append(obj[0])
#
#            return self.geraDic_DadosUser(result)
#        else:
#            return None
