from collections import Counter
from flask import redirect, url_for, request, Response, abort
from main import auth, BASE_DIR
from models import Course
from PIL import Image
import functools
import threading
import secrets
import os
import csv

recorder = []
def duplicate(val: list) -> list:
    pass

def list_available_course():
    pass


def user_logged_in(func):
    """\
        A function decorators that check if a user is logged in
        and redirect them to the match and to the login page otherwise
    """
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        if not auth.current_user():
            return redirect(url_for('users.login'))
        return func(*args, **kwargs)
    return inner_func


def admin_protected(func):
    def inner_func(*args, **kwargs):
        if auth.current_user().is_admin:
            pass
        else:
            abort(403)
        return func(*args, **kwargs)

def save_csv_file(obj: bin, path: str,
                filename: str = secrets.token_hex() + '.csv') -> bool:
    """\
        Save a csv file to users csv folder
    """
    path = path + "/static/users/csv/"
    filename = os.path.join(path, filename)
    obj.save(filename)

    return True

def get_point(grade):
    """\
        A function to get a single grade point
    """
    grades = {
        "A1": 8,
        "B2": 7,
        "B3": 6,
        "C4": 5,
        "C5": 4,
        "C6": 3
    }
    g = grades.get(grade, 0)
    return  g

def process_csv_file(path: str, to: str, name: str) -> bool:
    """\
        Process the csv and save it in the
        processed csv folder 
        By following this order
        Name,Score,Qualified,Reason
    """
    courses_count = {
                        course.course_title: 0 for course in Course.query.all()
                    }# adds all courses to take their count
    with open(path, 'r+', encoding="utf-8") as f:#open file that's being read
        reader = csv.DictReader(f)
        fname = to + "/processed_" + name #where the file will be saved
        with open(fname, "w", encoding="utf-8") as pf:
            writer = csv.writer(pf)
            writer.writerow(
                [
                    'Full Name', 'Jamb', 'Course', 'subject1', 'grade1',
                    'subject2', 'grade2', 'subject3', 'grade3',
                    'subject4', 'grade4', 'subject5', 'grade5',
                    "score", "Qualified", "Why",
                ]
            )
            for row in reader:
                subjects = [
                    row.get('subject1').title(),
                    row.get('subject2').title(),
                    row.get('subject3').title(),
                    row.get('subject4').title(),
                    row.get('subject5').title(),
                ]
                grades = [
                    row.get('grade1'),
                    row.get('grade2'),
                    row.get('grade3'),
                    row.get('grade4'),
                    row.get('grade5'),
                ]
                point = tuple(map(lambda x: get_point(x.title()), grades))
                waec = sum(point)
                jamb = int(row.get("jamb")) * 0.15
                score = (waec + jamb)
                prow = [
                    row.get('full_name'), row.get('jamb'), row.get('course'),
                    row.get('subject1'), row.get('grade1'), row.get('subject2'),
                    row.get('grade2'), row.get('subject3'), row.get('grade3'),
                    row.get('subject4'), row.get('grade4'), row.get('subject5'),
                    row.get('grade5'), score,
                ]
                course = Course.query.filter_by(course_title=row.get("course")).first()
                if course:
                    max_cand = course.max_candidate
                    waec_sub = course.waec
                    sub_match = list(map(lambda x: (x.name in subjects), waec_sub))
                    title = course.course_title
                    if all(sub_match):
                        if course.great(score):
                            if courses_count[title] < max_cand:
                                courses_count[title] += 1 
                                prow.append("Yes")
                                prow.append("Passed Gracefully")
                            else:
                                prow.append("Yes, but class is filled")
                                prow.append("""\
                                                Passed but department is filled, click on recommend for other courses
                                            """.strip())
                        else:
                            prow.append("No")
                            prow.append("Subject combination matched  but score was low")
                    else:
                        prow.append("No")
                        prow.append("There's an error with subject combination")
                else:
                    prow.append("No")
                    prow.append("Course Does Not Exist")
                writer.writerow(prow)
                print(courses_count)
            pf.close()
        f.close()

def process_csv_file_parallel(path: str, to: str, name: str):
    p = threading.Thread(target=process_csv_file, args=(path, to, name))
    r = p.run()

    if r:
        return p

class AcceptedImage:
    """
        it is a class meant to mimick the image module and
        improve it
    """
    def __init__(self, byt, size: list[tuple, list] = (480, 480)):
        self.image = byt
        self.convert_image(size)

    def generate_random_image_names(self) -> str:
        """
            generates random names for the image
        """
        return secrets.token_hex(10)+".jpg"

    def convert_image(self, size: tuple):
        """
           converts the image size to the given size
        """
        self.size = size
        self.img = Image.open(self.image)
        self.img.thumbnail(size)
        return self

    def save_image(self, loc: str ='default') -> bool:
        if loc == 'default':
            name = self.generate_random_image_names()
            self.filename = name
            path = os.path.join(BASE_DIR+'/static/img/users', name)
            self.img.save(path)
            return True
        else:
            name = self.generate_random_image_names()
            self.filename = name
            path = os.path.join(loc, name)
            self.img.save(path)
            return True
        return False
