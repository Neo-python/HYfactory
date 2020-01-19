import time
from flask import g, request
from sqlalchemy.exc import IntegrityError
from views import Factory
from views.user import api
from plugins import Redis, core_api
from plugins.HYplugins.common import result_format, valid_random
from plugins.HYplugins.common.authorization import login, auth
from plugins.HYplugins.error import ViewException
from forms import user as forms


@api.route('/sign_in/', methods=['POST'])
def sign_in():
    """登录"""
    form = forms.SignInForm().validate_()

    user = Factory.query.filter_by(open_id=form.open_id).first()

    if user:
        return result_format(data={'token': user.generate_token(), 'user_info': user.serialization()})
    else:
        return result_format(error_code=5011, message='用户未注册')


@api.route('/visitors/', methods=['POST'])
def visitors():
    """访客模式"""

    forms.VisitorsForm().validate_()

    user = Factory.query.filter_by(create_time="2028-01-01 12:00:00").first()
    if user:
        return result_format(data={'token': user.generate_token(), 'user_info': user.serialization()})
    else:
        return result_format(data={'token': '', 'user_info': ''})


@api.route('/refresh_token/')
@auth.login_required
def refresh_token():
    """刷新token"""

    day = 20

    iat = g.user.get('iat')

    if time.time() - time.mktime(time.localtime(iat)) > (60 * 60 * 24 * day):
        user = Factory.query.filter_by(uuid=g.user.uuid).first_or_404()
        return result_format(data={'token': user.generate_token(), 'user_info': user.serialization()})
    else:
        return result_format(error_code=5009, message='token刷新失败.')


@api.route('/token/internal_use/')
def token_internal_use():
    """token内部调用
    参数:
    factory_uuid:str
    """
    form = forms.TokenInternalUse(request.args).validate_()
    if valid_random(form.random.data) is False:
        return result_format(1001, message='验证码错误')

    factory = Factory.query.filter_by(uuid=form.factory_uuid.data).first()
    if not factory:
        return result_format(5011, message='厂家编号错误.')
    else:
        return result_format(error_code=0, data=factory.generate_token())


@api.route('/registered/', methods=['POST'])
def registered():
    """注册成为厂家
    注册完成 删除Redis中的短信验证码信息
    :return:
    """

    form = forms.RegisteredForm().validate_()

    # 表单验证成功,处理redis与表单数据,创建账号
    data = form.data
    data.pop('code')
    data.pop('wechat_code')

    try:
        factory = Factory(open_id=form.open_id, **data).direct_commit_()
    except IntegrityError as err:
        raise ViewException(error_code=1001, message="用户已注册,请直接登录!")
    Redis.delete(form.redis_key)  # 删除验证码
    core_api.notice_sms(template_id="484144", params=[form.name.data])  # 通知管理员注册完成
    return result_format(data={'token': factory.generate_token(), 'user_info': factory.serialization()})


@api.route('/factory/info/')
@login()
def factory_info():
    """厂家信息查询"""
    user = Factory.query.filter_by(uuid=g.user.uuid).first_or_404()
    return result_format(data=user.serialization())


@api.route('/factory/info/edit/', methods=['POST'])
@login()
def factory_info_edit():
    """厂家信息修改"""
    user = Factory.query.filter_by(uuid=g.user.uuid).first_or_404()
    form = forms.FactoryEditForm(user=user).validate_()
    user.set_attrs(form.data).direct_update_()
    Redis.delete(form.redis_key)
    return result_format()
