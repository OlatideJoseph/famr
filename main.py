#!/bin/python3
from flask_wtf.csrf import CSRFProtect as CSRF
from flask import (Flask, render_template as render,
                flash, request, make_response,
                jsonify, redirect, abort, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy.exc import IntegrityError
import click
import os




BASE_DIR = '' 
naming_convention = {
    "ix": 'ix_%(column_0_lablel)s',
    "uq": 'uq_%(table_name)s_%(column_0_name)s',
    "ck": 'ck_%(table_name)s_%(column_0_name)s',
    "fk": 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    "pk": 'pk_%(table_name)s',
}
migrate = Migrate()
db = SQLAlchemy()
auth = HTTPTokenAuth(scheme="Bearer")
csrf = CSRF()

def create_app():
    app = Flask(__name__)
    app.name = 'famr'

    from users import users
    from admin import admin
    from school import school
    from ajax import  ajax
    from views import view
    from models import model as md
    from forms import form as fm
    from utils import Config

    app.config.from_object(Config)
    app.register_blueprint(users)
    app.register_blueprint(school)
    app.register_blueprint(admin, url_prefix="/admin/")
    app.register_blueprint(ajax, url_prefix="/ajax/v1.0/")
    app.register_blueprint(md, url_prefix="/models/")
    app.register_blueprint(view, url_prefix="/views/")
    app.register_blueprint(fm, url_prefix="/forms/")

    global BASE_DIR

    BASE_DIR = app.root_path

    return app

app = create_app()
db.init_app(app)
csrf.init_app(app)
migrate.init_app(app, db)

@app.cli.command("create-default")
def create_default():
    db.create_all()
    from models import UserRole as Role, CourseCategory as Category
    cat = Category.create_default()
    role = Role.create_default()
    if not (role and cat):
        print("* They've been created before")

#Request context processor
@app.context_processor
def context_processor():
    return {"auth": auth}

@auth.error_handler
def forbidden(resp):
    return make_response(
        {
            "user": "forbidden",
            "code": (401,)
        },
            401,
            {"Content-Type":"application/json"})

@app.errorhandler(500)
def internal_error(e):
    return render("admin/500.html"), 500

#Application shell processor
@app.shell_context_processor
def shell_context_processor():
    import models
    return {"db": db, "migrate": migrate, "auth": auth, "models": models}