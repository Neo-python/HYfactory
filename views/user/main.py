import time
from views.user import api
from plugins.HYplugins.common import result_format
from plugins.HYplugins.common.authorization import login, auth
from init import wechat_api


@api.route('/sign_in/', methods=['POST'])
def sign_in():
    """登录"""
    # open_id = wechat_api.get_open_id()
    #
    # user = User.query.filter_by(open_id=open_id).first()
    #
    # if user and user.genre is not None:  # 用户信息存在,并且用户类型已经选择
    #
    #     return common.result_format(data={'token': user.generate_token(), 'user_info': user.info()})
    # else:
    #     return common.result_format(error_code=4001, message='客户未注册', data={'open_id': open_id})
    return result_format()


@api.route('/refresh_token/')
@auth.login_required
def refresh_token():
    """刷新token"""
    # iat = g.token_payload.get('iat')
    # if time.time() - time.mktime(time.localtime(iat)) > 6000:
    #     user = User.query.filter_by(id=g.user['id']).first()
    #     return common.result_format(data={'token': user.generate_token(), 'user_info': user.info()})
    # else:
    #     return common.result_format(error_code=4008, message='token refresh failure!')


@api.route('/registered/', methods=['POST'])
def registered():
    """注册成为厂家"""


@api.route('/factory/info/')
@login()
def factory_info():
    """厂家信息查询"""
    # user = User.query.filter_by(id=g.user['id']).first_or_404()
    # return common.result_format(data=user.info(remove={'genre'}))


@api.route('/factory/info/edit/', methods=['POST'])
@login()
def factory_info_edit():
    """厂家信息修改"""
    # user = User.query.filter_by(id=g.user['id']).first_or_404()
    # form = validators.FactoryEditForm(user=user).validate_()
    #
    # user.set_attrs(form.data).direct_update_()
    # return common.result_format(data=user.info(remove={'genre'}))
