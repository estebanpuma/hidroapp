from flask import redirect, render_template, flash, url_for

from app.utils import get_prev_ref

from . import sst_bp


@sst_bp.route("/sst")
def sst():
    title = "Seguridad y salud"
    previous_url = get_prev_ref()
    return render_template("sst/sst.html",
                           title = title,
                           previous_url = previous_url)