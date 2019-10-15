import wtforms
import json
from wtforms.validators import DataRequired, Length
from plugins.HYplugins.form.primary import BaseForm, JsonField
from models.HYModels.business import Order
from forms.business.fields import *


class OrderAddForm(BaseForm, DescriptionField, ImagesField, DateField, TimeField):
    """添加订单"""


class OrderEditForm(OrderAddForm, OrderIdField):
    """订单编辑"""

    # def __init__(self, factory_uuid, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.uuid = factory_uuid


class OrderInfoForm(BaseForm, OrderIdField):
    """订单详情"""


class OrderDeleteForm(BaseForm, OrderIdField):
    """订单删除"""
