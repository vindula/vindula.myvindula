# -*- coding: utf-8 -*-

##
## ARQUIVO DE CONFIGURAÇÃO DO VINDULA
##


REDIS_HOST = 'redis.vindula.infra'
REDIS_PORT = 6379
REDIS_DB = 2

HA_VINDULAPP_HOST ='ha.vindulapp.vindula.infra'
HA_VINDULAPP_PORT = '9001'



try:
    from custom_config import *
except ImportError:
    pass
