
from flask_wtf import FlaskForm
from flask_wtf.file import DataRequired, FileAllowed
from wtforms import FileField, TextAreaField, PasswordField
from wtforms.fields import SubmitField, StringField, DateField, IntegerField, RadioField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import EqualTo


class RegForm(FlaskForm):
    agent_first_name = StringField(validators=[DataRequired()])
    agent_last_name = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    agent_password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    agent_email = StringField(validators=[DataRequired()])
    agent_phone_no = StringField(validators=[DataRequired()])
    gender = SelectField(choices=[('male', "Male"), ("female", "Female")],
                         validators=[DataRequired()])
    agent_photo = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    agent_email = StringField(validators=[DataRequired()])
    agent_password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Sign In')