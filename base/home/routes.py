import datetime

import shortuuid
from flask import *

from base import db
from base.home.forms import ApartmentForm
from base.home.utils import save_img
from base.models import Apartment, Agent, AgentSchema
import random

main = Blueprint('main', __name__)


@main.route('/search', methods=['POST'])
def search():
    data = request.form.get('text')
    data1 = request.form.get('text1')
    data2 = request.form.get('text2')
    sea = Apartment.query.all()
    search = Apartment.query.filter(Apartment.city == data).all()
    search2 = Apartment.query.filter(Apartment.no_of_bedrooms == data).all()
    search3 = Apartment.query.filter(Apartment.no_of_bathrooms == data).all()
    if data in sea and data1 in sea and data2 in sea:
        agent_schema = AgentSchema(many=True)
        res = agent_schema.dump(data)
        return jsonify(res)
    agent_schema = AgentSchema(many=True)
    res = agent_schema.dump(search)
    res2 = agent_schema.dump(search2)
    res3 = agent_schema.dump(search3)
    return jsonify(res, res2, res3)


@main.route('/')
def home():
    form = ApartmentForm()
    apt = (
        Apartment.query.filter(Apartment.property_type == 'apartment').paginate())
    house = (
        Apartment.query.filter(Apartment.property_type == 'house').paginate())
    office = (
        Apartment.query.filter(Apartment.property_type == 'office').paginate())
    store = (
        Apartment.query.filter(Apartment.property_type == 'store').paginate())
    resturant = (
        Apartment.query.filter(Apartment.property_type == 'resturant').paginate())

    apartment = (Apartment.query.all()[:10])
    x = random.shuffle(apartment)
    latest = (
        Apartment.query.filter(Apartment.date_uploaded >= (datetime.datetime.now() - datetime.timedelta(days=7))).all()[
        :10])

    latest_apt = (
        Apartment.query.filter(Apartment.property_type == 'apartment').filter(
            Apartment.date_uploaded >= (datetime.datetime.now() - datetime.timedelta(days=7))).all()[
        :10])
    latest_office = (
        Apartment.query.filter(Apartment.property_type == 'office').filter(
            Apartment.date_uploaded >= (datetime.datetime.now() - datetime.timedelta(days=7))).all()[
        :10])
    latest_house = (
        Apartment.query.filter(Apartment.property_type == 'house').filter(
            Apartment.date_uploaded >= (datetime.datetime.now() - datetime.timedelta(days=7))).all()[
        :10])
    latest_store = (
        Apartment.query.filter(Apartment.property_type == 'store').filter(
            Apartment.date_uploaded >= (datetime.datetime.now() - datetime.timedelta(days=7))).all()[
        :10])
    latest_rest = (
        Apartment.query.filter(Apartment.property_type == 'resturant').filter(
            Apartment.date_uploaded >= (datetime.datetime.now() - datetime.timedelta(days=7))).all()[
        :10])
    rand_apt = Apartment.query.all()
    rand_apt2 = Apartment.query.all()
    if rand_apt:
        rand_apt = random.choice(Apartment.query.all())
        rand_apt2 = random.choice(Apartment.query.all())

    return render_template('index.html', apartment=apartment, latest=latest, latest_apt=latest_apt,
                           latest_house=latest_house, latest_office=latest_office,
                           latest_rest=latest_rest, latest_store=latest_store,
                           form=form, apt=apt, rand_apt=rand_apt, rand_apt2=rand_apt2, office=office, store=store,
                           resturant=resturant, house=house)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/property/list')
def property_list():
    page = request.args.get('page', 1, type=int)
    apartment = Apartment.query.order_by(Apartment.date_uploaded.desc()).paginate(page=page, per_page=15)

    return render_template('property.html', apartment=apartment)


@main.route('/property/comparison')
def property_comparison():
    return render_template('property-comparison.html')


@main.route('/property/<string:property_type>')
def type(property_type):
    page = request.args.get('page', 1, type=int)
    apartment = (
        Apartment.query.filter_by(property_type=property_type).paginate(page=page, per_page=15))
    return render_template('properties.html', apartment=apartment)




@main.route('/property/detail/<string:public_id>')
def property_details(public_id):
    apartment = Apartment.query.filter_by(public_id=public_id).first()

    return render_template('property-details.html', apartment=apartment)


@main.route('/property/submit', methods=['GET', 'POST'])
def property_submit():
    form = ApartmentForm()

    if form.validate_on_submit():
        photo_file = save_img(form.photo.data)
        file = request.files['photo']
        photo_file1 = save_img(form.photo1.data)
        file1 = request.files['photo1']
        photo_file2 = save_img(form.photo2.data)
        file2 = request.files['photo1']
        photo_file3 = save_img(form.front_plan.data)
        file3 = request.files['front_plan']
        photo_file4 = save_img(form.agent_photo.data)
        file4 = request.files['agent_photo']
        agent = Agent()
        agent.first_name = form.agent_first_name.data
        agent.last_name = form.agent_last_name.data
        agent.country = form.country.data
        agent.email = form.agent_email.data
        agent.gender = form.gender.data
        agent.phone_no = form.agent_phone_no.data
        agent.agent_image_file = photo_file4
        agent.agent_photo_data = file4.read()
        apartment = Apartment(broker=agent)
        apartment.image_file = photo_file
        apartment.photo_data2 = file.read()
        apartment.image_file2 = photo_file1
        apartment.photo_data3 = file1.read()
        apartment.image_file3 = photo_file2
        apartment.photo_data = file2.read()
        apartment.floor_plan_file = photo_file3
        apartment.floor_plan_photo_data = file3.read()
        apartment.apartment_name = form.apartment_name.data
        apartment.description = form.description.data
        apartment.public_id = str(shortuuid.uuid())
        apartment.country = form.country.data
        apartment.city = form.city.data
        apartment.location = form.location.data
        apartment.neighbourhood = form.neighborhood.data
        apartment.postal_code = form.postal_code.data
        apartment.property_status = form.property_status.data
        apartment.property_type = form.property_type.data
        apartment.year_built = form.year_built.data
        apartment.video_tour = form.video_tour.data
        apartment.no_of_bedrooms = form.no_of_bedrooms.data
        apartment.no_of_bathrooms = form.no_of_bathrooms.data
        apartment.no_of_garages = form.no_of_garages.data
        apartment.property_id = form.property_id.data
        apartment.area_size = form.area_size.data
        apartment.price = form.price.data
        apartment.second_price = form.second_price.data

        db.session.add(apartment)
        db.session.add(agent)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('property-submit.html', form=form)
