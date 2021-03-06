from flask import render_template, redirect, session, url_for, g, request, make_response #, send_from_directory, current_app
from flask.ext.login import login_user , logout_user , current_user , login_required
from wtforms import widgets, SelectMultipleField

from app import app
from forms import NewUserForm, AddTestsForm, NewAdminForm, EditUserForm, LoginForm, FiltersForm, GetClinicDateForm
from sqlalchemy import or_, and_

#from flask_mail import Message
#from app import mail    

import os, sys
from config import HOST, ADMINS


def get_filtered_recs (paginate=True):
    from app import db, Admin, Userdata
    #recs = Userdata.query.order_by(Userdata.lastname)
    if session['list_order']=='Last name':
        listby=Userdata.lastname
    else:
        listby=Userdata.days_to_expiry
    
    if session['facility']=='All':
        recs= Userdata.query.order_by(listby)
    else:
        recs = Userdata.query.filter( or_(Userdata.facility1==session['facility'],
                                      Userdata.facility2==session['facility']) ).order_by(listby)

    if session['status']!='All':
        recs= recs.filter (Userdata.active_status==session['status']).order_by(listby)
    if paginate:
        return recs.paginate (session['current_pg'], 20) # return Pagination object
    else:
        return recs  # return records, not Pagination object


@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    #from app import User
    if HOST!='EASE':  # working on either local or pythonanywhere. username=os.getenv("USERNAME") works only on localhost
        return redirect(url_for('fake_EASE_login'))
    else:
        username = request.environ.get('REMOTE_USER')
        session['this_user_name']= username
        return redirect(url_for('process_login'))

@app.route('/fake_EASE_login', methods = ['GET', 'POST'])
def fake_EASE_login():
    #from app import User
    ###
    session['this_user_name']='mdutia'
    return redirect(url_for('process_login'))
    ###
    form= LoginForm()
    if (request.method=='GET'):
        return render_template('fake_EASE_login.html', form=form)
    else:
        if not form.validate():
            return render_template('fake_EASE_login.html', form=form)
        else:
            username= form.uname.data
            session['this_user_name']= username
            return redirect(url_for('process_login'))

@app.route('/process_login', methods = ['GET', 'POST'])
def process_login():
    from app import db, Admin, Userdata
    try:
        username= session['this_user_name']  #this fails if not routed correctly, but is not 100% secure
    except:
        return redirect (url_for('login'))
    ad = Admin.query.filter_by(username=username).first()
    if ad is None:
        return redirect(url_for('unknown_admin'))
    login_user(ad)    
    session['Selected_User_Id']= 0
    session['facility']='All'
    session['status']='All'
    session['list_order']='Last name'
    session['current_pg']= 1
    selected_rec=0
    mode=''
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    td= datetime.date(datetime.today())
    recs= Userdata.query.order_by(Userdata.lastname)
    for rec in recs:
        try:
            d, r= rec.last_test.split(',')
            dtime= datetime.date(datetime.strptime(d, "%d/%m/%Y"))
        except:
            d, r= '-','-'
            rec.active_status= 'No'
        if ('Fit' in r):
            if ('6' in r):
                expirydate= dtime + relativedelta(months=6)
                diff= (expirydate - td).days  #days difference from today's date
            elif ('12' in r):
                expirydate= dtime + relativedelta(months=12)                    
                diff= (expirydate - td).days  #days difference from today's date
            else:
                expirydate= dtime + relativedelta(months=3)  #assume 3 month period for any others
                diff= (expirydate - td).days  #days difference from today's date
            expirydate= datetime.strftime(expirydate, "%d/%m/%Y")
        else:
            expirydate='-'
            diff= 0
        rec.days_to_expiry= diff
        rec.expiry_date= expirydate
        db.session.merge (rec)
    db.session.commit()
    return redirect(url_for('dashboard'))    

@app.route('/unknown_admin', methods = ['GET', 'POST'])
def unknown_admin():
    return render_template ('unknownuser.html', hostname= HOST)

