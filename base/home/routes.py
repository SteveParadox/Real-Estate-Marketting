import datetime
import os
import shutil

import shortuuid
from flask import *
from flask_login import login_required, current_user

from base import db, create_app
from base.home.forms import ApartmentForm, ReviewForm, SMForm
from base.home.utils import save_img
from base.models import Apartment, Agent, AgentSchema, ApartmentSchema, Review, ReviewSchema
import random

main = Blueprint('main', __name__)


@main.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        print(request.form['rating'])
        return request.form['rating']
    return render_template('contact.html')


@main.route('/search', methods=['GET', 'POST'])
def search_():
    data = request.form.get('text')
    data4 = request.form.get('text4')
    data5 = request.form.get('textx')
    data6 = request.form.get('texty')
    search = Apartment.query.filter_by(city=data).filter(Apartment.price > data5). \
        filter(data6 > Apartment.price).filter_by(property_type=data4).all()
    if len(data) < 1:
        search = Apartment.query.filter(Apartment.price > data5). \
            filter(data6 > Apartment.price).filter_by(property_type=data4).all()

    if len(data5) < 1 and len(data6) <1:
        search = Apartment.query.filter_by(city=data) \
            .filter_by(property_type=data4).all()
    if data4 is None:
        search = Apartment.query.filter_by(city=data).filter(Apartment.price > data5). \
            filter(data6 > Apartment.price).all()
    if (len(data5) < 1 and len(data6) <1) and data4 is None:
        search = Apartment.query.filter_by(city=data).all()
    if len(data) < 1 and len(data4) < 1:
        search = Apartment.query.filter(Apartment.price > data5). \
            filter(data6 > Apartment.price).all()
    if (len(data5) < 1 and len(data6) <1) and len(data) < 1:
        search = Apartment.query.filter_by(property_type=data4).all()

    apt_schema = ApartmentSchema(many=True)
    res = apt_schema.dump(search)
    return jsonify(res)


@main.route('/property/detail/love/<string:public_id>', methods=['POST'])
def add_rate(public_id):
    data = request.form.get('text')
    apartment = Apartment.query.filter_by(public_id=public_id).first()
    apartment.love = apartment.love + ((int(data) * 0) + 1)
    db.session.commit()
    return jsonify(apartment.love)


@main.route('/', methods=['GET', 'POST'])
def home():
    agent = (Agent.query.all()[:5])
    apt = (
        Apartment.query.filter(Apartment.property_type == 'apartment').paginate())
    house = (
        Apartment.query.filter(Apartment.property_type == 'house').paginate())
    office = (
        Apartment.query.filter(Apartment.property_type == 'office').paginate())
    store = (
        Apartment.query.filter(Apartment.property_type == 'store').paginate())
    condo = (
        Apartment.query.filter(Apartment.property_type == 'condo').paginate())

    apartment = (Apartment.query.all()[:10])
    x = random.shuffle(apartment)
    latest = (
        Apartment.query.order_by(Apartment.date_uploaded.desc()).all()[:10])

    latest_apt = (
        Apartment.query.filter(Apartment.property_type == 'apartment').order_by(Apartment.date_uploaded.desc()).all()[
        :10])
    latest_office = (
        Apartment.query.filter(Apartment.property_type == 'office').order_by(Apartment.date_uploaded.desc()).all()[
        :10])
    latest_house = (
        Apartment.query.filter(Apartment.property_type == 'house').order_by(Apartment.date_uploaded.desc()).all()[
        :10])
    latest_store = (
        Apartment.query.filter(Apartment.property_type == 'store').order_by(Apartment.date_uploaded.desc()).all()[
        :10])
    latest_rest = (
        Apartment.query.filter(Apartment.property_type == 'condo').order_by(Apartment.date_uploaded.desc()).all()[
        :10])
    rand_apt = Apartment.query.all()
    rand_apt2 = Apartment.query.all()
    if rand_apt:
        rand_apt = random.choice(Apartment.query.all())
        rand_apt2 = random.choice(Apartment.query.all())
    att = ''
    if current_user.is_authenticated:
        att = Agent.query.filter(Agent.facebook_name is not None).filter(Agent.twitter_name is not None) \
            .filter_by(id=current_user.id).first()
        if not att:
            att = Agent.query.filter(Agent.facebook_name is not None) \
                .filter_by(id=current_user.id).first()

        if not att:
            att = Agent.query.filter(Agent.twitter_name is not None) \
                .filter_by(id=current_user.id).first()

    form = SMForm()
    if form.is_submitted():
        social = Agent.query.filter_by(id=current_user.id).first()
        social.facebook_name = form.facebook.data
        social.twitter_name = form.twitter.data
        db.session.commit()
        return redirect(request.url)
    return render_template('index.html', apartment=apartment, att=att, latest=latest, latest_apt=latest_apt,
                           latest_house=latest_house, latest_office=latest_office,
                           latest_rest=latest_rest, latest_store=latest_store,
                           form=form, apt=apt, rand_apt=rand_apt, rand_apt2=rand_apt2, office=office, store=store,
                           condo=condo, house=house, agent=agent)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/property/list')
def property_list():
    page = request.args.get('page', 1, type=int)
    apartment = Apartment.query.order_by(Apartment.date_uploaded.desc()).paginate(page=page, per_page=15)

    return render_template('property.html', apartment=apartment)


@main.route('/property/<string:property_type>')
def type(property_type):
    page = request.args.get('page', 1, type=int)
    apartment = (
        Apartment.query.filter_by(property_type=property_type).paginate(page=page, per_page=15))
    return render_template('properties.html', apartment=apartment, property_type=property_type)


