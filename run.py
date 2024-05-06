from app import create_app
from config import DevelopmentConfig, configurations

app = create_app(configurations["development"])

