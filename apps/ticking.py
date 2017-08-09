#python uploads.py runserver -p 80 
#!/usr/bin/env python
from flask_script import Manager,prompt_bool
#from apps import create_app

from gevent.pywsgi import WSGIServer
from gevent.queue import Queue, Empty
from flask import Flask, render_template, redirect, url_for, request
#from forms import LoginForm
from flask_bootstrap import Bootstrap
import simplejson
#loginForm
from flask_wtf import Form
from wtforms import StringField
from wtforms import SubmitField


class LoginForm(Form):
    name = StringField("name")
submit = SubmitField("Submit")

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'HARD'
messages = []
user_dict = {}



@app.route('/put_post/<user>', methods=["POST"])
def put_post(user):
    post = request.form['message']
    for u in user_dict:
         user_dict[u].put_nowait(post)
    return ""


@app.route('/get_post/<user>', methods=["GET", "POST"])
def get_post(user):
    q = user_dict[user]
    try:
        p = q.get(timeout=10)
    except Empty:
        p = ''
    return simplejson.dumps(p)


@app.route('/chatroom/<user>/')
def chatroom(user):
    user_con = user_dict.setdefault(user, Queue())
    return render_template("chatroom.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("chatroom", user=form.name.data))
    return render_template("login.html", form=form)


if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
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


if __name__ == '__main__':
    manager.run()
'''
