import datetime
from flask import g, request
from views import Order
from views.business import api
from forms.business import primary as forms
from models.user import Driver
from plugins.HYplugins.common.authorization import login
from plugins.HYplugins.common import result_format, paginate_info
from plugins import core_api


@api.route('/order/list/')
@login()
def order_list():
    """厂家订单列表"""

    form = forms.OrderListForm(request.args).validate_()

    key_word = request.args.get('key_word')
    schedule = request.args.get('schedule', type=int, default=0)

    query = Order.query.filter_by(factory_uuid=g.user.uuid)

    if key_word:
        query = query.filter(Order.description.ilike(f'%{key_word}%'))

    if schedule != 0:
        query = query.filter_by(schedule=2)
    else:
        query = query.filter(Order.schedule < 2)

    # 订单进度高的优先排序,订单创建时间次级优先排序
    query = query.order_by(Order.schedule.desc(), Order.id.desc())

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

    # 存入订单基本信息(联系人等信息)
    order.factory.save_contact(contact_name=order.contact_name, contact_phone=order.contact_phone,
                               longitude=order.longitude, latitude=order.latitude,
                               address=order.address, address_replenish=order.address_replenish)
    driver_phone = [driver.phone for driver in Driver.query.filter_by(verify=1).all()]
    core_api.batch_sms(template_id="488983", phone_list=driver_phone,
                       params=[g.user.name, order.order_uuid])  # 通知驾驶员有新的订单
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
        return result_format(error_code=5110, message='订单状态发生改变,订单已被驾驶员接走!')

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
    # form = forms.OrderDeleteForm(request.form).validate_()
    # order = form.order
    order_uuid = request.get_json(force=True).get('order_uuid', '')

    factory_uuid = g.user.uuid
    query = Order.query.with_for_update(of=Order)  # 指明上锁的表为Order, 如果不指明, 则查询中涉及的所有表(行)都会加锁.
    order = query.filter_by(order_uuid=order_uuid, factory_uuid=factory_uuid).first()
    if not order:
        return result_format(1001, message='订单编号错误')
    # 检查订单状态
    if order.schedule == 1:
        return result_format(error_code=5110, message='订单已被接走,请联系驾驶员先取消订单.')
    else:
        order.direct_delete_()
        return result_format(message='订单已删除')
