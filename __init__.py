from flask import Blueprint

bp = Blueprint('goals', __name__, template_folder = 'templates')

from . import routes, models