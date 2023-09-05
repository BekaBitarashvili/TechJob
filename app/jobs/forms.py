from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    title = StringField('სათაური', validators=[DataRequired()])
    description = TextAreaField('აღწერა', validators=[DataRequired()])
    salary = StringField('Salary')
    location = StringField('Location')
    benefits = TextAreaField('Benefits')
    data_verification = TextAreaField('Data Verification')
    required_skills = TextAreaField('Required Skills')
    submit = SubmitField("დამატება")