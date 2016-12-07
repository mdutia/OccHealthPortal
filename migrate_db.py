
DUMMY_RUN=False

from app import db, Admin, Userdata, Test

if not DUMMY_RUN:
    db.drop_all()
    db.create_all()

#now migrate and update userdata
F= 'OHRdump.txt'
with open (F) as f:
    classlist= f.readlines()

#recreate admins - first line is a comma-separated list of admin UUNs
lin= classlist[0].strip().split(',')
for u in lin[:-1]:  #ignore the final empty field, after the last comma
    a=Admin()
    a.username=u
    db.session.add (a)
    print a
if not DUMMY_RUN:
    db.session.commit()

d={}
for line in classlist[2:]:  # start with the third line, i.e ignore the id (1) of the first userdata record
    try:
        k,v= line.strip('\n').split(':')
        d[k]=v
        #print k,v
    except: #if only one value on the line, means end of that record
        if d=={}: #d should contain all the fields for one record, not be empty
            print "Error - Empty record found"
            sys.exit()
        print
        #fill a new user record with the items in d
        u= Userdata()
        for k in d.keys():
            if k != 'id':
                u.__setattr__(k, d[k])
                #print d[k],
        #u should now have all the field values copied over from the dumped record
        #Add any new records to u here:
        if u.facility2=='':
            u.facility2='None'
        print u.firstname, u.lastname, u.facility1, u.facility2
        db.session.add (u)

if not DUMMY_RUN:
    db.session.commit()

print "Done."
        
pass



pass
