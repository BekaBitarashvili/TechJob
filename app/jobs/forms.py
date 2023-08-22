from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    title = StringField('სათაური', validators=[DataRequired()])
    description = TextAreaField('აღწერა', validators=[DataRequired()])
    submit = SubmitField("დამატება")