from flask import Blueprint

sst_bp = Blueprint("sst", __name__, template_folder="templates")

from . import routes