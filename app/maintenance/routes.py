
from flask import render_template, url_for, redirect, request, flash, current_app, send_from_directory, jsonify
from flask_login import current_user, login_required
from sqlalchemy import case

from app.common.models import Report, Module, WorkOrder
from app.admin.models import User
from app.utils import get_prev_ref, get_users_list, save_images
from app.common.datetime_format import get_today, format_datetime, format_time
from .utils import create_wo_notification

from . import maintenance_bp


@maintenance_bp.route("/maintenance/index")
def maintenance():
    title = "Mantenimiento"
    previous_url = get_prev_ref()
    
    reports = Report.query.all()
    
    return render_template("maintenance/maintenance.html",
                           title = title,
                           previous_url = previous_url,
                           reports = reports)
    

@maintenance_bp.route("/OTs")
@login_required
def work_orders():
    title = "Ordenes de trabajo"
    previous_url = get_prev_ref()
    nr = request.args.get("report")
    man = Module.query.filter_by(code="MAN").first()
    
    if nr:
        priority_order = case(
        
            (WorkOrder.priority_level == "Inmediata", 1),
            (WorkOrder.priority_level == "Alta", 2),
            (WorkOrder.priority_level == "Media", 3),
            (WorkOrder.priority_level == "Baja", 4),
            else_=5 
        
        )

        work_orders = (
            WorkOrder.query
            .filter_by(status="Abierta", mod_id=man.id)
            .order_by(priority_order, WorkOrder.request_date.desc())
            .all()
        )
    else:
        work_orders = WorkOrder.query.order_by(WorkOrder.id.desc()).all()
    
    
    return render_template("maintenance/work_orders.html",
                           title = title,
                           work_orders = work_orders,
                           previous_url = previous_url)
    

@maintenance_bp.route("/OT/view/<int:wo_id>")
@login_required
def work_order_view(wo_id):
    title = "Orden de trabajo"
    previous_url = get_prev_ref()
    wo = None
    try:
        wo = WorkOrder.get_by_id(WorkOrder,wo_id)
    except:
        flash("No se encontro la OT", "danger")
        return redirect(url_for("maintenance.work_orders"))
    
    reports = Report.query.filter_by(work_order_id = wo.id)
    return render_template("maintenance/work_order_view.html",
                           title = title,
                           wo = wo,
                           previous_url = previous_url,
                           mod_id = wo.mod_id,
                           reports = reports)

    
@maintenance_bp.route("/OT/<int:wo_id>", methods=["GET", "POST"])
@maintenance_bp.route("/OT", methods=["GET", "POST"])
@login_required
def work_order(wo_id=None):
    title = "Orden de trabajo"
    previous_url = url_for("maintenance.work_orders")
    work_order = None
    today = get_today()
    users = get_users_list()
    mods = Module.query.all()
    
    if wo_id:
        work_order = WorkOrder.query.get_or_404(wo_id)
        today = work_order.request_date
        
    if request.method == "POST":
        date = request.form.get('date')
        request_date = format_datetime(date)
        activity = request.form.get("activity")
        description = request.form.get('description')
        responsible_id = request.form.get("responsible_id")
        mod_id = int(request.form.get("mod_id"))
        priority_level = request.form.get("priority_level")
        assigned_personnel = request.form.get("assigned_personnel")
        
        if work_order:
            work_order.request_date = request_date
            work_order.activity = activity
            work_order.description = description
            work_order.responsible_id = responsible_id
            work_order.mod_id = mod_id
            work_order.assigned_personnel_id = assigned_personnel
            work_order.priority_level = priority_level
            
        else:
            try:
                work_order = WorkOrder(mod_id = int(mod_id) ,
                                        request_date = request_date,
                                        responsible_id = responsible_id,
                                        activity = activity,
                                        description = description,
                                        assigned_personnel_id = assigned_personnel,
                                        priority_level = priority_level)
            except Exception as e:
                flash(f"error mod_id {(type(mod_id), mod_id), (type(responsible_id), responsible_id)} , error:{e}")
                return render_template("maintenance/work_order.html",
                           title = title,
                           previous_url = previous_url,
                           work_order = work_order,
                           users = users,
                           today = today,
                           mods = mods)
        try:
            work_order.save()
            create_wo_notification(user_id=assigned_personnel, wo_id=work_order.id)
            flash("OT guardada correctamente", "success")
        except:
            flash("Algo salio mal con la OT", "danger")
            return redirect(url_for("maintenance.work_orders"))
        
        return redirect(url_for("maintenance.work_orders"))
    
    return render_template("maintenance/work_order.html",
                           title = title,
                           previous_url = previous_url,
                           work_order = work_order,
                           users = users,
                           today = today,
                           mods = mods)
    

@maintenance_bp.route("/close_ot/<int:wo_id>", methods=["GET", "POST"])
@login_required
def close_work_order(wo_id):
    
    title = "Cerrar OT"
    previous_url = get_prev_ref()
    users = get_users_list()
    today = get_today()
    
    try: 
        work_order = WorkOrder.get_by_id(WorkOrder, wo_id)
    except:
        flash("No se encontro la orden de trabajo", "warning")
        return redirect(url_for("maintenance.work_orders"))
    
    if request.method == "POST":
        end_date = request.form.get("date")
        end_date = format_datetime(end_date)
        close_responsible = request.form.get("close_responsible")
        status = request.form.get("status")
        
        work_order.status = status
        work_order.end_date = end_date
        work_order.close_responsible = close_responsible
    
        try:
            work_order.save()
        except:
            flash("No se pudo cerrar la OT", "danger")
        
        return redirect(url_for("maintenance.work_orders"))
    
    return render_template("maintenance/close_work_order.html",
                           title = title,
                           previous_url = previous_url,
                           work_order = work_order,
                           users = users,
                           today = today)


@maintenance_bp.route("/delete_work_order/<int:wo_id>")
@login_required
def delete_work_order(wo_id):
    
    try:
        wo = WorkOrder.query.get_or_404(wo_id)
        wo.delete()
        flash("Registro borrado exitosamente", "success")
    except:
        flash("No se puede eliminar el registro", "danger")
            
    return redirect(url_for("maintenance.work_orders"))



@maintenance_bp.route('/wo_search')
def wo_search():
    query = request.args.get('q', '').lower()
    results_by_activity = WorkOrder.query.filter(WorkOrder.activity.ilike(f'%{query}%')).all()
    results_by_responsible = WorkOrder.query.join(User, WorkOrder.responsible_id == User.id) \
                                            .filter(User.name.ilike(f'%{query}%')).all()
    results_by_code = WorkOrder.query.filter(WorkOrder.code.ilike(f"%{query}%")).all()
    # Supongamos que `request_date` es una cadena en formato 'YYYY-MM-DD'
    results_by_date = WorkOrder.query.filter(WorkOrder.request_date.ilike(f'%{query}%')).all()
    
    # Combinar los resultados, eliminando duplicados
    results = list({wo.id: wo for wo in results_by_activity + results_by_responsible + results_by_date + results_by_code}.values())
    
    # Serializar los resultados
    results_serialized = [
        {
            'id': wo.id,
            'activity': wo.activity,
            'request_date': wo.request_date.strftime('%Y-%m-%d'),
            'responsible': wo.responsible.name,
            'code': wo.code
        }
        for wo in results
    ]
    
    return jsonify({'results': results_serialized})
