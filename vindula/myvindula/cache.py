# -*- coding: utf-8 -*-
import redis
import json
#from redis_completion import RedisEngine

#TODO: colocar essa configuração no painel de controle do plone.
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 2
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def get_redis_connection(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB):
    return redis.StrictRedis(connection_pool=pool)

def set_redis_cache(key,key_set,value,expire=600):
	pipe = get_redis_connection().pipeline()
	pipe.setex(key, expire, json.dumps(value))
	pipe.sadd(key_set, key)
	pipe.execute()

def get_redis_cache(key):
	data = get_redis_connection().get(key)
	if data:
		return json.loads(data)
	else: 
		return None
	