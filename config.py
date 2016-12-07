CSRF_ENABLED = True
SECRET_KEY = 'Cjq0nz2@kWl2Pm'
SQLALCHEMY_DATABASE_URI = 'sqlite:///userdata.db'
SQLALCHEMY_BINDS = {
    'projects':      'sqlite:///admins.db'
}
#MAIL_SERVER='smtp.staffmail.ed.ac.uk'
#MAIL_USERNAME= "mdutia@staffmail.ed.ac.uk"

#MAIL_SERVER='smtp.gmail.com'
#MAIL_PORT = 465
#MAIL_USERNAME= "sbms.bmto@gmail.com"
#MAIL_PASSWORD= "t3stingsyst3m1"
#MAIL_USE_TLS = False
#MAIL_USE_SSL = True

MAIL_SERVER='smtp.office365.com'
MAIL_PORT = 587
MAIL_USERNAME= "mdutia@ed.ac.uk"
MAIL_PASSWORD= "password"
MAIL_USE_TLS = True
MAIL_USE_SSL = False


HOST='Local' #EASE 
ADMINS= 'mdutia'
