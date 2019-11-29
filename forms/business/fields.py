"""业务类范围内的字段"""
import wtforms
from flask import g
from wtforms.validators import DataRequired, Length
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM
from plugins.HYplugins.form.primary import JsonField
from models.business import Order


class DescriptionField:
    """订单详情"""

    description = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '订单详情')),
        Length(min=5, message=VM.say('length_unite', '订单详情', 5))
    ])


class ContactField:
    """联系人字段"""
    contact = wtforms.StringField(validators=[
        Length(max=6, message=VM.say('length', '联系人名', 1, 6))
    ], default=""
    )


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

    order_id = wtforms.IntegerField(validators=[DataRequired(message=VM.say('required', '订单编号'))])

    def validate_order_id(self, value):
        """检查订单"""
        self.factory_uuid = g.user.uuid
        order_id = value.data
        query = Order.query.with_for_update(of=Order)  # 指明上锁的表为Order, 如果不指明, 则查询中涉及的所有表(行)都会加锁.
        self.order = query.filter_by(id=order_id, factory_uuid=self.factory_uuid).first_or_404()
        return True
