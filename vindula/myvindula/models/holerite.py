# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select

from vindula.myvindula.models.base import BaseStore
from vindula.myvindula.models.descricao_holerite import ModelsFuncHoleriteDescricao

class ModelsFuncHolerite(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_holerite'
    
    id = Int(primary=True)
    nome = Unicode()
    cpf = Unicode()
    matricula = Unicode() 
    cargo= Unicode()
    cod_cargo = Unicode()
    date_creation = DateTime()
    competencia = Unicode()
    empresa = Unicode()
    cod_empresa = Unicode()
    endereco_empresa = Unicode()
    cidade_empresa = Unicode()
    estado_empresa = Unicode()
    cnpj_empresa = Unicode()
    total_vencimento = Unicode()
    total_desconto = Unicode()
    observacao = Unicode()
    valor_liquido = Unicode()
    salario_base = Unicode()
    base_Inss = Unicode()
    base_fgts = Unicode()
    fgts_mes = Unicode()
    base_irrf = Unicode()
    
    descricao = Reference(id, "ModelsFuncHoleriteDescricao.vin_myvindula_holerite_id")
       
    def set_FuncHolerite(self, **kwargs):
        # adicionando...
        funcHolerite = ModelsFuncHolerite(**kwargs)
        self.store.add(funcHolerite)
        self.store.flush()
        
        return funcHolerite.id       
    
    def get_FuncHolerites_byCPF(self, cpf):
        #Checando se atributo é None, se for já não retorna nenhum holerite
        #Por seguranca retorna None quando CPF = None, pois na importacao, 
        #pode ser improtado algum holerite com cpf vazio 
        if cpf == None: return None
        data = self.store.find(ModelsFuncHolerite, ModelsFuncHolerite.cpf==cpf).order_by(ModelsFuncHolerite.competencia)
        if data.count() > 0:
            return data
        else:
            return None    
    
    def get_FuncHolerites_byCPFAndID(self, cpf,id):
        #Checagem de seguranca
        if cpf == None: return None
        
        data = self.store.find(ModelsFuncHolerite, ModelsFuncHolerite.cpf==cpf, ModelsFuncHolerite.id==id).one()
        if data:
            return data
        else:
            return None    

    def get_FuncHolerites_byData(self, data):
        data = self.store.find(ModelsFuncHolerite, ModelsFuncHolerite.date_creation==data)
        if data.count() > 1:
            return data
        else:
            return None        
    
    def get_FuncHolerites_Import(self):        
        result = self.store.execute("SELECT count(*),DATE_FORMAT(date_creation,'%d/%m/%Y %H:%i') as data,\
                                    date_creation, empresa FROM vin_myvindula_holerite group by data,empresa")
        L = []        
        for i in result:
            L.append({'contador':i[0],
                      'date_creation':i[1],
                      'date_excluir':i[2], 
                      'empresa':i[3],                      
                      })        
        return L    

    def del_HoleritesLote(self, date,empresa):
        results = self.store.find(ModelsFuncHolerite, ModelsFuncHolerite.date_creation>=date,
                                                      ModelsFuncHolerite.date_creation<=date.replace(second=59),
                                                      ModelsFuncHolerite.empresa==empresa)
        if results:
            for result in results:
                ModelsFuncHoleriteDescricao().del_HoleritesDescricao(result.id)
                self.store.remove(result)
                self.store.flush()  