from flask import Blueprint

environment_reforestation_bp = Blueprint("reforestation", __name__, template_folder="templates")

from . import routes