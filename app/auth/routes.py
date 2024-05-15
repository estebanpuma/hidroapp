from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user

from app import login_manager
from ..admin.models import User

from . import auth_bp


@auth_bp.route("/login", methods = ["POST", "GET"])
def login():
    title = "Login"
    password_error = False
    password_msg = None
    email_error = False
    email_msg = None
    if request.method == "POST":
        print("form")
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.get_by_email(email)
        print(f"user: {user}")
        
        if user:
            
            if user.check_password(password):
            
                login_user(user)
                
                next_page = request.args.get('next', None)
                
                if not next_page:
                    next_page = url_for("public.index")
                
                return redirect(next_page)
            else:
                password_error = True
                password_msg = "Contraseña incorrecta. Vuelve a intentarlo"
                
        else:
            email_error = True
            email_msg = "Usuario no encontrado-Registrese"
            
        
    return render_template("auth/login.html", 
                           title = title,
                           email_msg = email_msg,
                           email_error = email_error,
                           password_msg = password_msg,
                           password_error = password_error
                           )
    
    

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))