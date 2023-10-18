import functools
from flask import url_for, redirect, request, render_template as render, g
from app import auth, app
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

# @admin.route("/authenticate/", methods=["GET", "POST"])
# def authenticate():
# 	form = AdminLoginForm()
# 	if form.validate_on_submit():
# 		username = form.username.data
# 		password = form.password.data
# 		user = User.query.filter_by(username=username).first()
# 		if user and user.check_pass(password):
# 			token = Token.gen_token(user.pk)
# 			return jsonify({
# 				"refresh_token":token,
# 				"is_admin": user.is_admin
# 				})
# 	return render("/admin/authenticate.html", form=AdminLoginForm())

admin.add_url_rule("/authenticate/", view_func=AdminLoginView.as_view("authenticate"))
admin.add_url_rule("/register-admin-user/", view_func=AdminSignUpView.as_view("sign-up"))

@admin.route("/register-user/")
def register_user():
	return render("admin/register.html", form=forms)



@admin.route("/add-form/", methods = ["GET", "POST"])
def add_form():
	return render("admin/addform.html")

@admin.route("/add-subject-waec/", methods = ["GET", "POST"])
def add_subject():
    """A request view that accept a request argument s and add it to the database
       Note: It is to keep It only adds subject to the database
    """
    return render("admin/subject.html")

@admin.route("/grade-add/", methods=["POST", "GET"])
def grade_point():
	return render("admin/addgrade.html")



@admin.after_request
def admin_last_seen(resp):
	if auth.current_user() and auth.current_user().is_admin:
		auth.current_user().save_last_seen()
	return resp