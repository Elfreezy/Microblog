from flask import Flask
from flask import request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

from config import Config

# Регистрация БД и миграции
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


# Создание приложения
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Отправка лога на почту
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                        fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                        toaddrs=app.config['ADMIN'],
                        subject='Microblog Failure',
                        credentials=auth,
                        secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    # Запись лога в файл
    if not app.debug:
        if not os.path.exists('log'):
            os.mkdir('log')
        file_handler = RotatingFileHandler(
                    filename='log/microblog.log',
                    maxBytes=10240,
                    backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog status')

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db}

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config.get('LANGUAGES')) # best_match выбирает предпочтительный язык по его весу
