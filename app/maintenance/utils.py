from flask import flash



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