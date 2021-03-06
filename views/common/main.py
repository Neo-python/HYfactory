import config
import uuid
from flask import request, g
from views.common import api
from init import client, Redis, sms, cos_sts
from plugins.HYplugins.common import ordinary
from plugins.HYplugins.common.authorization import login, auth
from plugins.HYplugins.error import ViewException


@api.route('/user/list/')
def user_list():
    """用户列表"""


@api.route('/upload_url/')
@auth.login_required
def upload_url():
    """获取上传图片授权地址"""
    # genre = request.args.get('genre', default=None)
    # suffix = request.args.get('suffix', default=None)
    #
    # if not genre and not suffix:
    #     raise ViewException(error_code=4005, message='<genre>图片用途类型或<suffix>图片文件类型,不能为空.')
    # name = uuid.uuid1().hex
    # path = f'/test/{name}.{suffix}'
    # url = client.get_presigned_url(config.Bucket, path, Method='POST')
    # image_url = f'{config.cos_base_url}{path}'
    # Images(user_id=g.user['id'], url=image_url, genre=genre, status=0).direct_commit_()
    # return common.result_format(data={'upload_url': url, 'image_url': image_url})


@api.route('/upload_credentials/')
@auth.login_required
def upload_credentials():
    """腾讯cos上传凭证
    文档:https://github.com/tencentyun/qcloud-cos-sts-sdk/tree/master/python
    """
    result = cos_sts.get_credential()
    data = result['credentials']
    data.update({'expiredTime': result['expiredTime']})
    return ordinary.result_format(data=data)


@api.route('/send_sms/code/', methods=['POST'])
def send_sms():
    """发送短信接口
    params:统一规范 验证码 + 时效(分钟)
    """
    # form = validators.SMSCodeForm().validate_()
    # code = ordinary.generate_verify_code()
    # key = f'validate_phone_{form.genre.data}_{form.phone_number.data}'
    # Redis.set(key, code, ex=3000)  # 设置缓存
    # sms.send(template_id=config.SMS_TEMPLATE_REGISTERED[form.genre.data], phone_number=form.phone_number.data,
    #          params=[code, 5])
    # return ordinary.result_format()
