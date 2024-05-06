import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = "this34is66the90new33secret12key66forya"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "schema.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False