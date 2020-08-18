from flask import *

from base.models import Agent, Apartment

agent = Blueprint('agent', __name__)


@agent.route('/agents')
def agents():
    agent= Agent.query.paginate()
    return render_template('agents.html', agent=agent)


@agent.route('/profile/<string:agent_name>/<string:agent_last_name>')
def profile(agent_name, agent_last_name):
    agent = Agent.query.filter_by(first_name=agent_name).filter_by(last_name=agent_last_name).first()
    apartment = Apartment.query.filter_by(agent=agent.id).order_by(Apartment.date_uploaded.desc()).paginate()
    return render_template('profile.html', agent=agent, apartment=apartment)

