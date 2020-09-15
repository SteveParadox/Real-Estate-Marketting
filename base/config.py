import os


class Config:
    ENV = 'dev'

    if ENV == 'dev':
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:

        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'crazythoughtverify@gmail.com'
    MAIL_PASSWORD = 'saintvirus11'
    MAIL_DEFAULT_SENDER = 'from@example.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BABEL_DEFAULT_LOCALE = 'en'
    WHOOSH_BASE = 'whoosh'
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY')
