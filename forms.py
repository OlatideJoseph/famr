from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Regexp, Length
from models import WaecSubject as ss, Course
from utils.main import duplicate
subjects = [
        ("English", "English"),
        ("Mathematics", "Math"),
        ("Physics", "Physics"),
        ("Chemistry", "Chemistry"),
        ("Government", "Government"),
]
regexp = r""
add_choice = [("","-------------")]
add_choice += [(sub.name, sub.name) for sub in ss.query.all()]
course_choice = [("","-------------")]
course_choice = [(sub.course_title, sub.course_title) for sub in Course.query.all()]




class MatchForm(FlaskForm):
    course_name = SelectField("Choose Your Course", validators = [DataRequired()],
                         choices = course_choice)
    subject1 = SelectField("Subject 1", validators = [DataRequired()],
                           choices = add_choice)
    subject2 = SelectField("Subject 2", validators = [DataRequired()], 
                           choices = add_choice)
    subject3 = SelectField("Subject 3", choices = add_choice)
    subject4 = SelectField("Subject 4", choices = add_choice)
    subject5 = SelectField("Subject 5", choices = add_choice)
    subject6 = SelectField("Subject 6", choices = add_choice)
    subject7 = SelectField("Subject 7", choices = add_choice)
    subject8 = SelectField("Subject 8", choices = add_choice)
    subject9 = SelectField("Subject 9", choices = add_choice)
    submit = SubmitField("Check")

class CourseForm(FlaskForm):
    field1 = SelectField("Course *", validators = [DataRequired()], coerce=str, choices = [])
    submit = SubmitField("Submit")
    
class AddSubjectForm(FlaskForm):
    name = StringField("Subject Name*", validators = [DataRequired()])
    submit = SubmitField("Add")
    
    
class AddCourseForm(FlaskForm):
    course_name = StringField("Course Name *", validators = [DataRequired()])
    field1 = SelectField("Subject 1", validators = [DataRequired()],
                   choices = add_choice)
    field2 = SelectField("Subject 2", validators = [DataRequired()],
                   choices = add_choice)
    field3 = SelectField("Subject 3", validators = [DataRequired()],
                   choices = add_choice)
    field4 = SelectField("Subject 4", validators = [DataRequired()],
                   choices = add_choice)
    field5 = SelectField("Subject 5", validators = [DataRequired()],
                   choices = add_choice)
    field6 = SelectField("Subject 6", validators = [DataRequired()],
                   choices = add_choice)
    field7 = SelectField("Subject 7", validators = [DataRequired()],
                   choices = add_choice)
    field8 = SelectField("Subject 8", validators = [DataRequired()],
                   choices = add_choice)
    field9 = SelectField("Subject 9", validators = [DataRequired()],
                   choices = add_choice)
    submit = SubmitField("Add Course")

    def validate_is_not_multiple(self,
            f1=field1.data, f2=field2.data,
            f3=field3.data, f4=field4.data,
            f5=field5.data, f6=field6.data,
            f7=field7.data, f8=field8.data,
            f9=field9.data, 
        ):
        fields = [f1, f2, f3, f4, f5, f6, f7, f8, f9]
        d = duplicate(fields)
        if d:
            raise ValidationError(f"This {d} exist either twice or more")

class AddGradeForm(FlaskForm):
    grade = StringField("Enter Grade Value:", validators=[DataRequired(), Length(min=2,max=2)])
    point = FloatField("Enter The Point:", validators=[DataRequired()])