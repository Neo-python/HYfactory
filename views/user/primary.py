import time
from flask import g
from views.user import api
from init import Redis, core_api
from plugins.HYplugins.common import result_format
from plugins.HYplugins.common.authorization import login, auth
from models.user import Factory
from forms import user as forms


@api.route('/sign_in/', methods=['POST'])
def sign_in():
    """登录"""
    form = forms.SignInForm().validate_()
    open_id = core_api.get_open_id(code=form.wechat_code.data)

    user = Factory.query.filter_by(open_id=open_id).first()
    #
    if user:  # 用户信息存在,并且用户类型已经选择

        return result_format(data={'token': user.generate_token(), 'user_info': user.serialization()})
    else:
        return result_format(error_code=4001, message='客户未注册')


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
        return result_format(error_code=4008, message='token刷新失败,有效期还长着呢.')


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

    Factory(**data).direct_commit_()

    Redis.delete(form.redis_key)
    return result_format()


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
