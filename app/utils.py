import os

from flask import url_for, request, current_app

from werkzeug.utils import secure_filename

import uuid

from app.common.datetime_format import *

import pytz


def get_current_time_quito():
    quito_tz = pytz.timezone('America/Guayaquil')
    return datetime.now(quito_tz)


def get_users_list():
    from app.admin.models import User
    
    users = User.query.filter(User.name != "admin").all()
    
    return users


def get_operators_list():
    from app.admin.models import User, Role
    operators = User.query.join(Role).filter(Role.name == "Operador").all()
    
    return operators


def get_ma_workers():
    from app.admin.models import User, Role
    ma = User.query.join(Role).filter(Role.name == "Monitor Ambiental").all()
    
    return ma

def get_ap_workers():
    from app.admin.models import User, Role
    ap = User.query.join(Role).filter(Role.name == "Ayudantes de operación").all()
    
    return ap

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
    
    
    

