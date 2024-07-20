from flask import render_template, redirect, url_for, request, flash, current_app, send_from_directory

from . import common_bp
from .models import Activity, Module, Report, ReportImages
from app.utils import get_prev_ref, already_exist, get_users_list, get_last_report_number
from werkzeug.utils import secure_filename
from .datetime_format import *
import os
from datetime import datetime, time
import uuid

@common_bp.route("/<module>/activity/<int:activity_id>")
def activity(module, activity_id):
    title = "Actividad"
    module = module
    activity = Activity.query.get(activity_id)
    previous_url = get_prev_ref()
        
    print(f"This is the pppp {previous_url}")
    print(f"This is the module {module}")
    return render_template("common/activity.html", 
                           title = title,
                           activity = activity,
                           module = module,
                           previous_url = previous_url)
    

@common_bp.route('/report/<int:report_id>/', methods=['GET', 'POST'])
@common_bp.route('/report', methods=['GET', 'POST'])
def report(report_id=None):
    mod_id = request.args.get('mod_id')
    print(f"mod_id: {mod_id}")
    mod=None
    code = None
    report = None
    
    if mod_id:
        mod = Module.get_by_id(mod_id)
        code = mod.code
        if mod.code == "MAN":
            return redirect(url_for("maintenance.maintenance_report"))
        
    report_number = get_last_report_number(mod_id)+1
    
    title = "Reporte"
    previous_url = get_prev_ref()
    users = get_users_list()
    activities = Activity.query.all()
    print(f"code before: {code}")
    code = "HID-" + str(code) +"-" + str(this_year()) + "-" + str(report_number) 
    print(f"code after: {code}")
    today = get_today()
    if report_id:
        report = Report.query.get_or_404(report_id)
        code = report.code
    else:
        report = Report()
    
    if request.method == 'POST':
        
        code = request.form.get("code")
        mod_id = request.form.get("mod_id")
        responsible = request.form.get('responsible')
        date = request.form.get('date')
        activity = request.form.get("activity")
        description = request.form.get('description')
        team = request.form.get('team')
        start_hour = request.form.get('start')
        end_hour = request.form.get('end')
        place = request.form.get('place')
        notes = request.form.get("notes")
        
        
        
        if end_hour <= start_hour:
            flash("La hora de finalización no puede ser menor a la hora de inicio", "danger")
            return redirect(request.url)
        
        try:
            date = format_datetime(date)
            start_hour = format_time(start_hour)
            end_hour = format_time(end_hour)
        except ValueError as e:
            flash(str(e), "error")
            return redirect(request.url)
        
        total_time = calculate_time_difference(start_hour, end_hour)

        
        mod_id = request.form.get("mod_id")
        code = request.form.get("code")
        report.code = code
        report.mod_id = mod_id
        report.responsible_id = int(responsible)
        report.date = date
        report.activity = activity
        report.description = description
        report.team = team
        report.start_hour = start_hour
        report.end_hour = end_hour
        report.total_time = total_time
        report.place = place
        report.notes = notes
        mod = Module.get_by_id(mod_id)
        report.save()
        
        files = request.files.getlist('files')
        print(files)
        for file in files:
            if file and file.filename:
                filename = str(get_timestamp())[6:]+".jpeg"
                filename = secure_filename(filename)
                existing_file = ReportImages.query.filter_by(filename=filename).first()
                if existing_file:
                    filename = f"{uuid.uuid4().hex}_{filename}"
                file_dir = current_app.config["REPORT_IMAGES_DIR"]
                os.makedirs(file_dir, exist_ok=True)
                file_path = os.path.join(file_dir, filename)
                file.save(file_path)
                n_file = ReportImages(report_id = report.id,
                                    filename = filename)
                n_file.save()
    
        return redirect(url_for("common.reports")) 

    return render_template("common/report.html", 
                           title = title,
                           mod = mod,
                           code = code,
                           activities = activities,
                           users = users,
                           report = report,
                           previous_url = previous_url,
                           today = today)


@common_bp.route("/delete_report/<int:report_id>/")
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    print(report.id, report.activity, report.description)
    report_images = ReportImages.query.filter_by(report_id=report.id).all()
    
    
    try:
        for image in report.images:
            image.delete()
        report.delete()
        flash("Reporte eliminado", "info")
    except:
        flash("No se puedo eliminar el registro", "danger")
        return redirect(url_for("common.reports"))
    
    return redirect(url_for("common.reports"))


@common_bp.route("/reports")
def reports():
    previous_url = get_prev_ref()
    title = "Reportes"
    reports = Report.query.all()
    return render_template("common/reports.html", 
                           title = title,
                           previous_url = previous_url,
                           reports = reports)


@common_bp.route("/report_view/<int:report_id>")
def report_view(report_id):
    report = Report.get_by_id(Report, report_id)
    title = "Reporte"
    previous_url = get_prev_ref()
    return render_template("common/report_view.html",
                           title = title,
                           previous_url = previous_url,
                           report = report)
        

@common_bp.route("/media/reports/<filename>")
def media_report(filename):
    dir_path = os.path.join(
        current_app.config["MEDIA_DIR"],
        current_app.config["REPORT_IMAGES_DIR"]
    )
    return send_from_directory(dir_path, filename)
    
    
@common_bp.route("/<module>/add_activity/<int:activity_id>", methods=["GET", "POST"])
@common_bp.route("/<module>/add_activity/", methods=["GET", "POST"])
def add_activity(module, activity_id=None):
    title = "Nueva actividad"
    module = module
    previous_url = get_prev_ref()
    activity = Activity.query.get(activity_id)
    error_msg = None
    
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
            
            if already_exist(Activity, name, module):
                error_msg = f"La actividad: {name} ya existe"
            n_env_activity = Activity(module= module,
                                      name=name,
                                      description=description,
                                      notes=notes)
            n_env_activity.save()
        
        return redirect(previous_url)
    
    return render_template("common/add_activity.html", 
                           title = title,
                           module = module,
                           activity = activity,
                           previous_url = previous_url,
                           error_msg = error_msg)
    

