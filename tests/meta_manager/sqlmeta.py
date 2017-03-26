# -*- coding: utf-8 -*-
import sqlite3
import os

sql_create_meta = '''
-- Tables
CREATE TABLE IF NOT EXISTS tbl (
id INTEGER PRIMARY KEY,
tblname TEXT NOT NULL UNIQUE, -- Table name
title TEXT NOT NULL UNIQUE, -- table title
titlep TEXT NOT NULL UNIQUE, -- table title plural
reprsql TEXT NOT NULL, -- sql to represent table
about TEXT);
-- Fields of tables
CREATE TABLE IF NOT EXISTS fld (
id INTEGER PRIMARY KEY,
tbl_id INTEGER NOT NULL REFERENCES tbl(id) ,
fldname TEXT NOT NULL UNIQUE,
lbl TEXT NOT NULL UNIQUE,
lblp TEXT NOT NULL UNIQUE,
sqltype TEXT NOT NULL, --INTEGER, TEXT, NUMERIC, DATE ...
qt TEXT NOT NULL,  --qt widget to use
status INTEGER DEFAULT (1), -- 0: NULL, 1: NOT NULL, 2: UNIQUE, 3: UNIQUE Table
max_size INTEGER DEFAULT (0) --If 0 no limit at all
);
'''


def make_new_db(dbpath, sql=sql_create_meta):
    '''
    sql   : A set of sql commands (create, insert or update)
    '''
    if not sql:
        return False

    if os.path.exists(dbpath):
        return False

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

