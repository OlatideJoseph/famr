from flask import (render_template as render,
                flash, request, make_response,
                jsonify, redirect, abort, url_for)
from werkzeug.security import generate_password_hash as gph
from forms import UserLoginForm, UserCreationForm
from models import User, Token, UserRole, Level
from app import db, auth
from views import LoginView
from . import users




xhr = "X-Requested-With"
xhr_val = "XMLHttpRequest"

#class based views
users.add_url_rule("/login/", view_func=LoginView.as_view("login"))

#function based views
@users.route("/sign-up/", methods=["POST", "GET"])
def sign_up():
    form = UserCreationForm()
    headers = {
        "Content-Type": "application/json"
    }
    role = UserRole.query.filter_by(name="users").first()

    if ((request.method == "POST") and (
        request.headers.get(xhr) == xhr_val)):
        js = request.get_json()
        username = js.get("username")
        first_name = js.get("first_name")
        last_name = js.get("last_name")
        mid_name = js.get("middle_name")
        birth_date = js.get("birth_date")
        password = gph(js.get("auth"))
        if username and password:
            user  = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
        return make_response({
            "msg": [
                f"User {username} added successfully !", "success"
            ], 
            "code": 201,
            "redirect": url_for("users.login")
        }, 201, headers)
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        first_name = form.first_name.data.title()
        last_name = form.last_name.data.title()
        birth_date = form.birth_date.data
        password = form.password.data
        hashed = gph(password)
        user = User(username=username, email=email,
            password=hashed, first_name=first_name,
            last_name=last_name,birth_date=birth_date)
        mid_name = form.middle_name.data
        if mid_name:
            user.mid_name = mid_name.title()

        level = Level(role=role, user=user)
        db.session.add(user)
        db.session.add(level)
        db.session.commit()
        flash(f"User {username} added successfully !", "success")
    return render("signup.html", form=form)


@users.route("/list-users/")
@auth.login_required
def list_users():
    return jsonify(
        users=[user.username for user in User.query.all()]
    )

@users.route("/log-out/")
@auth.login_required
def log_out():
    auth = request.authorization
    print(auth.token)
    Token.log_out_from(auth.token)
    return render("logout.html")