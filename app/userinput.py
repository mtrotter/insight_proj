from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class UserInputForm(Form):
    title = TextField('title', validators = [Required()])
    category = TextField('category')
    BooleanField('remember_me', default = False)