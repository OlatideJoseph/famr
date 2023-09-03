from flask import Blueprint

model = Blueprint("models", __name__)

from .models import (User, Token, Subject,
				WaecSubject, Course, Grade,
				Subject, AdminJamb)