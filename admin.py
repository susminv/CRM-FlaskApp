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
from flask import flash,request
from flask_login import LoginManager,login_user,UserMixin
from flask_login import current_user,logout_user,login_required
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
from wtforms_sqlalchemy.fields import QuerySelectField

app=Flask(__name__)
bootstrap=Bootstrap(app)
material=Material(app)
app.config.from_object('config.Config')#loading the configuration from the config class

mydb_obj = SQLAlchemy(app) #create an SQLAlchemy object
migrate=Migrate(app,mydb_obj)

#USER Table
class User(mydb_obj.Model):
    __tablename__ = 'user'  # Explicitly define the table name

    id = mydb_obj.Column(mydb_obj.Integer, primary_key=True) #primary key
    username = mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    password = mydb_obj.Column(mydb_obj.String(150), unique=False, nullable=False)
    firstname = mydb_obj.Column(mydb_obj.String(150), nullable=False)
    lastname = mydb_obj.Column(mydb_obj.String(150), nullable=False)
    email = mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    phone_number = mydb_obj.Column(mydb_obj.Integer, unique=False, nullable=False)
    age = mydb_obj.Column(mydb_obj.Integer, unique=False, nullable=False)
    gender = mydb_obj.Column(mydb_obj.String(101), unique=False, nullable=False)
    address = mydb_obj.Column(mydb_obj.String(200), unique=False, nullable=False)
    date_of_birth = mydb_obj.Column(mydb_obj.Date, nullable=False)  # Date of birth
    highest_qualification = mydb_obj.Column(mydb_obj.String(150),nullable=False) 
    marks = mydb_obj.Column(mydb_obj.Integer, nullable=False)
    yearofgraduation =  mydb_obj.Column(mydb_obj.Integer, nullable=False)  
    role_user = mydb_obj.Column(mydb_obj.String(10), unique=False, nullable=False,default='user1')

    enquiry=mydb_obj.relationship('Enquiries',backref='user',uselist=False)

#COURSE Table
class Courses(mydb_obj.Model):
    courseid = mydb_obj.Column(mydb_obj.Integer, primary_key=True) #primary key
    coursename= mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    description= mydb_obj.Column(mydb_obj.String(150), unique=True, nullable=False)
    course_duration = mydb_obj.Column(mydb_obj.Integer, nullable=False)  # Duration in hours
    fees = mydb_obj.Column(mydb_obj.Integer, nullable=False)

    qualification = mydb_obj.Column(mydb_obj.String(150),nullable=False) #FK
  
   
class Enquiries(mydb_obj.Model):
    
    enqid = mydb_obj.Column(mydb_obj.Integer, primary_key=True)
    userid = mydb_obj.Column(mydb_obj.Integer, mydb_obj.ForeignKey('user.id'),nullable=False)
    course = mydb_obj.Column(mydb_obj.String(100)) #FK
    enquiry_date =  mydb_obj.Column(mydb_obj.DateTime, default=datetime.now) 
    message =  mydb_obj.Column(mydb_obj.String(150))
    status = mydb_obj.Column(mydb_obj.String(150),nullable=False,default='pending') #FK
    resource = mydb_obj.Column(mydb_obj.String(150),nullable=False) #FK
    


class Qualifications(mydb_obj.Model):
    qualification_id = mydb_obj.Column(mydb_obj.Integer, primary_key=True)
    qualification_name = mydb_obj.Column(mydb_obj.String(150))





class addform(FlaskForm):
    firstname=StringField('First Name:',validators=[DataRequired()])
    lastname=StringField('Last Name:',validators=[DataRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=72)])
    username=StringField('Username:',validators=[DataRequired()])
    age=IntegerField(' Age:',validators=[DataRequired()])
    email=StringField(' Email:',validators=[DataRequired(),Email()])
    address=StringField(' Adress:')
    gender=SelectField('Gender:',choices=[('Male','Male'),('Female','Female')])
    phone=FloatField('Number',validators=[DataRequired()])
    dob = DateField('Date of Birth:', validators=[DataRequired()])
    qualification = SelectField('Whats your qualification',choices=[],validators=[DataRequired()])
    marks=IntegerField('Marks(%):',validators=[DataRequired()])
    yearofgrad=StringField(' Year of Graduation:',validators=[DataRequired()])
    submit_btn=SubmitField('SUBMIT')






