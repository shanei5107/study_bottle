# -*- coding: utf-8 -*-
from sre_constants import SUCCESS
from bottle import HTTPResponse, response, request


class _BasicResponse(HTTPResponse):
    code = 500
    success = False
    msg = '抱歉，服务器未知错误'

    # 默认支持跨域
    customize_headers = {'Access-Control-Allow-Origin': '*'}

    def __init__(self, status=code, body=None, **options):
        if not body:
            body = dict(code=self.code, success=self.success, msg=self.msg)
        # 设置返回响应体信息
        if self.customize_headers:
            super(_BasicResponse,
                  self).__init__(body=self.body,
                                 headers=self.customize_headers,
                                 status=status,
                                 **options)
        else:
            # 默认的允许进行跨域请求处理
            self.headers['Access-Control-Allow-Origin'] = '*'
            self.headers['Access-Control-Allow-Credentials'] = 'true'
            self.headers['Access-Control-Allow-Origin'] = '*'
            self.headers[
                'Access-Control-Allow-Methods'] = 'GET,POST,PUT,OPTIONS,DEL'
            self.headers['Access-Control-Allow-Headers'] = "*"
            super(_BasicResponse, self).__init__(body=self.body,
                                                 headers=self.headers,
                                                 status=status,
                                                 **options)


class ApiResponse(_BasicResponse):
    code = 200
    success = True
    msg = '成功'
    data = None

    def __init__(self, code=None, msg=None, data=None, **options):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if data:
            self.data = data

        # 返回内容体
        body = dict(
            code=self.code,
            success=(self.code == 200),
            msg=self.msg,
            data=self.data,
        )

        response.content_body_text = body
        super(ApiResponse, self).__init__(status=self.code,
                                          body=self.body,
                                          **options)


class BadRequestException(ApiResponse):
    code = 400
    msg = '错误的请求'


class ParameterException(ApiResponse):
    code = 400
    msg = '参数校验错误'


class UnauthorizedException(ApiResponse):
    code = 401
    msg = '未经许可授权'


class ForbiddenException(ApiResponse):
    code = 403
    msg = '当前访问没有权限'


class NotfoundException(ApiResponse):
    code = 404
    msg = '访问地址不存在'
    data = None


class MethodNotAllowedException(ApiResponse):
    code = 405
    msg = '不允许使用此方法提交访问'


class OtherException(ApiResponse):
    code = 800
    msg = '未知的其他HTTPEOOER异常'


class InternalErrorException(ApiResponse):
    code = 500
    msg = ' 服务内部异常'


class RateLimitApiException(ApiResponse):
    code = 429
    msg = '请求次数受限'


class CustomizeApiResponse(ApiResponse):
    code = 1
    data = None
    msg = '成功'
