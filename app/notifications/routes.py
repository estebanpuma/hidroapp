from flask import jsonify, redirect, url_for, flash

from flask_login import login_required, current_user

from .models import Notification, UserNotification

from . import notifications_bp

@notifications_bp.route("/get_notifications")
@login_required
def get_notifications():
    try: 
        user_id = current_user.id
        notifications = Notification.query.join(UserNotification).filter(UserNotification.user_id == user_id).order_by(Notification.created_at.desc()).all()
        notifications_uncheck = Notification.query.join(UserNotification).filter(UserNotification.user_id == user_id, UserNotification.is_checked == False).all()
        total_notifications = len(notifications_uncheck)
        
        # Serializa las notificaciones en formato JSON
        
        
        from app.common.models import Report, ReportDetail, WorkOrder
        
        notifications_data = []
        for n in notifications:
            # Encuentra el UserNotification correspondiente para el usuario actual
            user_notification = UserNotification.query.filter_by(notification_id = n.id).first()
            
            activity = None
            if n.report_id:
                report = Report.query.get(n.report_id)
                if report:
                
                    
                    details = ReportDetail.query.filter_by(report_id = report.id).first()
                    activity = details.activity
                  
            elif n.wo_id:
                wo =  WorkOrder.query.get(n.wo_id)
                if wo:
                    activity = wo.activity
                
            notifications_data.append({
                "id": n.id,
                "report_id": n.report_id if n.report_id else False,
                "wo_id": n.wo_id if n.wo_id else False,
                "message": n.message,
                "activity": activity,
                "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "is_read": user_notification.is_read if user_notification else False,
            })
        
        
        
        return jsonify({
            "total_notifications": total_notifications,
            "notifications": notifications_data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notifications_bp.route("/check_notifications")
@login_required
def check_notifications():
    user_id = current_user.id
    user_notifications = UserNotification.query.filter(UserNotification.user_id == user_id, UserNotification.is_checked == False).all()
    
    try:
        for notification in user_notifications:
            notification.is_checked = True
            notification.save()
            
    except Exception as e:
        return jsonify("Ocurrio un error al checkar las notificaciones")
    
    return jsonify("Notificaciones checadas")


@notifications_bp.route("/read_notification/<int:notification_id>")
@login_required
def read_notification(notification_id):
    
    user_id = current_user.id
    notificacion = Notification.query.get_or_404(notification_id)
    
    user_notification = UserNotification.query.filter(UserNotification.notification_id == notificacion.id,
                                                      UserNotification.user_id == user_id).first()
    user_notification.is_read = True
    
    
    try:
        user_notification.save()
    except Exception as e:
        return jsonify(f"Error {e}")
    
    if notificacion.report_id:
        return redirect(url_for("common.report_view", report_id=notificacion.report_id))
    
    elif notificacion.wo_id:
        return redirect(url_for("maintenance.work_order_view", wo_id=notificacion.wo_id))
    
    return jsonify("Nofificación leida por el usuario")


