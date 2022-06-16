# -*- coding: utf-8 -*-

import jwt
import datetime


# 7天有效期
def create_token_by_data(sub='', data={}, secret='', scopes=['open'], is_back_data=False, exp_time=60 * 60 * 24 * 7):
    """
    生成jwt的token值
    """
    if not secret:
        return False, {'access_token': '', 'msg': '密匙不能为空'}

    if not data:
        return False, {'access_token': '', 'msg': '需要签名信息不能为空'}

    payload = {
        "iss": "fly.top",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=exp_time),
        "iat": datetime.datetime.utcnow(),
        "aud": "www.fly.top",
        "sub": sub,
        "scopes": scopes,
        "data": data
    }

    # 不参与进行签名计算
    if not sub:
        payload.pop('sub')
    # token生成处理
    token = jwt.encode(payload, secret, algorithm='HS256')
    # 返回授权token
    if is_back_data:
        back_result = {
            'access_token': str(token, 'utf-8'),
            'data': data,
        }
    else:
        back_result = {
            'access_token': str(token, 'utf-8'),
        }
    return True, back_result


def verify_bearer_token(ischeck_sub=False, secret='', sub_in='', token=''):
    """
    校验token
    """
    try:
        payload = jwt.decode(token, secret, audience='www.fly.top', algorithms=['HS256'])
        if ischeck_sub and sub_in != '':
            sub = payload['sub']
            if sub != sub_in:
                return False, "无效的Token"

        if payload and ('data' in payload):
            return True, payload['data']
        else:
            raise jwt.InvalidTokenError

    except jwt.ExpiredSignatureError:
        return False, "Token已过期"
    except jwt.InvalidTokenError:
        return False, "Token已失效"
    except:
        return False, "无效的Token"
