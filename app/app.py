# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bottle import run, route, hook
from core.application import create_default_app_application
from core.logger import logger, create_customize_log, register_link_init_log_record_handler, register_link_end_log_record_handler
from core.rsp import *
from core.config import config, register_init_confg


@route('/hello')
def hello():
    return ApiResponse(msg='Hello Ray!!!')


def curr_create_customize_log():
    """
    配置日志路径、配置信息
    """
    create_customize_log(pro_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_customize_log_writer():
    """
    测试写入日志
    """
    logger.info('服务启动......')


def curr_register_init_config():
    """
    配置文件
    """
    logger.info('配置文件加载......')
    pro_path = os.path.split(os.path.realpath(__file__))[0] + '/' + 'config/'
    register_init_confg(config_pro_path=pro_path, file_name='config.ini')


# def test_read_config():
#     """
#     从配置文件中读取redis配置
#     """
#     redis_config_const = {
#         # 服务地址
#         'host': config.get('redis', 'host'),
#         # 服务端口
#         'post': config.get('redis', 'port'),
#         # 服务密码
#         'password': config.get('redis', 'password'),
#         # 数据库序号
#         'db': config.getint('redis', 'db')
#     }
#     print(redis_config_const)


def register_cache(config):
    """
    注册缓存处理
    """
    logger.info('缓存配置加载......')
    redis_config_const = {
        # 服务地址
        'host': config.get('redis', 'host'),
        # 服务端口
        'port': config.get('redis', 'port'),
        # 服务密码
        'password': config.get('redis', 'password'),
        # 数据库序号
        'db': config.getint('redis', 'db')
    }
    from core.cache.redis_pool_helper import redisCache
    redisCache.init_app(_redis=redis_config_const)


@hook('before_request')
def before_request():
    """
    每次请求前的勾子
    """
    REQUEST_METHOD = request.environ.get('REQUEST_METHOD')
    HTTP_ACCESS_CONTROL_REQUEST_METHOD = request.environ.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD')
    if REQUEST_METHOD == 'OPTIONS' and HTTP_ACCESS_CONTROL_REQUEST_METHOD:
        request.environ['REQUEST_METHOD'] = HTTP_ACCESS_CONTROL_REQUEST_METHOD

    # 忽略路由尾部的'/'斜杠，统一不需要多个路由来处理
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')
    # todo Token 校验
    pass
    # 初始化日志记录
    register_link_init_log_record_handler()


@hook('after_request')
def after_request():
    """
    每次请求结束后的勾子
    """
    # 结束请求日志
    register_link_end_log_record_handler()


from app import api

if __name__ == '__main__':
    # 日志配置
    curr_create_customize_log()

    # 读取配置文件
    curr_register_init_config()

    # 缓存注册
    register_cache(config)

    # 测试写入日志
    # test_customize_log_writer()

    # 创建应用实例
    app = create_default_app_application()
    # 运行应用实例
    run(app=app, debug=True, host='127.0.0.1', port=8756, reloader=True)