# -*- coding: utf-8 -*-

import jwt
import datetime

# 7天有效期
def create_token_by_data(sub='', data={}, secret='', scope=['open'])