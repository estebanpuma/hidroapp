from flask import redirect, url_for, request, current_app, render_template, send_file, make_response
from flask_login import current_user
from werkzeug.utils import secure_filename
from app.common.datetime_format import *
import os
import uuid


def get_users_list():
    from app.admin.models import User
    
    users = User.query.filter(User.name != "admin").all()
    
    return users


def get_role_list():
    from app.admin.models import Role
    
    roles = Role.query.all()
    return roles
        
        
def already_exist(obj_class, name, module=None):
    if module:
        n_instance = obj_class.query.filter_by(name=name, module=module).first()
    else:
        n_instance = obj_class.get_by_name(name)

    return bool(n_instance)


def delete_activity(activity_id):
    from app.common.models import Activity
    activity = Activity.get_by_id(activity_id)
    if activity:
        activity.delete()
        
    

def get_prev_ref():
    previous_url = request.referrer
    if previous_url is None:
        previous_url = url_for("public.index")
    
    return previous_url


def count_module_reports(mod_id):
    
    from app.common.models import Report
    
    reports_number = Report.query.filter_by(mod_id=mod_id).count()
    
    return int(reports_number)


def get_last_report_number(mod_id):
    from app.common.models import Report
    
    reports = Report.query.filter_by(mod_id=mod_id).all()
    numbers = []
    
    for report in reports:
        code = report.code
        number = code.rsplit("-", 1)[-1]
        numbers.append(int(number))  # Convertir a entero para comparar correctamente

    if not numbers:
        return 0  # Devolver 0 si no hay números en la lista

    # Encontrar el número más grande usando la función max
    biggest = max(numbers)
    
    return biggest

    
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_IMAGES_EXTENSIONS"]
           
           
def save_images(dir, file, obj_class, report_id):
    
    print("infresa a funcion", obj_class)
    filename = str(get_timestamp())[6:]+".jpeg"
    filename = secure_filename(filename)
    existing_file = obj_class.query.filter_by(filename=filename).first()
    if existing_file:
        filename = f"{uuid.uuid4().hex}_{filename}"
    file_dir = current_app.config[f"{dir}"]
    os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, filename)
    file.save(file_path)
    print(f"se suipone guarda el path: {file_path} con report_id = {report_id}")
    n_file = obj_class(report_id = report_id,
                        filename = filename)
    n_file.save()
    
    
    

