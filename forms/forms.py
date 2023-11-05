from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SelectField, StringField, SubmitField, IntegerField, PasswordField, DateField
from wtforms.validators import DataRequired, Regexp, Length, Email
from models import Subject as ss, Course, WaecSubject, Grade
from utils.main import duplicate



subjects = [
        ("English", "English"),
        ("Mathematics", "Math"),
        ("Physics", "Physics"),
        ("Chemistry", "Chemistry"),
        ("Government", "Government"),
]
regexp = r""
grades_choice = [(0,"---")]
add_choice = [("","-------------")]
course_choice = [("","-------------")]




class MatchForm(FlaskForm):
    jamb_score = IntegerField("Jamb Score", validators=[DataRequired()])
    course_name = SelectField("Choose Your Course", validators = [DataRequired()],
                         choices = course_choice)
    field1 = SelectField("Subject 1", validators = [DataRequired()],
                   choices = add_choice)
    grade_1 = SelectField("Grade *", validators = [DataRequired()], coerce=int,
                   choices = grades_choice)
    field2 = SelectField("Subject 2", validators = [DataRequired()],
                   choices = add_choice)
    grade_2 = SelectField("Grade *", validators = [DataRequired()], coerce=int,
                   choices = grades_choice)
    field3 = SelectField("Subject 3", validators = [DataRequired()],
                   choices = add_choice)
    grade_3 = SelectField("Grade *", validators = [DataRequired()], coerce=int,
                   choices = grades_choice)
    field4 = SelectField("Subject 4", validators = [DataRequired()],
                   choices = add_choice)
    grade_4 = SelectField("Grade *", validators = [DataRequired()], coerce=int,
                   choices = grades_choice)
    field5 = SelectField("Subject 5", validators = [DataRequired()],
                   choices = add_choice)
    grade_5 = SelectField("Grade *", validators = [DataRequired()], coerce=int,
                   choices = grades_choice)
    # field6 = SelectField("Subject 6",
    #                choices = add_choice)
    # grade_6 = SelectField("Grade *", coerce=int,
    #                choices = grades_choice)
    # field7 = SelectField("Subject 7",
    #                choices = add_choice)
    # grade_7 = SelectField("Grade",
    #                choices = grades_choice)
    # field8 = SelectField("Subject 8",
    #                choices = add_choice)
    # grade_8 = SelectField("Grade",
    #                choices = grades_choice)
    # field9 = SelectField("Subject 9",
    #                choices = add_choice)
    # grade_9 = SelectField("Grade",
    #                choices = grades_choice)
    submit = SubmitField("Check")

class CourseForm(FlaskForm):
    field1 = SelectField("Course *", validators = [DataRequired()], coerce=str, choices = [])
    submit = SubmitField("Submit")
    
class AddSubjectForm(FlaskForm):
    name = StringField("Subject Name*", validators = [DataRequired()])
    submit = SubmitField("Add")
    
    
class AddCourseForm(FlaskForm):
    course_name = StringField("Course Name *", validators = [DataRequired()])
    jamb_score = IntegerField("Min Jamb Score *", validators =[DataRequired()])
    field1 = SelectField("Subject 1", validators = [DataRequired()],
                   choices = add_choice)
    grade_1 = SelectField("Grade *", validators = [DataRequired()], coerce=int,
                   choices = grades_choice)
    field2 = SelectField("Subject 2", validators = [DataRequired()],
                   choices = add_choice)
    grade_2 = SelectField("Grade *", validators = [DataRequired()], coerce=int,
                   choices = grades_choice)
    field3 = SelectField("Subject 3", validators = [DataRequired()],
                   choices = add_choice)
    grade_3 = SelectField("Grade *", validators = [DataRequired()], coerce=int,
                   choices = grades_choice)
    field4 = SelectField("Subject 4", validators = [DataRequired()],
                   choices = add_choice)
    grade_4 = SelectField("Grade *", validators = [DataRequired()], coerce=int,
                   choices = grades_choice)
    field5 = SelectField("Subject 5", validators = [DataRequired()],
                   choices = add_choice)
    grade_5 = SelectField("Grade *", validators = [DataRequired()], coerce=int,
                   choices = grades_choice)
    # field6 = SelectField("Subject 6", validators = [DataRequired()],
    #                choices = add_choice)
    # grade_6 = SelectField("Grade *", validators = [DataRequired()], coerce=int,
    #                choices = grades_choice)
    # field7 = SelectField("Subject 7", validators = [DataRequired()],
    #                choices = add_choice)
    # grade_7 = SelectField("Grade", validators = [DataRequired()],
    #                choices = grades_choice)
    # field8 = SelectField("Subject 8", validators = [DataRequired()],
    #                choices = add_choice)
    # grade_8 = SelectField("Grade", validators = [DataRequired()],
    #                choices = grades_choice)
    # field9 = SelectField("Subject 9", validators = [DataRequired()],
    #                choices = add_choice)
    # grade_9 = SelectField("Grade", validators = [DataRequired()],
    #                choices = grades_choice)
    submit = SubmitField("Add Course")

    def validate_is_not_multiple(self,
            f1=field1, f2=field2,
            f3=field3, f4=field4,
            f5=field5
        ):
        fields = [f1, f2, f3, f4, f5]
        d = duplicate(fields)
        if d:
            raise ValidationError(f"This {d} exist either twice or more")

class AddGradeForm(FlaskForm):
    grade = StringField("Enter Grade Value:", validators=[DataRequired(), Length(min=2,max=2)])
    point = IntegerField("Enter The Point:", validators=[DataRequired()])
    submit = SubmitField("Add")

class UserLoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    login = SubmitField("Login")

class AdminLoginForm(UserLoginForm):
    pass

class UserCreationForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email(), Length(min=6, max=50)])
    password = PasswordField("Password: ", validators=[DataRequired()])
    first_name = StringField("*First Name:*", validators=[DataRequired(), Length(max=25, min=3)])
    last_name = StringField("*Last Name:*", validators=[DataRequired(), Length(max=25, min=3)])
    birth_date = DateField("*Date-Of-Birth:*", validators=[DataRequired()])
    middle_name = StringField("*Middle Name:* (opt)", validators=[Length(max=25, min=3)])
    signup = SubmitField("Sign Up")


class EditProfileForm(FlaskForm):
    email = StringField("Email Address: ")
    username = StringField("Username: ")
    first_name = StringField("FirstName: ")
    middle_name = StringField("MiddleName: ")
    last_name = StringField("LastName: ")
    update = SubmitField("Update me")

class EditBioDataForm(FlaskForm):
    jamb_reg = StringField("Jamb Reg No:", validators=[DataRequired()])
    waec_id = StringField("Waec Reg No:", validators=[DataRequired()])
    update = SubmitField("Update data")

class ImageForm(FlaskForm):
    img = FileField("Image Field", validators=[DataRequired()])
    upload = SubmitField("Upload Image")
    
class AdminSignUpForm(UserCreationForm):
    pass