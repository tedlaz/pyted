# -*- coding: utf-8 -*-
'''
Created on Nov 8, 2013

@author: tedlaz
'''

import sqlite3
import os
import num_txt_etc as nm
import model

zdb = None
debuging = False

def dprint(val):
    if debuging:
        print(val)
        
def executeScript(script,db):
    '''
    Generic sql script execution
    '''
    try:
        con = sqlite3.connect(db) 
        cur = con.cursor()
        cur.executescript(script)
        con.commit()

    except sqlite3.Error, e:
        if con:
            con.rollback()
        dprint("dbutils Line 33 Error : %s" % e.args[0])
    finally:
        cur.close()
        con.close()

sql_lg = '''
CREATE TABLE IF NOT EXISTS lg(
id INTEGER NOT NULL PRIMARY KEY,
ldt TEXT NOT NULL,  --Ημερομηνία - Ώρα (πχ 2013-01-31 20:30:15)
logp TEXT NOT NULL  --Σχόλια
);
'''
def addLogToDb(logText,dbfile=None):
    '''
    Create log records
    Must have table lg( id, datetime, text)
    '''
    datetime = nm.strDateTimeNow()
    if dbfile:
        commitToDb("INSERT INTO lg(ldt,logp) VALUES (?,?)",[datetime,logText],dbfile)

sql_lk = '''
CREATE TABLE IF NOT EXISTS lk(
id INTEGER NOT NULL PRIMARY KEY,
lkd DATE NOT NULL UNIQUE
);
'''        
def checkDate(strDate,db):
    '''
    Checks if closeDate exists
    if Yes 
        If closeDate >= strDate returns False
        else returns True
    if No
        returns True
    Requires lock table lk
    '''
    sql = "SELECT lkd FROM lk WHERE id=?"
    closeDate = getDbSingleVal(sql,(1,),db)
    if closeDate:
        if strDate <= closeDate:
            return False
        else:
            return True
    else:
        return True
    
def getDbSingleVal(sql,sqlp,db):
    if not os.path.exists(db):
        return None    
    try:
        con = sqlite3.connect(db) 
        cur = con.cursor()
        cur.execute(sql,sqlp) #sql with ? instead of %s 
        val = cur.fetchone()[0]
        cur.close()
        con.close()
    except sqlite3.Error, e:
        dprint("dbutils line 95 Error 39: %s" % e.args[0])
        dprint("dbutils line 96 sql:%s sqlp: %s db: %s" % (sql,sqlp,db))
        val = None
    except:
        val = None
    return val

def getDbOneRow(sql, db):
    if not os.path.exists(db):
        return None
    try:
        con = sqlite3.connect(db) 
        cur = con.cursor()
        cur.execute(sql)
        row = cur.fetchone()
    except sqlite3.Error, e:
        dprint("dbutils line 111 Error: %s" % e.args[0])
        row = []
    finally:
        cur.close()
        con.close()
    return row

def getDbRows(sql, db, colNames=True):
    if not os.path.exists(db):
        return [],[]
    columnNames = []
    
    try:
        con = sqlite3.connect(db) #,detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        cur.execute(sql)
        columnNames = [t[0] for t in cur.description]
        rws = cur.fetchall()
        cur.close()
        con.close()
        
    except sqlite3.Error, e:
        dprint("dbutils line 127 Error : %s" % e.args[0])
        rws = []
    if colNames:
        return rws, columnNames
    else:
        return rws
    
def printDbRows(sql,db):
    vals, lbls = getDbRows(sql,db)
    for el in lbls:
        print '%20s' % el,
    print ''
    for row in vals:
        for col in row:
            print '%20s' % col,
        print ''
              
def getDbRowsDict(sql,db):
    if not os.path.exists(db):
        return {}
    try:  
        con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql)
        rws = cur.fetchall()
        cur.close()
        con.close()
    except sqlite3.Error, e:
        dprint("dbutils line 145 Error : %s" % e.args[0])
        rws = {}
    return rws 
           
