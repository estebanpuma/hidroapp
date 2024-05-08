from flask import render_template, redirect, url_for, request
from flask_login import login_user
from .models import User
from .forms import LoginForm, AddUserForm
from . import admin_bp

@admin_bp.route("/users")
def users():
    title = "Usuarios"
    return render_template("admin/users.html",
                           title = title)
    
    
@admin_bp.route("/add_user/<int:user_id>/", methods=["GET", "POST"])
@admin_bp.route("/add_user", methods=["GET", "POST"])
def add_user(user_id=None):
    title = "Nuevo Usuario"
    form = AddUserForm()
    
    if form.validate_on_submit():
        
        name = form.name.data
        email = form.email.data
        password = form.password.data
        role = form.role.data
        birth = form.birth.data
        
        user = User.get_by_email(email)
        
        if user is not None:
            error = f'El email {email} ya esta en uso'
            
        else:
            n_user = User(name=name, 
                          email=email,
                          role = role,
                          birth = birth)
            n_user.set_password(password)
            n_user.save()
            
            login_user(n_user)
            
            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for("admin.users")
            
            return redirect(next_page)
            
    return render_template("admin/add_user.html",
                           title = title,
                           error = error)
    

@admin_bp.route("/roles")
def roles():
    title = "Roles"
    return render_template("admin/roles.html",
                           title = title)
    
    
@admin_bp.route("/add_role/<int:role_id>/", methods=["GET", "POST"])
@admin_bp.route("/add_role", methods=["GET", "POST"])
def add_role(role_id=None):
    title = "Nuevo rol"
    
    return render_template("admin/add_role.html",
                           title = title)
    
    
@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    title = "Dashboard"
    return render_template("admin/admin_dashboard.html",
                           title = title)
    


@admin_bp.route("/permissions/<int:role_id>,<int:module_id>", methods=["GET", "POST"])
@admin_bp.route("/permissions", methods=["GET", "POST"])
def permissions(role_id=None, module_id=None):
    title = "Permisos"
    return render_template("admin/permissions.html",
                           title=title)