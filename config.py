import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
# Добавление переменных окружения из файла .env
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SEKRET_KEY') or 'any_sekret_word'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN = ['bloody.sekret@yandex.ru']

    POST_PER_PAGE = 25
    LANGUAGES = ['en', 'ru']

    DEBUG = True
    TESTING = False

