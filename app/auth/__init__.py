from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')

from app.auth import routes