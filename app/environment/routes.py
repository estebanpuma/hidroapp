from flask import render_template, redirect, url_for
from . import environment_bp

@environment_bp.route("/")
def environment():
    title = "Ambiente"
    return render_template("environment/environment.html",
                           title = title )