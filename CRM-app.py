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

@app.route('/home')
def home():
    return render_template('Home.html')

@app.route('/about')
def about():
    return render_template('About Us.html')

@app.route('/courses')
def courses():
    return render_template('Courses.html')