from sqlalchemy.exc import IntegrityError
from flask import (render_template as render,
                flash, request, make_response, current_app,
                jsonify, redirect, abort, url_for, Response)
from forms import (AddCourseForm,
                    AddSubjectForm, MatchForm,
                    AddGradeForm, MatchFileForm)
from models import (Course, WaecSubject, Grade, AdminJamb,
                        Subject, User, Token, UploadedCsv)
from utils import save_csv_file, process_csv_file_parallel as pcfp
from main import auth, db
from . import school
import secrets
import os

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

@school.route("/offered-courses/")
def offer():
    page = request.args.get("page", 1, type=int)
    courses = Course.query.order_by(Course.course_title.asc()).paginate(page=page).items
    return render("courses.html", courses=courses)

@school.route("/match-course-file/", methods=["GET", "POST"])
def match_file():
    form = MatchFileForm()
    if form.validate_on_submit():
        user_id = request.args.get("_id", 1, type=int)
        user = User.query.get(user_id)
        if user:
            file = form.file_csv.data
            name = secrets.token_hex() + '.csv'
            saved = save_csv_file(file, current_app.root_path, filename=name)
            if saved:
                uploaded_csv = UploadedCsv(user=user, filename=name)
                db.session.add(uploaded_csv)
                db.session.commit()
                path = current_app.root_path + '/static/users/'
                r_f = os.path.join(path + 'csv', name)
                to = path + 'processed_csv'
                pcfp(r_f, to, name)
                return make_response(jsonify(
                    msg=["Your file is saved and processed, please check your processed data", "success"]
                ), 201)
            return make_response(jsonify(
                msg=["Sorry an error occured! please try again later", "danger"]
            ), 200)
        return make_response(jsonify(msg=["Confilict Request Data", "warning"]))
    return render("match_file.html", form=form)
