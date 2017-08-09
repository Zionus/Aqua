import os

basedir = os.path.abspath(os.path.dirname(__file__))
from celery.schedules import crontab
from datetime import timedelta  
CeleryConfig = dict(
    broker_url= 'redis://localhost:6379/0',
    result_backend = 'redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'] , # Ignore other content
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True
)
'''about :
redis_db, redis_host,redis_password


'''
#rename CELERYBEAT_SCHEDULE to beat_scheduler
# import 
imports = (
    'celery_app.task1',
    'celery_app.task2')

# schedules
beat_schedule = {
    'add-every-1-hours': {
         'task': 'celo.tasks.add',
         'schedule': timedelta(seconds=30),       # per 30s 
         'args': (5, 8)                           # task 
    },
    'multiply-at-some-time': {
        'task': 'celo.tasks.used_apk_cdn',
        'schedule': crontab(hour=9, minute=50),   # daily  9:50
        #'args': ()                            # task
    }
}

class Config:
    #config authentication
    SECRET_KEY =  os.urandom(24)
    DEBUG = False
    broker_url = 'redis://localhost:6379/0'
    MAIL_SERVER  = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    DEFAULT_MAIL_SENDER = MAIL_USERNAME
    MAIL_SUBJECT_PREFIX = '[Aqua]'
    
    '''
    MAIL_DEBUG = True
    #smtpinternal.lenovo.com'
    POSTS_PER_PAGE =20
    FOLLOWERS_PER_PAGE = 20
    COMMENTS_PER_PAGE = 20
    '''

class DevelopmentConfig(Config):
    DEBUG = True     
    #mysql://username:password@hostname/database
    '''
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://saber:1234567u@127.0.0.1:3306/atlas'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    '''

class TestingConfig(Config):
    DEBUG = True
    '''
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://saber:1234567u@127.0.0.1:3306/test'
    '''


class ProductionConfig(Config):
    DEBUG = False
    '''
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://saber:1234567u@127.0.0.1:3306/test'
    '''


config_by_name = { 'dev':DevelopmentConfig,
            'testing':TestingConfig,
            'Production':ProductionConfig,
            'default':DevelopmentConfig
            }