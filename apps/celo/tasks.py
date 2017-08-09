import os
from apps 	 import celery, create_app,mail
#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app('default')
app.app_context().push()
from flask import current_app
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
from flask_mail import Message
from celery import  Task
#from apps.ticks.utilities import *
@celery.task
def send_async_email(msg ):

	msg.body = 'This is a test email sent from a background Celery task.'
	
	with app.app_context():
		logger.info('in context')
		logger.info('send message by  to ', msg.sender)
		mail.send(msg)
	
def send_email(to, subject, template, **kwargs):
	msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + '-> ' + subject,
				  sender=app.config['DEFAULT_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	send_async_email.delay(msg)
@celery.task 
def add(x, y):
    return x + y
@celery.task
def snitching( ):
    pass    
@celery.task(name='celo.tasks.used_apk_cdn')
def used_apk_cdn():
    logger.info("lalala ")
    pass
'''
def update_page_info(url):#chained task
    # fetch_page -> parse_page -> store_page
    chain = fetch_page.s(url) | parse_page.s() | store_page_info.s(url)
    chain()

@celery.task()
def fetch_page(url):
    return myhttplib.get(url)

@celery.task()
def parse_page(page):
    return myparser.parse_document(page)

@celery.task(ignore_result=True)
def store_page_info(info, url):
    PageInfo.objects.create(url=url, info=info)

	
@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}
            

class MyTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        print ('task done: {0}'.format(retval))
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print ('task fail, reason: {0}'.format(exc))
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)

#@app.task(base=MyTask)
'''       