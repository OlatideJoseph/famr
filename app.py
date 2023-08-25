from flask import Flask, render_template as render, flash, request, make_response, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
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
db = SQLAlchemy(app, metadata=meta)
migrate = Migrate(app, db)
import models
# @app.shell_context_processor
# def context_processor():
#     return {""}

    
@app.route("/")
def index():
    from forms import CourseForm
    form = CourseForm
    return render("index.html")

@app.route("/add-form", methods = ["GET", "POST"])
def add_form():
    from forms import AddCourseForm
    from models import Course
    form = AddCourseForm()
    print(session)
    print(form.errors)
    if form.validate_on_submit():
        course_title = form.course_name.data.title()
        print(course_title)
        field1 = form.field1.data.title()
        field2 = form.field2.data.title()
        field3 = form.field3.data.title()
        field4 = form.field4.data.title()
        field5 = form.field5.data.title()
        field6 = form.field6.data.title()
        field7 = form.field7.data.title()
        field8 = form.field8.data.title()
        field9 = form.field9.data.title()
        course = Course(course_title = course_title,
                            field1=field1, field2=field2, field3=field3, field4=field4,
                            field5=field5, field6=field6, field7=field7, field8=field8, field9=field9)
        try:
            db.session.add(course)
            db.session.commit()
            flash(f"{form.course_title} added successfully", "info")
            return redirect("/")
        except:
            flash("Course Initialization Error")

    return render("addform.html", form=form)

@app.route("/add-subject-waec/", methods = ["GET", "POST"])
def add_subject():
    """A request view that accept a request argument s and add it to the database
       Note: It is to keep It only adds subject to the database
    """
    from models import WaecSubject
    from forms import AddSubjectForm
    form = AddSubjectForm()
    if request.method == "POST" and request.is_json:
        print(dir(request))
        subject = request.args.get("s")
        if subject:
            wsub = SecondarySubject(name=subject.title()) #Adds the subject to the database and it makes sure it starts with a capital letter
            try:
                db.session.add(wsub)
                db.session.commit()
            except:
                return make_response(jsonify(added = False), 200)
            return make_response(jsonify(added = True), 201)
    elif form.validate_on_submit():
        subject = form.name.data.title()
        wsub = SecondarySubject(name=subject.title()) #Adds the subject to the database and it makes sure it starts with a capital letter
        try:
            db.session.add(wsub)
            db.session.commit()
            flask(f"{subject} added !", "success")
        except:
            flash('DatabaseError')
    return render("subject.html", form = form )
    
@app.route("/match-course")
def match():
    from forms import MatchForm
    form = MatchForm()
    if form.validate_on_submit():
        course = form.course.data
        
    return render("match.html", form=form)
    
@app.route("/grade-course")
def course_grade():
    return render("grading.html")

@app.route("/grade-add")
def grade_point():
    from models import Grade
    from forms import AddGradeForm
    form = AddGradeForm
    grade = Grade(grade=form.grade.data, point=form.point.data)   
if __name__ == "__main__":
    app.run(debug = True)

