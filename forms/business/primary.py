import wtforms
import json
from wtforms.validators import DataRequired, Length
from plugins.HYplugins.form.primary import BaseForm, JsonField, ListPage
from plugins.HYplugins.form.fields import PhoneField
from forms.fields.primary import LLField
from forms.business.fields import *


class OrderListForm(BaseForm, ListPage):
    """订单列表"""


class OrderAddForm(BaseForm, ContactField, PhoneField, DescriptionField, ImagesField, DateField, TimeField, LLField):
    """添加订单"""


class OrderEditForm(OrderAddForm, OrderIdField, LLField):
    """订单编辑"""


class OrderInfoForm(BaseForm, OrderIdField):
    """订单详情"""


class OrderDeleteForm(BaseForm, OrderIdField):
    """订单删除"""
