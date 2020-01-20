from wtforms.validators import Optional
from forms.fields.primary import *
from plugins import Redis
from plugins.HYplugins.form import BaseForm
from plugins.HYplugins.form.fields import PhoneField, CodeField, WechatCodeField, VisitorsParameterField


class SignInForm(BaseForm, WechatCodeField):
    """登录"""


class VisitorsForm(BaseForm, VisitorsParameterField):
    """访客审核验证"""

    server_name = '厂家端'


class RegisteredForm(BaseForm, PhoneField, CodeField, FactoryNameField, LLField, AddressField, WechatCodeField):
    """厂家注册"""

    def validate_code(self, *args):
        """验证手机验证码"""
        phone = self.phone.data
        self.redis_key = f'validate_phone_registered_{phone}'
        if self.code.data == Redis.get(self.redis_key):
            return True
        else:
            raise wtforms.ValidationError(message='验证码错误')


class FactoryEditForm(BaseForm, PhoneField, FactoryNameField, LLField, AddressField):
    """信息修改"""

    code = wtforms.StringField(validators=[Optional(), Length(min=4, max=4, message=VM.say('length_unite', '验证码', 4))])

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def validate_phone(self, *args):
        """验证手机验证码"""
        phone = self.phone.data
        self.redis_key = f'validate_phone_edit_phone_{self.user.phone}'

        if self.user.phone != phone:
            if self.code.data == Redis.get(self.redis_key):
                return True
            else:
                raise wtforms.ValidationError(message='验证码错误')
        else:
            return True


class TokenInternalUse(BaseForm):
    """token内部调用"""
    factory_uuid = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '用户编号'))
    ])

    random = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '随机码'))
    ])
