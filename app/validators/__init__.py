# -*- coding: utf-8 -*-
from core.forms import BaseForm
from wtforms import DateTimeField, PasswordField, FieldList, IntegerField, StringField
from wtforms.validators import DataRequired, Regexp, EqualTo, length, Optional, NumberRange


class LoginForm(BaseForm):
    username = StringField(validators=[DataRequired(message='username 必须传入')])
    password = StringField(validators=[DataRequired(message='password 必须传入')])
