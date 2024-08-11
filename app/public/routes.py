from flask import render_template, current_app
from . import public_bp

@public_bp.route("/")
def index():
    title = "Hidrotambo"
    current_app.logger.info('Inicio de aplicacion')
    return render_template("public/index.html",
                           title = title)
    

    
