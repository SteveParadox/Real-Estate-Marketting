from functools import wraps
import uuid
from flask import *
from flask_login import login_user, current_user, logout_user, login_required

from base.models import *
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.logged_in is False:
            return jsonify('Admin verification required')
        return func(*args, **kwargs)

    return decorated_function


@api.route('/reg/admin', methods=['POST'])
def admin():
    data = request.get_json()
    # checking if the database has record of the email
    check = Admin.query.filter_by(email=data['email']).filter_by().first()
    try:
        # if it does not have record, register new admin
        if not check:
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            country = data['country']
            auth_key = str(uuid.uuid4())
            password = generate_password_hash(data['password'], method='sha256')
            admin = Admin()
            admin.first_name = first_name
            admin.last_name = last_name
            admin.email = email
            admin.country = country
            admin.auth_key = auth_key
            admin.password = password
            db.session.add(admin)
            db.session.commit()
            return jsonify({"message": "admin registered",
                            'auth_key': admin.auth_key})
        # if already registered as an admin
        return {'message': "already registered as admin",
                'auth_key': check.auth_key}
    except:
        # if there is any problem with the data
        return jsonify({'message': "Could not register admin"})


@api.route('/login/admin', methods=['GET'])
def login_admin():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify, Login to gain access", 401,
                             {'WWW-Authenticate': 'Basic realm="Login required"'})
    admin = Admin.query.filter_by(auth_key=auth.username).first()
    if not admin:
        return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    if admin and check_password_hash(admin.password, auth.password):
        admin.logged_in = True
        db.session.commit()
        login_user(admin)
        return jsonify({"message": "logged in"})
    return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


@api.route('/admin/login', methods=['GET'])
def admin_login():
    data = request.get_json()
    admin = Admin.query.filter_by(auth_key=data['auth_key']).first()
    if admin and check_password_hash(admin.password, data['password']):
        admin.logged_in = True
        db.session.commit()
        login_user(admin)
        return jsonify({"message": "logged in"})
    return jsonify('could not log in'), 401


@api.route('/logout/admin')
@login_required
@admin_required
def logout():
    # logging out the admin
    current_user.logged_in = False
    db.session.commit()
    logout_user()
    return jsonify('Logged out')


@api.route('/admin', methods=['GET'])
def get_admin():
    admin = Admin.query.all()
    admin_schema = AdminSchema(many=True)
    result = admin_schema.dump(admin)
    return jsonify(result)


@api.route('/agent', methods=['POST'])
@login_required
@admin_required
def add_agent():
    # registering an agent to the database
    data = request.get_json()
    try:
        agent = Agent(first_name=data['first_name'],
                      last_name=data['last_name'],
                      gender=data['gender'],
                      dob=data['dob'],
                      country=data['country'],
                      date_employed=data['date_employed'],
                      ssn=data['ssn'])

        db.session.add(agent)
        db.session.commit()

        return jsonify({'message': "Agent Registered"})
    except:
        # if there is any problem with the data
        return jsonify({'message': "Could not register agent"})


@api.route('/agent', methods=['GET'])
def get_agent():
    # printing the list of all the agents in the database
    agent = Agent.query.all()
    agent_schema = AgentSchema(many=True)
    result = agent_schema.dump(agent)
    return jsonify(result)


@api.route('/apartment', methods=['POST'])
@login_required
@admin_required
def add_apartment():
    # registering an apartment to the database
    data = request.get_json()
    try:
        apartment = Apartment(location=data['location'],
                              apartment_name=data['apartment_name'],
                              apartment_no=data['apartment_no'],
                              sold=data['sold'])
        db.session.add(apartment)
        db.session.commit()
        return jsonify({'message': "Apartment Registered"})
    except:
        # if there is any problem with the data
        return jsonify({'message': "Could not register apartment"})


@api.route('/apartment', methods=['GET'])
def get_apartment():
    # printing the list of all the apartments in the database
    apartment = Apartment.query.all()
    apartments_schema = ApartmentSchema(many=True)
    result = apartments_schema.dump(apartment)
    return jsonify(result)


@api.route('/client', methods=['POST'])
@login_required
@admin_required
def add_client():
    # registering a client to the database
    data = request.get_json()
    try:
        client = Client(first_name=data['first_name'],
                        last_name=data['last_name'],
                        gender=data['gender'],
                        dob=data['dob'],
                        phone_no=data['phone_no'],
                        ssn=data['ssn'],
                        country=data['country'],
                        criminal_record=data['criminal_record'])

        db.session.add(client)
        db.session.commit()
        return jsonify({'message': "Client Registered"})
    except:
        # if there is any problem with the data
        return jsonify({'message': "Could not register client"})


@api.route('/client', methods=['GET'])
@login_required
@admin_required
def get_client():
    # printing the list of all clients
    client = Client.query.all()
    clients_schema = ClientSchema(many=True)
    result = clients_schema.dump(client)
    return jsonify(result)


@api.route('/sold', methods=['GET'])
@login_required
@admin_required
def sold():
    # filtering the list of apartments that has not been sold from the database
    log = Apartment.query.filter(Apartment.sold == False).all()
    apartments_schema = ApartmentSchema(many=True)
    result = apartments_schema.dump(log)
    return jsonify(result)


# _______Selling the apartment_______
# The apartment table will be located through the id(can be switched to name if preferred)

@api.route('/sale/<int:apartment_id>', methods=['POST'])
@login_required
@admin_required
def sale(apartment_id):
    data = request.get_json()
    apartment = Apartment.query.get_or_404(apartment_id)
    # this checks if the apartment is sold through the apartment.sold table in the database
    try:
        if not apartment.sold:
            # this search for and filters the name of the client and the agent from the database
            agent = Agent.query.filter_by(first_name=data['sold_by']).first()
            client = Client.query.filter_by(first_name=data['purchased_by']).first()
            # this runs if the names in the agent and client are met (if the inputted names are in the database)
            if agent and client:
                apartment.sold_by = data['sold_by']
                apartment.purchased_by = data['purchased_by']
                apartment.sold = True
                agent.buildings_sold = agent.buildings_sold + 1
                agent.amount_earned = agent.amount_earned + data['amount_earned']
                db.session.commit()
                # returns all the conditions are met and the apartment is sold
                return jsonify({'message': 'sold'})
            # returns if the inputted name is not in the database
            return jsonify({'message': ' invalid data, check agent or client'})
        # this runs if the apartment is already sold
        return jsonify({'message': 'already sold'})
    except:
        return 'problem with making sale, check data to confirm validity'


@api.route('/sack/agent_name', methods=['POST'])
@login_required
@admin_required
def sack(agent_name):
    # sacking an agent
    agent = Agent.query.filter_by(first_name=agent_name).first()
    agent.sacked = True
    db.session.commit()
    return jsonify({'message': "agent sacked"})
