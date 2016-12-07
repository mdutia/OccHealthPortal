from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, RadioField, TextAreaField, SelectField, IntegerField
from wtforms.validators import Required, NumberRange, Length
from wtforms.fields.html5 import DateField

class LoginForm(Form):
    uname= TextField('username', validators = [Required()])
   #pwd = PasswordField('pwd', validators = [Required()])
    #remember_me = BooleanField('remember_me', default = False)
    
    
class NewUserForm (Form):
    title= SelectField(choices=[('Ms', 'Ms'), ('Mr', 'Mr'), ('Dr', 'Dr'), ('Prof', 'Prof') ])
    firstname= TextField(label='First name', validators= [Length(min=3, max=255, message='First name (max 40 chars)')])
    lastname= TextField(label='Last name', validators= [Length(min=3, max=255, message='Last name (max 40 chars)')])
    roll= IntegerField(label='StaffNo', validators = [Required()] ) #, validators= [Length(min=3, max=55, message='Staff number')])
    group= TextField(label='Group', validators= [Length(min=1, max=255, message='Group')])
    location= TextField(label='Location', validators= [Length(min=1, max=255, message='Location')])
    facility1= SelectField(choices=[('None', 'None'), ('Other', 'Other'), ('Ash', 'Ash'), ('AWB', 'AWB'), ('MacRH', 'MacRH'), ('WGH', 'WGH'), ('Evans', 'Evans'),
                                   ('LF1', 'LF1'), ('LF2', 'LF2'), ('HRB', 'HRB'), ('CSQ', 'CSQ'), ('SCRM', 'SCRM'), ('1GSQ','1GSQ'), ('Teviot', 'Teviot') ])    
    facility2= SelectField(choices=[('None', 'None'), ('Other', 'Other'), ('Ash', 'Ash'), ('AWB', 'AWB'), ('MacRH', 'MacRH'), ('WGH', 'WGH'), ('Evans', 'Evans'),
                                    ('LF1', 'LF1'), ('LF2', 'LF2'), ('HRB', 'HRB'), ('CSQ', 'CSQ'), ('SCRM', 'SCRM'), ('1GSQ','1GSQ'), ('Teviot', 'Teviot')  ])   
    activity_status= SelectField(choices=[('Yes', 'Yes'), ('No', 'No'), ('-', '-') ])
    restrictions= SelectField(choices=[('No', 'No'), ('Yes', 'Yes')], default='No')
    skin= SelectField(choices=[('No', 'No'), ('Yes', 'Yes')], default='No')
    lung= SelectField(choices=[('No', 'No'), ('Yes', 'Yes')], default='No')
    facefit= SelectField(choices=[('No', 'No'), ('Yes', 'Yes')], default='No')
    comment= TextAreaField()
    
class EditUserForm (Form):
    #title= SelectField(choices=[('Ms', 'Ms'), ('Mr', 'Mr'), ('Dr', 'Dr'), ('Prof', 'Prof') ])
    firstname= TextField(label='First name', validators= [Length(min=3, max=255, message='First name (max 40 chars)')])
    lastname= TextField(label='Last name', validators= [Length(min=3, max=255, message='Last name (max 40 chars)')])
    email= TextField(label='Email', validators= [Length(min=3, max=255, message='Email(max 40 chars)')])
    roll= IntegerField(label='StaffNo', validators = [Required()] ) #, validators= [Length(min=3, max=55, message='Staff number')])
    supervisor= TextField(label='Group', validators= [Length(min=1, max=255, message='Group')])
    location= TextField(label='Location', validators= [Length(min=1, max=255, message='Location')])
    facility1= SelectField(choices=[('None', 'None'), ('Other', 'Other'), ('Ash', 'Ash'), ('AWB', 'AWB'), ('MacRH', 'MacRH'), ('WGH', 'WGH'), ('Evans', 'Evans'),
                                   ('LF1', 'LF1'), ('LF2', 'LF2'), ('HRB', 'HRB'), ('CSQ', 'CSQ'), ('SCRM', 'SCRM'), ('1GSQ','1GSQ'), ('Teviot', 'Teviot')  ])   
    facility2= SelectField(choices=[('None', 'None'), ('Other', 'Other'), ('Ash', 'Ash'), ('AWB', 'AWB'), ('MacRH', 'MacRH'), ('WGH', 'WGH'), ('Evans', 'Evans'),
                                    ('LF1', 'LF1'), ('LF2', 'LF2'), ('HRB', 'HRB'), ('CSQ', 'CSQ'), ('SCRM', 'SCRM'), ('1GSQ','1GSQ'), ('Teviot', 'Teviot')  ])   
    active_status= SelectField(choices=[('Yes', 'Yes'), ('No', 'No'), ('-', '-') ])
    restrictions= SelectField(choices=[('Yes', 'Yes'), ('No', 'No'), ('-', '-') ], default='No')
    skin= SelectField(choices=[('Yes', 'Yes'), ('No', 'No'), ('-', '-') ], default='No')
    lung= SelectField(choices=[('Yes', 'Yes'), ('No', 'No'), ('-', '-') ], default='No')
    facefit= SelectField(choices=[('Yes', 'Yes'), ('No', 'No'), ('-', '-') ], default='No')
    comment= TextAreaField()
    
    
class AddTestsForm (Form):
    date=  TextField(label='Group', validators= [Length(min=1, max=55, message='Date')])#'DatePicker', format='%Y-%m-%d')
    result= SelectField(choices=[('-','-'),('Fit 3', 'Fit 3'), ('Fit 6', 'Fit 6'), ('Fit 12', 'Fit 12'), ('Not Fit', 'Not Fit'), ('Exit', 'Exit'), ('Pending', 'Pending') ])

class GetClinicDateForm (Form):
    date=  TextField(label='Group', validators= [Length(min=1, max=55, message='Date')])#'DatePicker', format='%Y-%m-%d')
    
class NewAdminForm (Form):
    AdminUUN= TextField(label='UUN', validators= [Length(min=3, max=20, message='Please enter new admin UUN (max 20 chars)')])

    
class FiltersForm (Form):
    #lf1,lf2.hrb,csq,scrm,n/a, ash, awb, macrh, wgh, evans
    sel_facility= SelectField(choices=[('All', 'All'),('None', 'None'), ('Other', 'Other'), ('Ash', 'Ash'), ('AWB', 'AWB'), ('MacRH', 'MacRH'), ('WGH', 'WGH'), ('Evans', 'Evans'),
                                   ('LF1', 'LF1'), ('LF2', 'LF2'), ('HRB', 'HRB'), ('CSQ', 'CSQ'), ('SCRM', 'SCRM'), ('1GSQ','1GSQ'), ('Teviot', 'Teviot')  ], default='All')  

    sel_status= SelectField(choices=[('All','All'),('Yes', 'Active'), ('No', 'Not Active') ])
    list_order= SelectField(choices=[('Last name','Last name'),('Retest date', 'Retest date') ])
    #sel_facility= RadioField('Facility', choices= [
        #('1','All  '),
        #('2','LF1  '),
        #('3','LF2  '),
        #('4','HRB  '),
        #('5','CSQ  '),
        #('6','ASH  '),
        #('7','AWB  '),
        #('8','MACRH'),
        #('9','WGH  '),
        #('10','EVANS'),
    #] )
    #sel_status= RadioField('Facility', choices= [
        #('1','Active'),
        #('2','Not Active'),
    #] )
    
