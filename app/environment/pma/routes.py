from flask import render_template, redirect, url_for, request

from . import environment_pma_bp
from .models import PmaActivity, Month, PmaActivityMonth, User, Activity
from . variables import module

from app.common_func import get_users_list

@environment_pma_bp.route("/pma")
def pma():
    title = "PMA"
    months = Month.query.all()
    
    pma_activities = Activity.get_by_module(module)
    
    for a in pma_activities:
        print(a.months)
    
    pma_activity_month = PmaActivityMonth.query.filter_by(year=2024).all()

    
    return render_template("pma/pma.html",
                           title = title,
                           months = months,
                           pma_activities = pma_activities,
                           pma_activity_month = pma_activity_month)
    

@environment_pma_bp.route("/pma_activities")
def pma_activities():
    title = "Actividades del PMA"
    pma_activities = Activity.get_by_module(module)
    
    return render_template("pma/pma_activities.html",
                           title = title,
                           pma_activities = pma_activities)
    
    
@environment_pma_bp.route("/add_pma_activity/<int:pma_activity_id>/", methods=["GET", "POST"])
@environment_pma_bp.route("/add_pma_activity", methods=["GET","POST"])
def add_pma_activity(pma_activity_id=None):
    title = "Plan de Manejo Ambiental"
    error_msg = None
    users = get_users_list()
    print(f"users: {users}")
    months = Month.query.all()
    pma_activity = Activity.get_by_id(pma_activity_id)
    pma_activity_month = PmaActivityMonth.query.filter_by(pma_activity_id=pma_activity_id, year=2024).all()
    am_list = []
    if pma_activity_month:
        for ac in pma_activity_month:
            am_list.append(int(ac.month_id)) 
    print(am_list)
        
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        selected_months = request.form.getlist("months")
        responsible = request.form["responsible"]
        
        print(f"esta es monthss{selected_months}")
        
        if pma_activity:
            pma_activity.name = name
            pma_activity.description = description
            pma_activity.responsible_id = responsible
            
            for a in pma_activity_month:
                a.delete()
                
            for month in selected_months:
                    
                    activity_month = PmaActivityMonth(month_id=int(month), pma_activity_id=pma_activity.id, year=2024)
                    activity_month.save()
            pma_activity.save()
            
            
            print(f"este es el nuevo pma {pma_activity.name, pma_activity.description}")
            return redirect(url_for('pma.pma_activities'))
        else:
            name_exist = already_exist(Activity, name)
            
            if name_exist:
                error_msg = f"La actividad con el nombre '{name}' ya se encuentra registrada"
            else:
                n_pma_activity = Activity(name = name,
                                          module = module,
                                            description = description)
                n_pma_activity.save()
                
                for month in selected_months:
                    activity_month = PmaActivityMonth(month_id=int(month), pma_activity_id=n_pma_activity.id, year=2024)
                    activity_month.save()
                
                    
                return redirect(url_for('pma.pma_activities'))
            
            
    return render_template("pma/add_pma_activity.html",
                           title = title,
                           pma_activity = pma_activity,
                           error_msg = error_msg,
                           months = months,
                           am_list = am_list,
                           users = users)
    

@environment_pma_bp.route("/pma_schedule/<int:pma_activity_id>", methods=["GET", "POST"])
@environment_pma_bp.route("/pma_schedule", methods=["GET", "POST"])
def pma_schedule(pma_activity_id=None):
    title = "Agregar actividad al pma"
    am_list = []
    users = get_users_list()
    if pma_activity_id:
        pma_activity = PmaActivity.get_by_id()
        pacm = PmaActivityMonth.query.filter_by(pma_activity_id=pma_activity_id, year=2024)
    else:
        pma_activity = None
    
    
    return render_template("pma.pma_schedule.html",
                           title = title,
                           pma_activitiy = pma_activity,
                           users = users,
                           am_list = am_list)


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