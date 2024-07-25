from flask import Blueprint

ops_bp = Blueprint("ops", __name__, template_folder="templates")

from . import routes