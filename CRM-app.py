from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from wtforms import StringField, DateField,FloatField, EmailField, SelectField, PasswordField, RadioField, SubmitField, widgets, TextAreaField,IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo,Regexp,InputRequired
from config import Config  # Make sure to import your Config class
from flask_login import login_user, LoginManager, logout_user, current_user, login_required
from flask_login import UserMixin
from flask import session
from datetime import datetime, timezone
from flask_login import LoginManager,login_user, logout_user, current_user, login_required, UserMixin

app = Flask(__name__) 
app.config.from_object('config.Config')
mydb_obj = SQLAlchemy(app)
migrate = Migrate(app,mydb_obj)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'



boostrap = Bootstrap(app)

#---------Database------------#

#USER Table
class User(mydb_obj.Model, UserMixin):
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




#---------Form classes--------#
class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])
    age = IntegerField('Age',validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    address=TextAreaField(' Address ')
    qualification = SelectField('Highest qualification',choices=[],validators=[DataRequired()])
    marks = IntegerField('Marks',validators=[DataRequired()])
    yearofgrad =  IntegerField('Graduation year',validators=[DataRequired()])

    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=20),
        Regexp(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,20}$', 
               message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
    ])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

class EnquiryForm(FlaskForm):
    userid=SelectField('UserID  ',choices=[],validators=[DataRequired()])
    coursename = SelectField('Course name  ',choices=[],validators=[DataRequired()])
    message = TextAreaField('Your message', validators=[DataRequired()])
    resource=SelectField('Where did you find us',choices=[('SOCIAL MEDIA','SOCIAL MEDIA'),('FRIEND/RELATIVE','FRIEND/RELATIVE'),('GOOGLE SEARCH','GOOGLE SEARCH')],default='GOOGLE SEARCH')
    submit = SubmitField('Enquire')


#============================================# Pre Login #============================================#



@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/about')
def about():
    return render_template('About Us.html')

@app.route('/courses')
def courses():
    return render_template('Courses.html',co=Courses.query.all())

#============================================# Login or Sign Up options #============================================#


#User loader for Flask-Login
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user.role_user)
        print(user.email)
        print(user.password)
        print(form.password.data)

        if user and user.password == form.password.data:
            print(user.role_user)
            print(user.email)
            login_user(user, remember=False)
            if user.role_user == 'user1':
                return redirect(url_for('uprofile',id=user.id))
            else:
                print("Admin working")
                print(user.role_user)
                print(user.email)
                return redirect(url_for('index2'))
        else:
            flash("Incorrect credentials")
            
        
        
    return render_template('Login.html',form=form) # login page

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
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

    form.qualification.choices=['10th','12th','Bachelors','Masters']
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
        dob=form.birthday.data

        user=User(firstname=firstname,lastname=lastname,age=age,email=email,password=password,username=username,phone_number=phone,address=address,gender=gender,highest_qualification=qualification,marks=marks,yearofgraduation=yearofgrad,date_of_birth=dob)
        mydb_obj.session.add(user)
        mydb_obj.session.commit()

        flash(f'Data recieved')

        return redirect(url_for('login'))
    return render_template('Register.html',form=form) # login page





#============================================# User #============================================#

# @app.route('/user/')
# def userindex():
#     return render_template('UserBase.html')

@app.route('/user/dash')
def userdash():
    return render_template('UserDash.html')

@app.route('/user/about')
def userabout():
    return render_template('UserAboutUs.html')

#============================================# User Profile options #============================================#


@app.route('/user/profile/<id>')
def uprofile(id):
    return render_template('UserViewProfile.html',userprofile=User.query.get_or_404(id),n=current_user.id) # view user profile

@app.route('/user/edit/<id>', methods=['GET', 'POST'])
def uedit(id):
    user=User.query.get_or_404(id)
    form = RegistrationForm(obj=user)
    uid=user.id
    form.qualification.choices=['10th','12th','Bachelors','Masters']

    if request.method=='GET':
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
        form.birthday.data=user.date_of_birth
        return render_template('UserEditProfile.html',form=form,val=uid) # Edit user profile 
    else:
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
        user.highest_qualification=form.qualification.data
        user.yearofgrad=form.yearofgrad.data
        user.dob=form.birthday.data
        mydb_obj.session.commit()    
        return redirect(url_for('uprofile',id=uid)) 

@app.route('/user/delete/<id>') #delete user, and go to pre-login home page
def udel(id):
    id=id
    return render_template('UserDelete.html',id=id)

@app.route('/user/deleteconfirm/<id>',methods=['GET','POST']) #delete user, and go to pre-login home page
def delconfirm(id):
    user=User.query.get_or_404(id)
    Enquiries.query.filter_by(userid=id).delete()
    
    mydb_obj.session.delete(user)
    mydb_obj.session.commit()
    return redirect(url_for('home'))


#============================================# User Enquiry options #============================================#


@app.route('/user/courses')
def ucourses():
    return render_template('UserViewCourses.html',co=Courses.query.all()) # view courses                     

@app.route('/user/enquire',methods=['GET','POST'])
def uenquire():
    form = EnquiryForm()

    coursename=None
    userid=None
    message=None
    resource=None
    
    # form.coursename.choices = [(course.coursename) for course in Courses.query.all()]
    # form.userid.choices=[(c.id) for c in User.query.all()]

    form.coursename.choices = ['Java','Python','R','Fullstack']
    form.userid.choices=[(c.id) for c in User.query.all()]
    if form.validate_on_submit():
        coursename=form.coursename.data
        userid=form.userid.data
        message=form.message.data
        resource=form.resource.data

        enquiry=Enquiries(course=coursename,userid=userid,message=message,resource=resource)
        mydb_obj.session.add(enquiry)
        mydb_obj.session.commit()


        return redirect(url_for('uviewenq',id=userid))
    return render_template('UserEnquire.html',form=form) # enquire about a course

@app.route('/user/viewenquiries/<id>')
def uviewenq(id):
    return render_template('UserViewEnq.html',all_enquiry=Enquiries.query.filter_by(userid=id).all()) # view user enquiries

@app.route('/user/test')
def u():
    return render_template('ViewBase.html') # view user enquiries



#---------Admin--------#

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






@app.route('/admindash')
def index2():
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    session.clear()
    return redirect(url_for('login'))