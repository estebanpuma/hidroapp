from flask import render_template, redirect, url_for, request, flash, current_app, send_from_directory, make_response, abort
from app.pdf import create_pdf
from . import common_bp
from .models import Activity, Module, Report, ReportImages, ReportDetail, MaintenanceDetails, WorkOrder

from app.utils import get_prev_ref, already_exist, get_users_list, get_last_report_number, save_images
from werkzeug.utils import secure_filename
from .datetime_format import *
import os
import uuid

#

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
    

def save_report(mod_id, form, files=None, report=None, wo_id=None ):
    mod = Module.query.get_or_404(mod_id)
    
    if report is None:
        
        report = Report()
        report.mod_id = mod.id
        code = report.generate_code(mod.id)
        report.code = code
        report.work_order_id = wo_id
        report.save()
        
    if report.details:
        detail = report.details
    else:
        detail = ReportDetail()
        report.details = detail

    detail.report_id = report.id
    detail.activity = form.get("activity")
    detail.description = form.get("description")
    detail.responsible_id = form.get("responsible_id")
    date = form.get("date")
    detail.date = format_datetime(date)
    start_hour = format_time(form.get("start_hour")) 
    end_hour = format_time(form.get("end_hour"))
    detail.start_hour = start_hour
    detail.end_hour = end_hour
    detail.total_time = detail.calculate_total_time(start_hour, end_hour)
    detail.notes = form.get("notes")
    detail.team = form.get("team")
    try:
        detail.save()
    except:
        report.delete()
        flash("No se pudo guardar el reporte", "danger")
        return redirect(url_for("common.reports"))

    # Handle file uploads
    
    if mod.code == "MAN":
        if report.maintenance_details:
            maintenance_details = report.maintenance_details
        else:
            maintenance_details = MaintenanceDetails()
            report.maintenance_details = maintenance_details
        maintenance_details.report_id = report.id
        maintenance_details.maintenance_type = form.get("type")
        maintenance_details.element = form.get("element")
        maintenance_details.system = form.get("system")
        maintenance_details.subsystem = form.get("subsystem")
        try:
            maintenance_details.save()
        except:
            report.delete()
            flash("No se pudo guardar el reporte", "danger")
            return redirect(url_for("common.reports"))
    
    for file in files:
        if file and file.filename:
            print("ingresa a file")
            save_images("REPORT_IMAGES_DIR", file, ReportImages, report.id)        
    

 


@common_bp.route('/report/<int:mod_id>', methods=['GET', 'POST'])
def report(mod_id):
    title = "Reporte"
    wo_id = request.args.get("wo_id")
    wo = WorkOrder.get_by_id(WorkOrder, wo_id)
    previous_url = get_prev_ref()
    users = get_users_list()
    mod = Module.query.get_or_404(mod_id)
    if mod.code == "MAN" and wo_id == None:
        return redirect(url_for("maintenance.work_orders"))
    today = get_today()
    activities = Activity.query.all()

    if request.method == "POST":
        form = request.form
        files = request.files.getlist("files")
        save_report(mod_id=mod_id,
                    form=form,
                    files=files,
                    wo_id=wo_id)
        
        flash('Reporte creado satisfactoriamente!', 'success')
        
        return redirect(url_for('common.reports'))

    return render_template("common/report.html",
                           title = title,
                           previous_url = previous_url,
                           users = users,
                           mod = mod,
                           today = today,
                           wo = wo,
                           activities = activities)
    

@common_bp.route('/edit_report/<int:report_id>', methods=['GET', 'POST'])
def edit_report(report_id):
    title = "Editar Reporte"
    previous_url = get_prev_ref()
    report = Report.query.get_or_404(report_id)

    if request.method == "POST":
        form = request.form
        files = request.files.getlist("files")
        report = save_report(mod_id=report.mod_id,
                             form=form,
                             files=files,
                             report = report)
        
        return redirect(url_for("common.reports"))

    return render_template('common/edit_report.html',
                           title = title,
                           previous_url = previous_url)



@common_bp.route("/delete_report/<int:report_id>/")
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    report_images = ReportImages.query.filter_by(report_id=report.id).all()
    
    
    try:
        for image in report_images:
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
    images = ReportImages.query.filter_by(report_id=report.id).all()
    title = "Reporte"
    previous_url = get_prev_ref()
    return render_template("common/report_view.html",
                           title = title,
                           previous_url = previous_url,
                           report = report,
                           images = images)
        

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
    



@common_bp.route('/generate_pdf/<int:report_id>')
def generate_pdf(report_id):
    
    report = Report.query.get(report_id)
    images = ReportImages.query.filter_by(report_id=report.id)
    data = {
        'codigo': str(report.code),
        'orden_trabajo': str(report.work_order.code),
        'fecha': str(report.details.date),
        'hora_inicio': str(report.details.start_hour),
        'hora_fin': str(report.details.end_hour),
        'responsable': str(report.details.responsible.name),
        'tipo_mantenimiento': '',
        'sistema': '',
        'subsistema': '',
        'elemento': '',
        'titulo_mantenimiento': str(report.details.activity),
        'descripcion': str(report.details.description),
        'observaciones': ''
    }
    
    image_paths = []  # Add up to 10 image paths
    
        
    for image in images:
        if image.filename:
            image_path = os.path.join(current_app.config['REPORT_IMAGES_DIR'], image.filename)
            if os.path.exists(image_path):
                image_paths.append(image_path)
            else:
                print(f"Image file not found: {image_path}")
        
        if len(image_paths) >= 10:
            break  # Limit to 10 images
    
    print(f"Image paths: {image_paths}")
    
    print(image_paths)
    pdf = create_pdf(data, image_paths)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=Reporte_{report.code}.pdf'

    return response