@main.route('/property/detail/<string:public_id>', methods=['GET', 'POST'])
def property_details(public_id):
    page = request.args.get('page', 1, type=int)
    apartment = Apartment.query.filter_by(public_id=public_id).first()
    review = Review.query.filter_by(apartment_id=apartment.id).order_by(Review.date_comment.desc()).paginate(page=page,
                                                                                                             per_page=100)
    form = ReviewForm()
    if form.is_submitted():
        rev = Review(message=form.message.data, first_name=form.name.data, email=form.email.data,
                     apartment_id=apartment.id)
        db.session.add(rev)
        db.session.commit()
        print('committed')
        return redirect(url_for('main.property_details', public_id=apartment.public_id))

    return render_template('property-details.html', apartment=apartment,
                           review=review, form=form)


@main.route('/calc', methods=['POST'])
def calc():
    def morgagecalc(morgage, years, interest):
        interest = interest / 100
        nper = years * 12
        interest_monthly = interest / 12
        num = interest_monthly * ((1 + interest_monthly) ** nper)
        den = (1 + interest_monthly) ** nper - 1
        payment = float("{0:.2f}".format(morgage * num / den))
        return jsonify(payment)

    data = request.form.get('text')
    data1 = request.form.get('text1')
    data2 = request.form.get('text2')

    return morgagecalc(float(data), float(data1), float(data2))


@main.route('/share/<string:public_id>', methods=['GET', 'POST'])
def share(public_id):
    apartment = Apartment.query.filter_by(public_id=public_id).first()
    apartment_schema = ApartmentSchema()
    res = apartment_schema.dump(apartment)
    return jsonify(res)


@main.route('/property/details/<string:public_id>', methods=['GET', 'POST'])
def property_detail(public_id):
    data = request.form.get('text')
    page = request.args.get('page', int(data), type=int)
    apartment = Apartment.query.filter_by(public_id=public_id).first()
    review = Review.query.filter_by(apartment_id=apartment.id).order_by(Review.date_comment.desc()).paginate()
    review_schema = ReviewSchema(many=True)
    result = review_schema.dump(review.items)

    return jsonify(result)


@main.route('/property/<string:apartment_name>/compare/with', methods=['GET', 'POST'])
def compare(apartment_name):
    apartment = Apartment.query.filter_by().all()

    return render_template('compare.html', apartment=apartment, apartment_name=apartment_name)


@main.route('/property/compare/<string:apartment_name>/with/<string:apt_name>', methods=['GET', 'POST'])
def property_compare(apartment_name, apt_name):
    apartment = Apartment.query.filter_by(apartment_name=apartment_name).first()
    apt = Apartment.query.filter_by(apartment_name=apt_name).first()
    return render_template('property-comparison.html', apt=apt, apartment=apartment, apartment_name=apartment_name)


@main.route('/compare/<string:apartment_name>', methods=['GET', 'POST'])
def compare_(apartment_name):
    data = request.form.get('text')
    apt = Apartment.query.filter_by(apartment_name=apartment_name).first()
    apartment_schema = ApartmentSchema()
    res = apartment_schema.dump(apt)
    return jsonify(res)


@main.route('/property/compare/<string:apartment_name>/search', methods=['GET', 'POST'])
def property_compare_(apartment_name):
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
                                        if not apartment:
                                            apartment = Apartment.query.filter_by(price=data).all()
                                            if not apartment:
                                                apartment = Apartment.query.filter_by(property_id=data).all()
    apartment_schema = ApartmentSchema(many=True)
    res = apartment_schema.dump(apartment)

    return jsonify(res), apartment_name


@main.route('/rev', methods=['GET'])
def get_rev():
    # printing the list of all the reviwes in the database
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
                                        if not apartment:
                                            apartment = Apartment.query.filter_by(price=data).all()
                                            if not apartment:
                                                apartment = Apartment.query.filter_by(property_id=data).all()
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
        video_data = save_img(form.video_data.data)
        video_file = request.files['video_data']

        photo_filex = save_img(form.front_plan.data)
        filex = request.files['front_plan']
        agent = Agent()
        apartment = Apartment(broker=current_user)
        apartment.video_tour = video_data
        apartment.video_data = video_file.read()
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

        apartment.no_of_bedrooms = form.no_of_bedrooms.data
        apartment.no_of_bathrooms = form.no_of_bathrooms.data
        apartment.no_of_garages = form.no_of_garages.data
        apartment.property_id = form.property_id.data
        apartment.area_size = form.area_size.data
        apartment.price = form.price.data
        apartment.second_price = form.second_price.data
        apartment.air_conditioning = form.air_conditioning.data
        apartment.laundry = form.laundry.data
        apartment.lawn = form.lawn.data
        apartment.outdoor_shower = form.outdoor_shower.data
        apartment.barbecue = form.balcony.data
        apartment.dryer = form.dryer.data
        apartment.gym = form.gym.data
        apartment.swimming_pool = form.swimming_pool.data
        apartment.sauna = form.sauna.data

        apartment.window_coverings = form.window_coverings.data
        apartment.wifi = form.wifi.data
        apartment.washer = form.washer.data
        apartment.villa = form.fireplace.data
        apartment.tv_cable = form.tv_cable.data
        apartment.refrigerator = form.refrigerator.data
        apartment.microwave = form.microwave.data

        db.session.add(apartment)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('property-submit.html', form=form)
