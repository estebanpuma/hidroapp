from flask_login import current_user
from app.admin.models import User, Role


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
        