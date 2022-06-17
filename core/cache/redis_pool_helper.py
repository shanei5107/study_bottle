# -*- coding: utf-8 -*-

import redis


class RedisDbConfig:
    HOST = '127.0.0.1'
    PORT = 6379
    DBID = 1
    PASSWORD = ''


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


def operator_status(func):

    def gen_status(*args, **kwargs):
        error, result = None, None
        try:
            pass
        except Exception as e:
            error = str(e)
        return {'result': result, 'error': error}

    return gen_status


# 使用单例模式来创建redis实例
@Singleton
class RedisCache(object):

    def __init__(self, _redis=None):
        if _redis:
            pool = redis.ConnectionPool(host=_redis.get('host', ''),
                                        port=_redis.get('port', ''),
                                        db=_redis.get('db', ''),
                                        password=_redis.get('password', ''),
                                        socket_timeout=1,
                                        socket_connect_timeout=1,
                                        decode_responses=True)
            self._connection = redis.Redis(connection_pool=pool)

    def init_app(self, _redis):
        if _redis:
            pool = redis.ConnectionPool(host=_redis.get('host', ''),
                                        port=_redis.get('port', ''),
                                        db=_redis.get('db', ''),
                                        password=_redis.get('password', ''),
                                        socket_timeout=1,
                                        socket_connect_timeout=1,
                                        decode_responses=True)
        else:
            pool = redis.ConnectionPool(host=RedisDbConfig.HOST,
                                        port=RedisDbConfig.PORT,
                                        db=RedisDbConfig.DBID,
                                        password=RedisDbConfig.PASSWORD,
                                        socket_timeout=1,
                                        socket_connect_timeout=1,
                                        decode_responses=True)
        self._connection = redis.Redis(connection_pool=pool)

    def get_connection(self, _redis=None):
        if _redis:
            pool = redis.ConnectionPool(host=_redis.get('host', ''),
                                        port=_redis.get('port', ''),
                                        db=_redis.get('db', ''),
                                        password=_redis.get('password', ''),
                                        socket_timeout=1,
                                        socket_connect_timeout=1,
                                        decode_responses=True)
        else:
            pool = redis.ConnectionPool(host=RedisDbConfig.HOST,
                                        port=RedisDbConfig.PORT,
                                        db=RedisDbConfig.DBID,
                                        password=RedisDbConfig.PASSWORD,
                                        socket_timeout=1,
                                        socket_connect_timeout=1,
                                        decode_responses=True)
        self._connection = redis.Redis(connection_pool=pool)

        return self._connection

    def set(self, key, value, ex=None):
        return self._connection.set(key, value, ex=ex)

    def get(self, key):
        return self._connection.get(key)

    def delkey(self, key):
        return self._connection.delete(key)

    def setnx(self, key, value):
        return self._connection.setnx(key, value)

    def setex(self, key, value, time):
        return self._connection.setex(name=key, value=value, time=time)

    def psetex(self, key, value, time_ms):
        return self._connection.psetex(name=key, value=value, time_ms=time_ms)

    def mset(self, *args, **kwargs):
        return self._connection.mset(*args, **kwargs)

    def mget(self, *args, **kwargs):
        return self._connection.mget(*args, **kwargs)

    def getset(self, key, value):
        return self._connection.getset(name=key, value=value)

    def getrange(self, key, value):
        pass

    def incr(self, key, amount=1):
        return self._connection.incr(name=key, amount=amount)

    def decr(self, key, amount=1):
        return self._connection.decr(name=key, amount=amount)


# 创建单列对象
redisCache = RedisCache()