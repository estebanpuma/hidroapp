from flask import render_template, redirect, url_for, request, flash

from . import environment_pga_bp
from .models import PgaActivity, Month, PgaActivityMonth, User, Activity
from . variables import this_module

from app.utils import get_users_list, already_exist, delete_activity

@environment_pga_bp.route("/pga")
def pga():
    title = "Programa de Gestión Ambiental"
    months = Month.query.all()
    
    activities = PgaActivity.query.all()
    
    pga_activity_month = PgaActivityMonth.query.filter_by(year=2024).all()

    
    return render_template("pga/pga.html",
                           title = title,
                           months = months,
                           activities = activities,
                           pga_activity_month = pga_activity_month)
    

@environment_pga_bp.route("/env_activities")
def env_activities():
    title = "Actividades"
    env_activities = Activity.get_by_module(this_module)
    
    return render_template("pga/env_activities.html",
                           title = title,
                           env_activities = env_activities,
                           module = this_module)
    

@environment_pga_bp.route("/add_activity/<int:activity_id>", methods=["GET", "POST"])
@environment_pga_bp.route("/add_activity", methods=["GET", "POST"])
def add_activity(activity_id=None):
    
    activity = Activity.query.get(activity_id)
    error_msg = None
   
    title = "Nueva actividad"
    
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        notes = request.form["notes"]
        
        if activity:
            title = "Editar"
            activity.name = name
            activity.description = description
            activity.notes = notes
            
            activity.save()
            
        else:
            
            if already_exist(Activity, name, this_module):
                error_msg = f"La actividad: {name} ya existe"
            n_env_activity = Activity(module= this_module,
                                      name=name,
                                      description=description,
                                      notes=notes)
            n_env_activity.save()
        
        return redirect(url_for('pga.env_activities'))
   
    return render_template("pga/add_activity.html",
                           title = title,
                           activity = activity,
                           error_msg = error_msg)
    
    
@environment_pga_bp.route("/add_pga_activity/<int:pga_activity_id>/", methods=["GET", "POST"])
@environment_pga_bp.route("/add_pga_activity", methods=["GET","POST"])
def add_pga_activity(pga_activity_id=None):
    title = "Programa de Gestión Ambiental"
    error_msg = None
    users = get_users_list()
    months = Month.query.all()
    activities = Activity.get_by_module(this_module)
    pga_activity = PgaActivity.get_by_id(pga_activity_id)
    pga_activity_month = PgaActivityMonth.query.filter_by(pga_activity_id=pga_activity_id, year=2024).all()
    am_list = []
    if pga_activity_month:
        for ac in pga_activity_month:
            am_list.append(int(ac.month_id)) 
        
    if request.method == "POST":
        
        selected_months = request.form.getlist("months")
        responsible = request.form["responsible"]

        
        if pga_activity:
            pga_activity.activity_id = pga_activity_id
            pga_activity.responsible_id = responsible
            pga_activity.save()
            for a in pga_activity_month:
                a.delete()
                
            for month in selected_months:
                    
                    activity_month = PgaActivityMonth(month_id=int(month), pga_activity_id=pga_activity.id, year=2024)
                    activity_month.save()
            
 
            return redirect(url_for('pga.pga'))
        else:
            activity = request.form["activity"]
           
            n_pga_activity = PgaActivity(activity_id = activity,
                                        responsible_id = responsible,)
            n_pga_activity.save()
            print(selected_months)
            for month in selected_months:
                activity_month = PgaActivityMonth(month_id=int(month), pga_activity_id=n_pga_activity.id, year=2024)
                activity_month.save()
                print(activity_month)
                    
            return redirect(url_for('pga.pga'))
            
            
    return render_template("pga/add_pga_activity.html",
                           title = title,
                           activities = activities,
                           pga_activity = pga_activity,
                           error_msg = error_msg,
                           months = months,
                           am_list = am_list,
                           users = users)


@environment_pga_bp.route("/delete_env_activity/<int:activity_id>", methods=["GET", "POST"])
def delete_env_activity(activity_id):
    delete_activity(activity_id)
    return redirect(url_for('pga.env_activities'))
    

@environment_pga_bp.route("/delete_pga_activity/<int:pga_activity_id>", methods=["GET", "POST"])
def delete_pga_activity(pga_activity_id):
    if not pga_activity_id:
        flash("Error: No se proporcionó ningún ID de actividad PGA", "danger")
        return redirect(url_for('pga.pga'))

    query = PgaActivity.query.get(pga_activity_id)
    if query is None:
        flash(f"No existe una actividad PGA con el ID: {pga_activity_id}", "danger")
    else:
        try:
            query.delete()
            flash("La actividad PGA ha sido eliminada correctamente", "success")
        except Exception as e:
            flash(f"Error al eliminar la actividad PGA: {str(e)}",  "danger")

    return redirect(url_for('pga.pga'))