
# pip install tinydb
from tinydb import TinyDB, Query
db = TinyDB('db.json')
terg = db.table('erg')
terg.all()
for el in terg.all():
    print("%s %s" % (el['epo'], el['ono']))
    
