from flask import Blueprint

model = Blueprint("models", __name__)

from .models import (User, Token, Subject,
				WaecSubject, Course, Grade, UploadedCsv, CourseCategory,
				Subject, AdminJamb, UserRole, Level, UserBioData)