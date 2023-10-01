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


class UserRole(db.Model, BaseMixin):
    __tablename__ = 'roles'
    _id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(25), unique = True, nullable = False)
    users = db.relationship("User", backref="role", lazy=True)

    def __repr__(self):
        return f"Role:<{self.name}>"

    @classmethod
    def create_default(cls):
        """A function that creates the default role"""
        role1 = cls(name="admins")
        role2 = cls(name="users")
        role3 = cls(name="staffs")
        db.session.add_all([role2, role1, role3])
        try:
            db.session.commit()
            return True
        except:
            return False

class User(db.Model, UserAdminMixin):
    """The User table"""
    __tablename__ = "users"
    username = db.Column(db.String(15), nullable=False, unique = True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    token = db.relationship("Token", backref='user', lazy=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    mid_name = db.Column(db.String(25), nullable=True)
    birth_date = db.Column(db.Date, nullable=False)
    bio_data = db.relationship("UserBioData", backref="user", uselist=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles._id"), unique=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)


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

    def active_token(self):
        """\
            Unlike the active token method this returns the active of the
            current instance.
        """
        active = []
        a = self.token
        if a:
            for actve in a:
                try:
                    d = actve.decode()
                    if d and actve.logged_out is False:
                        active.append(actve)
                    raise Exception
                except:
                    pass
        return active

    def save_last_seen(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

class UserBioData(db.Model, BaseMixin):
    __tablename__ = "biodata"
    _id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users._id"))
    jamb_reg = db.Column(db.String(25), unique=True, nullable=True)
    waec_id = db.Column(db.String(25), unique=True, nullable=True)


class Token(db.Model, BaseMixin):
    __tablename__ = "tokens"
    token = db.Column(db.Text(), nullable=False, unique=True)
    exp = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users._id'))
    logged_out = db.Column(db.Boolean, default=False)
    
    @classmethod
    def active_token(cls):
        """\
            it returns the all the active token of the model class
            by classifying through the active attribute and the 
            logged_out attributes of the instance class.
        """
        active = []
        a = cls.query.all()
        if a:
            for actve in a:
                try:
                    d = cls.decode_token(actve.token)
                    if d and actve.logged_out is False:
                        active.append(actve)
                    raise Exception
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

    def decode(self):
        """\
            Returns the decode token for the current instance
            Example:
            >>> token = Token.query.get(1)
            <Token 1>
            >>> token.decode()
            {'id': 1, 'exp': 1727747097}
            >>> token.token
            ... # some long random tokens
        """
        return self.decode_token(self.token)

    def log_out(self) -> None:
        self.logged_out = True
        db.session.add(self)
        db.session.commit()
        return None

    @classmethod
    def log_out_from(cls, token: str) -> None:
        token = cls.query.filter_by(token=token).first()
        token.log_out()
        return None


    

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