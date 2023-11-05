from flask import (render_template as render,
                flash, request, make_response,
                jsonify, redirect, abort, url_for)
from werkzeug.security import generate_password_hash as gph
from forms import UserLoginForm, UserCreationForm
from models import User, Token, UserRole, Level
from main import auth
from views import (LoginView, SignUpView,
                   ProfileView, EditProfileView,
                   ProfileImageView, EditBioDataView)
from . import users


xhr = "X-Requested-With"
xhr_val = "XMLHttpRequest"

#class based views
users.add_url_rule("/login/", view_func=LoginView.as_view("login"))
users.add_url_rule("/sign-up/", view_func=SignUpView.as_view('sign_up'))
users.add_url_rule("/profile/", view_func=ProfileView.as_view('profile'))
users.add_url_rule("/edit/profile/<string:prn>/",
                   view_func=EditProfileView.as_view('edit_profile'))
users.add_url_rule("/edit/profile/image/<int:id>/",
                   view_func=ProfileImageView.as_view("edit_image"))
users.add_url_rule("/edit/profile/bio/data/", view_func=EditBioDataView.as_view("edit_bio"))

#function based views
@users.route("/list-users/")
@auth.login_required
def list_users():
    return jsonify(
        users=[user.username for user in User.query.all()]
    )

@users.route("/log-out/")
@auth.login_required
def log_out():
    auth = request.args.get('token')
    if auth:
        Token.log_out_from(auth)
        return make_response(jsonify(msg="Logged out successfully !", code=200), 200)
    return jsonify(msg = "An error occured !", status="danger")