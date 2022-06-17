# -*- coding: utf-8 -*-

from bottle import route

from core.rsp import ApiResponse


@route('/user/action', method=['POST', 'GET', 'OPTIONS'])
def index():
    return ApiResponse(msg='我是用户接口')
