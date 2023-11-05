from flask import (render_template as render,
                flash, request, make_response,
                jsonify, redirect, abort, url_for, Response)
from sqlalchemy.exc import IntegrityError
from forms import AddCourseForm, AddSubjectForm, MatchForm, AddGradeForm
from models import Course, WaecSubject, Grade, AdminJamb, Subject, User, Token
from main import auth, db
from utils.main import user_logged_in
from . import school

@auth.verify_token
def verify_password(token):
    if token:
        import jwt
        user_id = Token.decode_token(token)["id"]
        if user_id:
            user = User.query.get(int(user_id))
            if user:
                return user

@school.route("/")
def index():
    # from forms import CourseForm
    # form = CourseForm()
    # return redirect(url_for("school.match"))
    return render("index.html")

    
@school.route("/match-course/")
def match():
    return render("match.html")

@school.route("/course/")
@auth.login_required
def cause():
    arg = request.args.get('c')
    if arg:
        course = Course.query.filter_by(course_title=arg).first()
        if course:
            return {
                "subject":[{sub.name:sub.grade.point} for sub in course.waec],
                "score":course.jamb.min_score,
            }
    abort(404)


@school.route("/grade-course/")
def course_grade():
    return render("grading.html")




