# -*- coding: utf-8 -*-

import sqlite3
import os
from logger import log
from collections import OrderedDict as odi

CREATE, INSERT, UPDATE, DELETE, SCRIPT, SELECT = range(6)
SQL_CREATE = 'sql_create.sql'


class Sqlcon(object):
    def __new__(cls, action, db, sql):
        if not action:
            return None
        if not db:
            return None
        return super(Sqlcon, cls).__new__(cls)

    def __init__(self, action, db, sql=''):
        self.action = action
        self.db = db
        self.sql = sql
        self.con = None
        self.cur = None

    def run(self):
        if self.action == CREATE:
            return self._create()
        elif self.action == INSERT:
            return self._insert()
        elif self.action == UPDATE:
            return self._update()
        elif self.action == DELETE:
            return self._delete()
        elif self.action == SCRIPT:
            return self._script()
        elif self.action == SELECT:
            return self._select()
        else:
            return self._other()


    def _connect(self):
        try:
            self.con = sqlite3.connect(self.db)
            self.cur = self.con.cursor()
            self.connected = True
            return True
        except sqlite3.Error as sqe:
            log.error('Connection error : %' % sqe)
            return False

    def __del__(self):
        if not self.con:
            print('no connection')
        self.cur.close()
        self.con.close()
        self.cur = None
        self.con = None

    def _create(self):
        if os.path.exists(self.db):
            log.error('file %s exists. Exiting' % self.db)
            return False
        if not os.path.exists(SQL_CREATE):
            log.error('file %s not exists. Exiting' % SQL_CREATE)
        with open(SQL_CREATE) as filesql:
            sql_create = filesql.read()
        rval = False
        if self._connect():
            try:
                self.cur.executescript(sql_create)
                self.con.commit()
                rval = True
            except sqlite3.Error as sqe:
                log.error('Script error : %s' % sqe)
                self.con.rollback()
                os.remove(self.db)
            finally:
                # self._close()
                log.info('database %s created' % self.db)
        return rval

    def _insert(self):
        if not len(self.sql) > 6:
            return 0
        if not self.sql[:6].upper() == 'INSERT':
            return 0
        return 1

    def _update(self):
        if not len(self.sql) > 6:
            return 0
        if not self.sql[:6].upper() == 'UPDATE':
            return 'update'

    def _delete(self):
        if not len(self.sql) > 6:
            return 0
        if not self.sql[:6].upper() == 'DELETE':
            return 'delete'

    def _script(self):
        if not os.path.exists(self.db):
            log.error('_script: db file %s not exists. Exiting' % self.db)
            return False
        rval = False
        if self._connect():
            try:
                self.cur.executescript(self.sql)
                self.con.commit()
                rval = True
            except sqlite3.Error as sqe:
                log.error('_script : %s' % sqe)
                self.con.rollback()
        if rval:
            log.info('Script execution completed. No errors !!!')
        return rval

    def _select(self):
        return 'select'

    def _other(self):
        return 'other'


class tst(object):

    def __new__(cls, param, pas):
        if param:
            return super(tst, cls).__new__(cls)
        else:
            return None

    def __init__(self, param, pas):
        self.param = param
        self.pas = pas


class Dbm(object):

    def __init__(self, db):
        self.db = db
        self.conn = None
        self.cur = None
        self._connect()

    def _connect(self):
        self.conn = sqlite3.connect(self.db)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def select(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
        columnNames = [t[0] for t in self.cur.description]
        data = self.cur.fetchall()
        listdict = []
        for row in data:
            tdic = odi()
            for i, col in enumerate(row):
                tdic[columnNames[i]] = col
            listdict.append(tdic)
        return listdict

    def select_one(self, table, id):
        sql = "SELECT * FROM %s WHERE id=%s" % (table, id)
        return self.select(sql)[0]

    def __del__(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print('cur and con closed')

if __name__ == '__main__':
    #for row in Dbm('tst.sql3').select("select * from dia"):
    #    print(row)
    #for row in Dbm('tst.sql3').select("select * from ej"):
    #    print(row)
    print(Dbm('tst.sql3').select_one('dia', 100).values())
    #dbm.qprint("select * from ej")
