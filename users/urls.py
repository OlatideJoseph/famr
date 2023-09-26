from flask import (render_template as render,
                flash, request, make_response,
                jsonify, redirect, abort, url_for)
from werkzeug.security import generate_password_hash as gph
from forms import UserLoginForm, UserCreationForm
from models import User, Token
from app import db, auth
from . import users

@users.route("/login/", methods = ["GET", "POST"])
def login():
    form = UserLoginForm()
    headers = {"Content-Type":"application/json"}
    #creates an auth token if the request is an 
    if (request.method == "POST") and (request.is_json):
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
    return render("login.html", form=form)



@users.route("/sign-up/", methods=["POST", "GET"])
def sign_up():
    form = UserCreationForm()
    headers = {
        "Content-Type": "application/json"
    }
    if ((request.method == "POST") and (request.is_json)):
        js = request.get_json()
        username = js.get("username")
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
        password = form.password.data
        hashed = gph(password)
        user = User(username=username, password=password)
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
def log_out():
    return render("logout.html")