@app.route('/')
def index():
    user_count = User.query.count()
    enquiry_count = Enquiries.query.count()
    course_count = Courses.query.count()

    mydb_obj.create_all()
    return render_template('ADMINHOME1.html',user_count=user_count,enquiry_count=enquiry_count,course_count=course_count)

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
    form.qualification.choices=[(c.qualification_name) for c in Qualifications.query.all()]
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
        dob=form.dob.data

        user=User(firstname=firstname,lastname=lastname,age=age,email=email,password=password,username=username,phone_number=phone,address=address,gender=gender,highest_qualification=qualification,marks=marks,yearofgraduation=yearofgrad,date_of_birth=dob)
        mydb_obj.session.add(user)
        mydb_obj.session.commit()

        flash(f'Data recieved {firstname}')

        return redirect(url_for('listusers'))
    return render_template('adduser.html',form=form)

@app.route('/listusers')
def listusers():
    #return render_template('listusers.html')
    return render_template('listusers.html',all_user=User.query.all())

@app.route('/edituser/<id>',methods=['GET','POST'])
def edit(id):
    user=User.query.get_or_404(id)
    form=addform(obj=user)
    form.qualification.choices=[(c.qualification_name) for c in Qualifications.query.all()]

    if form.validate_on_submit():
        user.firstname=form.firstname.data
        user.lastname=form.lastname.data
        user.password=form.password.data
        user.username=form.username.data
        user.age=form.age.data
        user.phone=form.phone.data
        user.email=form.email.data
        user.address=form.address.data
        user.gender=form.gender.data
        user.marks=form.marks.data
        user.qualification=form.qualification.data
        user.yearofgrad=form.yearofgrad.data
        user.dob=form.dob.data

        mydb_obj.session.commit()    

        return redirect(url_for('listusers'))
    elif request.method=='GET':
        form.firstname.data=user.firstname
        form.lastname.data=user.lastname
        form.password.data=user.password
        form.username.data=user.username
        form.age.data=user.age
        form.phone.data=user.phone_number
        form.email.data=user.email
        form.address.data=user.address
        form.gender.data=user.gender
        form.marks.data=user.marks
        form.qualification.data=user.highest_qualification
        form.yearofgrad.data=user.yearofgraduation
        form.dob.data=user.date_of_birth
        mydb_obj.session.commit()


    return render_template('edituser.html',form=form)

@app.route('/deleteuser/<id>',methods=['GET','POST'])
def delete(id):

    user=User.query.get_or_404(id)
    Enquiries.query.filter_by(userid=id).delete()
    mydb_obj.session.delete(user)
    mydb_obj.session.commit()

    return redirect(url_for('listusers'))

class addenquiryform(FlaskForm):
    coursename = SelectField('Course to Enquire',choices=[],validators=[DataRequired()])
    userid=SelectField('UserID of Enquirer:',choices=[],validators=[DataRequired()])
    message=StringField('Message:')
    status=SelectField('Status:',choices=[('Accepted','Accepted'),('Closed','Closed'),('Pending','Pending')],default='Pending')
    resource=SelectField('Where did you find us:',choices=[('SOCIAL MEDIA','SOCIAL MEDIA'),('FRIEEND/RELATIVE','FRIEEND/RELATIVE'),('GOOGLE SEARCH','GOOGLE SEARCH')],default='GOOGLE SEARCH')
    submit_btn=SubmitField('SUBMIT')

@app.route('/addenquiry',methods=['GET','POST'])
def addenquiry():
    coursename=None
    userid=None
    message=None
    status=None
    resource=None
    form=addenquiryform()
    form.coursename.choices = [(course.coursename) for course in Courses.query.all()]
    form.userid.choices=[(c.id) for c in User.query.all()]

    if form.validate_on_submit():
        coursename=form.coursename.data
        userid=form.userid.data
        message=form.message.data
        status=form.status.data
        resource=form.resource.data

        enquiry=Enquiries(course=coursename,userid=userid,message=message,status=status,resource=resource)
        mydb_obj.session.add(enquiry)
        mydb_obj.session.commit()


        return redirect(url_for('listenquiries'))
    return render_template('addenquiry.html',form=form)



@app.route('/listenquiries')
def listenquiries():
    return render_template('listenquires.html',all_enquiry=Enquiries.query.all())


