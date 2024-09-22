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

#-----------------------------------------------------------------------------------------------------#

#---------CLASSES----->

#-----------------------------------------------------------------------------------------------------#

#============================================# Pre Login #============================================#

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

#============================================# Login or Sign Up options #============================================#

@app.route('/login')
def login():
    return render_template('Login.html') # login page

#============================================# User #============================================#

@app.route('/user/')
def userindex():
    return render_template('UserBase.html')

@app.route('/user/dash')
def userdash():
    return render_template('UserDash.html')

#============================================# User Profile options #============================================#


@app.route('/user/profile')
def uprofile():
    return render_template('UserViewProfile.html') # view user profile

@app.route('/user/edit')
def uedit():
    return render_template('UserEditProfile.html') # Edit user profile

@app.route('/user/delete') #delete user, and go to pre-login home page
def udel():
    pass


#============================================# User Enquiry options #============================================#


@app.route('/user/courses')
def ucourses():
    return render_template('UserViewCourses.html') # view courses                     

@app.route('/user/enquire')
def uenquire():
    return render_template('UserEnquire.html') # enquire about a course

@app.route('/user/viewenquiries')
def uviewenq():
    return render_template('UserViewEnq.html') # view user enquiries


