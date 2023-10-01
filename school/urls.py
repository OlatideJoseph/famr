from flask import (render_template as render,
                flash, request, make_response,
                jsonify, redirect, abort, url_for, Response)
from sqlalchemy.exc import IntegrityError
from forms import AddCourseForm, AddSubjectForm, MatchForm, AddGradeForm
from models import Course, WaecSubject, Grade, AdminJamb, Subject, User, Token
from app import auth, db
from utils.main import user_logged_in
from . import school

@auth.verify_token
def verify_password(token):
    if token:
        import jwt
        user_id = Token.decode_token(token)["id"]
        if user_id:
            return User.query.get(int(user_id))

@school.route("/")
def index():
    # from forms import CourseForm
    # form = CourseForm()
    # return redirect(url_for("school.match"))
    return render("index.html")

    
@school.route("/match-course/")
def match():
    # form = MatchForm()
    # if form.validate_on_submit():
    #     course = form.course.data
    #     jamb = form.jamb.data
    #     first = form.field1.data
    #     second = form.field2.data
    #     third = form.field3.data
    #     fourth = form.field4.data
    #     fifth = form.field5.data
    #     course_mod = Course.query.filter_by(course_title = course).first()
    #     if course.is_full:
    #         return jsonify(course={
    #                "full":True,
    #                "score":80
    #             })
    #     if course:
    #         resp = {
    #             "course": true
    #         }
    #     print(dir(request))
    return render("match.html")
@school.route("/course/")
def cause():
    if request.is_json:
        js = request.get_json()
        course = Course.query.filter_by(course_title=js["course"]).first()
        if course:
            return {
                "subject":[{sub.name:sub.grade.point} for sub in course.waec],
                "score":course.jamb.min_score,
            }
    abort(404)


@school.route("/grade-course/")
def course_grade():
    return render("grading.html")

@school.route("/grade-add/", methods=["POST", "GET"])
def grade_point():
    return render("addgrade.html")


