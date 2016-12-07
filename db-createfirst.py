from app import db, Admin, Userdata, Test

db.drop_all()
db.create_all()

F= 'admins.csv'
with open (F) as f:
    classlist= f.readlines() # should only be one line, but can cope with more
for line in classlist:
    lin= line.strip().split(',')
    for u in lin:
        a=Admin()
        a.username=u
        db.session.add (a)
db.session.commit()

F= 'OccHealthRecords.csv'
with open (F) as f:
    classlist= f.readlines() 
for line in classlist[1:]:
    lin= line.strip().split(',')
    #title, firstname, lastname, roll, position, supervisor, location, \
    #facility, active_status, skin, lung, facefit, comment = lin       
    u= Userdata()
    #u.title, u.firstname, u.lastname, u.roll, u.position, u.supervisor, u.location, \
    #u.facility, u.active_status, u.skin, u.lung, u.facefit, u.comment = lin
    #u.tests=''
    #to import modified HRB users file, Sept 2015
    u.lastname, u.firstname, u.supervisor, u.position, u.location, \
    testdate, result, u.comment, email, dummy1, dummy2, dummy3 =lin
    #u.facility, u.active_status, u.skin, u.lung, u.facefit, u.comment = lin
    u.facility1='HRB'
    u.roll=''
    if result<>'':
        u.tests= '' #testdate+','+result+';'
        u.last_test= testdate+','+result
    if 'yes' in dummy3:
        u.active_status='Yes'
    else:
        u.active_status='No'
    u.facefit='No'
    u.skin='No'
    u.lung='No'
    u.restrictions='No'
    db.session.add (u)
db.session.commit()

pass
                

print "Done."