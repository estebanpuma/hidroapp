from flask import render_template, redirect, url_for, request, send_from_directory, flash

from app.utils import get_prev_ref

from . import ops_bp


@ops_bp.route("/ops")
def ops():
    title = "Operaciones"
    previous_url = get_prev_ref()
    
    return render_template("ops/ops.html",
                           title = title,
                           previous_url = previous_url)