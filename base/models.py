from datetime import datetime
from flask_login import UserMixin
from itsdangerous import Serializer
from marshmallow_sqlalchemy import ModelSchema
from base import db, login_manager, app


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))


@login_manager.user_loader
def load_user(agent_id):
    return Agent.query.get(int(agent_id))


# the model configuration of the database

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    logged_in = db.Column(db.Boolean, default=False)
    auth_key = db.Column(db.String(), unique=True)


class Agent(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    phone_no = db.Column(db.String(), nullable=False)
    gender = db.Column(db.String(), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.now)
    agent_image_file = db.Column(db.String(20), nullable=False)
    agent_photo_data = db.Column(db.LargeBinary)
    amount_earned = db.Column(db.Integer(), default=0)
    buildings_sold = db.Column(db.Integer(), default=0)
    location = db.Column(db.String())
    client = db.relationship('Client', backref='real_estate', lazy=True)
    apartment = db.relationship('Apartment', backref='broker', lazy=True)
    facebook_name = db.Column(db.String())
    twitter_name = db.Column(db.String())
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'agent_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            agent_id = s.loads(token)['agent_id']
        except ValueError:
            return None
        return Agent.query.get(agent_id)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}', '{self.confirmed}')"




class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(), nullable=False)
    love = db.Column(db.Integer, default=0)
    apartment_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    client = db.relationship('Client', backref='housing', lazy=True)
    review = db.relationship('Review', backref='reviews', lazy=True)
    sold_by = db.Column(db.String())
    purchased_by = db.Column(db.String())
    agent = db.Column(db.Integer, db.ForeignKey('agent.id'))
    sold = db.Column(db.Boolean, nullable=False, default=False)
    rented = db.Column(db.Boolean, nullable=False, default=False)
    for_sale = db.Column(db.Boolean, nullable=False, default=False)
    for_rent = db.Column(db.Boolean, nullable=False, default=False)
    country = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    neighbourhood = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    postal_code = db.Column(db.String(), nullable=False)
    property_status = db.Column(db.String(), nullable=False)
    property_type = db.Column(db.String(), nullable=False)
    no_of_bedrooms = db.Column(db.Integer, nullable=False, default=0)
    no_of_bathrooms = db.Column(db.Integer, nullable=False, default=0)
    area_size = db.Column(db.Integer, nullable=False)
    property_id = db.Column(db.Integer, nullable=False)
    no_of_garages = db.Column(db.Integer, nullable=False, default=0)
    year_built = db.Column(db.String, nullable=False)
    video_tour = db.Column(db.String)
    video_data = db.Column(db.LargeBinary)
    image_file = db.Column(db.String(20), nullable=False)
    photo_data = db.Column(db.LargeBinary)
    image_file2 = db.Column(db.String(20), nullable=False)
    photo_data2 = db.Column(db.LargeBinary)
    image_file3 = db.Column(db.String(20), nullable=False)
    photo_data3 = db.Column(db.LargeBinary)
    image_file4 = db.Column(db.String(20), nullable=False)
    photo_data4 = db.Column(db.LargeBinary)
    image_file5 = db.Column(db.String(20), nullable=False)
    photo_data5 = db.Column(db.LargeBinary)
    image_file6 = db.Column(db.String(20), nullable=False)
    photo_data6 = db.Column(db.LargeBinary)
    image_file7 = db.Column(db.String(20), nullable=False)
    photo_data7 = db.Column(db.LargeBinary)
    image_file8 = db.Column(db.String(20), nullable=False)
    photo_data8 = db.Column(db.LargeBinary)
    image_file9 = db.Column(db.String(20), nullable=False)
    photo_data9 = db.Column(db.LargeBinary)
    image_file0 = db.Column(db.String(20), nullable=False)
    photo_data0 = db.Column(db.LargeBinary)
    floor_plan_file = db.Column(db.String(20), nullable=False)
    floor_plan_photo_data = db.Column(db.LargeBinary)
    price = db.Column(db.Integer)
    second_price = db.Column(db.Integer)
    price_label = db.Column(db.String())
    size_prefix = db.Column(db.String(), default="sqft")
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)
    cleared = db.Column(db.Boolean, default=False)
    air_conditioning = db.Column(db.Boolean, default=False)
    laundry = db.Column(db.Boolean, default=False)
    refrigerator = db.Column(db.Boolean, default=False)
    washer = db.Column(db.Boolean, default=False)
    barbecue = db.Column(db.Boolean, default=False) # change to balcony
    lawn = db.Column(db.Boolean, default=False)
    sauna = db.Column(db.Boolean, default=False)
    wifi = db.Column(db.Boolean, default=False)
    dryer = db.Column(db.Boolean, default=False)
    microwave = db.Column(db.Boolean, default=False)
    swimming_pool = db.Column(db.Boolean, default=False)
    window_coverings = db.Column(db.Boolean, default=False)
    gym = db.Column(db.Boolean, default=False)
    outdoor_shower = db.Column(db.Boolean, default=False)
    tv_cable = db.Column(db.Boolean, default=False)
    villa = db.Column(db.Boolean, default=False) # change to fireplace


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    gender = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    dob = db.Column(db.String(), nullable=False)
    phone_no = db.Column(db.Integer(), nullable=False)
    criminal_record = db.Column(db.Boolean, default=False)
    ssn = db.Column(db.Integer(), nullable=False)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.now)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    message = db.Column(db.String(), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    date_comment = db.Column(db.DateTime, nullable=False, default=datetime.now)


# the schema configuration to convert the data in each table to json readable format
class AdminSchema(ModelSchema):
    class Meta:
        model = Admin


admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)


class AgentSchema(ModelSchema):
    class Meta:
        model = Agent


agent_schema = AgentSchema()
agents_schema = AgentSchema(many=True)


class ReviewSchema(ModelSchema):
    class Meta:
        model = Review


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)


class ApartmentSchema(ModelSchema):
    class Meta:
        model = Apartment


apartment_schema = ApartmentSchema
apartments_schema = ApartmentSchema(many=True)


class ClientSchema(ModelSchema):
    class Meta:
        model = Client


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
