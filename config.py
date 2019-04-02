import os
import psycopg2
basedir = os.path.abspath(os.path.dirname(__file__))
from werkzeug.utils import secure_filename


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/uploads/'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'])
    TEMPLATES_FOLDER = 'templates/'
    DOCS_FOLDER = 'docs/'
    TEMPLATES_AUTO_RELOAD = True
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    DATABASE_URL = os.environ.get['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
