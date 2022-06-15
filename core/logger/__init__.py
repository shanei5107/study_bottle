# -*- coding: utf-8 -*-
import time
from bottle import request, response
from datetime import datetime
from loguru import logger
# loguru日志集成


def create_customize_log(pro_path=None):
    '''
    loguru日志集成
    :param pro_path
    '''
    import os
    if not pro_path:
        pro_path = os.path.split(os.path.realpath(__file__))[0]
    # 定义info_log文件名称
    log_file_path = os.path.join(pro_path, 'log/info_{time:YYYYMMDD}.log')
    # 定义err_log文件名称
    err_log_file_path = os.path.join(pro_path, 'log/error_{time:YYYYMMDD}.log')

    # 对应不同的格式
    format = " {time:YYYY-MM-DD HH:mm:ss:SSS} | process_id:{process.id} process_name:{process.name} | thread_id:{thread.id} thread_name:{thread.name} | {level} | {message}"
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
    logger.add(err_log_file_path,
               format=err_format,
               rotation='00:00',
               encoding='utf-8',
               level='ERROR',
               enqueue=True)  # Automatically rotate too big file
