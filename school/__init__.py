from flask import Blueprint

school = Blueprint("school", __name__)

from . import urls