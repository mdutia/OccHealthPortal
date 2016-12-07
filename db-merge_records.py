from app import db, Admin, Userdata, Test


#F= 'admins.csv'
#with open (F) as f:
    #classlist= f.readlines() # should only be one line, but can cope with more
#for line in classlist:
    #lin= line.strip().split(',')
    #for u in lin:
        #a=Admin()
        #a.username=u
        #db.session.add (a)
#db.session.commit()

#F= 'OccHealthRecords.csv'
F= 'Chancellors OCU fit-unfit 2015.csv'

with open (F) as f:
    classlist= f.readlines() 
for line in classlist[2:]:  #note two header lines...!
    lin= line.strip().split(',')
    u= Userdata()
    #u.title, u.firstname, u.lastname, u.roll, u.position, u.supervisor, u.location, \
    #u.facility, u.active_status, u.skin, u.lung, u.facefit, u.comment = lin
    #u.tests=''
    #to import modified HRB users file, Sept 2015
    u.firstname, u.lastname, u.email, u.supervisor, u.location, u.facility1, \
    u.facility2, u.active_status, testdate, result, \
    u.skin, u.lung, u.facefit, u.restrictions =lin

    u.position=''
    u.roll=''
    if result<>'':
        u.tests=  '' #testdate+','+result+';'
        u.last_test= testdate+','+result

    print u.firstname, u.lastname, u.facility1, u.facility2
    db.session.add (u)
db.session.commit()

pass
                

print "Done."