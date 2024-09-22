from flask import Flask,redirect,url_for,render_template
from flask_bootstrap import Bootstrap
from flask_material import Material
from flask_sqlalchemy import SQLAlchemy #import SQLAlchemy class from flask_sqlalchemy pkg
from flask_migrate import Migrate
import urllib.parse
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,DecimalField,SelectField,FloatField,PasswordField,DateField,PasswordField

from wtforms.validators import DataRequired,Length,EqualTo,Email,InputRequired
from flask import session
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from flask import flash
from flask_login import LoginManager,login_user,UserMixin
from flask_login import current_user,logout_user,login_required
from email_validator import validate_email, EmailNotValidError
from datetime import datetime

app=Flask(__name__)
bootstrap=Bootstrap(app)
material=Material(app)
app.config.from_object('config.Config')#loading the configuration from the config class

mydb_obj = SQLAlchemy(app) #create an SQLAlchemy object
migrate=Migrate(app,mydb_obj)

class Qualifications(mydb_obj.Model):
    __tablename__ = 'qualifications'
    qualification_id = mydb_obj.Column(mydb_obj.Integer, primary_key=True)#PK
    qualification_name = mydb_obj.Column(mydb_obj.String(150))
    courseid = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('courses.courseid'),nullable=False) #FK


    users = mydb_obj.relationship('user', backref='qualifications', uselist=False)  # One-to-one relationship with Enquiries
    courses = mydb_obj.relationship('Courses',backref='qualifications', uselist=False)  # One-to-one relationship with Enquiries
    #user = mydb_obj.relationship('User', back_populates='qualifications', uselist=False)  # One-to-one relationship with Enquiries

#USER Table
class User(mydb_obj.Model):
    __tablename__ = 'users'
    id = mydb_obj.Column(mydb_obj.Integer, primary_key=True) #primary key
    username = mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    password = mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    firstname = mydb_obj.Column(mydb_obj.String(150), nullable=False)
    lastname = mydb_obj.Column(mydb_obj.String(150), nullable=False)
    gender=mydb_obj.Column(mydb_obj.String(10),nullable=False)
    age = mydb_obj.Column(mydb_obj.Integer,nullable=False) 
    email = mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    phone_number = mydb_obj.Column(mydb_obj.Integer, unique=True, nullable=False)
    address = mydb_obj.Column(mydb_obj.String(200), unique=True, nullable=False)
    date_of_birth = mydb_obj.Column(mydb_obj.Date, nullable=False)  # Date of birth
    highest_qualificationid = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('qualifications.qualification_id'),nullable=False) #FK


    marks = mydb_obj.Column(mydb_obj.Integer, nullable=False)
    yearofgraduation =  mydb_obj.Column(mydb_obj.Integer, nullable=False)
    #enquiries = mydb_obj.relationship('Enquiries', backref='user', uselist=False)  # One-to-one relationship with Enquiries

class CourseModules(mydb_obj.Model):
    __tablename__ = 'coursemodules'
    moduleid = mydb_obj.Column(mydb_obj.Integer, primary_key=True)#PK
    modulename = mydb_obj.Column(mydb_obj.String(150))
    courseid = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('courses.courseid'),nullable=False) #Foreignkey

    coursess = mydb_obj.relationship('Courses', backref='coursemodules')  # One-to-many relationship with Courses


#COURSE Table
class Courses(mydb_obj.Model):
    __tablename__ = 'courses'
    courseid = mydb_obj.Column(mydb_obj.Integer, primary_key=True) #primary key
    coursename= mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    description= mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    course_duration = mydb_obj.Column(mydb_obj.Integer, nullable=False)  # Duration in hours
    fees = mydb_obj.Column(mydb_obj.Integer, nullable=False)
    qualification_id = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('qualifications.qualification_id'),nullable=False) #FK
    moduleid= mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('coursemodules.moduleid'),nullable=False) #Foreignkey
    #courses = mydb_obj.relationship('Courses', backref='user')

    enquiriess= mydb_obj.relationship('Enquiries', backref='courses', uselist=False)  # One-to-one relationship with courses
    #qualifications = mydb_obj.relationship('qualifications', backref='courses', uselist=False)  # One-to-one relationship with Enquiries
    #coursemodules = mydb_obj.relationship('courseModules', backref='courses', uselist=False)  # One-to-one relationship with Enquiries


#Resources Table
class Resources(mydb_obj.Model):
    __tablename__ = 'resources'
    resourceid = mydb_obj.Column(mydb_obj.Integer, primary_key=True) #PK
    resourcename = mydb_obj.Column(mydb_obj.String(150))
    enquiriess = mydb_obj.relationship('Enquiries', backref='resources', uselist=False)  # One-to-one relationship with Enquiries

#Enquiry Status Table
class EnquiryStatus(mydb_obj.Model):
    __tablename__ = 'enquirystatus'
    enquirys_id = mydb_obj.Column(mydb_obj.Integer, primary_key=True) #PK
    enquiry_status =  mydb_obj.Column(mydb_obj.Integer)
    enquiries = mydb_obj.relationship('Enquiries', backref='enquirystatus', uselist=False)  # One-to-one relationship with Enquiries

