# -*- coding: utf-8 -*-
import redis
import json
import hashlib
import pickle
#from redis_completion import RedisEngine

#TODO: colocar essa configuração no painel de controle do plone.
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 2
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def get_redis_connection(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB):
    return redis.StrictRedis(connection_pool=pool)

def set_redis_cache(key,key_set,value,expire=600):
	try:
		value = json.dumps(value)
	except:
		value = pickle.dumps(value)
		
	pipe = get_redis_connection().pipeline()
	pipe.setex(key, expire, value)
	pipe.sadd(key_set, key)
	pipe.execute()

def get_redis_cache(key):
	data = get_redis_connection().get(key)
	if data:
		try:
			return json.loads(data)
		except:
			return pickle.loads(data)
	else: 
		return None

def generate_cache_key(domain,**kwargs):
	key = hashlib.md5(':'.join([kwargs[i] for i in kwargs.keys() if kwargs[i]!=None])).hexdigest()
	key = '%s::%s' % (domain,key)
	print 'Cached Key:', key
	return key

