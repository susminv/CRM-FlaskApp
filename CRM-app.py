from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField, SelectField, PasswordField, RadioField, SubmitField, widgets, TextAreaField,IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo,Regexp
from config import Config  # Make sure to import your Config class
from flask_login import login_user, LoginManager, logout_user, current_user, login_required
from flask_login import UserMixin
from flask import session
from datetime import datetime, timezone

app = Flask(__name__) 
app.config.from_object('config.Config')
mydb_obj = SQLAlchemy(app)
migrate = Migrate(app,mydb_obj)

boostrap = Bootstrap(app)

#---------Database------------#

#USER Table
class Users(mydb_obj.Model):
    __tablename__ = 'users'  # Explicitly define the table name

    id = mydb_obj.Column(mydb_obj.Integer, primary_key=True) #primary key
    username = mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    firstname = mydb_obj.Column(mydb_obj.String(150), nullable=False)
    lastname = mydb_obj.Column(mydb_obj.String(150), nullable=False)
    password = mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)

    email = mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    phone_number = mydb_obj.Column(mydb_obj.Integer, unique=True, nullable=False)
    address = mydb_obj.Column(mydb_obj.String(200), unique=True, nullable=False)
    date_of_birth = mydb_obj.Column(mydb_obj.Date, nullable=False)  # Date of birth
    highest_qualificationid = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('qualifications.qualification_id'),nullable=False) #FK
    marks = mydb_obj.Column(mydb_obj.Integer, nullable=False)
    yearofgraduation =  mydb_obj.Column(mydb_obj.Integer, nullable=False)

#QUALIFICATIONS Table
class Qualifications(mydb_obj.Model):
    qualification_id = mydb_obj.Column(mydb_obj.Integer, primary_key=True)#PK
    qualification_name = mydb_obj.Column(mydb_obj.String(150))

#COURSE Table
class Courses(mydb_obj.Model):
    courseid = mydb_obj.Column(mydb_obj.Integer, primary_key=True) #primary key
    coursename= mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    description= mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    course_duration = mydb_obj.Column(mydb_obj.Integer, nullable=False)  # Duration in hours
    fees = mydb_obj.Column(mydb_obj.Integer, nullable=False)
    qualification_id = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('qualifications.qualification_id'),nullable=False) #FK

#ENQUIRIES Table
class Enquiries(mydb_obj.Model):

    enqid = mydb_obj.Column(mydb_obj.Integer, primary_key=True)
    userid = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('users.id'),nullable=False)
    courseid = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('courses.courseid'),nullable=False) #FK
    message =  mydb_obj.Column(mydb_obj.String(150))
    enquiry_date =  mydb_obj.Column(mydb_obj.DateTime, default=datetime.now) 
    status = mydb_obj.Column(mydb_obj.Integer,nullable=False) #FK
    resource = mydb_obj.Column(mydb_obj.Integer, nullable=False) #FK

#---------Form classes--------#
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    state = StringField('State of Domicile', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    qualifications = RadioField(
        'Highest Qualification',
        choices=[('10th','10th'),('12th', '12th'), ('Bachelors', 'Bachelors'), ('Masters', 'Masters')],
    )
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=20),
        Regexp(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', 
               message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
    ])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

class EnquiryForm(FlaskForm):
    userid = IntegerField('User ID',validators=[DataRequired()])
    courseid = IntegerField('Course ID',validators=[DataRequired()])
    message = TextAreaField('Your message', validators=[DataRequired()])
    resource = SelectField(
        'Resource',
        choices=[('1','nil'),('2','Acquaintances'),('3', 'Social Media'), ('4', 'Staff')]
    )
    submit = SubmitField('Enquire')


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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('Login.html',form=form) # login page

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('Register.html',form=form) # login page

#============================================# User #============================================#

@app.route('/user/')
def userindex():
    return render_template('UserBase.html')

@app.route('/user/dash')
def userdash():
    return render_template('UserDash.html')

@app.route('/user/about')
def userabout():
    return render_template('UserAboutUs.html')

#============================================# User Profile options #============================================#


@app.route('/user/profile')
def uprofile():
    return render_template('UserViewProfile.html') # view user profile

@app.route('/user/edit')
def uedit():
    form = RegistrationForm()
    return render_template('UserEditProfile.html',form=form) # Edit user profile

@app.route('/user/delete') #delete user, and go to pre-login home page
def udel():
    return render_template('UserDelete.html')


#============================================# User Enquiry options #============================================#


@app.route('/user/courses')
def ucourses():
    return render_template('UserViewCourses.html') # view courses                     

@app.route('/user/enquire')
def uenquire():
    form = EnquiryForm()
    return render_template('UserEnquire.html',form=form) # enquire about a course

@app.route('/user/viewenquiries')
def uviewenq():
    return render_template('UserViewEnq.html') # view user enquiries


@app.route('/user/test')
def u():
    return render_template('ViewBase.html') # view user enquiries