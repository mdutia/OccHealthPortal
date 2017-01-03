from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from sqlalchemy.types import PickleType
from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_folder='Static')
app.config.from_object('config')
db = SQLAlchemy(app)
Bootstrap(app)

from app import views

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False)

    def __init__(self ): 
        self.username=''

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username



class Userdata(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)    
    #Name
    #title = db.Column(db.String(6))
    firstname= db.Column(db.String(40), unique=False)
    lastname= db.Column(db.String(40), unique=False)
    #centre= db.Column (db.String(120), unique=False)    
    #Staff/ student number
    roll= db.Column(db.Integer, unique=False)
    email= db.Column(db.String(60), unique=False)
    #Supervisor / manager
    supervisor= db.Column(db.String(60), unique=False)
    #Position
    position= db.Column (db.String(40), unique=False)
    #Location
    location= db.Column (db.String(120), unique=False)
    facility1= db.Column(db.String(20), unique=False)
    facility2= db.Column(db.String(20), unique=False)
    #Active / non active
    active_status= db.Column(db.String(16))
    #Date of test recorded somehow so we have a history
    #Fit 3, fit 6, fit 12, fit with restriction , not fit   from drop down menu
    tests= db.Column(db.String(5024))
    last_test= db.Column (db.String(40), unique=False)
    expiry_date= db.Column (db.String(20), unique=False)
    days_to_expiry= db.Column (db.Integer, unique=False)
    #tests = db.relationship('Test', backref="user", lazy='dynamic')
    #Skin / lung
    restrictions= db.Column(db.String(6), unique=False)
    skin= db.Column(db.String(6), unique=False)
    lung= db.Column(db.String(6), unique=False)
    #Face fit or not
    facefit= db.Column(db.String(20), unique=False)
    comment = db.Column(db.String(1024))
    
    #Ability to search on ( filtered by active and non active)
    #Person   produce history of tests
    #Place  who here needs a test in the next x months
    #Facility  who are all the people who work in a facility 

    def __init__(self ): 
        self.title, self.firstname, self.lastname, self.roll= '','','',''
        self.position, self.supervisor, self.location = '','',''
        self.facility1, self.active_status, self.skin, self.lung, self.facefit, self.comment = '','','','','',''
        self.facility2= ''
        self.tests= ''
        self.last_test= '-,-'
        

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return unicode(self.id) #'<User {0} {1}>'.format (self.id, self.firstname.encode('utf-8'), self.lastname) 

class Test(db.Model):
    __tablename__='tests'
    id = db.Column(db.Integer, primary_key=True)    
    #date
    date= db.Column(db.String(60), unique=False)
    result= db.Column(db.String(10), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self ): 
        self.date, self.result, self.user_id = 3*' '

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<Test {0} {1}>'.format (self.id, self.date, self.result) 


login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return Userdata.query.get(int(id))