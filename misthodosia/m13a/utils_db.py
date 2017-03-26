# -*- coding: utf-8 -*-
'''
Created on 18 Δεκ 2012

@author: tedlaz
'''
import sqlite3

def getDbRows(sql, db):
    try:
        con = sqlite3.connect(db) 
        cur = con.cursor()
        cur.execute(sql)
        rws = cur.fetchall()
    except sqlite3.Error, e:
        print "Error : %s" % e.args[0]
        rws = [[]]
    finally:
        cur.close()
        con.close()
    return rws

def getDbRowsCounted(sql, db):
    try:
        con = sqlite3.connect(db) 
        cur = con.cursor()
        cur.execute(sql)
        rws = cur.fetchall()
    except sqlite3.Error, e:
        print "Error : %s" % e.args[0]
        rws = [[]]
    finally:
        cur.close()
        con.close()
    i = 1
    finalArr = []
    for lin in rws:
        alist = list(lin)
        alist.insert(0,i)
        finalArr.append(alist)
        i += 1
    return finalArr

def getDbRowsByFldName(sql, db):
    try:
        con = sqlite3.connect(db)
        con.row_factory =  sqlite3.Row
        cur = con.cursor()
        cur.execute(sql)
        rws = cur.fetchall()
    except sqlite3.Error, e:
        print "Error : %s" % e.args[0]
        rws = [[]]
    finally:
        cur.close()
        con.close()
    return rws

def getHeadersRows(sql, db):
    try:
        con = sqlite3.connect(db)
        con.row_factory =  sqlite3.Row
        cur = con.cursor()
        cur.execute(sql)
        rws = cur.fetchall()
    except sqlite3.Error, e:
        print "Error : %s" % e.args[0]
        rws = [[]]
    finally:
        cur.close()
        con.close()
    if not rws:
        return [],[[]]
    
    keys = rws[0].keys()
    headers = []
    for key in keys:
        headers.append(getLabelFromField(key,db))
    return headers, rws 

def getDbOneRow(sql, db):
    try:
        con = sqlite3.connect(db) 
        cur = con.cursor()
        cur.execute(sql)
        row = cur.fetchone()
    except sqlite3.Error, e:
        print "Error : %s" % e.args[0]
        row = []
    finally:
        cur.close()
        con.close()
    return row

def getDbSingleVal(sql, db):
    try:
        con = sqlite3.connect(db) 
        cur = con.cursor()
        cur.execute(sql)
        val = cur.fetchone()
        if val:
            val = val[0]
    except sqlite3.Error, e:
        print "Error : %s" % e.args[0]
        val = None
    finally:
        cur.close()
        con.close()
    return val

def commitToDb(sql,db): #For insert or Update records
    try:
        con = sqlite3.connect(db) 
        cur = con.cursor()
        cur.execute(sql)
        last_id = cur.lastrowid
        con.commit()
    except sqlite3.Error, e:
        if con:
            con.rollback()
        print "Error : %s" % e.args[0]
        last_id = None
    finally:        
        cur.close()
        con.close()
    return last_id

def executeScript(script,db):
    
    try:
        con = sqlite3.connect(db) 
        cur = con.cursor()
        cur.executescript(script)
        con.commit()
    except sqlite3.Error, e:
        if con:
            con.rollback()
        print "Error : %s" % e.args[0]
    finally:
        cur.close()
        con.close()
                 
class dbUtils(): # Class for testing purposes
    def __init__(self,db):
        self.db = db
    def DbRows(self,sql):
        return getDbRows(sql,self.db)

def dumpToFile(filename,db):
    con = sqlite3.connect(db)
    with open(filename, 'w') as f:
        for line in con.iterdump():
            txtLine = u'%s\n' % line
            f.write(txtLine.encode('utf-8'))
    return True

def parseDDL(table,db):
    sqla = "select sql from sqlite_master where type='table' AND tbl_name='%s'" % table
    sql = getDbSingleVal(sqla,db)
    for i in range(len(sql)):
        if sql[i] == '(':
            arr = sql[i+1:].split(',')
            break 
    farr = []
    for el in arr:
        farr.append(el.replace('\n','').strip().split(' '))
        el = 'ted'
    #print farr
    finalArray = [] 
    for line in farr:
        if line[0] == 'UNIQUE':
            break
        
        colname = line[0].replace('"','')
        #print line[1]
        if   line[1]     == 'integer': typ = 'int'
        elif line[1][:7] == 'varchar': typ = 'txt'
        elif line[1][:4] == 'text'   : typ = 'txt' 
        elif line[1][:4] == 'date'   : typ = 'dat'
        elif line[1][:7] == 'decimal': typ = 'dec'
        elif line[1][:4] == 'bool'   : typ = 'boo'
        else: typ = 'error'
        if '_id' in colname:
            typ = 'key' 
        if 'NOT' in line:
            required = True
        else:
            required = False
        finalArray.append({'cname':colname, 'ctype':typ, 'requi':required})
    return  finalArray

def checkDDL(db):
    sql = "select tbl_name, sql from sqlite_master where type='table'  AND tbl_name LIKE 'm12_%' ORDER BY  tbl_name"
    tablesql = getDbRows(sql,db)
    arr = []
    for el in  tablesql:
        row = parseDDL(el[0],db)  
        for col in row:
            arr.append('%s-%s' % (col['cname'],el[0]))
    arr.sort()
    st = "l['%s'] = u''\n"
    sfinal = ''
    for el in arr:
        sfinal += st % el
    print len(arr)
    return sfinal

def getLabelFromField(field,db):
    sql = "SELECT fldlbl FROM z_dbfld WHERE fldnam='%s'" % field
    return getDbSingleVal(sql,db)

def test_getDbRowsByFldName(sql,db,pars=None):
    if pars:
        sql = sql % pars
    res = getDbRowsByFldName(sql,db)
    if res:
        keys = res[0].keys()
        lbls = {}
        for key in keys:
            lbls[key] = getLabelFromField(key,db)
    for el in res:
        for key in keys:
            print '%s : %s' % (lbls[key],el[key]),
        print ''
if __name__ == '__main__':
    sql = "SELECT * FROM m12_fpr"
    db = 'c:/ted/testing.m13'
    test_getDbRowsByFldName(sql,db)
    #print checkDDL('c:/ted/mis.sql3')

    