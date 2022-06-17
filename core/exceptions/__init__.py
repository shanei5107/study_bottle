# -*- coding: utf-8 -*-

from shutil import ExecError


class ErrorsRestPlugin():
    name = 'ErrorsRestPlugin'
    api = 2

    def __init__(self, dumps=None, error_handler=None):
        self.json_dumps = dumps
        self.error_handler = error_handler

    def setup(self, app):

        def default_error_handler(res):
            return self.error_handler(res)

        app.default_error_handler = default_error_handler

    def apply(self, callback, route):

        def wrapper(*args, **kwargs):
            try:
                rv = callback(*args, **kwargs)
                return rv
            except Exception as e:
                return self.error_handler(e)

        return wrapper


class BusinessException(Exception):
    """
    自定义异常类
    """

    def __init__(self, code=9999, msg=''):
        self.code = code
        self.msg = msg
