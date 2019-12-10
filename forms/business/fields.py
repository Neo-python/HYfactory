"""业务类范围内的字段"""
import wtforms
from flask import g
from wtforms.validators import DataRequired, Length, Regexp
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM
from plugins.HYplugins.form.primary import JsonField
from plugins.HYplugins.error import FormException
from models.business import Order


class DescriptionField:
    """订单详情"""

    description = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '订单详情')),
        Length(min=5, max=255, message=VM.say('length', '订单详情', 5, 255))
    ])


class ContactField:
    """联系人字段"""
    contact_name = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '联系人名称')),
        Length(max=20, message=VM.say('length', '联系人名', 0, 20))
    ], default=""
    )
    contact_phone = wtforms.StringField(validators=[
        Regexp('1\d{10}', message='手机号错误,请检查手机号格式'),
        DataRequired(message=VM.say('required', '手机号')),
    ])


class ImagesField:
    """图片"""
    images = JsonField()


class DateField:
    """日期"""
    date = wtforms.DateField(validators=[DataRequired(message=VM.say('required', '日期'))])


class TimeField:
    """时间"""
    time = wtforms.TimeField()


class OrderIdField:
    """订单编号"""

    order_uuid = wtforms.IntegerField(validators=[DataRequired(message=VM.say('required', '订单编号'))])

    def validate_order_uuid(self, *args):
        """检查订单"""
        self.factory_uuid = g.user.uuid
        query = Order.query.with_for_update(of=Order)  # 指明上锁的表为Order, 如果不指明, 则查询中涉及的所有表(行)都会加锁.
        self.order = query.filter_by(order_uuid=self.order_uuid.data, factory_uuid=self.factory_uuid).first()
        if not self.order:
            raise FormException(message='订单编号错误')
        return True
