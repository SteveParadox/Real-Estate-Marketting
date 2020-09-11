from flask_wtf import FlaskForm
from flask_wtf.file import DataRequired, FileAllowed
from wtforms import FileField, TextAreaField, PasswordField, BooleanField
from wtforms.fields import SubmitField, StringField, DateField, IntegerField, RadioField, SelectField

from wtforms.validators import EqualTo

class SMForm(FlaskForm):
    facebook= StringField('FaceBook username')
    twitter= StringField('Twitter username')
    submit = SubmitField('Add')

class ApartmentForm(FlaskForm):
    apartment_name = StringField(validators=[DataRequired()])
    description = TextAreaField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    city = StringField(validators=[DataRequired()])
    neighborhood = StringField(validators=[DataRequired()])
    location = StringField(validators=[DataRequired()])
    postal_code = StringField(validators=[DataRequired()])
    property_status = SelectField(choices=[('for sale', "For Sale"), ("for rent", "For Rent")],
                                 validators=[DataRequired()])
    property_type = SelectField(
        choices=[("apartment", 'Apartment'), ("house", "House"), ("office", "Office"), ("hotel", "Hotel"),
                 ("store", "Store")], validators=[DataRequired()])
    year_built = DateField(validators=[DataRequired()])
    video_data = FileField('Video tour guide', validators=[FileAllowed(['mp4', 'webm', 'hd'])])
    photo = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    photo1 = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    photo2 = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    photo3 = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    photo4 = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    photo5 = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    photo6 = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    photo7 = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    photo8 = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    photo9 = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    photo0 = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    front_plan = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    no_of_bedrooms = IntegerField(validators=[DataRequired()])
    no_of_bathrooms = IntegerField(validators=[DataRequired()])
    no_of_garages = IntegerField(validators=[DataRequired()])
    property_id = IntegerField(validators=[DataRequired()])
    area_size = IntegerField(validators=[DataRequired()])
    price = IntegerField(validators=[DataRequired()])
    second_price = IntegerField(validators=[DataRequired()])
    price_label = SelectField(choices=[("full sale", "Sale"),('month', "Monthly"), ("year", "Yearly")],
                                  validators=[DataRequired()])
    air_conditioning=BooleanField('air_conditioning')
    laundry = BooleanField('laundry')
    refrigerator = BooleanField('refrigerator')
    washer = BooleanField('washer')
    balcony = BooleanField('balcony')
    lawn = BooleanField('lawn')
    sauna = BooleanField('sauna')
    wifi = BooleanField('wifi')
    dryer = BooleanField('dryer')
    fireplace = BooleanField('fireplace')
    swimming_pool = BooleanField('swimming_pool')
    window_coverings = BooleanField('window_coverings')
    gym = BooleanField('gym')
    outdoor_shower = BooleanField('outdoor_shower')
    tv_cable = BooleanField('tv_cable')
    microwave = BooleanField('microwave')
    submit = SubmitField('Submit Property')




class ReviewForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    message = TextAreaField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    submit=SubmitField('Post review')
