from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from flask_login import current_user
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('სახელი', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('ემილი', validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    confirm_password = PasswordField('გაიმეორეთ პაროლი', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("რეგისტრაცია")

    def validete_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('ასეთი სახელი დაკავებულია. გთხოვთ აირჩიეთ სხვა.')

    def validete_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('ასეთი იმეილი დაკავებულია. გთხოვთ აირჩიეთ სხვა.')


class LoginForm(FlaskForm):
    email = StringField('იმეილი', validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    remember = BooleanField('დაიმახსოვრე')
    submit = SubmitField("ავტორიზაცია")


class UpdateAccountForm(FlaskForm):
    username = StringField('სახელი', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('იმეილი', validators=[DataRequired(), Email()])
    picture = FileField("განაახლეთ სურათი", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("განახლება")

    def validete_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('ასეთი სახელი დაკავებულია. გთხოვთ აირჩიეთ სხვა.')

    def validete_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('ასეთი იმეილი დაკავებულია. გთხოვთ აირჩიეთ სხვა.')


class ResetRequestForm(FlaskForm):
    email = StringField(label='იმეილი', validators=[DataRequired()])
    submit = SubmitField(label='პაროლის აღდგენა', validators=[DataRequired()])


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='პაროლი', validators=[DataRequired()])
    confirm_password = PasswordField(label='დაადასტურეთ პაროლი', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label="პაროლის შეცვლა")
