# -*- coding: utf-8 -*-
'''
Functions for Database (sqlite) access
Programmer : Ted Lazaros (tedlaz@gmail.com)

All functions return 1 for normal execution or 0 for error
'''

import sqlite3
import os

#status VALUES
DB_ERROR, NULL_VAL, ONE_VAL, MANY_VAL = range(4)
       
def dbScript(script,db):
    '''
    Generic sql script execution
    input
        script : one or many sql expressions divided by ;
        db  : database name
    output:
        1 if no error , 0 if error
        text message
    '''
    #if not os.path.exists(db):
    #    return DB_ERROR, 'dbScript : Path %s not exists' % db
    if not script:
        return DB_ERROR, 'dbScript : script is empty'
    
    status = NULL_VAL
    msg = 'dbScript : Everything executed Fine !!'
    
    try:
        con = sqlite3.connect(db) 
        cur = con.cursor()
        cur.executescript(script)
        con.commit()

    except sqlite3.Error, e:
        if con:
            con.rollback()
        status = DB_ERROR
        msg = e
    finally:
        cur.close()
        con.close()
    return status, msg
    
def dbRows(sql, db, limit=None):
    """
    input
        sql : sql code to run
        db  : database name
    output:
        1.Array of dbrows
        2.Array of fieldNames
        3.execution status : 
            DB_ERROR (0) for error 
            NULL_VAL (1) for success but empty recordset 
            ONE_VAL  (2) for only one row
            MANY_VAL (3) for more than one row
        4.text message
    """
    if not os.path.exists(db):
        return [],[], 0, 'Path %s not exists' % db
    if not sql:
        return [],[], 0, 'sql is empty'
       
    status = None
    msg = 'dbRows : Something terrible happened !!'
            
    columnNames = []

    if limit:
        sql += ' limit(%s)' % limit
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(sql)
        columnNames = [t[0] for t in cur.description]
        rws = cur.fetchall()
        cur.close()
        con.close()
        rowNum = len(rws)
        if rowNum == 0:
            status = NULL_VAL
            msg = 'dbRows: Success , But no records'
        elif rowNum == 1:
            status = ONE_VAL
            msg = 'dbRows: Success , Only One record'
        else:
            status = MANY_VAL
            msg = 'dbRows: Success , More than one record'
             
    except sqlite3.Error, e:
        rws = []
        status = DB_ERROR
        msg = 'dbRows : %s' % e
        
    return rws, columnNames, status, msg
               
def dbCommit(sql,db,params=None): #For insert or Update records
    """
    input
        sql : sql code to run
        db  : database name
        params : parameters
    output:
        last inserted id or 0 (error)
        text message
    """
    last_id = None
    msg = 'dbCommit : Something bad happened !!'
    
    if not os.path.exists(db):
        return DB_ERROR, 'dbCommit : Path %s not exists' % db
    if not sql:
        return DB_ERROR, 'dbCommit : sql is empty'
    
    try:
        con = sqlite3.connect(db) 
        cur = con.cursor()
        if params:
            cur.execute(sql,params) #sql with ? instead of %s
        else:
            cur.execute(sql)
        last_id = cur.lastrowid
        if not last_id:
            last_id = -1
            msg = 'dbCommit : Record updated !!!'
        else:
            msg = 'dbCommit : Record saved with id=%s' % last_id
        con.commit()
    except sqlite3.Error, e:
        if con:
            con.rollback()
        last_id = DB_ERROR
        msg = 'dbCommit : %s' % e 
    finally:        
        cur.close()
        con.close()
    return last_id, msg

def tst():
    db = 'test.tst'
    sqla = "CREATE TABLE IF NOT EXISTS tst(id INTEGER PRIMARY KEY, sname TEXT); INSERT INTO tst(sname) VALUES ('teddy');"
    print(dbScript(sqla, db))
    
    sqlc = "INSERT INTO tst(sname) VALUES ('popi')"
    print(dbCommit(sqlc,db))
    
    sql1 = "SELECT * FROM tst"
    print(dbRows(sql1, db))

    sqlf = "DROP TABLE tst"
    print(dbScript(sqlf, db))
    os.remove(db)
    
if __name__ == '__main__':
    tst()
