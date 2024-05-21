from flask import redirect, url_for
from flask_login import current_user

from app.admin.models import User, Role
from app.common.models import Activity


def get_users_list():
    users = User.query.all()
    try:
        if current_user.id != 1:
            user_to_remove = User.query.get(1)  # Suponiendo que deseas eliminar el usuario con ID 1
    # Filtrar la lista de usuarios para eliminar el usuario específico
        else:
            user_to_remove = None
    except User.query.get(1) is None as e:
        print(f"No existe usuario, user:{e}")
    users = [user for user in users if user != user_to_remove]
    
    return users


def get_role_list():
    roles = Role.query.all()
    return roles
        
        
def already_exist(obj_class, name, module=None):
    if module:
        n_instance = obj_class.query.filter_by(name=name, module=module).first()
    else:
        n_instance = obj_class.get_by_name(name)

    return bool(n_instance)


def delete_activity(activity_id):
    activity = Activity.get_by_id(activity_id)
    if activity:
        activity.delete()
        
    
