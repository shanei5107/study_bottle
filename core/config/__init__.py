# -*- coding: utf-8 -*-

import configparser
import warnings

config = configparser.ConfigParser()


def register_init_confg(config_pro_path=None, file_name=None):
    try:
        if not config_pro_path:
            warnings.warn('服务配置信息文件为空！')
        else:
            file_path = config_pro_path + '/' + file_name
            config.read(file_path, encoding='utf-8')
    except Exception as e:
        print(e)
        warnings.warn('服务配置信息文件读取错误')