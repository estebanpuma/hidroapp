
from os.path import abspath, dirname, join

BASE_DIR = dirname(dirname(abspath(__file__)))

SECRET_KEY = "this34is66the90new33secret12key66forya"

SQLALCHEMY_TRACK_MODIFICATIONS = False

# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''

MEDIA_DIR = join(BASE_DIR, 'media')
REPORT_IMAGES_DIR = join(MEDIA_DIR, 'reports')
ALLOWED_IMAGES_EXTENSIONS = {'png', 'jpg', 'jpeg'}