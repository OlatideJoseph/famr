from flask import (render_template as render,
                flash, request, make_response,
                jsonify, redirect, abort, url_for)
from werkzeug.security import generate_password_hash as gph
from forms import UserLoginForm, UserCreationForm
from models import User, Token, UserRole
from app import db, auth
from . import users




xhr = "X-Requested-With"
xhr_val = "XMLHttpRequest"

@users.route("/login/", methods = ["GET", "POST"])
def login():
    form = UserLoginForm()
    headers = {"Content-Type":"application/json"}
    #creates an auth token if the request is an 
    if (request.method == "POST") and (request.headers.get(xhr) == xhr_val+'ehghj'):
        js_data = request.get_json()
        u = js_data['username']
        usr = User.query.filter_by(username=u).first()
        if usr and usr.check_pass(js_data["password"]):

            token = Token.gen_token(usr.pk)
            tock = Token(token=token, user=usr)
            db.session.add(tock)
            db.session.commit()
            return {
                "refresh_token": token,
                "msg": ["User logged successfully","info"],
                "is_admin": usr.is_admin,
                "code": 200
                }
        return {
            "code": 401,
            "msg": ["Invalid User Credentials ", "warning"]
        }, 401
    #validates based on form and gen token
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        usr = User.query.filter_by(username=username).first()
        if len(usr.active_token()) < 3:#Only authenticate if token is less than 3
            if usr and usr.check_pass(password):

                token = Token.gen_token(usr.pk)
                tock = Token(token=token, user=usr)
                db.session.add(tock)
                db.session.commit()
                return make_response({
                    "refresh_token": token,
                    "msg": ["User logged successfully","info"],
                    "code": 200,
                    "redirect": url_for('school.index')
                    }, 200, headers)
                
            return make_response({
                "code": 401,
                "msg": ["Invalid User Credentials ", "warning"],
                "redirect": "/login"
            }, 401, headers)
        return make_response({
                "code": 401,
                "msg": ["You are logged in on three device", "error"],
                "redirect": "/login"
            }, 401, headers)
    return render("login.html", form=form)



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
            user  = User(username=username, password=password, role=role)
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
        last_name = form.first_name.data.title()
        birth_date = form.birth_date.data
        password = form.password.data
        hashed = gph(password)
        user = User(username=username, email=email,
            password=hashed, first_name=first_name,
            last_name=last_name,birth_date=birth_date, role=role)
        mid_name = form.middle_name.data
        if mid_name:
            user.mid_name = mid_name.title()
        db.session.add(user)
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
    Token.log_out_from(auth.token)
    return render("logout.html")