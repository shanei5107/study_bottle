# -*- coding: utf-8 -*-
from bottle import Bottle, default_app, run, response, request, hook, route, install, get, error, HTTPError, HTTPResponse, TEMPLATE_PATH, static_file
from beaker.middleware import SessionMiddleware


def create_default_app_application():
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
