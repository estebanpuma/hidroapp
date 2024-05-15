from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    login_manager.init_app(app)
    login_manager.login_view = "public.login"
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from .public import public_bp
    app.register_blueprint(public_bp)
    
    from .users import users_bp
    app.register_blueprint(users_bp)
    
    from .environment import environment_bp
    app.register_blueprint(environment_bp)
    
    from .environment.pma import environment_pma_bp
    app.register_blueprint(environment_pma_bp, url_prefix="/pma")
    
    from .environment.reforestation import environment_reforestation_bp
    app.register_blueprint(environment_reforestation_bp, url_prefix="/reforestation")
    
    return app