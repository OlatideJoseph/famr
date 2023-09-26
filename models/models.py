from datetime import datetime, timedelta
from flask import current_app
from werkzeug.security import generate_password_hash as g_pass, check_password_hash as c_pass
from app import db




class BaseMixin:
    _id = db.Column(db.Integer, primary_key=True)


    @property
    def pk(self):
        return self._id
    def __repr__(self) -> str:
        return f"{self.__class__.__name__} <{self.pk}>"


class UserAdminMixin(BaseMixin):
    is_admin = db.Column(db.Boolean, default=False)



class User(db.Model, UserAdminMixin):
    """The User table"""
    __tablename__ = "users"
    username = db.Column(db.String(15), nullable=False, unique = True)
    password = db.Column(db.Text(), nullable=False)
    token = db.relationship("Token", backref='user', lazy=True)


    def __repr__(self) -> str:
        return repr(self.username)

    # def gen_on_pass(self, password):
    #     """It generate with the"""
    #     chk = c_pass(se, password)

    def check_pass(self, password: str) -> bool:
        return c_pass(self.password, password)

    def check_token(self):
        pass
        
    @staticmethod
    def gen_pass(password: str) -> str:
        return g_pass(password)



class Token(db.Model, BaseMixin):
    __tablename__ = "tokens"
    token = db.Column(db.Text(), nullable=False, unique=True)
    exp = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users._id'))
    
    @classmethod
    def active_token(cls):
        """\
            it returns the all the active token of the model class
        """
        active = []
        a = cls.query.all()
        if a:
            for actve in a:
                try:
                    cls.decode_token(actve.token)
                    active.append(actve)
                except:
                    pass
        return active


    @staticmethod
    def gen_token(_id) -> str:
        import jwt
        expires = datetime.utcnow() + timedelta(days = 366)
        key = current_app.config['SECRET_KEY']
        tok = jwt.encode(
            {
                "id": _id,
                "exp": expires
            }, key
        )
        return tok
    @classmethod
    def decode_token(cls, token: str) -> dict:
        import jwt
        key = current_app.config['SECRET_KEY']
        b = jwt.decode(token, key, algorithms=["HS256"])

        return b
    @classmethod    
    def verify_token(cls, token: str) -> bool:
        t = cls.query.filter_by(token = token).first()
        if t is not None:
            return False
        return True

class Course(db.Model, BaseMixin):
    __tablename__  = "course"
    course_title = db.Column(db.String(50), nullable = False, unique = True)
    course_code = db.Column(db.Integer, unique = True)
    is_full = db.Column(db.Boolean, default=False)
    max_candidate = db.Column(db.Integer, default=200)
    jamb = db.relationship("AdminJamb", backref="course", lazy=True, uselist = False)
    waec = db.relationship("WaecSubject", backref="course", lazy=True)

    def __repr__(self):
        return "Lasustech <%s> Course" %(self.course_title)


class WaecSubject(db.Model, BaseMixin):
    __tablename__ = "waecsubject"
    name = db.Column(db.String(50), nullable = False)
    is_compulsory = db.Column(db.Boolean, default=False)
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

class AdminJamb(db.Model, BaseMixin):
    __tablename__ = "adminjamb"
    min_score = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey("course._id"))