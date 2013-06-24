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