from flask import redirect, render_template, request, url_for

from . import environment_reforestation_bp

@environment_reforestation_bp.route("/reforestation")
def reforestation():
    title = "Reforestación"
    return render_template("reforestation/reforestation.html",
                           title = title)


@environment_reforestation_bp.route("/greenhouse")
def greenhouse():
    title = "Vivero"
    
    return render_template("reforestation/greenhouse.html",
                           title = title)
    
    
@environment_reforestation_bp.route("/plant_exits")
def plant_exits():
    title = "Entregas"
    return render_template("reforestation/plant_exits.html",
                           title = title)


@environment_reforestation_bp.route("/docs")
def docs():
    title = "Documentos"
    return render_template("reforestation/docs.html",
                           title = title)


@environment_reforestation_bp.route("/plant_tracking")
def plant_tracking():
    title = "Seguimiento"
    return render_template("reforestation/plant_tracking.html",
                           title = title)
    

@environment_reforestation_bp.route("/add_plant", methods=['GET', 'POST'])
def add_plant():
    title = "Nueva planta"
    previous_url = request.referrer
    if previous_url is None:
        previous_url = url_for("public.index")
    return render_template("reforestation/add_plant.html",
                           title = title,
                           previous_url = previous_url)
    
    
@environment_reforestation_bp.route("/add_entry", methods=['GET', 'POST'])
def add_entry():
    title = "Ingreso de plantas"
    return render_template("reforestation/add_entry.html",
                           title = title)
    
    
@environment_reforestation_bp.route("/add_exit", methods=['GET', 'POST'])
def add_exit():
    title = "Egreso de plantas"
    return render_template("reforestation/add_exit.html",
                           title = title)