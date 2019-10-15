import wtforms
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional
from init import Redis
from forms.fields.main import *
from plugins.HYplugins.form import BaseForm
from plugins.HYplugins.form.fields import PhoneField, CodeField


class RegisteredForm(BaseForm, PhoneField, CodeField, FactoryNameField, LLField, AddressField, OpenIdField):
    """厂家注册"""

    def validate_code(self, *args):
        """验证手机验证码"""
        phone = self.phone.data
        self.redis_key = f'validate_phone_registered_{phone}'
        if self.code.data == Redis.get(self.redis_key):
            return True
        else:
            raise wtforms.ValidationError(message='code error')
