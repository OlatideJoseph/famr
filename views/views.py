from flask import render_template as render, url_for, request, redirect, jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash as gph
from models import User, Token, UserRole
from forms import UserLoginForm, UserCreationForm, AdminLoginForm

xhr = "X-Requested-With"
xhr_val = "XMLHttpRequest"

class LoginView(MethodView):
	template = "login.html"
	form = UserLoginForm

	def get(self):
		return render(self.template, form=self.form())

	def post(self):
		form = self.form()
		headers = {"Content-Type":"application/json"}
		if request.headers.get(xhr) == xhr_val+'ehghj':
			js_data = request.get_json()
			u = js_data['username']
			usr = User.query.filter_by(username=u).first()
			if usr and usr.check_pass(js_data["password"]):
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
				if len(usr.active_token()) < 3:#Only authenticate if token is less than 3
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


class AdminLoginView(LoginView):
	template = "admin/authenticate.html"
	form = AdminLoginForm