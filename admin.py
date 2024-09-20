from flask import Flask,redirect,url_for,render_template
from flask_bootstrap import Bootstrap
from flask_material import Material
from flask_sqlalchemy import SQLAlchemy #import SQLAlchemy class from flask_sqlalchemy pkg
from flask_migrate import Migrate
import urllib.parse
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,DecimalField,SelectField,FloatField,PasswordField,DateField
from wtforms.validators import DataRequired,Length,EqualTo,Email
from flask import session
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from flask import flash
from flask_login import LoginManager,login_user,UserMixin
from flask_login import current_user,logout_user,login_required
from email_validator import validate_email, EmailNotValidError

app=Flask(__name__)
bootstrap=Bootstrap(app)
material=Material(app)
app.config.from_object('config.Config')#loading the configuration from the config class

mydb_obj = SQLAlchemy(app) #create an SQLAlchemy object
migrate=Migrate(app,mydb_obj)



class addform(FlaskForm):
    name=StringField(' Name:',validators=[DataRequired()])
    username=StringField('Username:',validators=[DataRequired()])
    age=IntegerField(' age:',validators=[DataRequired()])
    email=StringField(' Email:',validators=[DataRequired(),Email()])
    address=StringField(' Adress:')
    gender=SelectField(' Gender:',choices=[('Male','Male'),('Female','Female')])
    phone=FloatField('Number',validators=[DataRequired()])
    qualification=StringField(' Qualification:',validators=[DataRequired()])
    yearofgrad=StringField(' Year of Graduation:',validators=[DataRequired()])
    submit_btn=SubmitField('SUBMIT')



@app.route('/')
def index():
    return render_template('ADMINHOME1.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/adduser',methods=['GET','POST'])
def adduser():
    name=None
    username=None
    age=None
    email=None
    address=None
    gender=None
    phone=None
    qualification=None
    yearofgrad=None
    form=addform()
    if form.validate_on_submit():
        name=form.name.data
        username=form.username.data
        age=form.age.data
        phone=form.phone.data
        email=form.email.data
        address=form.address.data
        gender=form.gender.data
        qualification=None
        yearofgrad=None

        flash(f'Data recieved {name},{age},{email},{address} and {phone}')

        return redirect(url_for('list'))
    return render_template('adduser.html',form=form)

@app.route('/listusers')
def listuser():
    return render_template('listusers.html')


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