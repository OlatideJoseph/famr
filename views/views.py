from flask import render_template as render, url_for, request, redirect, jsonify, make_response, flash
from flask.views import MethodView, View
from werkzeug.security import generate_password_hash as gph
from app import db
from models import User, Token, UserRole, Level
from forms import UserLoginForm, UserCreationForm, AdminLoginForm, AdminSignUpForm, UserCreationForm

xhr = "X-Requested-With"
xhr_val = "XMLHttpRequest"

class SignUpView(View):
	form = UserCreationForm
	methods = ["GET", "POST"]
	def dispatch_request(self):
		form = UserCreationForm()
		headers = {
            "Content-Type": "application/json"
		}
		role = UserRole.query.filter_by(name="users").first()

		if ((request.method == "POST") and (
			request.headers.get(xhr) == xhr_val)):
			pro = self.xhr_form_processor()
			if pro:
				pass
			return make_response({
				"msg": [
					f"User {username} added successfully !", "success"
				], 
				"code": 201,
				"redirect": url_for("users.login")
			}, 201, headers)
		if form.validate_on_submit():
			user = self.process_form(form, role) #processes the form submitted
			if user:
				level = Level(role=role, user=user)
				db.session.add(user)
				db.session.add(level)
				db.session.commit()
				flash(f"User {username} added successfully !", "success")
		return render("signup.html", form=form)

	def process_form(self, form):
		'''A method that process form and returns a user object'''
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
		return user

	def xhr_form_processor(self):
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
		return True


class LoginView(MethodView):
	template = "login.html"
	form = UserLoginForm

	def get(self):
		return render(self.template, form=self.form())

	def post(self):
		form = self.form()
		headers = {"Content-Type":"application/json"}
		if ((request.headers.get(xhr) == xhr_val) and
			(request.headers.get("Content-Type") == "application/json")):
			js_data = request.get_json()
			u = js_data['username']
			usr = User.query.filter_by(username=u).first()
			if usr and usr.check_pass(js_data["password"]):
				if len(usr.active_token()) <= 3:#Only authenticate if token is less than 3
					token = Token.gen_token(usr.pk)
					tock = Token(token=token, user=usr)
					db.session.add(tock)
					db.session.commit()
					return {"refresh_token": token,
						"msg": ["User logged successfully","info"],
						"is_admin": usr.is_admin,
					"code": 200}
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
				if len(usr.active_token()) <= 3:#Only authenticate if token is less than 3
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
				return make_response({"code": 401,
					"msg": ["You are logged in on three device", "danger"],
					"redirect": "/login"},
				 401, headers)
			return make_response({
				"code": 401,
				"msg": ["Invalid User Credentials ", "warning"],
				"redirect": "/login"
			}, 401, headers)
		return make_response({
				"code": 401,
				"msg": ["User not authorized", "danger"],
				"redirect": "/login"
			}, 401, headers)


class AdminLoginView(LoginView):
	template = "admin/authenticate.html"
	form = AdminLoginForm


class AdminSignUpView(SignUpView):
	init_every_request = False
	form = AdminSignUpForm

	def dispatch_request(self):
		form = self.form()
		role = UserRole.query.filter_by(name="users").first()
		role1 = UserRole.query.filter_by(name="admins").first()

		if form.validate_on_submit():
			user = self.process_form(form)
			if user:
				user.is_admin = True
				level0 = Level(role=role, user=user)
				level1 = Level(role=role1, user=user)
				db.session.add_all([user, level1, level0])
				db.session.commit()
				print("added")
				flash(f"User {username} added successfully !", "success")

		if ((request.method == "POST") and (
			request.headers.get(xhr) == xhr_val)):
			pro = self.xhr_form_processor()
			if pro:
				pass

			return make_response({
				"msg": [
					f"User {username} added successfully !", "success"
				], 
				"code": 201,
				"redirect": url_for("admin.login")
			}, 201, headers)

		return render("admin/registration.html", form=form)