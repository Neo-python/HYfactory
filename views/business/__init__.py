"""业务层"""
from flask import Blueprint

api = Blueprint('business', __name__, url_prefix='/business')

from views.business.primary import *
