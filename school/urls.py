from flask import (render_template as render,
                flash, request, make_response,
                jsonify, redirect, abort, url_for)
from forms import AddCourseForm, AddSubjectForm
from models import Course, WaecSubject, Grade, AdminJamb, Subject, User
from app import auth, db
from utils.main import user_logged_in
from . import school

@auth.verify_token
def verify_password(token):
    if token:
        print(token)
        import jwt
        from models import User, Token
        user_id = Token.decode_token(token)["id"]
        if user_id:
            return User.query.get(int(user_id))

@school.route("/")
@user_logged_in
def index():
    from forms import CourseForm
    form = CourseForm()
    return redirect(url_for("school.match"))
    return render("index.html")

@school.route("/add-form/", methods = ["GET", "POST"])
@auth.login_required()
def add_form():
    form = AddCourseForm()
    if form.validate_on_submit():
        course_title = form.course_name.data.title()
        print(course_title)
        jamb_score = int(form.jamb_score.data)
        field1 = form.field1.data.title()
        grade_1 = form.grade_1.data
        field2 = form.field2.data.title()
        grade_2 = form.grade_2.data
        field3 = form.field3.data.title()
        grade_3 = form.grade_3.data
        field4 = form.field4.data.title()
        grade_4 = form.grade_4.data
        field5 = form.field5.data.title()
        grade_5 = form.grade_5.data
        # field6 = form.field6.data.title()
        # grade_6 = form.grade_6.data
        # field7 = form.field7.data.title()
        # grade_7 = form.grade_7.data
        # field8 = form.field8.data.title()
        # grade_8 = form.grade_8.data
        # field9 = form.field9.data.title()
        # grade_9 = form.grade_9.data
        course = Course(course_title=course_title)
        jamb = AdminJamb(min_score = jamb_score, course = course)
        c_sub = [
                WaecSubject(course=course, name=field1,
                         grade=Grade.query.filter_by(point=grade_1).first()),
                WaecSubject(course=course, name=field2,
                         grade=Grade.query.filter_by(point=grade_2).first()),
                WaecSubject(course=course, name=field3,
                         grade=Grade.query.filter_by(point=grade_3).first()),
                WaecSubject(course=course, name=field4,
                         grade=Grade.query.filter_by(point=grade_4).first()),
                WaecSubject(course=course, name=field5,
                         grade=Grade.query.filter_by(point=grade_5).first()),
                # WaecSubject(course=course, name=field6,
                #          grade=Grade.query.filter_by(point=grade_6).first()),
                # WaecSubject(course=course, name=field7,
                #          grade=Grade.query.filter_by(point=grade_7).first()),
                # WaecSubject(course=course, name=field8,
                #          grade=Grade.query.filter_by(point=grade_8).first()),
                # WaecSubject(course=course, name=field9,
                #          grade=Grade.query.filter_by(point=grade_9).first())
            ]

        db.session.add(course)
        db.session.add(jamb)
        db.session.commit()
        db.session.add_all(c_sub)
        db.session.commit()
        flash(f"{form.course_name.data} added successfully", "info")
        return redirect("/")
        # except IntegrityError:
        #     flash(f"{form.course_title} is already created", "warning")
        # else:
        #     flash("DatabaseError", "error")

    return render("addform.html", form=form)

@school.route("/add-subject-waec/", methods = ["GET", "POST"])
@auth.login_required
def add_subject():
    """A request view that accept a request argument s and add it to the database
       Note: It is to keep It only adds subject to the database
    """
    form = AddSubjectForm()
    if request.method == "POST" and request.is_json:
        print(dir(request))
        subject = request.args.get("s")
        if subject:
            wsub = Subject(name=subject.title()) #Adds the subject to the database and it makes sure it starts with a capital letter
            try:
                db.session.add(wsub)
                db.session.commit()
            except:
                return make_response(jsonify(added = False), 200)
            return make_response(jsonify(added = True), 201)
    elif form.validate_on_submit():
        subject = form.name.data.title()
        wsub = Subject(name=subject.title()) #Adds the subject to the database and it makes sure it starts with a capital letter
        try:
            db.session.add(wsub)
            db.session.commit()
            flash(f"{subject} added !", "success")
        except:
            flash('DatabaseError')
    return render("subject.html", form = form )
    
@school.route("/match-course/")
@auth.login_required
def match():
    from forms import MatchForm

    from models import Course
    form = MatchForm()
    if form.validate_on_submit():
        course = form.course.data
        jamb = form.jamb.data
        first = form.field1.data
        second = form.field2.data
        third = form.field3.data
        fourth = form.field4.data
        fifth = form.field5.data
        course_mod = Course.query.filter_by(course_title = course).first()
        if course.is_full:
            return jsonify(course={
                   "full":True,
                   "score":80
                })
        if course:
            resp = {
                "course": true
            }
        print(dir(request))
    return render("match.html", form=form)
@school.route("/course/")
@auth.login_required
def cause():
    from models import Course
    course = request.args.get("c")
    course = Course.query.filter_by(course_title=course).first()
    if course:
        return {
            "subject":[{sub.name:sub.grade.point} for sub in course.waec],
            "score":course.jamb.min_score,
        }
    abort(404)


@school.route("/grade-course/")
@auth.login_required
def course_grade():
    return render("grading.html")

@school.route("/grade-add/", methods=["POST", "GET"])
@auth.login_required
def grade_point():
    from models import Grade
    from forms import AddGradeForm
    form = AddGradeForm()
    if form.validate_on_submit():
        grade = Grade(grade=form.grade.data, point=form.point.data)
        db.session.add(grade)
        db.session.commit()
        flash(f"Grade {grade.grade} added successfully!", "info")
        return redirect("/")
    return render("addgrade.html", form=form)
