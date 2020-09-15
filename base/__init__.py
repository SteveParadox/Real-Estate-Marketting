import datetime
from flask import *
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from base.config import Config
#from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
#migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'agent.login'
login_manager.login_message = None
login_manager.session_protection = "strong"
REMEMBER_COOKIE_NAME = 'remember_token'
REMEMBER_COOKIE_DURATION = datetime.timedelta(days=164, seconds=29156, microseconds=10)
REMEMBER_COOKIE_REFRESH_EACH_REQUEST = False
socketio = SocketIO()
mail = Mail()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    jwt.init_app(app)
    #migrate.init_app(app, db)

    from base.api.routes import api
    from base.home.routes import main
    from base.agent.routes import agent
    from base.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(agent)
    app.register_blueprint(api)
    app.register_blueprint(errors)
    return app
