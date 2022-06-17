# -*- coding: utf-8 -*-

import json


def dict_to_json_ensure_ascii_indent(obj={}, ensure_ascii=False):
    """
    对象转为json字符串
    """
    return json.dumps(obj=obj, ensure_ascii=ensure_ascii, indent=4, separators=(',', ':'))
