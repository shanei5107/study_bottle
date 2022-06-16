# -*- coding: utf-8 -*-

from bottle import route


@route('/pay/action', method=['POST', 'GET', 'OPTIONS'])
def index():
    return '我是支付接口'