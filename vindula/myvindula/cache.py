# -*- coding: utf-8 -*-

import redis
#from redis_completion import RedisEngine

#TODO: colocar essa configuração no painel de controle do plone.
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 2

def get_redis_connection(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB):
    return redis.StrictRedis(host=host,
                             port=port,
                             db=db)

