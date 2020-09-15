from flask_wtf import FlaskForm
from flask_wtf.file import DataRequired, FileAllowed
from wtforms import FileField, TextAreaField, PasswordField, BooleanField
from wtforms.fields import SubmitField, StringField, DateField, IntegerField, RadioField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import EqualTo, ValidationError, Email, Length

import pycountry

from base.models import Agent


def lst():


    index=[]
    d = {}

    for index, value in enumerate(pycountry.countries):
        d[index] = value

    return d[index].name


class RegForm(FlaskForm):
    agent_first_name = StringField(validators=[DataRequired()])
    agent_last_name = StringField(validators=[DataRequired()])

    country = SelectField(choices=lst())
    agent_password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    agent_email = StringField(validators=[DataRequired()])
    agent_phone_no = StringField(validators=[DataRequired()])
    gender = SelectField(choices=[('male', "Male"), ("female", "Female")],
                         validators=[DataRequired()])
    agent_photo = FileField('Upload', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    agent_email = StringField(validators=[DataRequired()])
    agent_password = PasswordField(validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')




class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        agent = Agent.query.filter_by(email=email.data).first()
        if agent is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=8, max=255)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )