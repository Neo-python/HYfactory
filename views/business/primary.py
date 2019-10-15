import datetime
from flask import g, request
from views.business import api
from forms.business import primary as forms
from plugins.HYplugins.common.authorization import login
from plugins.HYplugins.common import result_format, paginate_info
from models.HYModels.business import Order


@api.route('/order/list/')
@login()
def order_list():
    """厂家订单列表"""

    form = forms.OrderListForm(request.args).validate_()

    key_word = request.args.get('key_word')
    schedule = request.args.get('schedule', type=int, default=None)

    query = Order.query.filter_by(factory_uuid=g.user.uuid)

    if key_word:
        query = query.filter(Order.description.ilike(f'%{key_word}%'))

    if schedule is not None:
        query = query.filter_by(schedule=schedule)

    paginate = query.paginate(page=form.page.data, per_page=form.limit.data, error_out=False)

    data = paginate_info(paginate=paginate, items=[item.factory_serialization() for item in paginate.items])

    return result_format(data=data)


@api.route('/order/add/', methods=['POST'])
@login()
def order_add():
    """添加订单
    :return:
    """
    form = forms.OrderAddForm().validate_()
    order = Order(**form.data, factory_uuid=g.user.uuid).direct_commit_()

    return result_format(data={'order_id': order.id})


@api.route('/order/info/')
@login()
def order_info():
    """订单详情"""

    form = forms.OrderInfoForm(request.args).validate_()

    return result_format(data=form.order.factory_serialization(remove={'schedule'}))


@api.route('/order/edit/', methods=['POST'])
@login()
def order_edit():
    """修改订单
    更新订单内容
    更新订单更新时间
    """

    form = forms.OrderEditForm().validate_()

    # 检查订单状态
    if form.order.schedule != 0:
        return result_format(error_code=4009, message='订单状态发生改变,订单已被驾驶员接走!')

    form.order.set_attrs(form.data)
    form.order.update_time = datetime.datetime.now()
    form.order.direct_update_()

    return result_format()


@api.route('/order/delete/', methods=['DELETE'])
@login()
def order_delete():
    """厂家订单删除
    当订单处于被接单的状态时,无法删除订单,并提示厂家联系驾驶员先取消订单.
    """
    form = forms.OrderDeleteForm(request.args).validate_()
    order = form.order

    # 检查订单状态
    if order.schedule == 1:
        return result_format(error_code=4009, message='订单已被接走,请联系驾驶员先取消订单.')
    elif order.status == 0:
        return result_format(message='订单已删除,请勿重复请求.')
    else:
        order.delete().direct_update_()
        return result_format(message='订单已删除')
