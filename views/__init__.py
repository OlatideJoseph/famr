from flask import Blueprint

view = Blueprint("views", __name__)

from .views import LoginView, AdminLoginView
