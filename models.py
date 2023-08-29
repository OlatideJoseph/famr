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
    waec = db.relationship("WaecSubject", backref="course", lazy=True)

    def __repr__(self):
        return "Lasustech <%s> Course" %(self.course_title)


class WaecSubject(db.Model, BaseMixin):
    __tablename__ = "waecsubject"
    name = db.Column(db.String(50), nullable = False)
    course_id = db.Column(db.Integer, db.ForeignKey('course._id'))
    grade_id = db.Column(db.Integer, db.ForeignKey('grade._id'))

    def __repr__(self):
        return "%s %s" %(self.name, self._id)

class Subject(db.Model, BaseMixin):
    __tablename__ = "subject"
    name = db.Column(db.String, nullable=False, unique=True)

class Grade(db.Model, BaseMixin):
    __tablename__ = "grade"
    grade = db.Column(db.String(2), nullable=False, unique=True)
    point = db.Column(db.Integer, nullable=False, unique=True)
    waec = db.relationship(WaecSubject, backref="grade", lazy=True)
