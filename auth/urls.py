from auth import auth as app_auth
from main import auth as login_auth


@app_auth.post("/react-login/")
def react_login():
	return {
		"user": login_auth.current_user.username
	}