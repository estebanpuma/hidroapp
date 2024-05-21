from flask import Blueprint

environment_pga_bp = Blueprint("pga", __name__, template_folder="templates")

from . import routes