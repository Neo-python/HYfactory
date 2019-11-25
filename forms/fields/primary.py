"""整个项目都会使用到的字段存放在这里"""
import wtforms
from wtforms.validators import DataRequired, Length
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM


class FactoryNameField:
    """厂家名称字段"""
    name = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '厂方名称')),
        Length(max=50, message=VM.say('length', '厂方名称', 1, 50))
    ])


class LLField:
    """经纬度字段"""
    longitude = wtforms.FloatField(validators=[DataRequired(message=VM.say('required', '经度'))])
    latitude = wtforms.FloatField(validators=[DataRequired(message=VM.say('required', '纬度'))])


class AddressField:
    """厂家地址"""
    address = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '地址')),
        Length(max=255, message=VM.say('length', '地址', 1, 255))
    ])
    address_replenish = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '地址补充')),
        Length(max=255, message=VM.say('length', '地址补充', 1, 255))
    ])
