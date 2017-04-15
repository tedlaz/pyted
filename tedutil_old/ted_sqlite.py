# -*- coding: utf-8 -*-
import sqlite3
import os
import sys
import json
from tedutil_old import ted_util as tsq

pyver = sys.version_info.major


def txtEncoded(atxt):
    if pyver == 3:
        return atxt
    else:
        return atxt.encode('utf-8')


class sumjson():
    '''
    class to create custom aggregate for sqlite3
    '''

    def __init__(self):
        self.count = {}

    def step(self, value):
        a = json.loads(value)
        for key in a.keys():
            try:
                self.count[key] = self.count.get(key, 0) + a[key]
            except:
                pass

    def finalize(self):
        return json.dumps(self.count)


def p0(js, par):
    '''
    js: json object
    par: js key
    default: if key not exists return 0
    '''
    return json.loads(js).get(par, 0)


def p1(js, par):
    '''
    js: json object
    par: js key
    default: if key not exists return empty space
    '''
    return json.loads(js).get(par, '')


def jd(adic):
    '''
    create json object from dictionary adic
    '''
    assert type(adic) is dict
    return json.dumps(adic)


def select(dbpath, sql):
    """
    dbpath: sqlite file full path
    sql: sql like SELECT ...
    """
    assert os.path.exists(dbpath)
    assert sql[:6].upper() == 'SELECT'
    con = sqlite3.connect(dbpath)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows


def select_with_functions(dbpath, sql):
    '''
    dbpath: sqlite file full path
    sql: sql like SELECT ...
    '''
    assert os.path.exists(dbpath)
    assert sql[:6].upper() == 'SELECT'
    con = sqlite3.connect(dbpath)
    con.create_function("grup", 1, tsq.grupper)
    con.create_function("nul2z", 1, tsq.nul2zero)
    con.create_function('p0', 2, p0)
    con.create_function('p1', 2, p1)
    con.create_aggregate("sumjs", 1, sumjson)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows


def select_field_names(dbpath, sql):
    '''
    '''
    assert os.path.exists(dbpath)
    assert sql[:6].upper() == 'SELECT'
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    cur.execute(sql)
    columnNames = [t[0] for t in cur.description]
    cur.close()
    con.close()
    return columnNames


def script(dbpath, sql):
    '''
    execute sql script on existing sqlite file (dbpath)
    '''
    assert os.path.exists(dbpath)
    try:
        con = sqlite3.connect(dbpath)
        cur = con.cursor()
        cur.executescript(sql)
        con.commit()
    except sqlite3.Error:
        con.rollback()
        cur.close()
        con.close()
        return False
    cur.close()
    con.close()
    return True


def script_on_new_db(dbpath, sql):
    '''
    create a New sqlite database by running sql
    '''
    assert not os.path.exists(dbpath)
    try:
        con = sqlite3.connect(dbpath)
        cur = con.cursor()
        cur.executescript(sql)
        con.commit()
    except sqlite3.Error:
        con.rollback()
        cur.close()
        con.close()
        return False
    cur.close()
    con.close()
    return True


def insert(dbpath, sql):
    '''
    Insert a record
    '''
    # pre conditions
    assert os.path.exists(dbpath)
    assert sql[:6].upper() == 'INSERT'
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    cur.execute(sql)
    insert_id = cur.lastrowid
    con.commit()
    cur.close()
    con.close()
    # post conditions
    assert insert_id > 0
    return insert_id


def insertp(dbpath, sql, pars):
    '''
    insert a record
    dbpath: db file
    sql: sql with parameters ? (insert into test values (?, ?, ?, ?, ?))
    cur.execute(sqle, ('2015', '01', '01', 'ted', jd(a1)))
    pars: list of parameters (par1, par2 , ...)
    '''
    # pre conditions
    assert os.path.exists(dbpath)
    assert sql[:6].upper() == 'INSERT'
    assert sql.count('?') == len(pars)
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    cur.execute(sql, pars)
    insert_id = cur. lastrowid
    con.commit()
    cur.close()
    con.close()
    # post conditions
    assert insert_id > 0
    return insert_id


def backup(dbpath, sqlfile=None):
    '''
    Create a database backup as sql creates, inserts
    '''
    assert os.path.exists(dbpath)
    if not sqlfile:
        sqlfile = '%s.sql' % dbpath
    con = sqlite3.connect(dbpath)
    with open(sqlfile, 'w') as f:
        for line in con.iterdump():
            f.write('%s\n' % txtEncoded(line))
    con.close()
