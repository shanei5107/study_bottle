# -*- coding: utf-8 -*-

import datetime
import json
import time
import traceback
import requests

from core.logger import link_add_log_record
from ..signal import signal_send


# http请求封装
class Http:

    @staticmethod
    def post(
        url=None,
        params=None,
        headers=None,
        params_is_json=False,
        isback_json=True,
        verify=False,
        timeout=15,
        is_log=True,
        is_send_exception=False,
    ):
        """
        向指定接口发送post请求
        """
        result = {}
        r = ''
        remarks = ''
        request_ok = False
        start_time = time.time()

        if not headers:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            if params_is_json:
                # json传参
                r = requests.post(url, json=params, headers=headers, verify=verify, timeout=timeout)
            else:
                # form表单传参
                r = requests.post(url, data=params, headers=headers, verify=verify, timeout=timeout)

            # 字符处理
            if r.content and r.encoding is None:
                result = r.content.decode('utf-8')
            elif r.content and r.encoding.lower() == 'gbk':
                result = r.content.decode('gbk')
            elif r.content and r.encoding.lower() == 'gb2312' or r.apparent_encoding == 'GB2312':
                result = r.content.decode('gb2312')
            elif r.content:
                result = r.content.decode('utf-8')
            else:
                result = {}

            if r.status_code == 502 or r.status_code == 500:
                remarks = '第三方接口请求【FAIL】，status_code: %s 错误' % (r.status_code)
            elif r.status_code >= 400 and r.status_code <= 499:
                remarks = '第三方接口请求【FAIL】，status_code: %s 错误' % (r.status_code)
            else:
                if isback_json:
                    result = json.loads(result)
                remarks = '第三方接口请求【OK】'
                request_ok = True

        except requests.exceptions.ReadTimeout:
            result = {}
            # 读取超时
            remarks = '第三方接口请求【FAIL】，服务器在指定时间内没有应答，服务超时(ReadTimeOut)'
        except requests.exceptions.ConnectTimeout:
            # 服务器在指定时间内没有应签，链接超时
            result = {}
            remarks = '第三方接口请求【FAIL】，服务器在指定时间内没有应答，链接超时(ConnectTimeout)'
        except requests.exceptions.ConnectionError:
            # 未知的服务器
            result = {}
            remarks = '第三方接口请求【FAIL】，未知的服务器(ConnectionError)'
        except requests.exceptions.ChunkedEncodingError:
            result = {}
            remarks = '第三方接口请求【FAIL】，ChunkedEncodingError异常'
        except requests.exceptions.Timeout:
            result = {}
            remarks = '第三方接口请求【FAIL】,Timeout异常'
        except:
            result = {}
            remarks = '第三方接口请求【FAIL】,其他异常（ChunkedEncodingError）'
        finally:
            end_time = time.time()
            info_interface = {
                'url': url,
                'method': 'POST',
                'params': params,
                'params_str': str(params),
                'this_time_out': str(timeout) + 's',
                'req_stime': str(datetime.fromtimestamp(start_time)),
                'req_etime': str(datetime.fromtimestamp(end_time)),
                'cost_time': str((float("%.3f" % (end_time - start_time)) * 1000)) + 'ms',
                'state_code': str(r.status_code),
                'result': result,
            }
            if is_log:
                link_add_log_record(event_des='第三方接口请求日志', msg_dict=info_interface, remarks=remarks)

            # 第三方接口请求异常的时候是否发送广播通知发送
            # if not request_ok and is_send_exception:
            # signal_send('notify_third_inters_error', source='ThirdInternalErrorException', traceback=info_interface)

            return request_ok, result

    @staticmethod
    def get(
        url=None,
        params=None,
        headers=None,
        isback_json=True,
        verify=False,
        timeout=15,
        is_log=True,
        is_send_exception=False,
    ):
        """
        向指定接口发送get请求
        """
        result = {}
        r = ''
        remarks = ''
        request_ok = False
        start_time = time.time()

        if not headers:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            r = requests.get(url, params=params, headers=headers, verify=verify, timeout=timeout)
            # 字符处理
            if r.content and r.encoding is None:
                result = r.content.decode('utf-8')
            elif r.content and r.encoding.lower() == 'gbk':
                result = r.content.decode('gbk')
            elif r.content and r.encoding.lower() == 'gb2312' or r.apparent_encoding == 'GB2312':
                result = r.content.decode('gb2312')
            elif r.content:
                result = r.content.decode('utf-8')
            else:
                result = {}

            if r.status_code == 502 or r.status_code == 500:
                remarks = '第三方接口请求【FAIL】，status_code: %s 错误' % (r.status_code)
            elif r.status_code >= 400 and r.status_code <= 499:
                remarks = '第三方接口请求【FAIL】，status_code: %s 错误' % (r.status_code)
            else:
                if isback_json:
                    result = json.loads(result)
                remarks = '第三方接口请求【OK】'
                request_ok = True

        except requests.exceptions.ReadTimeout:
            result = {}
            # 读取超时
            remarks = '第三方接口请求【FAIL】，服务器在指定时间内没有应答，服务超时(ReadTimeOut)'
        except requests.exceptions.ConnectTimeout:
            # 服务器在指定时间内没有应签，链接超时
            result = {}
            remarks = '第三方接口请求【FAIL】，服务器在指定时间内没有应答，链接超时(ConnectTimeout)'
        except requests.exceptions.ConnectionError:
            # 未知的服务器
            result = {}
            remarks = '第三方接口请求【FAIL】，未知的服务器(ConnectionError)'
        except requests.exceptions.ChunkedEncodingError:
            result = {}
            remarks = '第三方接口请求【FAIL】，ChunkedEncodingError异常'
        except requests.exceptions.Timeout:
            result = {}
            remarks = '第三方接口请求【FAIL】,Timeout异常'
        except:
            result = {}
            remarks = '第三方接口请求【FAIL】,其他异常（ChunkedEncodingError）'
        finally:
            end_time = time.time()
            info_interface = {
                'url': url,
                'method': 'GET',
                'params': params,
                'params_str': str(params),
                'this_time_out': str(timeout) + 's',
                'req_stime': str(datetime.fromtimestamp(start_time)),
                'req_etime': str(datetime.fromtimestamp(end_time)),
                'cost_time': str((float("%.3f" % (end_time - start_time)) * 1000)) + 'ms',
                'state_code': str(r.status_code),
                'result': result,
            }
            if is_log:
                link_add_log_record(event_des='第三方接口请求日志', msg_dict=info_interface, remarks=remarks)

            # 第三方接口请求异常的时候是否发送广播通知发送
            # if not request_ok and is_send_exception:
            # signal_send('notify_third_inters_error', source='ThirdInternalErrorException', traceback=info_interface)

            return request_ok, result
