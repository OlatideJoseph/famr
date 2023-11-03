from flask import Blueprint

view = Blueprint("views", __name__)

from .views import (LoginView, AdminLoginView, SignUpView,
					AdminSignUpView, ProfileView, EditProfileView,
                    ProfileImageView, EditBioDataView)
