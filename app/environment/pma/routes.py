from flask import render_template, redirect, url_for

from . import environment_pma_bp

@environment_pma_bp.route("/pma")
def pma():
    title = "PMA"
    
    return render_template("pma/pma.html",
                           title = title)