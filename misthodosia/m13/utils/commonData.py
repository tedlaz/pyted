# -*- coding: utf-8 -*-
'''
Created on 1 Φεβ 2013

@author: tedlaz
'''
import dbutils

def coText(db):
    '''
    Returns text with Company Name , etc ...
    '''
    sql = "SELECT cop || ' ' || ono FROM m12_co WHERE id=1"
    coname = dbutils.getDbSingleVal(sql, db)
    if coname:
        return "%s" % coname.strip()
    else:
        return "Εταιρία χωρίς δεδομένα"
    
def getHeaderAndRows(head,sql,db):
    arr = dbutils.getDbRows(sql, db) 
    return head, arr

def textPrint(head,arr):
    txt = ''
    for l in head:
        txt += '%15s ' % l
    txt += '\n'
    for lin in arr:
        for col in lin:
            txt += '%15s ' % col
        txt += '\n'
    return txt

if __name__ == '__main__':
    db = 'C:/ted/mis.sql3'
    sql  = "SELECT m12_fpr.id, epon, onom,patr,mitr,sexp, igen,afm,amka,aika,pol,odo,num,tk FROM m12_fpr INNER JOIN m12_sex ON m12_sex.id=m12_fpr.sex_id"
    head = ['id',u'Επώνυμο',u'Όνομα',u'Πατρώνυμο',u'Μητρώνυμο',u'Φύλο',u'Ημ.Γέννησης',u'ΑΦΜ',u'ΑΜΚΑ',u'Α.Μ.ΙΚΑ',u'Πόλη',u'Οδός',u'Αριθμός',u'Τ.Κ.']
    print coText(db)
    a,b = getHeaderAndRows(head,sql,db)
    print textPrint(a,b)