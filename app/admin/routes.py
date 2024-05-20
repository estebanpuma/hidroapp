from flask import render_template, redirect, url_for, request
from flask_login import login_user

from .models import User, Role, Module, RolePermission

from app.vars_const import months
from . import admin_bp

from app import db
from app.models import Month


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
    roles = Role.query.all()
    print(f"rols {roles}")
    if request.method == "POST":
        name = request.form['name']
        email = request.form["email"]
        password = request.form["password"]
        role = int(request.form["role"])
        birth = request.form["birth"]
        if birth:
            birth = datetime.strptime(birth, '%Y-%m-%d').date()
        else:
            birth = None
        user = User.get_by_email(email)
        
        print(name,email,role, type(role), password, birth)
        
        if user is not None:
            error = f'El email {email} ya esta en uso'
            
        else:
            
            n_user = User(name=name, 
                          email=email,
                          role_id = role,
                          birth = birth)
            n_user.set_password(password)
            n_user.save()
            
            next_page = request.args.get('next', None)
            
            if not next_page:
                next_page = url_for("admin.users")
            
            return redirect(next_page)
            
    return render_template("admin/add_user.html",
                           title = title,
                           error = error,
                           roles = roles)
    

@admin_bp.route("/roles")
def roles():
    title = "Roles"
    roles = Role.query.all()
    return render_template("admin/roles.html",
                           title = title,
                           roles = roles)
    
    
@admin_bp.route("/add_role/<int:role_id>/", methods=["GET", "POST"])
@admin_bp.route("/add_role", methods=["GET", "POST"])
def add_role(role_id=None):
    title = "Nuevo rol"
    role = Role.get_by_id(role_id)
    modules = Module.query.all()
    error = None
    
    if request.method == "POST":
        name = request.form["role"]
        description = request.form["description"]
        n_role = Role.query.filter_by(name=name).first()
        
        if n_role is not None:
            error = f'El rol {name} ya ha sido creado'
        else:
            n_role = Role(name = name,
                      description = description)
        
            n_role.save()
        
            for module in modules:
                n_perm = RolePermission(role_id=n_role.id,
                              module_id=module.id,
                              read=True,
                              write=False,
                              delete=False)
                perm = RolePermission.query.filter_by(role_id=n_role.id,
                              module_id=module.id).first()
                
                if perm is not None: 
                    error = f"Ya se ha credo el permiso"    
                else:
                    n_perm.save()
                    
                print(RolePermission.query.all())
        return redirect(url_for('admin.roles'))
    
    return render_template("admin/add_role.html",
                           title = title,
                           role = role,
                           error = error)
    
    
@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    title = "Dashboard"
    roles = Role.query.all()
    modules = Module.query.all()
    users = User.query.all()
    all_role_perm = RolePermission.query.all()
    
    
    return render_template("admin/admin_dashboard.html",
                           title = title,
                           roles = roles,
                           modules = modules,
                           users = users,
                           all_role_perm = all_role_perm,
                           )    


@admin_bp.route("/permissions/<int:role_id>,<int:module_id>", methods=["GET", "POST"])
@admin_bp.route("/permissions", methods=["GET", "POST"])
def permissions(role_id, module_id):
    title = "Permisos"
    role = Role.get_by_id(role_id)
    print(f"Este es el role: {role}")
    module = Module.get_by_id(module_id)
    rp = RolePermission.query.filter_by(role_id=role_id, module_id=module_id).first()
    print(f"este es el rp: {rp}")
    
    if request.method == "POST":
        write = request.form.get("write")
        
        read = request.form.get("read")
        
        erase = request.form.get("del")
        
        
        print(f"wb:{write}, rb:{read}, eb: {erase}")
        if write: 
            write = True 
        else:
            write = False
            
        if read: 
            read = True 
        else:
            read = False
            
        if erase: 
            erase = True 
        else:
            erase = False
        print(f"w:{write}, r:{read}, e: {erase}")
        
        rp.set_permissions( read, write, erase)
        rp.save()   
        
        
        return redirect(url_for("admin.admin_dashboard"))
    
    return render_template("admin/permissions.html",
                           title=title,
                           role = role,
                           module = module,
                           rp = rp)
    

