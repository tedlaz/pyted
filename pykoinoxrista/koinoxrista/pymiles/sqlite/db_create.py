# -*- coding: utf-8 -*-
import os
import sqlite3
from pymiles.utils.logger import log
from pymiles.sqlite import db_select as udbs

ddl = """BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS zfld (
    id INTEGER PRIMARY KEY,
    fld TEXT NOT NULL UNIQUE,
    flbl TEXT NOT NULL,
    zftyp_id INTEGER REFERENCES zftyp(id),
    nonull INTEGER NOT NULL,
    max INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS zftyp (
    id INTEGER PRIMARY KEY,
    ftyp TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS zt (
    id INTEGER PRIMARY KEY,
    tbl TEXT NOT NULL UNIQUE,
    zttyp_id INTEGER REFERENCES zttyp(id),
    tlbl TEXT NOT NULL UNIQUE,
    tlblp TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS zt_d (
    id INTEGER PRIMARY KEY,
    zt_id INTEGER NOT NULL REFERENCES zt(id),
    zfld_id INTEGER NOT NULL REFERENCES zfld(id),
    uniq YESNO NOT NULL,
    tuniq YESNO NOT NULL,
    rpr YESNO NOT NULL
);
CREATE TABLE IF NOT EXISTS zttyp (
    id INTEGER PRIMARY KEY,
    ttyp TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS zkv (
    id INTEGER PRIMARY KEY,
    key TEXT NOT NULL UNIQUE,
    val TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS zv(
id INTEGER PRIMARY KEY,
vname VARCHAR NOT NULL UNIQUE,
vsql TEXT NOT NULL
);
INSERT INTO zttyp VALUES (1, 'table');
INSERT INTO zttyp VALUES (2, 'view');

INSERT INTO zftyp VALUES (1, 'BOOLEAN');
INSERT INTO zftyp VALUES (2, 'DATE');
INSERT INTO zftyp VALUES (3, 'DATEN');
INSERT INTO zftyp VALUES (4, 'INTEGER');
INSERT INTO zftyp VALUES (5, 'INTEGERS');
INSERT INTO zftyp VALUES (6, 'NUMERIC');
INSERT INTO zftyp VALUES (7, 'NUMERICS');
INSERT INTO zftyp VALUES (8, 'TEXT');
INSERT INTO zftyp VALUES (9, 'IDBUTTON');
INSERT INTO zftyp VALUES (10, 'IDCOMBO');
INSERT INTO zftyp VALUES (11, 'VARCHAR');
INSERT INTO zftyp VALUES (12, 'VARCHARN');
INSERT INTO zftyp VALUES (13, 'WEEKDAYS');
INSERT INTO zftyp VALUES (14, 'YESNO');

INSERT INTO zkv VALUES (1, 'appname', 'Test Application');
INSERT INTO zkv VALUES (2, 'version', '0.1');
INSERT INTO zkv VALUES (3, 'programmer', 'Ted Lazaros');

COMMIT;
"""

sqltablefields = '''SELECT zt.tbl, zfld.fld, zftyp.ftyp, zt_d.uniq,
zt_d.tuniq, zfld.nonull, zfld.max
FROM zt_d
INNER JOIN zt ON zt.id=zt_d.zt_id
INNER JOIN zfld ON zfld.id=zt_d.zfld_id
INNER JOIN zftyp ON zftyp.id=zfld.zftyp_id
ORDER BY zt.tbl, zt_d.id
'''
appmeta = 'app.meta'


def _sqlcreate():
    vals = udbs.select(appmeta, sqltablefields)
    sqlc = 'BEGIN TRANSACTION;\n%sCOMMIT;'
    sqlt = 'CREATE TABLE IF NOT EXISTS %s(\n%s\n);\n'

    sqltmp = ''
    tblLines = {}
    utbLines = {}
    for line in vals['rows']:
        table = line['tbl']
        field = line['fld']
        typos = line['ftyp']
        if line['nonull'] == 0:
            notnull = ''
        else:
            notnull = ' NOT NULL'
        if line['uniq'] == 0:
            uq = ''
        else:
            uq = ' UNIQUE'
        if field.endswith('_id'):
            rf = " REFERENCES %s(id)" % field[:-3]
        else:
            rf = ''
        if line['tuniq'] != 0:
            tl = utbLines.get(table, [])
            if not tl:
                utbLines[table] = [field]
            else:
                utbLines[table].append(field)
        tb = tblLines.get(table, [])
        if not tb:
            tblLines[table] = ['id INTEGER PRIMARY KEY']
        tblLines[table].append('%s %s%s%s%s' % (field, typos, notnull, uq, rf))
    for key in sorted(tblLines.keys()):
        tun = utbLines.get(key, '')
        if tun:
            tblLines[key].append('UNIQUE (%s)' % ','.join(tun))
        va = ',\n'.join(tblLines[key])
        sqltmp += sqlt % (key, va)

    return sqlc % sqltmp


def _create_db(dbpath, sqlcreate):
    # Create the actual database
    # dbpath      : the database path
    # tables      : dictionary
    # app_key     : Application's specific key for identification
    # app_version : Application's version

    if not dbpath:
        log.error('create_db(): dbath is empty')
        return False
    if os.path.exists(dbpath):  # There is another file already
        log.error('create_db(): File %s already exists' % dbpath)
    try:
        con = sqlite3.connect(dbpath)
        cur = con.cursor()
        cur.executescript(sqlcreate)
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


def createmeta():
    _create_db(appmeta, ddl)


def create_user_db(dbname):
    _create_db(dbname, _sqlcreate())
