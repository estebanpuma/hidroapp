import os

from flask import render_template, redirect, url_for, request, flash, current_app, send_from_directory, make_response, session, jsonify
from flask_login import current_user, login_required

from app.pdf import create_pdf
from . import common_bp
from .models import Activity, Module, Report, ReportImages, WorkOrder

from app.utils import get_prev_ref, already_exist, get_users_list
from .datetime_format import *

from .utils import save_report



#************************Acividades***********************************

@common_bp.route("/add_activity/<int:activity_id>", methods=["GET", "POST"])
@common_bp.route("/add_activity/", methods=["GET", "POST"])
@login_required
def add_activity(activity_id=None):
    previous_url = get_prev_ref()
    title = "Nueva actividad"
    mod_code = request.args.get("mod_code")
    mod = None
    if mod_code:
        try:
            mod = Module.query.filter_by(code = mod_code).first()
        except:
            flash("Ocurrió un error (mod_code)", "danger")
            return redirect("common.activities")
        
    activity = None
    
    if activity_id:
        activity = Activity.query.get_or_404(activity_id)
        title = "Editar"
    error_msg = None
    
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        module = request.form["mod"]
        
        
        if activity:
            title = "Editar"
            activity.name = name
            activity.description = description
            activity.mod_id = int(module)
            
            activity.save()
            
        else:
            
            if already_exist(Activity, name, module):
                error_msg = f"La actividad: {name} ya existe"
            n_env_activity = Activity(mod_id= module,
                                      name=name,
                                      description=description,
                                      )
            n_env_activity.save()
        
        return redirect(url_for("common.activities"))
    
    return render_template("common/add_activity.html", 
                           title = title,
                           activity = activity,
                           previous_url = previous_url,
                           error_msg = error_msg)


@common_bp.route("/activities/")
def activities():
    title = "Actividades"
    previous_url = get_prev_ref()
    activities = Activity.query.all()

    return render_template("common/activities.html",
                           title = title,
                           previous_url = previous_url,
                           activities = activities,
                           )


@common_bp.route("/view_activity/<int:activity_id>")
def view_activity(activity_id):
    title = "Actividad"
    
    activity = Activity.query.get_or_404(activity_id)
    previous_url = get_prev_ref()
        
    return render_template("common/view_activity.html", 
                           title = title,
                           activity = activity,
                           
                           previous_url = previous_url)
    

@common_bp.route("/delete_activity/<int:activity_id>/")
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    try:
        activity.delete()
        flash("Actividad eliminada satisfactoriamente", "success")
    except Exception:
        flash("Ocurrió un error al emininar la actividad", "danger")

    return redirect(url_for("common.activities"))
    
    
#******************Reports*************************************

@common_bp.route('/report/<int:mod_id>', methods=['GET', 'POST'])
@login_required
def report(mod_id):
    title = "Reporte"
    wo_id = request.args.get("wo_id")
    wo = WorkOrder.get_by_id(WorkOrder, wo_id)
    previous_url = get_prev_ref()
    users = get_users_list()
    users = [{'id': user.id, 'name': user.name} for user in users]
    mod = Module.query.get_or_404(mod_id)
    if mod.code == "MAN" and wo_id == None:
        return redirect(url_for("maintenance.work_orders", report="report"))
    if mod.code == "ASE":
        return redirect(url_for())
    today = get_today()
    activities = Activity.query.all()

    if request.method == "POST":
        form = request.form
        files = None
        files = request.files.getlist("files")
        
        try:
            save_report(mod_id=mod_id,
                        form=form,
                        files=files,
                        wo_id=wo_id)
        
        except:
            files.clear()
            print("entra a excet")
            return render_template("common/report.html",
                           title = title,
                           previous_url = previous_url,
                           users = users,
                           mod = mod,
                           today = form.get("date"),
                           wo = wo,
                           form = form,
                           activities = activities)
            
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
@login_required
def edit_report(report_id):
    title = "Editar Reporte"
    previous_url = get_prev_ref()
    report = Report.query.get_or_404(report_id)
    mods = Module.query.all()
    images = ReportImages.query.filter_by(report_id = report.id).all()
    users = get_users_list()

    if request.method == "POST":
        form = request.form
        files = request.files.getlist("files")
        mod_id = request.form.get("mod")
        try:
            save_report(mod_id=report.mod_id,
                             form=form,
                             files=files,
                             report = report)
            flash("Reporte guardado exitosamente", "success")
            return redirect(url_for("common.reports"))
        except:
            files.clear()
            print("entra a excet edit")
            return render_template('common/edit_report.html',
                           title = title,
                           report = report,
                           mods = mods,
                           users = users,
                           images = images,
                           form = form,
                           previous_url = previous_url)
            

    return render_template('common/edit_report.html',
                           title = title,
                           report = report,
                           mods = mods,
                           users = users,
                           images = images,
                           previous_url = previous_url)


