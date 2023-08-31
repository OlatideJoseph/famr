from flask import (Flask, render_template as render,
                flash, request, make_response,
                jsonify, redirect, abort, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy.exc import IntegrityError

naming_convention = {
    "ix": 'ix_%(column_0_lablel)s',
    "uq": 'uq_%(table_name)s_%(column_0_name)s',
    "ck": 'ck_%(table_name)s_%(column_0_name)s',
    "fk": 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    "pk": 'pk_%(table_name)s',
}

app = Flask(__name__)
app.config["SECRET_KEY"] = "8b9562889f24968e91ebdb6c2af18ba8cada1b34cfcccb1c64b5db118bf67143"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
app.config["SQLALCHEMY_COMMIT_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
meta = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth(app)
import models
# @app.shell_context_processor
# def context_processor():
#     return {""}

@app.before_request
@auth.login_required
def authenticate():
    pass

@auth.verify_password
def verify_password(user, password):
    pass
@app.route("/")
def index():
    from forms import CourseForm
    form = CourseForm()
    return redirect(url_for("match"))
    return render("index.html")

@app.route("/add-form/", methods = ["GET", "POST"])
def add_form():
    from forms import AddCourseForm
    from models import Course, WaecSubject, Grade, AdminJamb
    form = AddCourseForm()
    print(form.errors)
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

@app.route("/add-subject-waec/", methods = ["GET", "POST"])
def add_subject():
    """A request view that accept a request argument s and add it to the database
       Note: It is to keep It only adds subject to the database
    """
    from models import Subject
    from forms import AddSubjectForm
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
    
@app.route("/match-course/")
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
@app.route("/course/")
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


@app.route("/grade-course/")
def course_grade():
    return render("grading.html")

@app.route("/grade-add/", methods=["POST", "GET"])
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

if __name__ == "__main__":
    app.run(debug = True)

