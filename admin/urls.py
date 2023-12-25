import functools
from flask import url_for, redirect, request, render_template as render, g, make_response, flash
from main import auth
from admin import admin
from models import User, Token
from views import AdminLoginView, AdminSignUpView
from forms import AdminLoginForm



def admin_protected_view(user):
	admin_user = user #Note the variable name denote the person using this route is an admin
	if admin_user and  (admin_user.is_admin != True):
		flash("User: {admin_user.username} is not an admin, login with an admin account", "warning")
		return redirect(url_for("admin.authenticate"))
	else:
		return redirect(url_for("admin.authenticate"))

@admin.route("/")
def home():
	return render("admin/home.html")

admin.add_url_rule("/authenticate/ua/", view_func=AdminLoginView.as_view("authenticate"))
admin.add_url_rule("/register-admin-user/ua/", view_func=AdminSignUpView.as_view("sign_up"))

@admin.route("/add-form/", methods=["GET", "POST"])
def add_form():
	return render("admin/addform.html")

@admin.route("/add-subject-waec/", methods=["GET", "POST"])
def add_subject():
   """\
	   A request view that accept a request argument s and add it to the database
      Note: It is to keep It only adds subject to the database
   """
   return render("admin/subject.html")

@admin.route("/grade-add/", methods=["POST", "GET"])
def grade_point():
	return render("admin/addgrade.html")

@admin.route("/list-users/")
def list_user():
	return render("admin/listuser.html")

@admin.route("/students-exception/")
def sexception():
	return render('admin/exception.html')

@admin.after_request
def admin_last_seen(resp):
	if auth.current_user() and auth.current_user().is_admin:
		auth.current_user().save_last_seen()
	return resp

@admin.route("/get-admin-data/")
def admin_data():
	return make_response({
		"usrno": len(User.query.all())
		},200)