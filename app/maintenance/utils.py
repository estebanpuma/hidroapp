from flask import flash, request
from app.common.datetime_format import format_datetime



def create_wo_notification(user_id, wo_id):
    if user_id and wo_id:
        try:
            from app.admin.models import User
            from app.common.models import WorkOrder
            from app.notifications.models import Notification, UserNotification
            
            user = User.query.get(user_id)
        
           
            wo = WorkOrder.query.get(wo_id)
            
  
            new_notification = Notification(wo_id = wo_id, 
                                               message = f"Se le ha asignado una actividad")

            
            new_notification.save()
           
           
            user_notification = UserNotification(user_id=user_id, notification_id = new_notification.id)
            
            user_notification.save()
            
        except:
            flash(f"No se pudo generar notificación para el usuario id: {user_id}", "warning")
    
    else:
        flash("No se proporcionó un ID de reporte o actividad.", "warning")
        return
    
    
    
def save_wo(work_order=None, form = None):
    
    from app.common.models import WorkOrder
    
    date = form.get('date')
    request_date = format_datetime(date)
    activity = form.get("activity")
    description = form.get('description')
    responsible_id = form.get("responsible_id")
    mod_id = int(form.get("mod_id"))
    priority_level = form.get("priority_level")
    assigned_personnel_id = form.get("assigned_personnel")
    
    if work_order:
        work_order.request_date = request_date
        work_order.activity = activity
        work_order.description = description
        work_order.responsible_id = responsible_id
        work_order.mod_id = mod_id
        work_order.assigned_personnel_id = assigned_personnel_id
        work_order.priority_level = priority_level
        try:
            
            work_order.save()
        except:
            flash("Ocurrio un error gurdando OT", "danger")
        
    else:
        try:
            work_order = WorkOrder(mod_id = int(mod_id) ,
                                    request_date = request_date,
                                    responsible_id = responsible_id,
                                    activity = activity,
                                    description = description,
                                    assigned_personnel_id = assigned_personnel_id,
                                    priority_level = priority_level)
            
            work_order.save()
            
            create_wo_notification(user_id=assigned_personnel_id, wo_id=work_order.id)
            
        except Exception as e:
            flash("Ocurrio un error gurdando OT", "danger")
            
    