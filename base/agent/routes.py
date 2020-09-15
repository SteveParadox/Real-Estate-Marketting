import os


from flask import *
from flask_login import current_user, login_user, login_required, logout_user

from base import db, bcrypt
from base.agent.email import send_email
from base.agent.forms import RegForm, LoginForm, RequestResetForm, ResetPasswordForm
from base.agent.token import generate_confirmation_token, confirm_token
from base.agent.util import send_reset_email
from base.home.utils import save_img
from base.models import Agent, Apartment, AgentSchema

agent = Blueprint('agent', __name__)





@agent.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    agent= Agent.query.filter_by(email=email).first_or_404()
    if agent.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        agent.confirmed = True
        db.session.add(agent)
        db.session.commit()
        flash('Your account has been confirmed. Thanks!', 'success')
    return redirect(url_for('main.home'))

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
        agent.confirmed = False
        db.session.add(agent)
        db.session.commit()
        token = generate_confirmation_token(agent.email)
        confirm_url = url_for('agent.confirm_email', token=token, _external=True)
        html = render_template('confirm_url.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(agent.email, subject, html)

        login_user(agent)

        flash('A confirmation email has been sent via email.', 'success')
        # flash('Your account has been created! Log in', 'success')

        return redirect(url_for("agent.unconfirmed"))

    return render_template('register.html', form=form, title="Register")



@agent.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        agent =Agent.query.filter_by(email=form.email.data).first()
        send_reset_email(agent)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('agent.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@agent.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    agent= Agent.verify_reset_token(token)
    if agent is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('agent.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        agent.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('agent.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)



@agent.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    return render_template('unconfirmed.html', title='Unconfirmed')


@agent.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('agent.confirm_email', token=token, _external=True)
    html = render_template('confirm_url.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('agent.unconfirmed'))


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