from datetime import date
from flask import (render_template as render,
                flash, request, make_response,
                jsonify, redirect, abort, url_for, Response)
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from forms import AddCourseForm, AddSubjectForm, MatchForm, AddGradeForm
from models import Course, WaecSubject, Grade, AdminJamb, Subject, User, Token
from main import auth, db
from utils.main import user_logged_in
from . import ajax


xhr = 'X-Requested-With'
xhr0 = 'XMLHttpRequest'

def admin_protected_view(user):
    admin_user = user #Note the variable name denote the person using this route is an admin
    if admin_user and admin_user.is_admin:
        return True
    elif admin_user and  (admin_user.is_admin != True):
        print("if")
        flash("User: {admin_user.username} is not an admin, login with an admin account", "warning")
        return redirect(url_for("admin.authenticate"))
    else:
        print("else")
        return redirect(url_for("admin.authenticate"))


@ajax.route("/admin/add-form/", methods = ["GET", "POST"])
@auth.login_required()
def add_form():
    protected = admin_protected_view(auth.current_user())
    if protected:
        if isinstance(protected, Response):
            return protected
    form = AddCourseForm()
    if request.method == "POST" and request.headers.get(xhr) == xhr0:
        #data variable
        data = request.get_json()
        course_title = data["course_name"].title()
        jamb_score = int(data["jamb_score"])
        field1 = data["field1"].title()
        grade_1 = data["grade_1"]
        field2 = data["field2"].title()
        grade_2 = data["grade_2"]
        field3 = data["field3"].title()
        grade_3 = data["grade_3"]
        field4 = data["field4"].title()
        grade_4 = data["grade_4"]
        field5 = data["field5"].title()
        grade_5 = data["grade_5"]
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
        ]
        course.min_aggr = course.aggr()
        #database operation
        db.session.add(course)
        db.session.add(jamb)
        db.session.commit()
        db.session.add_all(c_sub)
        db.session.commit()

        return make_response({
            "msg": f"{data['course_name']} added successfully",
            "status": "success",
            "code": 201,
            }, 201,
            {"Content-Type":"application/json"})
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
        ]
        course.min_aggr = course.aggr()
        db.session.add(course)
        db.session.add(jamb)
        db.session.commit()
        db.session.add_all(c_sub)
        db.session.commit()

        return make_response({
            "msg": f"{form.course_name.data} added successfully",
            "status": "success",
            "code": 201,
            }, 201,
            {"Content-Type":"application/json"})
        # except IntegrityError:
        #     flash(f"{form.course_title} is already created", "warning")
        # else:
        #     flash("DatabaseError", "error")

    return render("ajax/addform.html", form=form)

@ajax.route("/admin/add-subject-waec/", methods = ["GET", "POST"])
@auth.login_required
def add_subject():
    """A request view that accept a request argument s and add it to the database
       Note: It is to keep It only adds subject to the database
    """
    protected = admin_protected_view(auth.current_user())
    if protected:
        if isinstance(protected, Response):
            return protected
    form = AddSubjectForm()
    if ((request.method == "POST") and (request.headers.get(xhr) == xhr0)):
        subject = request.get_json()["subject"]
        print(subject)
        if subject:
            if type(subject) is list:
                wsub_list = [Subject(name=sub.title()) for sub in subject]
            else:
                #Adds the subject to the database and it makes sure it starts with a capital letter
                wsub = Subject(name=subject.title())
            try:
                if type(subject) == list:
                    db.session.add_all(wsub_list)
                else:
                    db.session.add(wsub)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return make_response(jsonify(
                    added = False,
                    msg= [f"The subject '{subject}' already exist !", "warning"]
                ))
            except PendingRollbackError:
                db.session.rollback()
                return make_response(jsonify(
                    added = False,
                    msg= [f"The subject '{subject}' already exist !", "warning"]
                ))
            except:
                return make_response(jsonify(added=False, msg=f"DatabaseError"), 200)
            return make_response(jsonify(
                    added=True, redirect=url_for("school.match"),
                    msg=[f"Subject '{subject}' added successfully", "success"]
                ), 201)
    elif form.validate_on_submit():
        subject = form.name.data.title()
        #Adds the subject to the database and it makes sure it starts with a capital letter
        wsub = Subject(name=subject.title())
        try:
            db.session.add(wsub)
            db.session.commit()
            flash(f"{subject} added !", "success")
        except:
            db.session.rollback()
            flash('DatabaseError')
    return render("ajax/subject.html", form = form )
    
