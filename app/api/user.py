# -*- coding: utf-8 -*-

from bottle import route


@route('/user/action', method=['POST', 'GET', 'OPTIONS'])
def index():
    return '我是用户接口'