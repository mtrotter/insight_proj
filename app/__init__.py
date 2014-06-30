# imports
from flask import Flask, g
from flask_bootstrap import Bootstrap
import flask_wtf 
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
from flask_wtf import Form
from wtforms import SelectField
import pickle
import sklearn

# Creates our application.
app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'Testing BS'
# Development configuration settings
# WARNING - these should not be used in production
app.config.from_pyfile('settings/development.cfg')


app.kick_classify = pickle.load(open('kick_classifier.pkl','rb'))
app.indie_classify = pickle.load(open('indie_classifier.pkl','rb'))

app.kick_regress = pickle.load(open('kick_regressor_2.pkl','rb'))
app.indie_regress = pickle.load(open('indie_regressor_2.pkl','rb'))

# Production configuration settings
# To have these override your development settings,
# you'll need to set your environment variable to
# the file path:
# export PRODUCTION_SETTINGS=/path/to/settings.cfg
app.config.from_envvar('PRODUCTION_SETTINGS', silent=True)

# Application DEBUG - should be True in development
# and False in production
app.debug = app.config["DEBUG"]

# in a real app, these should be configured through Flask-Appconfig
app.config['SECRET_KEY'] = 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'



# DATABASE SETTINGS
host = app.config["DATABASE_HOST"]
port = app.config["DATABASE_PORT"]
user = app.config["DATABASE_USER"]
passwd = app.config["DATABASE_PASSWORD"]
db = app.config["DATABASE_DB"]


from app import views


