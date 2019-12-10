from plugins.HYplugins.form.primary import BaseForm, ListPage
from forms.fields.primary import LLField, AddressField
from forms.business.fields import *


class OrderListForm(BaseForm, ListPage):
    """订单列表"""


class OrderAddForm(BaseForm, ContactField, DescriptionField, ImagesField, DateField, TimeField, LLField,
                   AddressField):
    """添加订单"""


class OrderEditForm(OrderAddForm, OrderUUIdField, LLField, AddressField):
    """订单编辑"""


class OrderInfoForm(BaseForm, OrderUUIdField):
    """订单详情"""


class OrderDeleteForm(BaseForm, OrderUUIdField):
    """订单删除"""