@app.route('/finished', methods = ['GET', 'POST'])
@login_required
def finished():
    logout_user()
    return render_template ('finished.html')

@app.route('/SetVar', methods = ['GET', 'POST'])
@login_required
def SetVar():
    args=request.args
    try:
        if args['facility']:
            session['facility']= args['facility']
    except:
        pass
    try:
        if args['status']:
            session['status']= args['status']
    except:
        pass
    try:
        if args['list']:
            session['list_order']= args['list']
    except:
        pass
    session['current_pg']= 1                
    form=FiltersForm()
    recs= get_filtered_recs()
    #return render_template('show_recs.html', recs=recs, form=form) 
    return redirect (url_for('dashboard'))

@app.route('/dashboard', methods = ['GET', 'POST'])
@login_required
def dashboard():
    from app import db, Admin, Userdata
    from datetime import datetime  
    from dateutil.relativedelta import relativedelta
    
    ad=Admin.query.all()
    for a in ad:
        if a.username=='mmouse':
            db.session.delete(a)
            db.session.commit()

    recs= get_filtered_recs()
    
    if request.method=='GET':
        if 'mode' in request.args:
            if request.args['mode']=='Person':
                session['Selected_User_Id']= request.args['idd']#.id
                selected_rec=  Userdata.query.get(request.args['idd'])
                testhistory=[]
                for h in selected_rec.tests.split(';'):
                    testhistory.append( h )
                return render_template('show_one_rec.html', mode='Person', selected_rec=selected_rec, testhistory=testhistory)

            elif request.args['mode']=='Edit_Person':
                session['Selected_User_Id']= request.args['idd']#.id
                selected_rec=  Userdata.query.get(request.args['idd'])
                testhistory=[]
                for h in selected_rec.tests.split(';'):
                    testhistory.append( h )
                form= EditUserForm(obj= selected_rec)
                return render_template('show_one_rec.html', mode='Edit_Person', selected_rec=selected_rec, testhistory=testhistory, form=form)
            
            elif request.args['mode']=='Delete_Person':
                session['Selected_User_Id']= request.args['idd']#.id
                selected_rec=  Userdata.query.get(request.args['idd'])
                return render_template('delete_user.html', mode='Delete_Person', selected_rec=selected_rec)

            elif request.args['mode']=='Add_Test':
                session['Selected_User_Id']= request.args['idd']#.id
                selected_rec=  Userdata.query.get(request.args['idd'])
                form= AddTestsForm()
                testhistory=[]
                for h in selected_rec.tests.split(';'):
                    testhistory.append( h )
                return render_template('show_one_rec.html', mode='Add_Test', selected_rec=selected_rec, testhistory=testhistory, form=form)
            
            elif request.args['mode']=='prev_page':
                session['current_pg']-=1
                if session['current_pg']<=0:
                    session['current_pg']=1
                form=FiltersForm()
                recs= get_filtered_recs()
                return render_template('show_recs.html', recs=recs, form=form) 
                
            elif request.args['mode']=='next_page':
                session['current_pg']+=1
                form=FiltersForm()
                recs= get_filtered_recs()
                return render_template('show_recs.html', recs=recs, form=form) 
            

        else:
            form=FiltersForm()
            recs= get_filtered_recs()
            return render_template('show_recs.html', recs=recs, form=form) 
    
    else:  #POST
        args=request.args
        ad= Admin.query.all()
                         
        adUUN= []
        for a in ad:
            adUUN.append(a.username)
        form=NewAdminForm()
        
        if ('Manage' in request.form ['Button']):   #add authorised admins
            return render_template('get_new_admin.html', ad=ad, form=form, err=False) 
        
        elif ('Admin' in request.form ['Button']): 
            if (len(form.data['AdminUUN'])>=3) and not(form.data['AdminUUN'] in adUUN):
                aa=Admin()
                aa.username= form.data['AdminUUN']
                db.session.add(aa)
                db.session.commit()
            else:
                return render_template('get_new_admin.html', ad=ad, form=form, err=True)
            ad= Admin.query.all() #refresh the list of admins
            return render_template('get_new_admin.html', ad=ad, form=form, err=False)       
        
        elif ('Cancel' in request.form ['Button']):
            selected_rec=  Userdata.query.get(session['Selected_User_Id'])
            if selected_rec<>None:
                testhistory=[]
                for h in selected_rec.tests.split(';'):
                    testhistory.append( h )
                #mode='Person'
                return render_template('show_one_rec.html', mode='Person', selected_rec=selected_rec, testhistory=testhistory)
            else:
                session['Selected_User_Id']= ''
                form=FiltersForm()
                recs= get_filtered_recs()
                return render_template('show_recs.html', recs=recs, form=form) 
                
        
        elif (request.form ['Button']=='Save'):
            selected_rec= Userdata()
            merge=False
            if 'idd' in request.args:
                if request.args['idd']<>'':
                    session['Selected_User_Id']= request.args['idd']#.id
                    selected_rec=  Userdata.query.get(request.args['idd'])
                    if selected_rec<>None:
                        merge=True
            form= EditUserForm()
            form.errors['firstname']=False
            form.errors['lastname']=False
            if (len(form.data['firstname'])<2):
                form.errors['firstname']=True
            if (len(form.data['lastname'])<2):
                form.errors['lastname']=True
            if not(form.errors['firstname']) and not(form.errors['lastname']) :
                form.populate_obj (selected_rec)
                if merge==True:
                    db.session.merge(selected_rec)
                else:
                    db.session.add (selected_rec)
                db.session.commit()
                mode='Person'
                session['Selected_User_Id']= ''
                form=FiltersForm()
                recs= get_filtered_recs()
                return render_template('show_recs.html', recs=recs, form=form) 
            #if selected_rec<>None:
            else:
                testhistory=[]
                for h in selected_rec.tests.split(';'):
                    testhistory.append( h )
                #mode='Edit_Person'
                return render_template('show_one_rec.html', mode='Edit_Person', selected_rec=selected_rec, testhistory=testhistory)
        
        elif (request.form ['Button']=='Submit'):
            session['Selected_User_Id']= request.args['idd']#.id
            selected_rec=  Userdata.query.get(request.args['idd'])
            if selected_rec<>None:
                testhistory=[]
                for h in selected_rec.tests.split(';'):
                    testhistory.append( h )
            form= AddTestsForm()
            #mode='Add_Test'

            #check if valid date and result given by user
            form.errors ['Date_Error']=False
            dd=form.data['date']
            try:
                ddt= datetime.date(datetime.strptime(dd,'%d/%m/%Y') )
            except:
                form.errors ['Date_Error']= True
            form.errors ['Result_Error']=False
            if form.data['result']== '-':
                form.errors['Result_Error']= True
            if (form.errors['Date_Error']) or (form.errors['Result_Error']):
                return render_template('show_one_rec.html', mode='Add_Test', selected_rec=selected_rec, testhistory=testhistory, form=form)
            
            #check if the entered date is the first test result for this user
            if selected_rec.last_test=='-,-':
                selected_rec.last_test= form.data ['date'] +','+ form.data ['result']
            else:
                ldts= selected_rec.last_test.split(',')[0]
                ldt= datetime.date(datetime.strptime(ldts,'%d/%m/%Y') )
                if ddt == ldt:
                    #if the last test date has been entered again (change in current recall status)
                    #then replace the last test result. No record is kept of the previous result
                    selected_rec.last_test= form.data ['date'] +','+ form.data ['result']                    
                elif ddt > ldt:
                    #check if the entered date is more recent than rec.last_test
                    #if so, move rec.last_test to the rec.tests history list
                    selected_rec.tests+= ';'+ selected_rec.last_test
                    #put the entered test date and result in to last_test
                    selected_rec.last_test= form.data ['date'] +','+ form.data ['result']
                else:
                    #put the entered test date and result into the tests history
                    selected_rec.tests+= ';'+ form.data ['date'] +','+ form.data ['result']
                    if selected_rec.tests.startswith(';'):
                        selected_rec.tests=selected_rec.tests[1:] #get rid of initial ';' if necc
                    #revise the history list to descending order by date
                    hist=[]
                    tsts= selected_rec.tests.split(';')
                    for t in tsts:
                        dt, res= t.split(',')
                        hist.append ( (datetime.date(datetime.strptime(dt,'%d/%m/%Y')), res) )
                    hist.sort(reverse=True)
                    ss=''
                    for h in hist:
                        ss+= ';'+datetime.strftime(h[0], "%d/%m/%Y")+','+ h[1]
                    #remove leading ';' 
                    selected_rec.tests=ss[1:]
