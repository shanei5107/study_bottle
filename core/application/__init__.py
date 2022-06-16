# -*- coding: utf-8 -*-
import re
from bottle import Bottle, default_app, run, response, request, hook, route, install, get, error, HTTPError, HTTPResponse, TEMPLATE_PATH, static_file
from beaker.middleware import SessionMiddleware
from core.exceptions import ErrorsRestPlugin
from core.rsp import ForbiddenException, InternalErrorException, MethodNotAllowedException, NotfoundException, OtherException, ParameterException, RateLimitApiException
from core.logger import logger
from core.signal import signal_handle


def _register_default_signal_handle():
    """
    通知
    """

    @signal_handle("notify_error_500")
    def error_notify(sender, **kwargs):
        print('接收到了异常信号通知 by %r, data %r' % (sender, kwargs))


def _register_global_error_catch(e, is_send=True):
    """
    注册全局异常捕获
    """
    if isinstance(e, HTTPError):
        code = e.status_code
        # 异常处理
        if code == 400:
            # 参数校验异常
            return ParameterException(code=code, msg=e.body)
        elif code == 401:
            # 请求不允许
            return ForbiddenException()
        elif code == 404:
            # 找不到访问地址
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
        #  todo 发送告警
        if is_send:
            pass
        # 500异常
        return InternalErrorException(msg='服务器内部异常，请联系系统管理员')


def create_default_app_application():
    #  注册默认的接收广播
    _register_default_signal_handle()

    # 默认注册全局异常处理
    install(ErrorsRestPlugin(error_handler=_register_global_error_catch))

    #  配置session管理
    session_opts = {
        'session.type': 'file',
        'session.cookie_expires': 3600,
        'session.data_dir': '/Users/ray/workspace/tmp/sessions/order',
        'session.auto': True
    }
    # 创建应用实例
    # app = Bottle(autojson=False)
    # 使用默认的实例
    application = SessionMiddleware(default_app(), session_opts)
    return application
