# coding: utf-8

from storm.locals import *
from storm.expr import Desc
from storm.locals import Store

from vindula.myvindula.user import BaseStore



class ModelsFuncHolerite02(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_holerite02'
    
    id = Int(primary=True)
    empresa = Unicode()
    cnpj_empresa = Unicode()
    competencia = Unicode()
    matricula = Unicode()
    nome = Unicode()
    data_admissao = Unicode()    
    cargo= Unicode()
    setor= Unicode()
    carteira_trabalho = Unicode()
    secao = Unicode()
    dep_ir = Unicode()
    dep_sf = Unicode()
    cpf = Unicode()
    indentidade = Unicode()
    pis = Unicode()
    cod_pagamento = Unicode() 
    banco_pag = Unicode()
    agencia = Unicode()
    conta_corrente = Unicode()
    date_creation = DateTime()
    base_Inss = Unicode()
    base_fgts = Unicode()
    base_irrf = Unicode()
    salario_base = Unicode()
    salario_contribuicao = Unicode()
    total_proventos = Unicode()
    total_desconto = Unicode()
    fgts_mes = Unicode()
    valor_liquido = Unicode()
    observacao = Unicode()
    
        
    descricao = Reference(id, "ModelsFuncHoleriteDescricao02.vin_myvindula_holerite02_id")
       
    def set_FuncHolerite(self, **kwargs):
        # adicionando...
        funcHolerite = ModelsFuncHolerite02(**kwargs)
        self.store.add(funcHolerite)
        self.store.flush()
        
        return funcHolerite.id       
    
    def get_FuncHolerites_byCPF(self, cpf):
        #Checando se atributo é None, se for já não retorna nenhum holerite
        #Por seguranca retorna None quando CPF = None, pois na importacao, 
        #pode ser improtado algum holerite com cpf vazio 
        if cpf == None: return None
        data = self.store.find(ModelsFuncHolerite02, ModelsFuncHolerite02.cpf==cpf).order_by(ModelsFuncHolerite02.competencia)
        if data.count() > 0:
            return data
        else:
            return None    
    
    def get_FuncHolerites_byCPFAndID(self, cpf,id):
        #Checagem de seguranca
        if cpf == None: return None
        
        data = self.store.find(ModelsFuncHolerite02, ModelsFuncHolerite02.cpf==cpf, ModelsFuncHolerite02.id==id).one()
        if data:
            return data
        else:
            return None    

    def get_FuncHolerites_byData(self, data):
        data = self.store.find(ModelsFuncHolerite02, ModelsFuncHolerite02.date_creation==data)
        if data.count() > 1:
            return data
        else:
            return None        
    
    def get_FuncHolerites_Import(self):        
        result = self.store.execute("SELECT count(*),DATE_FORMAT(date_creation,'%d/%m/%Y %H:%i') as data,\
                                    date_creation, empresa FROM vin_myvindula_holerite02 group by data,empresa")
        L = []        
        for i in result:
            L.append({'contador':i[0],
                      'date_creation':i[1],
                      'date_excluir':i[2], 
                      'empresa':i[3],                      
                      })        
        return L    

    def del_HoleritesLote(self, date,empresa):
        #import pdb;pdb.set_trace()
        results = self.store.find(ModelsFuncHolerite02, ModelsFuncHolerite02.date_creation>=date,
                                                        ModelsFuncHolerite02.date_creation<=date.replace(second=59),
                                                        ModelsFuncHolerite02.empresa==empresa)
        if results:
            for result in results:
                ModelsFuncHoleriteDescricao02().del_HoleritesDescricao(result.id)
                self.store.remove(result)
                self.store.flush()        
    
    
    
class ModelsFuncHoleriteDescricao02(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_descricao_holerite02'
    
    id = Int(primary=True)    
    codigo = Unicode()
    descricao = Unicode()
    valor = Unicode()
    status = Unicode()
    referencial = Unicode()
    vin_myvindula_holerite02_id = Int()
    
    
    def set_FuncHoleriteDescricao(self, **kwargs):
        # adicionando...
        funcHoleriteDescricao = ModelsFuncHoleriteDescricao02(**kwargs)
        self.store.add(funcHoleriteDescricao)
        self.store.flush()          
    
    def get_FuncHoleriteDescricoes_byid(self, id):
        data = self.store.find(ModelsFuncHoleriteDescricao02, ModelsFuncHoleriteDescricao02.vin_myvindula_holerite02_id==id)
        if data.count() > 0:
            return data
        else:
            return None        
    
    def del_HoleritesDescricao(self, holerite_id):
        results = self.store.find(ModelsFuncHoleriteDescricao02, ModelsFuncHoleriteDescricao02.vin_myvindula_holerite02_id==holerite_id)
        if results:
            for result in results:
                self.store.remove(result)
                self.store.flush()
        