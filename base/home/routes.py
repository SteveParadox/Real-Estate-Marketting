import datetime

import shortuuid
from flask import *
from flask_login import login_required, current_user

from base import db
from base.home.forms import ApartmentForm, ReviewForm
from base.home.utils import save_img
from base.models import Apartment, Agent, AgentSchema, ApartmentSchema, Review, ReviewSchema
import random

main = Blueprint('main', __name__)


@main.route('/search', methods=['POST'])
def search():
    data = request.form.get('text')
    data2 = request.form.get('text2')
    data3 = request.form.get('text3')
    data4 = request.form.get('text4')
    search = Apartment.query.filter_by(no_of_bedrooms=data2).filter_by(city=data).filter_by(no_of_bathrooms=data3) \
        .filter_by(location=data4).all()
    if len(data) < 1:
        search = Apartment.query.filter_by(no_of_bedrooms=data2).filter_by(
            no_of_bathrooms=data3).filter_by(location=data4).all()
    if len(data2) < 1:
        search = Apartment.query.filter_by(city=data).filter_by(
            no_of_bathrooms=data3).filter_by(location=data4).all()
    if len(data3) < 1:
        search = Apartment.query.filter_by(no_of_bedrooms=data2). \
            filter_by(city=data).filter_by(location=data4).all()
    if len(data4) < 1:
        search = Apartment.query.filter_by(no_of_bedrooms=data2). \
            filter_by(city=data).filter_by(no_of_bathrooms=data3).all()

    agent_schema = ApartmentSchema(many=True)
    res = agent_schema.dump(search)
    return jsonify(res)


@main.route('/property/detail/love/<string:public_id>', methods=['POST'])
def add_rate(public_id):
    data = request.form.get('text')
    apartment = Apartment.query.filter_by(public_id=public_id).first()
    apartment.love = apartment.love + ((int(data) * 0) + 1)
    db.session.commit()
    return jsonify(apartment.love)


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


@main.route('/property/detail/<string:public_id>', methods=['GET', 'POST'])
def property_details(public_id):
    page = request.args.get('page', 1, type=int)
    apartment = Apartment.query.filter_by(public_id=public_id).first()
    review = Review.query.filter_by(apartment_id=apartment.id).order_by(Review.date_comment.desc()).paginate(page=page, per_page=0)
    form = ReviewForm()
    if form.is_submitted():
        rev = Review(message= form.message.data, first_name=form.name.data, email= form.email.data,
                     apartment_id=apartment.id)
        db.session.add(rev)
        db.session.commit()
        print('committed')
        return redirect(url_for('main.property_details', public_id=apartment.public_id))
    return render_template('property-details.html', apartment=apartment,
                           review=review, form=form)


@main.route('/property/details/<string:public_id>', methods=['GET', 'POST'])
def property_detail(public_id):
    data= request.form.get('text')
    page = request.args.get('page', int(data), type=int)
    apartment = Apartment.query.filter_by(public_id=public_id).first()
    review = Review.query.filter_by(apartment_id=apartment.id).order_by(Review.date_comment.desc()).paginate()
    review_schema = ReviewSchema(many=True)
    result = review_schema.dump(review.items)
    return jsonify(result)



@main.route('/rev', methods=['GET'])
def get_rev():
    # printing the list of all the agents in the database
    rev = Review.query.all()
    review_schema = ReviewSchema(many=True)
    result = review_schema.dump(rev)
    return jsonify(result)


@main.route('/search/apartment', methods=['POST'])
def apartment_search():
    data = request.form.get('text')
    apartment = Apartment.query.filter_by(apartment_name=data).all()
    if not apartment:
        apartment = Apartment.query.filter_by(city=data).all()
        if not apartment:
            apartment = Apartment.query.filter_by(location=data).all()
            if not apartment:
                apartment = Apartment.query.filter_by(neighbourhood=data).all()
                if not apartment:
                    apartment = Apartment.query.filter_by(postal_code=data).all()
                    if not apartment:
                        apartment = Apartment.query.filter_by(property_type=data).all()
                        if not apartment:
                            apartment = Apartment.query.filter_by(property_status=data).all()
                            if not apartment:
                                apartment = Apartment.query.filter_by(no_of_bedrooms=data).all()
                                if not apartment:
                                    apartment = Apartment.query.filter_by(no_of_bathrooms=data).all()
                                    if not apartment:
                                        apartment = Apartment.query.filter_by(no_of_garages=data).all()
    apartment_schema = ApartmentSchema(many=True)
    res = apartment_schema.dump(apartment)
    return jsonify(res)


@main.route('/property/submit', methods=['GET', 'POST'])
@login_required
def property_submit():
    form = ApartmentForm()
    if form.validate_on_submit():
        photo_file = save_img(form.photo.data)
        file = request.files['photo']
        photo_file1 = save_img(form.photo1.data)
        file1 = request.files['photo1']
        photo_file2 = save_img(form.photo2.data)
        file2 = request.files['photo2']

        photo_file3 = save_img(form.photo3.data)
        file3 = request.files['photo3']
        photo_file4 = save_img(form.photo4.data)
        file4 = request.files['photo4']
        photo_file5 = save_img(form.photo5.data)
        file5 = request.files['photo5']
        photo_file6 = save_img(form.photo6.data)
        file6 = request.files['photo6']
        photo_file7 = save_img(form.photo7.data)
        file7 = request.files['photo7']
        photo_file8 = save_img(form.photo8.data)
        file8 = request.files['photo8']
        photo_file9 = save_img(form.photo9.data)
        file9 = request.files['photo9']

        photo_filex = save_img(form.front_plan.data)
        filex = request.files['front_plan']
        agent = Agent()
        apartment = Apartment(broker=current_user)
        apartment.image_file = photo_file
        apartment.photo_data = file.read()
        apartment.image_file2 = photo_file1
        apartment.photo_data2 = file1.read()
        apartment.image_file3 = photo_file2
        apartment.photo_data3 = file2.read()
        apartment.image_file4 = photo_file3
        apartment.photo_data4 = file3.read()
        apartment.image_file5 = photo_file4
        apartment.photo_data5 = file4.read()
        apartment.image_file6 = photo_file5
        apartment.photo_data6 = file5.read()
        apartment.image_file7 = photo_file6
        apartment.photo_data7 = file6.read()
        apartment.image_file8 = photo_file7
        apartment.photo_data8 = file7.read()
        apartment.image_file9 = photo_file8
        apartment.photo_data9 = file8.read()
        apartment.image_file0 = photo_file9
        apartment.photo_data0 = file9.read()
        apartment.price_label = form.price_label.data
        apartment.floor_plan_file = photo_filex
        apartment.floor_plan_photo_data = filex.read()
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
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('property-submit.html', form=form)
