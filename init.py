import sys
import config
import logging
from flask import Flask
from pymysql import install_as_MySQLdb
from plugins.HYplugins.sms.main import SMS
from plugins.HYplugins.orm.main import db
from sts.sts import Sts
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# 短信
sms = SMS(app_id=config.SMS_APP_ID, app_key=config.SMS_APP_KEY)
# 应用
install_as_MySQLdb()
# cos
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
cos_config = CosConfig(Region=config.region, SecretId=config.SecretId, SecretKey=config.SecretKey, Token=config.token,
                       Scheme=config.scheme)
client = CosS3Client(cos_config)
# cos token
cos_sts = Sts(config.sts_config)


def register_blueprint(app):
    """注册蓝图"""


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    register_blueprint(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all(app=app)
    return app
