# -*- coding: utf-8 -*-

import os, sys
from loguru import logger


def auto():
    pro_path = os.path.split(os.path.realpath(__file__))[0]
    sys.path.append(pro_path)
    for root, dirs, files in os.walk(pro_path):
        for file in files:
            name, ext = os.path.splitext(file)
            if ext == '.py' and name != '__init__' and pro_path == root:
                __import__(name)
        for dir in dirs:
            if dir != '.svn':
                try:
                    __import__(__name__ + '.' + dir)
                except Exception as e:
                    logger.exception(e)
        break
    pass


auto()