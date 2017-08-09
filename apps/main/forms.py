from flask_wtf import FlaskForm as Form
from werkzeug.utils import  secure_filename
from  flask_wtf.file import FileField
from wtforms.fields import SubmitField

class PseudoForm(Form):
	pseudo = FileField('Your doc:')
	submit = SubmitField('Upload')