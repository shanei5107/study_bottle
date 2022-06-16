# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bottle import run, route, HTTPError, install
from core.application import create_default_app_application
from core.logger import logger, create_customize_log
from core.exceptions import ErrorsRestPlugin
from core.rsp import *


@route('/hello')
def hello():
    return 'hello RAY!'


def curr_create_customize_log():
    '''
    配置日志路径、配置信息
    '''
    create_customize_log(pro_path=os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')))


def test_customize_log_writer():
    '''
    测试写入日志
    '''
    logger.info('服务启动......')
    logger.error('服务启动......')


def register_global_error_catch(e, is_send=True):
    '''
    注册全局异常捕获
    '''
    if isinstance(e, HTTPError):
        code = e.status_code
        if code == 400:
            # 参数校验异常
            return ParameterException(code=code, msg=e.body)
        elif code == 401:
            # 请求不允许
            return UnauthorizedException()
        elif code == 403:
            # 访问权限受限
            return ForbiddenException()
        elif code == 404:
            # 资源不存在
            return NotfoundException()
        elif code == 405:
            # 请求方式异常
            return MethodNotAllowedException()
        elif code == 429:
            # 限流异常
            return RateLimitApiException()
        else:
            return OtherException(code=code)
    else:
        logger.exception(e)
        return CustomizeApiResponse(msg='系统内部错误，请联系系统管理员')


if __name__ == '__main__':
    # 日志
    curr_create_customize_log()
    # 测试写入日志
    test_customize_log_writer()

    # 配置全局异常
    install(ErrorsRestPlugin(error_handler=register_global_error_catch))

    # 创建应用实例
    app = create_default_app_application()
    # 运行应用实例
    run(app=app, debug=True, host='127.0.0.1', port=8756, reloader=True)