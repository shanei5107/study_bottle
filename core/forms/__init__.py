# -*- coding: utf-8 -*-

from wtforms import Form as WTForm, IntegerField
from wtforms.validators import StopValidation

from functools import wraps
from bottle import request, abort


class BaseForm(WTForm):

    def __init__(self):
        data = request.json
        args = request.params
        if not args:
            args = request.forms
        # 自定义新得对象，不过滤其他需要校验得参数 get_json 这个函数默认情况下只对 mime 为 application/json 的请求可以正确解析。
        # 使用 request.get_json(force=True) 忽略mimetype
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            error_first = ''
            for field in self.errors:
                error_first = self.errors[field][0]
                break
            # 抛异常，给全局异常处理
            abort(400, error_first)
        return self


def validate_form(form_cls):

    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            form = form_cls().validate_for_api()
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def validate_back_form(form_cls):

    def decorator(fn):

        @wraps
        def wrapper(*args, **kwargs):
            form = form_cls().validate_for_api()
            return fn(form, *args, **kwargs)

        return wrapper

    return decorator