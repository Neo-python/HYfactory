import datetime
from flask import g, request
from views.business import api
from plugins.HYplugins.common.authorization import login
from plugins import common


@api.route('/order/list/')
@login()
def order_list():
    """厂家订单列表"""


@api.route('/order/add/', methods=['POST'])
@login(verify=1)
def order_add():
    """添加订单
    验证厂家是否属于通过审核的厂家
    :return:
    """


@api.route('/order/info/')
@login()
def order_info():
    """订单详情"""


@api.route('/order/edit/', methods=['POST'])
@login()
def order_edit():
    """修改订单
    更新订单内容
    更新订单更新时间
    """


@api.route('/order/delete/', methods=['DELETE'])
@login()
def order_delete():
    """厂家订单删除
    当订单处于被接单的状态时,无法删除订单,并提示厂家联系驾驶员先取消订单.
    """
