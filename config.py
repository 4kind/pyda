import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET KEY') or 'ad8SFAsiu9faASF9sfls32'
    USERNAME = 'admin'
    PASSWORD = 'default'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PYDA_MAIL_SUBJECT_PREFIX = '[PyDA]'
    PYDA_MAIL_SENDER = 'PyDA Admin <kind@posteo.de>'
    PYDA_ADMIN = os.environ.get('PYDA_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 987
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                                'data-dev.sqlite')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                                 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevConfig
}
