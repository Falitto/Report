import os
basedir = os.path.abspath(os.path.dirname(__file__))
from werkzeug.utils import secure_filename


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:9935@localhost:3306/reportdb?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/uploads/'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'])
    TEMPLATES_FOLDER = 'templates/'
    DOCS_FOLDER = 'docs/'
    TEMPLATES_AUTO_RELOAD = True
