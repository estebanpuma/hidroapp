from flask import render_template, url_for, redirect, request, flash

from .models import MaintenanceImages, MaintenanceReport, WorkOrder
from app.common.models import Module, Activity
from app.admin.models import User
from app.utils import get_prev_ref, get_users_list, save_images
from app.common.datetime_format import get_today, format_datetime, format_time

from . import maintenance_bp


@maintenance_bp.route("/maintenance/index")
def maintenance():
    title = "Mantenimiento"
    previous_url = get_prev_ref()
    reports = MaintenanceReport.query.all()
    return render_template("maintenance/maintenance.html",
                           title = title,
                           previous_url = previous_url,
                           reports = reports)


@maintenance_bp.route("/maintenance/report_view/<int:report_id>")
def maintenance_report_view(report_id):
    title = "Reporte de Mantenimiento"
    previous_url = get_prev_ref()
    try:
        report = MaintenanceReport.query.get(report_id)
    except:
        flash("No se encontro el reporte", "danger")
        return redirect(url_for("maintenance.maintenance"))
    return render_template("maintenance/maintenance_report_view.html",
                           title = title,
                           previous_url = previous_url,
                           report = report)    
    
    
@maintenance_bp.route("/maintenance_report/<int:report_id>", methods=['GET', 'POST'])
@maintenance_bp.route('/maintenance_report', methods=['GET', 'POST'])
def maintenance_report(report_id=None):
    wo_code = request.args.get("code")
    title = "Reporte de mantenimiento"
    previous_ref = get_prev_ref()
    report=None
    mod = Module.query.filter_by(code="MAN").first()
    today = get_today()
    print(today)
    users = get_users_list()
    
    if report_id:
        try:
            report = MaintenanceReport.get_by_id(MaintenanceReport, report_id)
            wo_code = report.workorder_code
        except:
            flash(F"No se encontro Reporte, id: {report_id}", "danger")
            return redirect(url_for("maintenance.maintenance"))
    else:
        report = MaintenanceReport()
    
    try:
        wo = WorkOrder.query.filter_by(code=wo_code).first()
        print(wo.code)
    except:
        flash("OT no encontrada", "danger")
        return redirect(url_for("maintenance.maintenance"))
        
    if request.method == "POST":

        date = request.form.get('date')
        date = format_datetime(date)
        activity = request.form.get("activity")
        description = request.form.get('description')
        responsible_id = request.form.get("responsible_id")
        team = request.form.get('team')
        start_hour = request.form.get('start')
        end_hour = request.form.get('end')
        
        notes = request.form.get("notes")
        system = request.form.get("system")
        subsystem = request.form.get("subsystem")
        element = request.form.get("element")
        type = request.form.get("type")
        start_hour = format_time(start_hour)
        end_hour = format_time(end_hour)
        
        
        report.workorder_code = wo_code
        report.responsible_id = int(responsible_id)
        report.date = date
        report.activity = activity
        report.description = description
        report.team = team
        report.start_hour = start_hour
        report.end_hour = end_hour
        report.total_time = report.calculate_total_time(start_hour, end_hour)
        report.system = system
        report.subsystem = subsystem
        report.element = element
        report.type = type
        report.notes = notes
        
        report.save()
        
        files = request.files.getlist("files")
        print(files)
        for file in files:
            if file and file.filename:
                print("ingresa a file")
                save_images("REPORT_IMAGES_DIR", file, MaintenanceImages, report.id)
            
        return redirect(url_for("maintenance.maintenance"))    
    
    return render_template("maintenance/maintenance_report.html",
                           title = title,
                           previous_ref = previous_ref,
                           report = report,
                           mod = mod,
                           today = today,
                           users = users,
                           wo_code = wo_code)
    

@maintenance_bp.route("/OTs")
def work_orders():
    title = "Órdenes de trabajo"
    previous_url = get_prev_ref()
    work_orders = WorkOrder.query.all()
    return render_template("maintenance/work_orders.html",
                           title = title,
                           work_orders = work_orders,
                           previous_url = previous_url)
    

@maintenance_bp.route("/OT/view/<int:wo_id>")
def work_order_view(wo_id):
    title = "Órden de trabajo"
    previous_url = get_prev_ref()
    wo = None
    try:
        wo = WorkOrder.get_by_id(WorkOrder,wo_id)
    except:
        flash("No se encontro la OT", "danger")
        return redirect(url_for("maintenance.work_orders"))
    return render_template("maintenance/work_order_view.html",
                           title = title,
                           wo = wo,
                           previous_url = previous_url)

    
@maintenance_bp.route("/OT/<int:wo_id>", methods=["GET", "POST"])
@maintenance_bp.route("/OT", methods=["GET", "POST"])
def work_order(wo_id=None):
    title = "Orden de trabajo"
    previous_url = get_prev_ref()
    work_order = None
    today = get_today()
    print(today)
    users = get_users_list()
    
    if wo_id:
        work_order = WorkOrder.query.get_or_404(wo_id)
        print(work_order.activity)
    if request.method == "POST":
        date = request.form.get('date')
        date = format_datetime(date)
        activity = request.form.get("activity")
        description = request.form.get('description')
        responsible_id = request.form.get("responsible_id")
        
        if work_order:
            work_order.date = date
            work_order.activity = activity
            work_order.description = description
            work_order.responsible_id = responsible_id
            
        else:
            work_order = WorkOrder(date = date,
                                   responsible_id = responsible_id,
                                   activity = activity,
                                   description = description)
        
        try:
            work_order.save()
        except:
            flash("Algo salio mal", "danger")
            return redirect(url_for("maintenance.work_orders"))
        
        return redirect(url_for("maintenance.work_orders"))
    
    return render_template("maintenance/work_order.html",
                           title = title,
                           previous_url = previous_url,
                           work_order = work_order,
                           users = users,
                           today = today)
    

@maintenance_bp.route("/delete_work_order/<int:wo_id>")
def delete_work_order(wo_id):
    if wo_id:
        try:
            wo = WorkOrder.get_by_id(WorkOrder, wo_id)
            wo.delete()
            flash("Registro borrado exitosamente", "success")
        except:
            flash("No se puede eliminar el registro", "danger")
            
    return redirect(url_for("maintenance.work_orders"))