@app.route('/editenquiry/<id>',methods=['GET','POST'])
def editenquiry(id):
    enquiries=Enquiries.query.get_or_404(id)
    form=addenquiryform(obj=enquiries)
    form.coursename.choices = [(course.coursename) for course in Courses.query.all()]
    form.userid.choices=[(c.id) for c in User.query.all()]

    if form.validate_on_submit():
        enquiries.coursename=form.coursename.data
        enquiries.userid=form.userid.data
        enquiries.message=form.message.data
        enquiries.status=form.status.data
        enquiries.resource=form.resource.data

        mydb_obj.session.commit()    

        return redirect(url_for('listenquiries'))
    elif request.method=='GET':
        form.coursename.data=enquiries.course
        form.userid.data=enquiries.userid
        form.message.data=enquiries.message
        form.status.data=enquiries.status
        form.resource.data=enquiries.resource
        mydb_obj.session.commit()


    return render_template('editenquiry.html',form=form)

@app.route('/deleteenquiry/<id>',methods=['GET','POST'])
def deleteenquiry(id):
    enquiry=Enquiries.query.get_or_404(id)
    mydb_obj.session.delete(enquiry)
    mydb_obj.session.commit()
    return redirect(url_for('listenquiries'))



class addcourseform(FlaskForm):
    coursename=StringField('Course Name:',validators=[DataRequired()])
    duration=IntegerField('Duration(Hours):',validators=[DataRequired()])
    description=StringField(' Description:',validators=[DataRequired()])
    fees=IntegerField(' Fees:',validators=[DataRequired()])
    qualification = SelectField('Qualification Required:',choices=[],validators=[DataRequired()])
    submit_btn=SubmitField('SUBMIT')


@app.route('/addcourse',methods=['GET','POST'])
def addcourse():
    coursename=None
    duration=None
    description=None
    fees=None
    qualification=None
    form=addcourseform()
    form.qualification.choices=[(c.qualification_name) for c in Qualifications.query.all()]
    

    if form.validate_on_submit():
        coursename=form.coursename.data
        duration=form.duration.data
        fees=form.fees.data
        qualification=form.qualification.data
        description=form.description.data
        course=Courses(coursename=coursename,description=description,course_duration=duration,fees=fees,qualification=qualification)
        mydb_obj.session.add(course)
        mydb_obj.session.commit()

        return redirect(url_for('listcourse'))
    return render_template('addcourse.html',form=form)


@app.route('/listcourse')
def listcourse():
    return render_template('listcourse.html',all_courses=Courses.query.all())

@app.route('/editcourse/<id>',methods=['GET','POST'])
def editcourse(id):
    course=Courses.query.get_or_404(id)
    form=addcourseform(obj=course)
    form.qualification.choices=[(c.qualification_name) for c in Qualifications.query.all()]   

    if form.validate_on_submit():
        course.coursename=form.coursename.data
        course.description=form.description.data
        course.course_duration=form.duration.data
        course.fees=form.fees.data
        course.qualification=form.qualification.data

        mydb_obj.session.commit()    

        return redirect(url_for('listcourse'))
    elif request.method=='GET':
        form.coursename.data=course.coursename
        form.description.data=course.description
        form.duration.data=course.course_duration
        form.fees.data=course.fees
        form.qualification.data=course.qualification
        mydb_obj.session.commit()


    return render_template('editcourse.html',form=form)

@app.route('/deletecourse/<id>',methods=['GET','POST'])
def deletecourse(id):
    course=Courses.query.get_or_404(id)
    mydb_obj.session.delete(course)
    mydb_obj.session.commit()
    return redirect(url_for('listcourse'))

class addqualificationform(FlaskForm):
    qualificationname=StringField('Qualification Name:',validators=[DataRequired()])
    submit_btn=SubmitField('SUBMIT')

@app.route('/addqualification',methods=['GET','POST'])
def addqualification():
    qualification_name=None
    form=addqualificationform()
    
    if form.validate_on_submit():
        quali=form.qualificationname.data
        qualification=Qualifications(qualification_name=quali)
        mydb_obj.session.add(qualification)
        mydb_obj.session.commit()
        return redirect(url_for('listqualification'))
    return render_template('addqualification.html',form=form)

@app.route('/listqualification')
def listqualification():
    return render_template('listqualification.html',all_qualification=Qualifications.query.all())

@app.route('/deletequalification/<id>',methods=['GET','POST'])
def deletequalification(id):
    qualification=Qualifications.query.get_or_404(id)
    mydb_obj.session.delete(qualification)
    mydb_obj.session.commit()
    return redirect(url_for('listqualification'))