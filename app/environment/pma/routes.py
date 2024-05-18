from flask import render_template, redirect, url_for, request

from . import environment_pma_bp
from .models import PmaActivity, Month

@environment_pma_bp.route("/pma")
def pma():
    title = "PMA"
    months = Month.query.all()
    
    pma_activities = PmaActivity.query.all()
    
    return render_template("pma/pma.html",
                           title = title,
                           months = months,
                           pma_activities = pma_activities)
    

@environment_pma_bp.route("/pma_activities")
def pma_activities():
    title = "Actividades del PMA"
    pma_activities = PmaActivity.query.all()
    
    return render_template("pma/pma_activities.html",
                           title = title,
                           pma_activities = pma_activities)
    
    
@environment_pma_bp.route("/add_pma_activity/<int:pma_activity_id>/", methods=["GET", "POST"])
@environment_pma_bp.route("/add_pma_activity", methods=["GET","POST"])
def add_pma_activity(pma_activity_id=None):
    title = "Plan de Manejo Ambiental"
    error_msg = None
    months = Month.query.all()
    pma_activity = PmaActivity.get_by_id(pma_activity_id)
    
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        
        print(f"esta es la descriptcion {description}")
        
        if pma_activity:
            print(f"este es el actuall pma {pma_activity.name, pma_activity.description}")
            pma_activity.name = name
            pma_activity.description = description
            pma_activity.save()
            print(f"este es el nuevo pma {pma_activity.name, pma_activity.description}")
            return redirect(url_for('pma.pma_activities'))
        else:
            name_exist = already_exist(PmaActivity, name)
            
            if name_exist:
                error_msg = f"La actividad con el nombre '{name}' ya se encuentra registrada"
            else:
                n_pma_activity = PmaActivity(name = name,
                                            description = description)
                n_pma_activity.save()
                
                    
                return redirect(url_for('pma.pma_activities'))
            
            
    return render_template("pma/add_pma_activity.html",
                           title = title,
                           pma_activity = pma_activity,
                           error_msg = error_msg,
                           months = months)
    

@environment_pma_bp.route("/delete_pma_activity/<int:pma_activity_id>", methods=["GET", "POST"])
def delete_pma_activity(pma_activity_id=None):
    pma_activity = PmaActivity.get_by_id(pma_activity_id)
    if pma_activity:
        pma_activity.delete()
        return redirect(url_for('pma.pma_activities'))
    

def already_exist(obj_class, name):
    n_instance = obj_class.get_by_name(name)
    if n_instance:
        error_name = True
        return error_name