@admin_bp.route("/delete_user/<int:user_id>", methods=["GET", "POST"])
def delete_user(user_id):
    user = User.get_by_id(user_id)
    if user:
        user.delete()
    
    return redirect(url_for("admin.users"))


@admin_bp.route("/delete_role_perm/<int:role_perm_id>", methods=["GET", "POST"])
@admin_bp.route("/delete_role_perm", methods=["GET", "POST"])
def delete_role_perm(role_perm_id=None):
    if role_perm_id:
        role_perm = RolePermission.query.filter_by(id=role_perm_id).first()
        if role_perm:
            role_perm.delete()
    else:
        all_perms = RolePermission.query.all()
        for ap in all_perms:
            ap.delete()
    return redirect(url_for('admin.perm'))       


@admin_bp.route("/delete_role/<int:role_id>", methods=["GET", "POST"])
def delete_role(role_id):
    print(f"role_id que me pasa: {role_id}")
    role = Role.get_by_id(role_id)
    
    if role:
        print(f"rol a eliminar: {role}, {role.id}")
        role.delete()
    

    
    return redirect(url_for("admin.roles"))


@admin_bp.route("/mods")
def mods():
    title= "Modulos"
    mods = Module.query.all()
    return render_template("admin/mods.html", 
                           mods=mods,
                           title=title)
    
@admin_bp.route("/perm")
def perm():
    title= "Permisos"
    perms = RolePermission.query.all()
    return render_template("admin/prm.html", 
                           perms=perms,
                           title=title)
    

@admin_bp.before_app_request 
def set_defaults():
    
    create_dafult_modules()
    
    create_default_roles()
    
    set_default_perm(1)
    
    set_default_perm(2)
    
    create_admin_user()
    
    query_months = Month.query.all()
    if len(query_months) < 12:
        create_months()
        
    
def create_dafult_modules():   
    #Crear los modulos de la aplicacion
    mod_names_descriptions = [
        ("Generacion", "Datos de generacion"),
        ("Ambiente", "PMA"),
        ("Seguridad y Salud", "sst"),
        ("Social", "RSC")
    ]
    
    for name, description in mod_names_descriptions:
        mod = Module.query.filter_by(name=name).first()
        if not mod:
            mod = Module(name=name, description=description)
            mod.save()
    
    
def create_default_roles():
    #crear los roles por defecto
    guest_role = Role.query.filter_by(name="Invitado", id=2).first()
    if not guest_role:
        name = "Invitado"
        description = "Sesion de invitado"
        role = Role(id=2, name=name,
                    description= description)
        role.save()

    admin_role = Role.query.filter_by(name="admin", id=1).first()
    if not admin_role:
        name = "admin"
        description = "Manage the users, roles and permissions"
        role = Role(id=1, name=name,
                    description= description)
        role.save()


def set_default_perm(role_id):
    try:
        if role_id:
            modules = Module.query.all()
    
            for module in modules:
                perm = RolePermission.query.filter_by(role_id=role_id,
                                                    module_id=module.id).first()
                if not perm:
                    perm = RolePermission(role_id=role_id,
                              module_id=module.id,
                              read=True,
                              write=False,
                              delete=False)
                    perm.save()
    except role_id == None:
        print("No se pasa un id del role")
        

def create_admin_user():
    admin_user = User.query.filter_by(email="admin@admin.com", id=1).first()
    if not admin_user:
        # Si el usuario admin no existe, lo creamos
        admin_email = "admin@admin.com"
        admin_role = Role.query.filter_by(name="admin").first()
        admin_role = 1
        print(f"admin rol id = {add_role}")
        admin_user = User(id=1, name='admin', email = admin_email, role_id=admin_role)
        admin_user.set_password("admin")
        admin_user.save()
        
        
def create_months():
    
    for key, value in months.items():
        month = Month.get_by_id(Month,key)
        if not month:
            n_month = Month(id=key, name=value)
            n_month.save()