
#OHRecords
#dump the admin and userdata records, suitable for migration using migrate_db.py
#prints to the console, need to copy+paste output to a ORHdump.txt file
#
#first line is a comma-separated list of admin UUNs
#then list of userdata record fields

from app import db, Admin, Userdata, Test

us= Userdata.query.all()
s= Admin.query.all()

for ad in s:
    print ad.username+',',
    
print

for u in us:
    print u.id
    for a in u.__dict__:
        #dump each field in u, except the _sa_instance_state value
        if not(a.startswith('_')):
            print a +':'+ str(u.__dict__[a])
    
pass