def commitToDb(sql,db,sqlp=None): #For insert or Update records
    try:
        con = sqlite3.connect(db) 
        cur = con.cursor()
        if sqlp:
            cur.execute(sql,sqlp) #sql with ? instead of %s
        else:
            cur.execute(sql)
        last_id = cur.lastrowid
        con.commit()
    except sqlite3.Error, e:
        if con:
            con.rollback()
        dprint("dbutils line 148 Error 93: %s" % e.args[0])
        dprint("dbutils line 149 sql: %s sqlp: %s" % (sql, sqlp))
        last_id = None
    finally:        
        cur.close()
        con.close()
    return last_id

def getLabels(fldArr):
    '''
    Requires master DB with zfield table
    '''
    labels =[]
    for el in fldArr:
        labels.append(getLabel(el))
    return labels

def getLabel(fld):
    sql = "SELECT flp FROM zfld WHERE fln='%s'"
    v = getDbOneRow(sql % fld,zdb)
    if v:
        return v[0]
    else:
        return fld
    
def parseDDL(table,db):
    fields = getDbRows('pragma table_info(%s)' % table,db,False)
    finalArray=[]
    for fld in fields:
        cname = fld[1]
        tempTyp = fld[2].lower()
        if   tempTyp     == 'integer': ctype = 'int'
        elif tempTyp[:7] == 'varchar': ctype = 'txt'
        elif tempTyp[:4] == 'text'   : ctype = 'txt'
        elif tempTyp[:4] == 'date'   : ctype = 'dat'
        elif tempTyp[:7] == 'decimal': ctype = 'dec'
        elif tempTyp[:4] == 'bool'   : ctype = 'boo'
        else: ctype = 'txt'
        if fld[3] == '1': requi = True
        else: requi = False

        lbl = valFromTableOrDefault(cname,"SELECT flp FROM zfld WHERE fln=?",zdb)
        
        if '_id' in cname:
            ctype = 'key'
            fromzdb = getDbSingleVal("SELECT sq1 FROM fkey WHERE fln=?",(cname,),zdb)
            if fromzdb:
                sqlInsert = fromzdb
            else:
                sqlInsert = "SELECT * FROM %s" % cname[:-3]
            finalArray.append({'cname':cname,'ctype':ctype,'requi':requi,'lbl':lbl,'sqin':sqlInsert})
        else:    
            finalArray.append({'cname':cname,'ctype':ctype,'requi':requi,'lbl':lbl})
    return finalArray

def valFromTableOrDefault(defVal,sql,db):
    '''
    If find value from table returns thata value
    else returns default value
    '''
    val = getDbSingleVal(sql,(defVal,),db)
    if val:
        return val
    else:
        return defVal
    
def isTableOrView(tvname,db):
    sql = "SELECT count() FROM sqlite_master WHERE name = '%s'" % tvname
    a = getDbOneRow(sql,db)[0]
    if a == 1:
        return True
    else:
        return False
    
def fillTemplateFromDb(tmpl,sql,db):
    rows = getDbRowsDict(sql,db)
    finalstr = u''
    f ={}
    #Here we make specific field format
    for row in rows:
        keys = row.keys()
        for key in keys:
            if key[0] == 'n': #is numeric and we format it in a special way (Greek number format)
                f[key]= nm.strGrDec(row[key])
            else:
                f[key] = row[key]
    for row in rows:
        finalstr += tmpl.format(**f)
    return finalstr

def getTblOrView(tblOrViewName,db):
    fsql = model.tblFlds(tblOrViewName)
    return (tblOrViewName,tblOrViewName,fsql)

def tst():
    sql = "PRAGMA table_info(erp)"
    printDbRows('SELECT * FROM zlbl','tst.sql3')
            
if __name__ == '__main__':
    tst()
