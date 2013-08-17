# -*- coding: utf-8 -*-

import redis
import memcache


class Cache(object):

    hostname = ""
    server   = ""
    def __init__(self, hostname="127.0.0.1", port="11211"):
        self.hostname = "%s:%s" % (hostname, port)
        self.server   = memcache.Client([self.hostname])

    def set(self, key, value, expiry=3600):
        """
        This method is used to set a new value
        in the memcache server.
        """
        self.server.set(key, value, expiry)

    def get(self, key):
        """
        This method is used to retrieve a value
        from the memcache server
        """
        return self.server.get(key)

    def delete(self, key):
        """
        This method is used to delete a value from the
        memcached server. Lazy delete
        """
        self.server.delete(key)



#from redis_completion import RedisEngine

#TODO: colocar essa configuração no painel de controle do plone.
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 2

def get_redis_connection(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB):
    return redis.StrictRedis(host=host,
                             port=port,
                             db=db)

