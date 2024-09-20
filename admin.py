from flask import Flask,redirect,url_for,render_template
from flask_bootstrap import Bootstrap
from flask_material import Material
from flask_sqlalchemy import SQLAlchemy #import SQLAlchemy class from flask_sqlalchemy pkg
from flask_migrate import Migrate
import urllib.parse
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,DecimalField,SelectField,FloatField,PasswordField,DateField
from wtforms.validators import DataRequired,Length,EqualTo
from flask import session
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
from flask import flash
from flask_login import LoginManager,login_user,UserMixin
from flask_login import current_user,logout_user,login_required

app=Flask(__name__)
bootstrap=Bootstrap(app)
material=Material(app)
app.config.from_object('config.Config')#loading the configuration from the config class

mydb_obj = SQLAlchemy(app) #create an SQLAlchemy object
migrate=Migrate(app,mydb_obj)


class User(mydb_obj.Model,UserMixin):
    id=mydb_obj.Column(mydb_obj.Integer,primary_key=True)
    username=mydb_obj.Column(mydb_obj.String(150),unique=True,nullable=False)
    mail=mydb_obj.Column(mydb_obj.String(60),unique=True,nullable=False)
    address=mydb_obj.Column(mydb_obj.String(255),nullable=False)
    dob=mydb_obj.Column(mydb_obj.Date),nullable=False)
    phone=mydb_obj.Column(mydb_obj.Float,nullable=False)

    password=mydb_obj.Column(mydb_obj.String(150),nullable=False)
    role=mydb_obj.Column(mydb_obj.String(50),nullable=False,default='user')

@app.route('/')
def index():
    return render_template('ADMINHOME1.html')