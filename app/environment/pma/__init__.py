from flask import Blueprint

environment_pma_bp = Blueprint("pma", __name__, template_folder="templates")

from . import routes