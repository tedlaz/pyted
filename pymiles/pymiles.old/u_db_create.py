# -*- coding: utf-8 -*-
import sqlite3
from u_logger import log

sql_keyval = """
CREATE TABLE IF NOT EXISTS zk(key TEXT PRIMARY KEY, val TEXT NOT NULL);
INSERT INTO zk VALUES('app_key', '%s');
INSERT INTO zk VALUES('app_version', '%s');
CREATE TABLE IF NOT EXISTS z(
tname TEXT PRIMARY KEY,
title TEXT NOT NULL UNIQUE,
titlep TEXT NOT NULL UNIQUE,
rpr TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS zd(
fname TEXT PRIMARY KEY,
tname TEXT NOT NULL REFERENCES z(tname),
lbl TEXT NOT NULL UNIQUE,
lblp TEXT NOT NULL,
qt TEXT NOT NULL
);
"""


def create_table_sql(tabls, tabl):
    # tabls : A dictionary holding table dictionary values
    # tabl  : A Specific table dict to look
    sql = "CREATE TABLE IF NOT EXISTS %s (\n" % tabl
    sql += "id INTEGER PRIMARY KEY,\n"
    tbluq = ''
    for fld in tabls[tabl]["order"]:
        if fld == "id":
            continue
        typos = tabls[tabl]["fields"][fld].get("typ", 'TEXT')
        uniq = tabls[tabl]["fields"][fld].get("uq", 1)
        flduq = ''

        if uniq == 1:
            flduq = 'NOT NULL'
        elif uniq == 2:
            flduq = 'NOT NULL'
            tbluq += '%s, ' % fld
        elif uniq == 3:
            flduq = 'NOT NULL UNIQUE'

        sql += "%s %s %s,\n" % (fld, typos, flduq)
    if tbluq:
        sql += "UNIQUE (%s)\n);\n" % tbluq[:-2]
    else:
        sql = "%s\n);\n" % sql[:-2]
    return sql


def create_db(dbpath, tables, app_key, app_version):
    # Create the actual database
    # dbpath      : the database path
    # tables      : dictionary
    # app_key     : Application's specific key for identification
    # app_version : Application's version

    if not dbpath:
        log.error('create_db(): Path %s does not exist' % dbpath)
        return False

    # Create sql for all the tables
    sql = 'BEGIN TRANSACTION;\n'
    for tbl in tables.keys():
        sql += create_table_sql(tables, tbl)
    sql += sql_keyval % (app_key, app_version)
    sql += 'COMMIT;'

    log.debug('create_db(): sql created:\n%s' % sql)
    # Try to create tables in <dbpath> file
    try:
        con = sqlite3.connect(dbpath)
        cur = con.cursor()
        cur.executescript(sql)
        con.commit()
    except sqlite3.Error as sqe:
        log.error('create_db(): %s' % sqe)
        con.rollback()
        cur.close()
        con.close()
        return False
    cur.close()
    con.close()
    log.debug('create_db(): %s created succesfully!!!' % dbpath)
    return True
