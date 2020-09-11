import os


from flask import *
from flask_login import current_user, login_user, login_required, logout_user

from base import db, bcrypt
from base.agent.forms import RegForm, LoginForm
from base.home.utils import save_img
from base.models import Agent, Apartment, AgentSchema

agent = Blueprint('agent', __name__)


@agent.route('/agents')
def agents():
    page = request.args.get('page', 1, type=int)
    agent = Agent.query.paginate(page=page, per_page=100)

    return render_template('agents.html', agent=agent)


@agent.route('/search/agent', methods=['POST'])
def agent_search():
    data = request.form.get('text')
    agent = Agent.query.filter_by(first_name=data).all()
    if not agent:
        agent = Agent.query.filter_by(last_name=data).all()
        if not agent:
            agent = Agent.query.filter_by(email=data).all()
    agent_schema = AgentSchema(many=True)
    res = agent_schema.dump(agent)
    return jsonify(res)


@agent.route('/profile/<string:agent_name>/<string:agent_last_name>')
def profile(agent_name, agent_last_name):
    page = request.args.get('page', 1, type=int)
    agent = Agent.query.filter_by(first_name=agent_name).filter_by(last_name=agent_last_name).first()
    apartment = Apartment.query.filter_by(agent=agent.id).order_by(Apartment.date_uploaded.desc()).paginate(page=page,
                                                                                                            per_page=10)
    return render_template('profile.html', agent=agent, apartment=apartment)

@agent.route('/agent/<string:agent_name>/<string:agent_last_name>')
@login_required
def agent_apt(agent_name, agent_last_name):

    page = request.args.get('page', 1, type=int)
    agent = Agent.query.filter_by(first_name=agent_name).filter_by(last_name=agent_last_name).first()
    if agent.first_name is not current_user.first_name:
        abort(403)
    apartment = Apartment.query.filter_by(broker=current_user).order_by(Apartment.date_uploaded.desc()).paginate(page=page,
                                                                                                            per_page=10)
    return render_template('current_agent.html', agent=agent, apartment=apartment)



@agent.route('/agent/<string:agent_name>/<string:agent_last_name>/delete/<string:apartment_public_id>')
def delete_agent_apt(agent_name, agent_last_name, apartment_public_id):
    apartment = Apartment.query.filter_by(broker=current_user).filter_by(public_id=apartment_public_id).first()
    os.remove(f"{os.path.abspath('base/static/Apartment_pics')}/{apartment.image_file}")
    os.remove(f"{os.path.abspath('base/static/Apartment_pics')}/{apartment.image_file0}")
    os.remove(f"{os.path.abspath('base/static/Apartment_pics')}/{apartment.image_file2}")
    os.remove(f"{os.path.abspath('base/static/Apartment_pics')}/{apartment.image_file3}")
    os.remove(f"{os.path.abspath('base/static/Apartment_pics')}/{apartment.image_file4}")
    os.remove(f"{os.path.abspath('base/static/Apartment_pics')}/{apartment.image_file5}")
    os.remove(f"{os.path.abspath('base/static/Apartment_pics')}/{apartment.image_file6}")
    os.remove(f"{os.path.abspath('base/static/Apartment_pics')}/{apartment.image_file7}")
    os.remove(f"{os.path.abspath('base/static/Apartment_pics')}/{apartment.image_file8}")
    os.remove(f"{os.path.abspath('base/static/Apartment_pics')}/{apartment.image_file9}")
    os.remove(f"{os.path.abspath('base/static/Apartment_pics')}/{apartment.video_tour}")

    db.session.delete(apartment)
    db.session.commit()
    return redirect(url_for('agent.agent_apt', agent_name= current_user.first_name, agent_last_name=current_user.last_name))


@agent.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.is_submitted():
        photo_file4 = save_img(form.agent_photo.data)
        file4 = request.files['agent_photo']
        hashed_password = bcrypt.generate_password_hash(form.agent_password.data).decode('utf-8')
        agent = Agent()
        agent.first_name = form.agent_first_name.data
        agent.last_name = form.agent_last_name.data
        agent.password = hashed_password
        agent.country = form.country.data
        agent.email = form.agent_email.data
        agent.gender = form.gender.data
        agent.phone_no = form.agent_phone_no.data
        agent.agent_image_file = photo_file4
        agent.agent_photo_data = file4.read()
        db.session.add(agent)
        db.session.commit()
        return redirect(url_for('agent.login'))
    return render_template('register.html', form=form, title="Register")


@agent.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Agent.query.filter_by(email=form.agent_email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.agent_password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login failed. please check email and password', 'danger')
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))

    return render_template('login.html', title="Login", form=form)


@agent.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))