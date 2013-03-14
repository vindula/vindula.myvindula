# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore
from vindula.myvindula.models.department import ModelsDepartment


from vindula.myvindula.tools.utils import UtilMyvindula

from datetime import datetime, date


class ModelsDadosFuncdetails(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_dados_funcdetails'
    
    #Campos de edição
    id = Int(primary=True)
    date_creation = DateTime()
    
    valor = Unicode()
    vin_myvindula_confgfuncdetails_fields = Unicode()
    vin_myvindula_instance_id = Int()

    campo = Reference(vin_myvindula_confgfuncdetails_fields, "ModelsConfgMyvindula.fields")
    instance = Reference(vin_myvindula_instance_id, "ModelsInstanceFuncdetails.id")


    def set_DadosFuncdetails(self,**kwargs):
        # adicionando...
        dados = ModelsDadosFuncdetails(**kwargs)
        self.store.add(dados)
        self.store.flush()         

    
    def del_DadosFuncdetails(self,id_instance):
        results = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.vin_myvindula_instance_id==id_instance)
        if results.count() > 0:
            for result in results:
                self.store.remove(result)
                self.store.flush()   

    
    def del_DadosFuncdetails_by_field(self,campo):
        results = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.vin_myvindula_confgfuncdetails_fields==campo)
        if results.count() > 0:
            for result in results:
               self.store.remove(result)
               self.store.flush()          
    
    
    def get_DadosFuncdetails_byInstance(self,id_instance):
        data = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.vin_myvindula_instance_id==id_instance)
        
        if data.count() > 0:
            return data
        else:
            return None
      
    def get_DadosFuncdetails_byInstanceAndField(self,id_instance,fields):
        data = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.vin_myvindula_instance_id==id_instance,
                                                       ModelsDadosFuncdetails.vin_myvindula_confgfuncdetails_fields==fields).one()
        
        if data:
            return data
        else:
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
                D['instance_user'] = ids
                D['username'] = dados[0].instance.username
            
                for campo in campos:
                    tmp = dados.find(vin_myvindula_confgfuncdetails_fields=tools.Convert_utf8(campo.fields)).one()
                    if tmp:
                        try:
                            data = tools.decodePickle(tmp.valor)
                        except:
                            data = tmp.valor
                
                        D[campo.fields] = data 
            
                L.append(D)
        return L
        
        
#Metodos de busca de usuario para o portal    
    def get_FuncBusca(self,department_id='',form_campos=[],filtro=False):
        from vindula.myvindula.models.instance_funcdetail import ModelsInstanceFuncdetails
        ids_instances = []
        
        if filtro:
            form_campos.append({'phone_number':'None'})
            
        
        origin = [ModelsDadosFuncdetails,
                  Join(ModelsInstanceFuncdetails, ModelsInstanceFuncdetails.id==ModelsDadosFuncdetails.vin_myvindula_instance_id)]
        if department_id:
            origin.append(Join(ModelsDepartment, ModelsDepartment.vin_myvindula_funcdetails_id==ModelsInstanceFuncdetails.username))
        
        for item in form_campos:
            busca = "self.store.using(*origin).find(ModelsDadosFuncdetails,"
            if item.values()[0]:
                
                if item.keys()[0] == 'phone_number':
                    busca += "ModelsDadosFuncdetails.vin_myvindula_confgfuncdetails_fields==u'phone_number',\
                             ModelsDadosFuncdetails.valor, "
                else:
                    busca += "ModelsDadosFuncdetails.vin_myvindula_confgfuncdetails_fields==u'"+item.keys()[0]+"',\
                             ModelsDadosFuncdetails.valor.like( '%' + '%'.join(u'"+item.values()[0]+"'.split(' ')) + '%' ),"
        
                if ids_instances:
                    busca += "ModelsDadosFuncdetails.vin_myvindula_instance_id.is_in(ids_instances),"
                    
                if department_id:
                    busca += "ModelsDepartment.uid_plone==department_id,"
                
                busca += ')'
                
                #import pdb;pdb.set_trace()
                data = eval(busca)
                
                #if data.count()>0:
                ids_instances = []   
                for i in data:
                    id = i.vin_myvindula_instance_id
                    if not id in ids_instances:
                        ids_instances.append(i.vin_myvindula_instance_id)
        
        
        
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
        
        data = self.store.find(ModelsDadosFuncdetails, ModelsDadosFuncdetails.vin_myvindula_confgfuncdetails_fields==u'date_birth')
        for item in data:                                           

            data_usuario = date(date.today().year,
                        int(datetime.strptime(item.valor, "%d/%m/%Y").month),                        
                        int(datetime.strptime(item.valor, "%d/%m/%Y").day))
            
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
        
        L = sorted(L, key=lambda row: datetime.strptime(row.valor, "%d/%m/%Y").day)      
        L = sorted(L, key=lambda row: datetime.strptime(row.valor, "%d/%m/%Y").month)
            
        if L:
            result = [i.vin_myvindula_instance_id for i in L]        
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
