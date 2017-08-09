#python uploads.py runserver -p 80 
#!/usr/bin/env python
from flask_script import Manager,prompt_bool
from apps import create_app
from apps.utils import story as story


app = create_app( 'dev' )
manager = Manager(app)

'''
from flask_migrate import Migrate,MigrateCommand
from apps import db,create_app
from apps.models import User,Bookmark ,Tag,Post,Role,Follow



#app = create_app(os.getenv('ATLAS_ENV') or  'dev' )

migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

@manager.command
def insert_data():
    couchk = User(username="Kiriakis", email="Kiri@Zionlaxy.com", password="test")
    db.session.add(couchk)

    def add_bookmark(url, description, tags):
        db.session.add(Bookmark(url=url, description=description,  user_id=couchk.id,
                                tags=tags))

    for name in ["python", "flask", "webdev", "programming", "training", "news", "orm", "databases", "emacs", "gtd", "django"]:
        db.session.add(Tag(name=name))
    db.session.commit()

    add_bookmark("http://www.pluralsight.com", "Pluralsight. Hardcore developer training.", "training,programming,python,flask,webdev")
    add_bookmark("http://www.python.org", "Python - my favorite language", "python")
    add_bookmark("http://flask.pocoo.org", "Flask: Web development one drop at a time.", "python,flask,webdev")
    add_bookmark("http://www.reddit.com", "Reddit. Frontpage of the internet", "news,coolstuff,fun")
    add_bookmark("http://www.sqlalchemyorg", "Nice ORM framework", "python,orm,databases")

    arjen = User(username="arjen", email="arjen@robben.nl", password="test")
    db.session.add(arjen)
    db.session.commit()
    print ('Initialized the database')

@manager.command
def dropdb():
    if prompt_bool(
        'Are u sure to lose all data?'):
        db.drop_all()
        print('drop database finished. ')

@manager.command
def test():
	'run the unit test'
	import unittest
	tests = unittest.TestLoader().discover('test')
	unittest.TextTestRunner(verbosity = 2).run(tests)
'''
if __name__ == '__main__':
    manager.run()
