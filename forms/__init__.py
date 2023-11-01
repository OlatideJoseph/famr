from flask import Blueprint

form = Blueprint("forms", __name__)

from .forms import (MatchForm, AddSubjectForm, CourseForm,
					UserCreationForm, UserLoginForm, AddCourseForm, AddGradeForm,
					AdminLoginForm, AdminSignUpForm, EditProfileForm, ImageForm,
					EditBioDataForm)