#update the expiry date info on the main db
            #from dateutil.relativedelta import relativedelta
            td= datetime.date(datetime.today())
            d, r= selected_rec.last_test.split(',')
            dtime= datetime.date(datetime.strptime(d, "%d/%m/%Y"))
            if ('Fit' in r):
                if ('6' in r):
                    expirydate= dtime + relativedelta(months=6)
                    diff= (expirydate - td).days  #days difference from today's date
                elif ('12' in r):
                    expirydate= dtime + relativedelta(months=12)                    
                    diff= (expirydate - td).days  #days difference from today's date
                else:
                    expirydate= dtime + relativedelta(months=3)  #assume 3 month period for any others
                    diff= (expirydate - td).days  #days difference from today's date
                expirydate= datetime.strftime(expirydate, "%d/%m/%Y")
            else:
                expirydate='-'
                diff= 0
            selected_rec.days_to_expiry= diff
            selected_rec.expiry_date= expirydate
#

            db.session.merge(selected_rec)
            db.session.commit()
            testhistory=[]
            for h in selected_rec.tests.split(';'):
                testhistory.append( h )
            #mode='Person'
            return render_template('show_one_rec.html', mode='Person', selected_rec=selected_rec, testhistory=testhistory)

        elif ('Confirm Delete' in request.form ['Button']):
            session['Selected_User_Id']= request.args['idd']#.id
            selected_rec=  Userdata.query.get(request.args['idd'])
            db.session.delete(selected_rec)
            db.session.commit()
            mode='Person'
            session['Selected_User_Id']= ''
            recs= get_filtered_recs()
            form=FiltersForm()
            return render_template('show_recs.html', recs=recs, form=form)

        elif ('Add New User' in request.form ['Button']):
            session['Selected_User_Id']= ''
            selected_rec=Userdata()
            testhistory=[]
            form= EditUserForm () #(obj= selected_rec)
            return render_template('show_one_rec.html', mode='Edit_Person', selected_rec=selected_rec, testhistory=testhistory, form=form)
        
        elif ('Download' in request.form ['Button']):
            recs= get_filtered_recs( paginate=False ) #get all records matching filters, not just one page
            msg=[]
            msg.append ('Occupatonal Health Records database')
            s= datetime.date(datetime.today())  #datetime.datetime.today().strftime('%d/%m/%Y %H:%M')
            msg.append ( ('Download {0}'.format (s)) )
            if session['status']=='Yes':
                status='Active users only'
            elif session['status']=='No':
                status='Inactive users only'
            elif session['status']=='All':
                status='All users'
            msg.append ('Filters: Facility={0}    Status={1}    Ordered by:{2}'.format (session['facility'], status, session['list_order']))
            msg.append(' ')
            msg.append('Name, Last test, Result, Retest due, Days left')
            for r in recs:
                lastdate, lastresult= r.last_test.split(',')
                if r.days_to_expiry<0:
                    dexp='Expired'
                else:
                    dexp=r.days_to_expiry
                msg.append ('{0} {1}, {2}, {3}, {4}, {5}'.format 
                            (r.firstname, r.lastname, lastdate,lastresult,r.expiry_date,dexp ))
            msgstr= '\n'.join(msg) 
            response = make_response(msgstr)
            response.headers["Content-Disposition"] = "attachment; filename=Status.csv"
            return response

        elif ('Organiser' in request.form ['Button']):
            form= GetClinicDateForm () #(obj= selected_rec)
            return render_template('get_clinic_date.html', form=form)

        elif ('Back' in request.form ['Button']):   
            recs= get_filtered_recs()
            form=FiltersForm()
            return render_template('show_recs.html', recs=recs, form=form) 
        
        
        elif ('Users List' in request.form ['Button']):            
            form= GetClinicDateForm () 
            form.errors ['Date_Error']=False
            dd=form.data['date']
            try:
                ddt= datetime.date(datetime.strptime(dd,'%d/%m/%Y') )
            except:
                form.errors ['Date_Error']= True
                return render_template('get_clinic_date.html', form=form)

            recs= get_filtered_recs( paginate=False ) #get all records matching filters, not just one page
            msg=[]
            msg.append ('Occupatonal Health Records')
            msg.append ( ('CLINIC DATE {0}'.format (ddt.strftime("%d/%m/%Y"))) )
            if session['status']=='Yes':
                status='Active users only'
            elif session['status']=='No':
                status='Inactive users only'
            elif session['status']=='All':
                status='All users'
            msg.append ('Filters: Facility={0}    Status={1}    Ordered by:{2}'.format (session['facility'], status, session['list_order']))
            msg.append(' ')
            s= datetime.date(datetime.today())  #datetime.datetime.today().strftime('%d/%m/%Y %H:%M')
            offset= (ddt - s).days   #days
            dExpired, d30, d60, d90, d90plus= [],[],[],[],[]
            for r in recs:
                ##lastdate, lastresult= r.last_test.split(',')
                if r.days_to_expiry<0+offset:
                    dExpired.append (r)
                elif r.days_to_expiry <=30+offset:
                    d30.append(r)
                elif r.days_to_expiry <=60+offset:
                    d60.append(r)
                elif r.days_to_expiry <=(90+offset):
                    d90.append(r)
                elif r.days_to_expiry >(90+offset):
                    d90plus.append(r)
                    
            msg.append(' ')
            msg.append('Name, Email, Expiry date')
            msg.append('Expiring within 30 days from {0}'.format(ddt.strftime("%d/%m/%Y")))
            if len(d30)>0:
                for r in d30:
                    msg.append ('{0} {1}, {2}, {3}'.format 
                                (r.firstname, r.lastname, r.email, r.expiry_date ))
            else:
                msg.append('None')
            msg.append(' ')
            msg.append('Expiring within 60 days from {0}'.format(ddt.strftime("%d/%m/%Y")))
            #msg.append('Firstname, Lastname, Email, Expiry date')
            if len(d60)>0:
                for r in d60:
                    msg.append ('{0} {1}, {2}, {3}'.format 
                                (r.firstname, r.lastname, r.email, r.expiry_date ))
            else:
                msg.append('None')
            msg.append(' ')
            msg.append('Expiring within 90 days from {0}'.format(ddt.strftime("%d/%m/%Y")))
            #msg.append('Firstname, Lastname, Email, Expiry date')
            if len(d90)>0:
                for r in d90:
                    msg.append ('{0} {1}, {2}, {3}'.format 
                                (r.firstname, r.lastname, r.email, r.expiry_date ))
            else:
                msg.append('None')

            msg.append(' ')
            msg.append('Users out of date on {0}'.format(ddt.strftime("%d/%m/%Y")))
            #msg.append('Firstname, Lastname, Email, Expiry date')
            if len(dExpired)>0:
                for r in dExpired:
                    msg.append ('{0} {1}, {2}, {3}'.format 
                                (r.firstname, r.lastname, r.email, r.expiry_date ))
            else:
                msg.append('None')

            msgstr= '\n'.join(msg) 
            response = make_response(msgstr)
            response.headers["Content-Disposition"] = "attachment; filename=Status.csv"
            return response
            


        
            

