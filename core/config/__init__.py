# -*- coding: utf-8 -*-

import configparser
import warnings

config = configparser.ConfigParser()


def register_init_confg(config_pro_path=None, files_name=None):
    try:
        if not config_pro_path:
            warnings.warn('服务配置信息文件为空！')
        else:
            if isinstance(files_name, list):
                for item in files_name:
                    config.read(config_pro_path + '\\' + item,
                                encoding='utf-8')
            else:
                config.read(config_pro_path + '\\' + item, encoding='utf-8')
    except Exception as e:
        print(e)
        warnings.warn('服务配置信息文件读取错误')