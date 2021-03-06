# -*- coding: utf-8 -*-
from enum import Enum, unique
from bottle import HTTPResponse, response, request

from ..helper import json_helper

# 成功
SUCCESS_CODE = 0


class _BasicResponse(HTTPResponse):
    """
    基类封装
    """
    http_status_code = 500
    code = 500
    success = False
    msg = '抱歉，服务器未知错误'

    # 默认支持跨域
    customize_headers = {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json;charset=UTF-8'}

    def __init__(self, code=code, status=http_status_code, body=None, **options):
        if not body:
            body = dict(
                code=self.code,
                msg=self.msg,
                success=(self.code == SUCCESS_CODE),
            )
        # 设置返回响应体信息
        self.body = json_helper.dict_to_json_ensure_ascii_indent(obj=body)

        if self.customize_headers:
            super(_BasicResponse, self).__init__(body=self.body,
                                                 headers=self.customize_headers,
                                                 status=status,
                                                 **options)
        else:
            # 默认的允许进行跨域请求处理
            self.headers['Access-Control-Allow-Origin'] = '*'
            self.headers['Access-Control-Allow-Credentials'] = 'true'
            self.headers['Access-Control-Allow-Origin'] = '*'
            self.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,OPTIONS,DEL'
            self.headers['Access-Control-Allow-Headers'] = "*"
            super(_BasicResponse, self).__init__(body=self.body, headers=self.headers, status=status, **options)


class ApiResponse(_BasicResponse):
    """
    接口响应类封装
    """
    http_status_code = 200
    code = 0
    success = (code == SUCCESS_CODE)
    msg = '成功'
    data = None

    def __init__(self, code=None, data=None, msg=None, **options):
        if code:
            self.code = code
        if data:
            self.data = data
        if msg:
            self.msg = msg

        # 返回内容体
        body = dict(
            code=self.code,
            success=(self.code == SUCCESS_CODE),
            msg=self.msg,
            data=self.data,
        )

        # 返回消息体写入
        self.body = body
        response.content_body_text = body

        super(ApiResponse, self).__init__(status=self.http_status_code, code=self.code, body=self.body, **options)


class BadRequestException(ApiResponse):
    http_status_code = 400
    code = 400
    msg = '错误的请求'


class ParameterException(ApiResponse):
    http_status_code = 400
    code = 400
    msg = '参数校验错误'


class UnauthorizedException(ApiResponse):
    http_status_code = 401
    code = 401
    msg = '未经许可授权'


class ForbiddenException(ApiResponse):
    http_status_code = 403
    code = 403
    msg = '当前访问没有权限'


class NotfoundException(ApiResponse):
    http_status_code = 404
    code = 404
    msg = '访问地址不存在'
    data = None


class MethodNotAllowedException(ApiResponse):
    http_status_code = 405
    code = 405
    msg = '不允许使用此方法提交访问'


class OtherException(ApiResponse):
    http_status_code = 800
    code = 800
    msg = '未知的其他HTTPEOOER异常'


class InternalErrorException(ApiResponse):
    http_status_code = 500
    code = 500
    msg = ' 服务内部异常'


class RateLimitApiException(ApiResponse):
    http_status_code = 429
    code = 429
    msg = '请求次数受限'


class BusinessError(ApiResponse):
    http_status_code = 200
    code = 9999
    msg = '业务异常'
    data = None


@unique
class ApiStatus(Enum):
    OK = (0, '成功')
    FAIL = (-1, '未知异常')
    BUSINESS_ERROR = (9999, '业务异常')

    def get_code(self):
        """
        根据枚举名称取状态码code
        """
        return self.value[0]

    def get_msg(self):
        """
        根据枚举名称取状态说明msg
        """
        return str(self.value[1])