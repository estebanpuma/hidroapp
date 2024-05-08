from flask import Flask


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from .public import public_bp
    app.register_blueprint(public_bp)
    
    from .users import users_bp
    app.register_blueprint(users_bp)
    
    return app