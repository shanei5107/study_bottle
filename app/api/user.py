# -*- coding: utf-8 -*-

from bottle import route
from core.cache.redis_pool_helper import redisCache as cache

from core.rsp import ApiResponse


@route('/user/action', method=['POST', 'GET', 'OPTIONS'])
def index():
    return ApiResponse(msg='我是用户接口')


@route('/user/cache', method=['POST', 'GET', 'OPTIONS'])
def testCache():
    if not cache.get('test'):
        print(cache.set('test', 'Simple Test'))
        return ApiResponse(msg='写缓存，返回')
    else:
        print(cache.get('test'))
        return ApiResponse(msg='读缓存，返回')