@ajax.route("/match-course/")
@auth.login_required
def match():
    form = MatchForm()
    user_obj = auth.current_user()
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
                "course": True
            }
        print(dir(request))
    return render("ajax/match.html", form=form, user=user_obj)

@ajax.route("/course/")
@auth.login_required
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


@ajax.route("/grade-course/")
@auth.login_required
def course_grade():
    return render("ajax/grading.html")

@ajax.route("/admin/grade-add/", methods=["POST", "GET"])
@auth.login_required
def grade_point():
    form = AddGradeForm()
    protected = admin_protected_view(auth.current_user())
    if protected:
        if isinstance(protected, Response):
            return protected
    if form.validate_on_submit():
        grade = Grade(grade=form.grade.data, point=form.point.data)
        db.session.add(grade)
        db.session.commit()
        xhr = request.headers.get("X-Requested-With")
        print(xhr)
        if xhr == "XMLHttpRequest":
            return {
                "msg": [f"The grade '{grade.grade}' added successfully", "success"],
                "redirect": url_for("school.match")
            }
        flash(f"Grade {grade.grade} added successfully!", "info")
        return redirect("/")
    print(form.errors)
    return render("ajax/addgrade.html", form=form)

@ajax.route("/get-auth-data/")
@auth.login_required
def get_data():
    user = auth.current_user()
    data = {
        "id": user.pk,
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "dob": user.birth_date.strftime("%d-%m-%Y"),
        "mid_name": user.mid_name,
        "is_admin": user.is_admin,
        "age": (date.today().year - user.birth_date.year),
        "img_path": user.image_path,
        #bio data: they only have value if they've been created
        "jamb_reg": user.bio_data.jamb_reg if user.bio_data else None,
        "waec_id": user.bio_data.waec_id if user.bio_data else None,
    }
    return jsonify(**data)

@ajax.route("/get-user-all-data/")
def get_all_user():
    '''\
        This view function is meant for the admin user only
        it returns all the user in the database
    '''
    per_page = 3
    page = request.args.get('page', type=int)
    page = page if page else 1
    obj =  User.query.\
                order_by(User.username.asc()).\
                    paginate(per_page=per_page, page=page)
    userlist = {
        user.username:{
            "id": user.pk,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "dob": user.birth_date.strftime("%d-%m-%Y"),
            "mid_name": user.mid_name,
            "is_admin": user.is_admin,
            "age": (date.today().year - user.birth_date.year),
            "img_path": user.image_path,
            #bio data: they only have value if they've been created
            "jamb_reg": user.bio_data.jamb_reg if user.bio_data else None,
            "waec_id": user.bio_data.waec_id if user.bio_data else None,
        } for user in obj.items
    }
    userlist['next'] = obj.has_next
    userlist['prev'] = obj.has_prev
    userlist['page'] = page
    return userlist

@ajax.route("/get-grade-and-point/")
@auth.login_required
def ajx_grade():
    grades_choice = [[grd.point, grd.grade] for grd in Grade.query.all() if grd]
    return jsonify(grades_choice)

@ajax.route("/get-course-data/")
@auth.login_required
def ajx_course():
    course_choice = [[sub.course_title, sub.course_title] for sub in Course.query.all() if sub]
    return jsonify(course_choice)

@ajax.route("/get-subject-data/")
@auth.login_required
def ajx_subject():
    return jsonify([
        (sub.name, sub.name) for sub in \
                Subject.query.order_by(Subject.name.asc()).all() if sub]
        )

@ajax.after_request
def user_required_config(resp):
    if auth.current_user():
        auth.current_user().save_last_seen()
    return resp