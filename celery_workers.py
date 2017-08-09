import os
from apps import celery, create_app
#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app('default')
app.app_context().push()
