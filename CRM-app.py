import urllib.parse
from flask import Flask, redirect, url_for, render_template
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy
import urllib 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from flask import session, flash
from flask_migrate import Migrate


app = Flask(__name__) 
app.config['SECRET_KEY'] = 'some secret key'

boostrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('Base.html')