#python uploads.py runserver -p 80 
import sys
sys.path.append('..')

import os
from flask import Flask
from flask_bootstrap import Bootstrap

from flask_moment import Moment
from flask_login import LoginManager
from celery import Celery
from apps.config import Config,config_by_name,CeleryConfig
from flask_mail import Mail ,Message
'''

from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from flask_pagedown import PageDown
from flask.ext.script import Manager

pagedown = PageDown()
db = SQLAlchemy()

login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
toolbar = DebugToolbarExtension()
'''
from flask_uploads import UploadSet,configure_uploads,DOCUMENTS,patch_request_class
mail = Mail()
login_manager = LoginManager()
moment = Moment()
bootstrap=Bootstrap()
celery = Celery(__name__, broker=Config.broker_url)

def create_app(config_name):
    app= Flask(__name__)
    app.config.from_object(config_by_name[config_name] )
    
    UPLOAD_FOLDER = r'D:\aqua\apps\static\downloads'
    ALLOWED_EXTENSIONS= set(['txt','json','csv','xlsx'])
    app.config['UPLOADS_DEFAULT_DEST'] = UPLOAD_FOLDER
    app.config['UPLOAD_FOLDER'] ='downloads'
    docs = UploadSet('docs',DOCUMENTS)
    configure_uploads(app,docs)
    patch_request_class(app)
    celery.conf.update(CeleryConfig)
    mail.init_app(app)
    '''
    db.init_app(app)
    
    
    toolbar.init_app(app)
    pagedown.init_app(app)
    '''
    login_manager.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    from .main import  main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app

def make_celery(app):
        celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])#not working
        celery.conf.update(app.config)
        TaskBase = celery.Task
        class ContextTask(TaskBase):
            abstruct = True
            def __call__(self, *args, **keywords):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **keywords)
        celery.Task = ContextTask
        return celery
        
if __name__ == "__main__":
    pass