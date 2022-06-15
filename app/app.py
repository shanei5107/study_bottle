# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bottle import run, route
from core.application import create_default_app_application
from core.logger import logger, create_customize_log


@route('/hello')
def hello():
    return 'hello RAY!'


def curr_create_customize_log():
    pro_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    create_customize_log(pro_path)
    # create_customize_log(pro_path=os.path.split(os.path.realpath(__file__)[0]))


def test_customize_log_writer():
    logger.info('服务启动......')


def test_customize_error_log_writer():
    logger.error('服务启动......')


if __name__ == '__main__':
    # 日志
    curr_create_customize_log()
    # 写日志
    test_customize_log_writer()
    test_customize_error_log_writer()

    # 创建应用实例
    app = create_default_app_application()
    # 运行应用实例
    run(app=app, debug=True, host='127.0.0.1', port=8756, reloader=True)