@common_bp.route("/delete_image_report/<int:image_id>/", methods=["DELETE"])
@login_required
def delete_image_report(image_id):
    print("ingresa al metodo delete")
    try:
        # Llama a tu función de eliminación en la base de datos
        image = ReportImages.query.get(image_id)
        if image:
            print("hay image")
        print("no image")
        image.delete()
        return jsonify({'message': 'Imagen eliminada con éxito.'}), 200
    except Exception as e:
        # Maneja los errores adecuadamente
        return jsonify({'message': 'Error al eliminar la imagen.', 'error': str(e)}), 500
    

@common_bp.route("/delete_report/<int:report_id>/")
@login_required
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    report_images = ReportImages.query.filter_by(report_id=report.id).all()
      
    try:
        for image in report_images:
            image.delete()
        report.delete()
        flash("Reporte eliminado", "success")
    except:
        flash("No se puedo eliminar el registro", "danger")
        return redirect(url_for("common.reports"))
    
    return redirect(url_for("common.reports"))


@common_bp.route("/reports")
@login_required
def reports():
    previous_url = get_prev_ref()
    title = "Reportes"
    if current_user.role.name == "Operador":
        reports = Report.query.order_by(Report.id.desc()).all()
    else:
        reports = Report.query.join(Report.details).filter(Report.details.has(responsible_id=current_user.id)).order_by(Report.id.desc()).all()
    return render_template("common/reports.html", 
                           title = title,
                           previous_url = previous_url,
                           reports = reports)


@common_bp.route("/report_view/<int:report_id>")
@login_required
def report_view(report_id):
    report = Report.query.get_or_404(report_id)
    images = ReportImages.query.filter_by(report_id=report.id).all()
    title = "Reporte"
    previous_url = get_prev_ref()
    return render_template("common/report_view.html",
                           title = title,
                           previous_url = previous_url,
                           report = report,
                           images = images)


@common_bp.route("/report/sshh")
@login_required
def report_sshh():
    today = get_today()
    if request.method == "POST":
        activity = "Limpieza baños"
        date = today()
        notes = request.form.get("notes")
        files = request.files.getlist("files")
        responsible_id = current_user.id
        place = request.form.get("place")


@common_bp.route("/media/reports/<filename>")
def media_report(filename):
    dir_path = os.path.join(
        current_app.config["MEDIA_DIR"],
        current_app.config["REPORT_IMAGES_DIR"]
    )
    return send_from_directory(dir_path, filename)
    
    

    



@common_bp.route('/generate_pdf/<int:report_id>')
@login_required
def generate_pdf(report_id):
    
    report = Report.query.get_or_404(report_id)
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
        
        if len(image_paths) >= 9:
            break  # Limit to 10 images
    
    print(f"Image paths: {image_paths}")
    
    print(image_paths)
    pdf = create_pdf(data, image_paths)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=Reporte_{report.code}.pdf'

    return response




    

