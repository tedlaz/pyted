# -*- coding: utf-8 -*-
'''
Created on 21 Ιαν 2014

@author: tedlaz
'''
import sqlite3


class wdays(object):
    def __init__(self, arr):
        evtxt = "self.dar = %s" % arr
        exec(evtxt) # [0,0,0,0,0,0,0]
        self.days= [u'Δευτέρα',u'Τρίτη',u'Τετάρτη',u'Πέμπτη',u'Παρασκευή',u'Σάββατο',u'Κυριακή']
        
    def __repr__(self):
        trep = u''
        for i,el in enumerate(self.dar):
            if el:
                trep += '%s,' % self.days[i]
        return trep[:-1]
    
def adapt_wd(wday):
    return '%s' % wday.dar
sqlite3.register_adapter(wdays, adapt_wd)

def convert_wd(s):
    return wdays(s)
sqlite3.register_converter("wdays", convert_wd)

a =wdays('[1,0,0,0,1,0,1]')

#########################
# 1) Using declared types
con = sqlite3.connect("tst.sql3", detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()
#cur.execute("create table test(wd wdays)")

#cur.execute("insert into test(wd) values (?)", (a,))
con.commit()
cur.execute("select id, imer from erp")
f = cur.fetchone()
print f
cur.close()
con.close()
