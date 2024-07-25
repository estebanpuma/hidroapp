from flask import Flask, g, request, redirect
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

    
    @app.before_request
    def before_request():
        # Aquí puedes inicializar cualquier cosa que necesites antes de cada request
        # En este caso, podrías cargar los módulos disponibles
        g.mods = fetch_modules()  # Implementa esta función para obtener tus módulos desde la base de datos o donde los tengas almacenados

    @app.context_processor
    def inject_mods():
        # Este procesador de contexto hace que mods esté disponible globalmente en todas las plantillas
        return dict(mods=g.mods if 'mods' in g else [])
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    from .admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")
    
    from .common import common_bp
    app.register_blueprint(common_bp)
    
    from .public import public_bp
    app.register_blueprint(public_bp)
    
    from .users import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")
    
    from .ops import ops_bp
    app.register_blueprint(ops_bp)
    
    from .environment import environment_bp
    app.register_blueprint(environment_bp, url_prefix="/environment")
    
    from .environment.pga import environment_pga_bp
    app.register_blueprint(environment_pga_bp, url_prefix="/environment/pga")
    
    from .environment.reforestation import environment_reforestation_bp
    app.register_blueprint(environment_reforestation_bp, url_prefix="/environment/reforestation")
    
    from .social import social_bp
    app.register_blueprint(social_bp, url_prefix="/social")
    
    from .maintenance import maintenance_bp
    app.register_blueprint(maintenance_bp, url_prefix="/maintenance")
    
    from .sst import sst_bp
    app.register_blueprint(sst_bp)
    
    return app


def fetch_modules():
    # Aquí puedes implementar la lógica para obtener los módulos disponibles desde la base de datos o de donde sea necesario
    from app.common.models import Module
    return Module.query.all()