from flask import Blueprint

maintenance_bp = Blueprint("maintenance", __name__, template_folder="templates")

from . import routes