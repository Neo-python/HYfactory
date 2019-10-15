import wtforms
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional
from init import Redis
from forms.fields.main import *
from plugins.HYplugins.form import BaseForm
from plugins.HYplugins.form.fields import PhoneField, CodeField


class RegisteredForm(BaseForm, PhoneField, CodeField, FactoryNameField, LLField, AddressField, OpenIdField):
    """厂家注册"""

    def validate_phone(self, value):
        """验证手机验证码"""
        phone = value.data
        if self.code.data == Redis.get(f'validate_phone_registered_{phone}'):
            return True
        else:
            raise wtforms.ValidationError(message='code error')
