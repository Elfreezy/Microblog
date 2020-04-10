from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    username = StringField(_l('Name'), validators=[DataRequired()])             # Проверяет на пустоту поле
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember me'))
    submit = SubmitField(_l('Sign in'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[Email(), DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat password'), validators=[DataRequired(),\
    EqualTo('password')])
    submit = SubmitField(_l('Register'))

    # Проверка на существующее имя
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different name'))

    # Проверка на существующий адресс
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError(_l('Please use a different email adress'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Your password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat it'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Ok'))