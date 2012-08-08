# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.expr import Desc, Select


from vindula.myvindula.models.base import BaseStore



class ModelsFuncHoleriteDescricao(Storm, BaseStore):
    __storm_table__ = 'vin_myvindula_descricao_holerite'
    
    id = Int(primary=True)    
    codigo = Unicode()
    descricao = Unicode()
    ref = Unicode()
    vencimentos = Unicode()
    descontos = Unicode()
    vin_myvindula_holerite_id = Int()
    
    def set_FuncHoleriteDescricao(self, **kwargs):
        # adicionando...
        funcHoleriteDescricao = ModelsFuncHoleriteDescricao(**kwargs)
        self.store.add(funcHoleriteDescricao)
        self.store.flush()          
    
    def get_FuncHoleriteDescricoes_byid(self, id):
        data = self.store.find(ModelsFuncHoleriteDescricao, ModelsFuncHoleriteDescricao.vin_myvindula_holerite_id==id)
        if data.count() > 0:
            return data
        else:
            return None        
    
    def del_HoleritesDescricao(self, holerite_id):
        results = self.store.find(ModelsFuncHoleriteDescricao, ModelsFuncHoleriteDescricao.vin_myvindula_holerite_id==holerite_id)
        if results:
            for result in results:
                self.store.remove(result)
                self.store.flush()
        