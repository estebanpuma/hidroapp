from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user
from app import login_manager
from ..admin.models import User
from ..admin.forms import LoginForm
from . import public_bp

@public_bp.route("/")
def index():
    title = "Hidrotambo"
    return render_template("public/index.html",
                           title = title)
    
    
@public_bp.route("/login")
def login():
    title = "Login"
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.get_by_email(email)
        
        if user is not None and user.check_password(password):
            login_user(user)
    
    return render_template("public/login.html", 
                           title = title)
    
    

@public_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))