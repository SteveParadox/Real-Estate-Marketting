from flask_wtf import FlaskForm
from flask_wtf.file import DataRequired, FileAllowed
from wtforms import FileField, TextAreaField
from wtforms.fields import SubmitField, StringField, DateField, IntegerField, RadioField, SelectField
from wtforms.fields.html5 import URLField


class ApartmentForm(FlaskForm):
    agent_first_name = StringField(validators=[DataRequired()])
    agent_last_name = StringField(validators=[DataRequired()])
    agent_email = StringField(validators=[DataRequired()])
    agent_phone_no = StringField(validators=[DataRequired()])
    apartment_name = StringField(validators=[DataRequired()])
    gender = SelectField(choices=[('male', "Male"), ("female", "Female")],
                                  validators=[DataRequired()])
    agent_photo = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    description = TextAreaField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    city = StringField(validators=[DataRequired()])
    neighborhood = StringField(validators=[DataRequired()])
    location = StringField(validators=[DataRequired()])
    postal_code = StringField(validators=[DataRequired()])
    property_status = SelectField(choices=[('for sale', "For Sale"), ("for rent", "For Rent")],
                                 validators=[DataRequired()])
    property_type = SelectField(
        choices=[("apartment", 'Apartment'), ("house", "House"), ("office", "Office"), ("Store", "Store"),
                 ("resturant", "resturant")], validators=[DataRequired()])
    year_built = DateField(validators=[DataRequired()])
    video_tour = URLField()
    photo = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    photo1 = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    photo2 = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    front_plan = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    no_of_bedrooms = IntegerField(validators=[DataRequired()])
    no_of_bathrooms = IntegerField(validators=[DataRequired()])
    no_of_garages = IntegerField(validators=[DataRequired()])
    property_id = IntegerField(validators=[DataRequired()])
    area_size = IntegerField(validators=[DataRequired()])
    price = IntegerField(validators=[DataRequired()])
    second_price = IntegerField(validators=[DataRequired()])
    submit = SubmitField('Submit Property')
