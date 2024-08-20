import io

from flask import redirect, url_for, flash, request
from flask_login import current_user

from werkzeug.datastructures import FileStorage

from PIL.ImageTk import Image
import piexif

from app.utils import save_images, get_ap_workers, get_operators_list, get_ma_workers
from .datetime_format import *
from .models import Activity, Module, Report, ReportDetail, MaintenanceDetails, MaintenanceSpareParts, ReportImages, ReportTeam

from .exceptions import InvalidFileDate

def save_report(mod_id, form, files=None, report=None, wo_id=None ):
    print("Ingresa a save report")
    mod = Module.query.get_or_404(mod_id)
    
    if report is None:
        
        report = Report()
        report.mod_id = mod.id
        code = report.generate_code(mod.id)
        report.code = code
        report.work_order_id = wo_id
        report.save()
        is_new_report = True
    else:
        is_new_report = False
            
    if report.details:
        detail = report.details
    else:
        detail = ReportDetail()
        report.details = detail
        
    form_team = request.form.getlist('team[]')
    team = list(set(form_team))
   
    if "external" in team:
        n_external = form.get("n_external")
        if n_external is not None and n_external>0:
            n_external = int(n_external)
            detail.n_external = n_external
            
    else:
        detail.n_external = 0        
    
    detail.report_id = report.id
    detail.activity = form.get("activity")
    print(form.get("activity"))
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
    
    
    try:
        detail.save()
    except:
        if is_new_report:
            report.delete()
        flash("No se pudo guardar el reporte", "danger")
        return redirect(url_for("common.reports"))
   
    if team:
        existing_team_ids = []
        
        if is_new_report == False:
            
            existing_team_ids = [worker.person_id for worker in detail.team] 
            
            for worker in detail.team:
                if str(worker.person_id) not in team:
                    try:
                        worker.delete()
                    except Exception as e:
                        flash("Error al eliminar trabajador del equipo.")
           
        for worker in team:
            
            if worker != "external":
                worker_id = int(worker)
                if worker_id not in existing_team_ids:
                    report_team = ReportTeam(report_id=report.id, report_detail_id = detail.id, person_id= worker_id)
                    report_team.save()
            
                
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
            if is_new_report:
                report.delete()
            flash("No se pudo guardar el reporte, exites problemas con los datos del mantenimiento", "danger")
            return redirect(url_for("common.reports"))
    
    
    try:
        process_and_save_images(files, detail, report.id)
       

    except Exception as e:
        flash(f"{str(e)}", "danger")
        if is_new_report:
            report.delete()
        raise RuntimeError("err")
    
    if is_new_report:       
        create_notification(user_id=current_user.id, report_id=report.id)     
      
           
def get_image_metadata(image_file):
    # Abre la imagen usando PIL
            
    image = Image.open(image_file)

    # Extrae los datos EXIF
    exif_data = image._getexif()  # Utiliza el método _getexif() en lugar de image.info['exif']

    if exif_data:
        # Extrae la fecha y hora de la foto
        date_taken = exif_data.get(piexif.ExifIFD.DateTimeOriginal, None)
        if date_taken:
            # Convertir a cadena si es necesario
            date_taken = date_taken.decode('utf-8') if isinstance(date_taken, bytes) else date_taken
            return date_taken
    return None


def img_date_validator(temp_file, date):
    # Resetear el puntero del archivo para asegurarse de leer desde el inicio
    temp_file.seek(0)
    
    # Extraer la fecha de la foto
    date_taken = get_image_metadata(temp_file)
    
    if not date_taken:
         
        raise ValueError("No se pudo verificar la fecha de la foto. Asegúrate de que la foto no esté modificada ni descargada")
        

    # Validar que la foto fue tomada en el día correcto
    current_date = date.strftime("%Y:%m:%d")
    if current_date not in date_taken:
        raise InvalidFileDate("La foto no fue tomada en la fecha correcta.")
    
    return True


def process_and_save_images(files, detail, report_id):
    
    validated_images = []
    try:
    #ciclo para validar las imagenes
        for file in files:
            temp_file = None
            if file and file.filename:
                
                file_content = file.read()
                temp_file = io.BytesIO(file_content)
                if img_date_validator(temp_file, detail.date):
                    save_image = io.BytesIO(file_content)
                    new_img = FileStorage(save_image,filename=file.filename)
                    validated_images.append(new_img)                  
                else:
                    validated_images.clear()
                    raise InvalidFileDate(f"La imagen {file.filename} no fue tomada en la fecha correcta.")
    except Exception as e:
        # Limpiar imágenes guardadas si hay error
        validated_images.clear()
        raise Exception(f"Error: {str(e)}")
            
    finally:
        if temp_file:
            temp_file.close() 

    for img in validated_images:   
        try:
            save_images("REPORT_IMAGES_DIR", img, ReportImages, report_id  )
        except Exception as e:
            # Si falla el guardado de una imagen, eliminar todas las imágenes guardadas
            
            raise RuntimeError(f"Error guardando {img.filename}: {str(e)}")
        
        

def create_notification(user_id, report_id=None):
    if user_id:
        try:
            
           
            from app.admin.models import User
            user = User.query.get(user_id)
        
            from app.notifications.models import Notification, UserNotification

            if report_id:
                report = Report.query.get(report_id)
                new_notification = Notification(report_id = report_id, 
                                                message = f"{user.name} subió un reporte")
                
            
            else:
                flash("No se proporcionó un ID de reporte o actividad.", "warning")
                return
               
            new_notification.save()
           
            operators = get_operators_list()
            
            for user in operators:  # Suponiendo que recipient_users es una lista de usuarios
                user_notification = UserNotification(
                user_id=user.id,
                notification_id=new_notification.id,
                is_read=False  # Inicialmente, la notificación no se ha leído
                )
                user_notification.save()
            
            
            
        except:
            flash(f"No se pudo generar notificación para el usuario id: {user_id}", "warning")
            