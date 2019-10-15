from views.user import api
from plugins.HYplugins.common import result_format
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
