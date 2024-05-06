from flask import Flask


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    from .public import public_bp
    app.register_blueprint(public_bp)
    
    return app