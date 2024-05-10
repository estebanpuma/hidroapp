from flask import render_template, redirect, url_for, request
from flask_login import login_user
from .models import User
from .forms import LoginForm, AddUserForm
from . import admin_bp

from datetime import datetime

@admin_bp.route("/users")
def users():
    users = User.query.all()
    print(users)
    title = "Usuarios"
    return render_template("admin/users.html",
                           title = title,
                           users = users)
    
    
@admin_bp.route("/add_user/<int:user_id>/", methods=["GET", "POST"])
@admin_bp.route("/add_user", methods=["GET", "POST"])
def add_user(user_id=None):
    title = "Nuevo Usuario"
    
    error = None
    
    if request.method == "POST":
        name = request.form['name']
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        birth = request.form["birth"]
        
        birth = datetime.strptime(birth, '%Y-%m-%d').date()
        
        user = User.get_by_email(email)
        
        print(name,email,role, password)
        
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
            print(f"n user: {n_user}")
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
    

@admin_bp.route("/delete_user/<int:user_id>", methods=["GET", "POST"])
def delete_user(user_id):
    user = User.get_by_id(user_id)
    if user:
        user.delete()
    
    return redirect(url_for("admin.users"))
    
    

@admin_bp.before_app_request 
def create_default_user():
    admin_user = User.query.filter_by(id=0).first()
    if not admin_user:
        # Si el usuario admin no existe, lo creamos
        
        admin_email = "admin@admin.com"
        admin_role = "0"
        admin_user = User(id=0, name='admin', email = admin_email, role=admin_role)
        admin_user.set_password("admin")
        admin_user.save()