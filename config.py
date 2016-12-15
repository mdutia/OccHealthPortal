CSRF_ENABLED = True
SECRET_KEY = 'Cjq0nz2@kWl2Pm'
SQLALCHEMY_DATABASE_URI = 'sqlite:///userdata.db'
SQLALCHEMY_BINDS = {
    'projects':      'sqlite:///admins.db'
}
FacilitiesList =[('All', 'All'), ('1GSQ','1GSQ'), ('Ash', 'Ash'), ('AWB', 'AWB'), ('CSQ', 'CSQ'), ('Evans', 'Evans'), ('HRB', 'HRB'),
                                   ('LF1', 'LF1'), ('LF2', 'LF2'), ('MacRH', 'MacRH'), ('SCRM', 'SCRM'), ('Teviot', 'Teviot'),('WGH', 'WGH'), 
                                   ('None', 'None'), ('Other', 'Other')  ]
StatusList= [('All','All users'),('Yes', 'All Active users'), ('No', 'All inactive users'),
                                     ('Active_students','Active students only'),('Active_staff', 'Active staff only'), ('Inactive_students', 'Inactive students only'),
                                     ('Inactive_staff', 'Inactive staff only'),
                                     ('Exp_all','All expired users'),('Exp_students','Expired students only'), ('Exp_staff', 'Expired staff only')]
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
