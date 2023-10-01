from flask import (Flask, render_template as render,
                flash, request, make_response,
                jsonify, redirect, abort, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy.exc import IntegrityError

naming_convention = {
    "ix": 'ix_%(column_0_lablel)s',
    "uq": 'uq_%(table_name)s_%(column_0_name)s',
    "ck": 'ck_%(table_name)s_%(column_0_name)s',
    "fk": 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    "pk": 'pk_%(table_name)s',
}


app = Flask(__name__)
app.config["SECRET_KEY"] = "8b9562889f24968e91ebdb6c2af18ba8cada1b34cfcccb1c64b5db118bf67143"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
app.config["SQLALCHEMY_COMMIT_TEARDOWN"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
meta = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPTokenAuth(scheme="Bearer")

from users import users
from admin import admin
from school import school
from ajax import  ajax
from models import model as md
from forms import form as fm

app.register_blueprint(users)
app.register_blueprint(school)
app.register_blueprint(admin, url_prefix="/admin/")
app.register_blueprint(ajax, url_prefix="/ajax/v1.0/")
app.register_blueprint(md, url_prefix="/models/")
app.register_blueprint(fm, url_prefix="/forms/")

import models
#Application shell processor
@app.shell_context_processor
def shell_context_processor():
    return {"db": db, "migrate": migrate, "auth": auth, "models": models}
#Request context processor
@app.context_processor
def context_processor():
    return {"auth":auth}

if __name__ == "__main__":
    app.run(debug = True)