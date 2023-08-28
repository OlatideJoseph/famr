from app import db

class BaseMixin:
    _id = db.Column(db.Integer, primary_key=True)
    @property
    def pk(self):
        return self._id
    def __repr__(self):
        return f"{self.__class__.__name__} <{self.pk}>"

class Course(db.Model, BaseMixin):
    __tablename__  = "course"
    course_title = db.Column(db.String(50), nullable = False, unique = True)
    course_code = db.Column(db.Integer, unique = True)
    field1 = db.Column(db.String(2), nullable = False)
    field2 = db.Column(db.String(2), nullable = False)
    field3 = db.Column(db.String(2), nullable = False)
    field4 = db.Column(db.String(2), nullable = False)
    field5 = db.Column(db.String(2), nullable = False)
    field6 = db.Column(db.String(2), nullable = False)
    field7 = db.Column(db.String(2), nullable = False)
    field8 = db.Column(db.String(2), nullable = True)
    field9 = db.Column(db.String(2), nullable = True)

    waec_id = db.Column(db.Integer, db.ForeignKey('waecsubject._id'), nullable=False)

    def __repr__(self):
        return "Lasustech <%s> Course" %(self.course_title)


class WaecSubject(db.Model, BaseMixin):
    __tablename__ = "waecsubject"
    name = db.Column(db.String(50), nullable = False)
    course = db.relationship(Course, backref="waecsubject", lazy=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade._id'))

    def __repr__(self):
        return "%s %s" %(self.name, self._id)

class Subject(db.Model, BaseMixin):
    __tablename__ = "subject"
    name = db.Column(db.String, nullable=False, unique=True)

class Grade(db.Model, BaseMixin):
    __tablename__ = "grade"
    grade = db.Column(db.String(2), nullable=False, default="A1", unique=True)
    point = db.Column(db.Float, nullable=False, default=4.00)
    waec = db.relationship(WaecSubject, backref="grade", lazy=True)
