# -*- coding: utf-8 -*-

from blinker import signal


def signal_send(name, source='anoymous', **kw):
    """
    创建信息并发送
    """
    name_signal = signal(name)
    ret = name_signal.send(source, **kw)
    return ret


def signal_listen(name, handler):
    """
    接收信息
    """
    name_signal = signal(name)
    name_signal.connect(handler, weak=False)


def signal_handle(name, *args, **kwargs):
    """
    信号接收装饰器
    """
    s_name = name

    def wrapper(func):

        def inner(*args, **kwargs):
            func(*args, **kwargs)

        signal_listen(s_name, func)
        return inner

    return wrapper