class Enquiries(mydb_obj.Model):
    __tablename__ = 'enquiries'
    enqid = mydb_obj.Column(mydb_obj.Integer, primary_key=True)
    userid = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('users.id'),nullable=False)
    courseid = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('courses.courseid'),nullable=False) #FK

    enquiry_date =  mydb_obj.Column(mydb_obj.DateTime, default=datetime.now) 
    message =  mydb_obj.Column(mydb_obj.String(150))
    statusid = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('enquirystatus.enquirys_id'),nullable=False) #FK
    resource = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('resources.resourceid'),nullable=False) #FK











class addform(FlaskForm):
    firstname=StringField('First Name:',validators=[DataRequired()])
    lastname=StringField('Last Name:',validators=[DataRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=72)])
    username=StringField('Username:',validators=[DataRequired()])
    age=IntegerField(' Age:',validators=[DataRequired()])
    email=StringField(' Email:',validators=[DataRequired(),Email()])
    address=StringField(' Adress:')
    gender=SelectField(' Gender:',choices=[('Male','Male'),('Female','Female')])
    phone=FloatField('Number',validators=[DataRequired()])
    dob = DateField('Date of Birth:', validators=[DataRequired()])
    qualification=StringField(' Qualification:',validators=[DataRequired()])
    marks=IntegerField('Marks(%):',validators=[DataRequired()])
    yearofgrad=StringField(' Year of Graduation:',validators=[DataRequired()])
    submit_btn=SubmitField('SUBMIT')



@app.route('/')
def index():
    mydb_obj.create_all()
    return render_template('ADMINHOME1.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/adduser',methods=['GET','POST'])
def adduser():
    firstname=None
    lastname=None
    password=None
    marks=None
    username=None
    age=None
    email=None
    address=None
    gender=None
    phone=None
    qualification=None
    yearofgrad=None
    dob=None
    form=addform()
    if form.validate_on_submit():
        firstname=form.firstname.data
        lastname=form.lastname.data
        password=form.password.data
        username=form.username.data
        age=form.age.data
        phone=form.phone.data
        email=form.email.data
        address=form.address.data
        gender=form.gender.data
        marks=form.marks.data
        qualification=form.qualification.data
        yearofgrad=form.yearofgrad.data

        user=User(firstname=firstname,lastname=lastname,age=age,email=email,password=password,username=username,phone_number=phone,address=address,gender=gender,highest_qualificationid=qualification,marks=marks,yearofgraduation=yearofgrad,date_of_birth=dob)
        mydb_obj.session.add(user)
        mydb_obj.session.commit()

        flash(f'Data recieved {firstname}')

        return redirect(url_for('listusers'))
    return render_template('adduser.html',form=form)

@app.route('/listusers')
def listusers():
    #return render_template('listusers.html')
    return render_template('listusers.html',all_user=User.query.all())



class addenquiryform(FlaskForm):
    coursename=SelectField('course:',coerce=str)
    userid=StringField('User ID:',validators=[DataRequired()])
    message=StringField('Username:')
    status=SelectField(' Status:',choices=[('Accepted','Pending','Closed'),('Accepted','Pending','Closed')])
    submit_btn=SubmitField('SUBMIT')

@app.route('/addenquiry',methods=['GET','POST'])
def addenquiry():
    coursename=None
    userid=None
    message=None
    status=None
    form=addenquiryform()
    #form.course.choices = [(course.id, course.name) for course in Course.query.all()]

    if form.validate_on_submit():
        coursename=form.coursenmae.data
        userid=form.userid.data
        message=form.message.data
        status=form.status.data

        return redirect(url_for('listenquires'))
    return render_template('addenquiry.html',form=form)



@app.route('/listenquires')
def listenquires():
    return render_template('listenquires.html')


class addcourseform(FlaskForm):
    coursename=StringField('Course Name:',validators=[DataRequired()])
    duration=IntegerField('Duration(Hours):',validators=[DataRequired()])
    fees=IntegerField(' Fees:',validators=[DataRequired()])
    qualificationreq=StringField(' Qualification required:',validators=[DataRequired()])
    submit_btn=SubmitField('SUBMIT')


@app.route('/addcourse',methods=['GET','POST'])
def addcourse():
    coursename=None
    duration=None
    fees=None
    qualificationreq=None
    form=addcourseform()
    

    if form.validate_on_submit():
        coursename=form.coursename.data
        duration=form.duration.data
        fees=form.fees.data
        qualificationreq=form.qualificationreq.data

        return redirect(url_for('listcourse'))
    return render_template('addcourse.html',form=form)


@app.route('/listcourse')
def listcourse():
    return render_template('listcourse.html')


class addqualificationform(FlaskForm):
    qualificationname=StringField('Qualification Name:',validators=[DataRequired()])
    submit_btn=SubmitField('SUBMIT')

@app.route('/addqualification',methods=['GET','POST'])
def addqualification():
    qualificationname=None
    form=addqualificationform()
    

    if form.validate_on_submit():
        qualificationname=form.qualificationname.data
        return redirect(url_for('listqualification'))
    return render_template('addqualification.html',form=form)

@app.route('/listqualification')
def listqualification():
    return render_template('listqualification.html')