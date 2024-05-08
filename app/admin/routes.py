from flask import render_template
from . import admin_bp

@admin_bp.route("/users")
def users():
    title = "Usuarios"
    return render_template("admin/users.html",
                           title = title)
    
    
@admin_bp.route("/add_user/<int:user_id>/")
@admin_bp.route("/add_user")
def add_user(user_id=None):
    title = "Nuevo Usuario"
    
    return render_template("admin/add_user.html",
                           title = title)
    

@admin_bp.route("/roles")
def roles():
    title = "Roles"
    return render_template("admin/roles.html",
                           title = title)
    
    
@admin_bp.route("/add_role/<int:role_id>/")
@admin_bp.route("/add_role")
def add_role(role_id=None):
    title = "Nuevo rol"
    
    return render_template("admin/add_role.html",
                           title = title)
    
    
@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    title = "Dashboard"
    return render_template("admin/admin_dashboard.html",
                           title = title)
    


@admin_bp.route("/permissions/<int:role_id>,<int:module_id>")
@admin_bp.route("/permissions")
def permissions(role_id=None, module_id=None):
    title = "Permisos"
    return render_template("admin/permissions.html",
                           title=title)