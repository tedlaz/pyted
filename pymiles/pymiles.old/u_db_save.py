# -*- coding: utf-8 -*-
import sqlite3
import os
from u_logger import log


def save(dbpath, sqllist):
    '''
    A single insert or update
    '''
    if not os.path.exists(dbpath):
        log.error('save(): dbpath %s not exists' % dbpath)
        return None

    for sql in sqllist:
        if len(sql) < 10:
            log.error('save(): Wrong sql-> %s' % sql)
            return {}
        if sql[:6].upper() not in ('INSERT', 'UPDATE'):
            log.error('save(): sql(%s) not INSERT or UPDATE' % sql)

    try:
        con = sqlite3.connect(dbpath)
    except sqlite3.Error as sqe:
        log.error('save: %s' % sqe)
        return None
    cur = con.cursor()
    last_id = []
    try:
        for sql in sqllist:
            cur.execute(sql)
            last_id.append(cur.lastrowid)
        con.commit()
    except sqlite3.Error as sqe:
        log.critical('save: %s' % sqe)
        con.rollback()
        cur.close()
        con.close()
        return None
    cur.close()
    con.close()

    if len(last_id) == 1:
        last_id = last_id[0]
    log.debug('save(): Completed with id = %s' % last_id)
    return last_id


def save_one_many(dbpath, listsql):
    '''
    listsql : touple of the form :
    (
        "SELECT OR INSERT .......",  // Master data
        [
            "SELECT OR INSERT ...",  // Detail lines
            "SELECT OR INSERT ..."
        ]
    )
    detail sql if new master record must be formatted by idval
    '''
    if not os.path.exists(dbpath):
        log.error('save_one_many(): dbpath %s not exists' % dbpath)
        return None
    sql_one, sqlmany = listsql
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    try:
        cur.execute(sql_one)
        last_id = cur.lastrowid
        for sql in sqlmany:
            if last_id:
                cur.execute(sql.format(idval=last_id))  # formatting here
            else:
                cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
    except sqlite3.Error as sqe:
        log.critical('save_one_many(): %s' % sqe)
        con.rollback()
        cur.close()
        con.close()
    log.debug('save_one_many(): Completed without errors')
    return last_id
