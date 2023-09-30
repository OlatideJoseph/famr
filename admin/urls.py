import functools
from flask import url_for, redirect, request, render_template as render
from app import auth
from admin import admin
from forms import AdminLoginForm

def admin_protected_view(func):
	@functools.wraps(func)
	def inner_func(*args, **kwargs):
		admin_user = auth.current_user() #Note the variable name denote the person using this route is an admin
		if admin_user and admin_user.is_admin:
			return func(*args, **kwargs)
		elif admin_user and not (admin_user.is_admin):
			flash("User: {admin_user.username} is not an admin, login with an admin account", "warning")
			return redirect(url_for("admin.authenticate"))
		else:
			return redirect(url_for("admin.authenticate"))
	return inner_func

@admin.route("/")
@admin_protected_view
@auth.login_required
def home():
	return "<h1>Admin Home Page!</h1>"

@admin.route("/authenticate/", methods=["GET", "POST"])
def authenticate():
	form = AdminLoginForm()
	return render("/admin/authenticate.html", form=AdminLoginForm())

@admin.route("/register-user/")
def register_user():
	return render("admin/register.html", form=forms)