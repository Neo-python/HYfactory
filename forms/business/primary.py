import wtforms
import json
from wtforms.validators import DataRequired, Length
from plugins.HYplugins.form.primary import BaseForm, JsonField, ListPage
from models.HYModels.business import Order
from forms.business.fields import *


class OrderListForm(BaseForm, ListPage):
    """订单列表"""


class OrderAddForm(BaseForm, DescriptionField, ImagesField, DateField, TimeField):
    """添加订单"""


class OrderEditForm(OrderAddForm, OrderIdField):
    """订单编辑"""


class OrderInfoForm(BaseForm, OrderIdField):
    """订单详情"""


class OrderDeleteForm(BaseForm, OrderIdField):
    """订单删除"""
