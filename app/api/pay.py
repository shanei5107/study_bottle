# -*- coding: utf-8 -*-

from bottle import route
from core.exceptions import BusinessException

from core.rsp import ApiResponse


@route('/pay/action', method=['POST', 'GET', 'OPTIONS'])
def index():
    raise BusinessException(msg='故意抛出')
    return ApiResponse(msg='我是支付接口')
