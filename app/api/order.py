# -*- coding: utf-8 -*-
from bottle import route

from core.rsp import ApiResponse, OtherException


@route('/order/action', method=['POST', 'GET', 'OPTIONS'])
def index():
    return ApiResponse(msg='我是订单接口')