from models.HYModels import business


class FactoryContact(business.FactoryContactBase):
    """厂家订单常用联系人"""


class Order(business.OrderBase):
    """厂家订单"""


class DriverOrder(business.DriverOrderBase):
    """驾驶员订单"""


class DriverOrderScheduleLog(business.DriverOrderScheduleLogBase):
    """驾驶员订单记录"""
