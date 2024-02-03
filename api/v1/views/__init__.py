#!/usr/bin/python3
""" Init file for api/v1
"""

from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.guardians import *
from api.v1.views.students import *
from api.v1.views.teachers import *
from api.v1.views.admins import *
from api.v1.views.index import *