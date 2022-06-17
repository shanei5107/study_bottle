# -*- coding: utf-8 -*-
from importlib.resources import path
import json
from resource import getrusage
import time
from bottle import request, response
from datetime import datetime
from loguru import logger

from core.helper import json_helper


#  自定义日志配置
def create_customize_log(pro_path=None):
    """
    loguru日志集成
    :param pro_path
    """
    import os
    if not pro_path:
        pro_path = os.path.split(os.path.realpath(__file__))[0]
    # 定义info_log文件名称
    log_file_path = os.path.join(pro_path, 'log/info_{time:YYYYMMDD}.log')
    # 定义err_log文件名称
    err_log_file_path = os.path.join(pro_path, 'log/error_{time:YYYYMMDD}.log')

    # 对应不同的格式
    format = " {time:YYYY-MM-DD HH:mm:ss:SSS} | process_id:{process.id} process_name:{process.name} | thread_id:{thread.id} thread_name:{thread.name} | {level} |\n {message}"
    # 记录的充值通知的日志
    # enqueue=True表示 开启异步写入
    # 使用 rotation 参数实现定时创建 log 文件,可以实现每天 0 点新创建一个 log 文件输出了
    logger.add(log_file_path,
               format=format,
               rotation='00:00',
               compression="zip",
               encoding='utf-8',
               level='INFO',
               enqueue=True)  # Automatically rotate too big file

    # 错误日志不需要压缩
    err_format = " {time:YYYY-MM-DD HH:mm:ss:SSS} | process_id:{process.id} process_name:{process.name} | thread_id:{thread.id} thread_name:{thread.name} | {level} |\n {message}"
    # enqueue=True表示 开启异步写入
    # 使用 rotation 参数实现定时创建 log 文件,可以实现每天 0 点新创建一个 log 文件输出了
    logger.add(err_log_file_path, format=err_format, rotation='00:00', encoding='utf-8', level='ERROR',
               enqueue=True)  # Automatically rotate too big file


# 封闭一下关于记录序号的日志记录用于全链路的日志请求的日志
def _link_init_log_record():
    request.request_links_logs = []
    request.request_links_index = 0


# 封闭一下关于记录序号的日志记录用于全链路的日志请求的日志
def link_add_log_record(event_des='', msg_dict={}, remarks=''):
    request.request_links_index = request.request_links_index + 1
    log = {'link_index': request.request_links_index, 'event_des': event_des, 'msg_dict': msg_dict, 'remarks': remarks}
    if not remarks:
        log.pop('remarks')
    if not msg_dict:
        log.pop('msg_dict')
    request.request_links_logs.append(log)


# 路由白名单: 不记录请求日志
WHITE_PATH_LIST = ['/favicon.ico', 'health']


# 初始化请求日志
def register_link_init_log_record_handler():
    """
    过滤指定一些路由的请求，不记录日志
    """
    path_info = request.environ.get('PATH_INFO')
    if path_info not in WHITE_PATH_LIST:
        response.content_body_text = None
        # 配置日志初始化
        _link_init_log_record()
        # 计算时间
        request.request_start_time = time.time()
        # 开始记录日志
        link_add_log_record(event_des='request-start')


# 请求日志完结
def register_link_end_log_record_handler():
    """
    一个请求结束的时候，日志记录下这个请求的整个过程和返回响应体信息
    """
    path_info = request.environ.get('PATH_INFO')
    if path_info not in WHITE_PATH_LIST and request.method != 'OPTIONS':
        link_add_log_record(event_des='request-end')

        # 请求头信息
        # print(dict(request.headers))

        # 统筹记录最后的请求日志信息
        log_msg = {
            'host': request.headers.get('Host'),
            'ip': request.remote_addr,
            'url': request.url,
            'method': request.method,
            'params': {
                'query': '' if not request.query else request.query.decode("utf-8"),
                'forms': '' if not request.forms else request.forms,
                'body': '' if not request.body else request.body,
            },
            'req_links_logs': request.request_links_logs,
        }

        try:
            req_json_data = request.json
            if req_json_data:
                log_msg['params']['req_json_data'] = req_json_data
        except:
            pass

        try:
            log_msg['rsp_data'] = response.content_body_text
        except:
            pass

        # 计算请求完成消耗的时间--保留两位小数点
        end_time = time.time()
        log_msg['req_stime'] = str(datetime.fromtimestamp(request.request_start_time))
        log_msg['req_etime'] = str(datetime.fromtimestamp(end_time))
        log_msg['cost_time'] = str((float("%.3f" % (end_time - request.request_start_time)) * 1000)) + ''
        logger.info(log_msg)
