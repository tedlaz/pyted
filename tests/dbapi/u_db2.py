# -*- coding: utf-8 -*-

import sqlite3
import os
import sys
from collections import OrderedDict as odi
from logger import log
import u_sql as usql

pyver = sys.version_info.major


def txtEncoded(txt):
    if pyver == 3:
        return txt
    else:
        return txt.encode('utf-8')
# db = path of database file
# tbl, tmaster, tdetail = table name
# fields of the form "<name>_id" are foreign keys pointing to table <name>


def select_deep(db, sql):
    pass


def select_table(db, tbl):
    pass


def select_table1(db, tbl, id):
    pass


def select_master_detail(db, tmaster, tdetail, id):
    pass


def select_master_detail_deep(db, tmaster, tdetail, id):
    pass


def save_master_d(db, tmaster, tdetail, dicmaster, listdicdetail):
    if not os.path.exists(db):
        log.error('save_master_d: Path %s does not exist' % db)
        return None
    sqlmaster = usql.save(tmaster, dicmaster)
    log.debug("save_master_d: sqlmaster = '%s'" % sqlmaster)
    try:
        con = sqlite3.connect(db)
    except sqlite3.Error as sqe:
        log.error('save_master_d: %s' % sqe)
        return None
    cur = con.cursor()
    last_id = None
    try:
        cur.execute(sqlmaster)
        last_id = cur.lastrowid
    except sqlite3.Error as sqe:
        log.critical('save_master_d: %s' % sqe)
        cur.close()
        con.close()
        return None
    if not last_id:
        last_id = dicmaster['id']
    # listdicdetail dics should have <tmaster>_id key. det_fld
    det_fld = '%s_id' % tmaster
    for dic in listdicdetail:
        if dic.get(det_fld, 0) == 0:
            dic[det_fld] = last_id
        else:
            if dic[det_fld] != last_id:
                log.critical('save_master_d: Error %s in %s' % (det_fld, dic))
                return None
    listsqld = usql.save_list(tdetail, listdicdetail)
    try:
        for sqld in listsqld:
            log.debug('save_master_d: sqld -> %s' % sqld)
            cur.execute(sqld)
        con.commit()
    except sqlite3.Error as sqe:
        con.rollback()
        log.critical('save_master_d: %s' % sqe)
        cur.close()
        con.close()
        return None
    cur.close()
    con.close()
    log.debug('save_master_d: Completed with no errors !!!')
    return last_id


class Db():

    def __init__(self, dbpath):
        if os.path.exists(dbpath):
            self.dbpath = dbpath
        else:
            log.info('Db: Path %s not exists' % dbpath)
            self.dbpath = None

    def __repr__(self):
        return 'Db %s' % self.dbpath

    def save(self, sql):
        '''
        A single insert or update
        '''
        if not self.dbpath:
            return None
        if len(sql) < 10:
            log.error('Db.save(): Wrong sql-> %s' % sql)
            return {}
        if sql[:6].upper() not in ('INSERT', 'UPDATE', 'DELETE'):
            log.error('Db.select(): sql (%s) not INSERT, UPDATE, DELETE' % sql)
        try:
            con = sqlite3.connect(self.dbpath)
        except sqlite3.Error as sqe:
            log.error('Db.save: %s' % sqe)
            return None
        cur = con.cursor()
        last_id = None
        try:
            cur.execute(sql)
            last_id = cur.lastrowid
            con.commit()
        except sqlite3.Error as sqe:
            log.critical('save: %s' % sqe)
            cur.close()
            con.close()
            return None
        cur.close()
        con.close()
        log.debug('Db.save(): Completed with id = %s' % last_id)
        return last_id

    def select(self, sql):
        '''A select'''
        if not self.dbpath:
            return {}
        if len(sql) < 10:
            log.error('Db.select(): Wrong sql-> %s' % sql)
            return {}
        if sql[:6].upper() != 'SELECT':
            log.error('Db.select(): sql (%s ) is not SELECT' % sql)
        try:
            con = sqlite3.connect(self.dbpath)
            # hook functions here
            # con.create_function("grup", 1, grup)
            # con.create_function("nul2z", 1, nul2z)
            # con.create_function('jget', 2, jget)
            cur = con.cursor()
            cur.execute(sql)
            columnNames = [t[0] for t in cur.description]
            rows = cur.fetchall()
        except sqlite3.Error as sqe:
            log.error('Db.select(): %s' % sqe)
            rows = [[]]
            cur.close()
            con.close()
            return {}
        cur.close()
        con.close()
        listdict = []
        for row in rows:
            tdic = odi()  # Ordered dict
            for i, col in enumerate(row):
                tdic[columnNames[i]] = col
            listdict.append(tdic)
        log.debug('Db.select(): Completed with no errors !!!')
        return {'fields': columnNames, 'rows': listdict}

    def fields(self, table):
        '''
        Returns a list with table fields
        '''
        if not self.dbpath:
            return []
        sql = 'SELECT * FROM %s LIMIT 0' % table
        return self.select(sql)['fields']

    def script(self, sql, new_db=False):
        '''
        sql   : A set of sql commands (create, insert or update)
        '''
        if not sql:
            log.error('Db.script(): sql parameter is empty')
            return False
        if not new_db:
            if not self.dbpath:
                log.error('Db.script(): Path %s does not exist' % self.dbpath)
                return False
        else:
            log.debug('Db.script(): creating database %s' % self.dbpath)

        try:
            con = sqlite3.connect(self.dbpath)
            cur = con.cursor()
            cur.executescript(sql)
            con.commit()
        except sqlite3.Error as sqe:
            log.error('Db.script(): %s' % sqe)
            con.rollback()
            cur.close()
            con.close()
            return False
        cur.close()
        con.close()
        log.debug('Db.script(): Completed with no errors !!!')
        return True

    def dump(self, fileout=None):
        # Convert dbfile to SQL dump file dbfile.sql
        if not self.dbpath:
            return False
        con = sqlite3.connect(self.dbpath)
        if not fileout:
            fileout = '%s.sql' % self.dbpath
        with open(fileout, 'w') as f:
            for line in con.iterdump():
                f.write('%s\n' % txtEncoded(line))
        log.info('Db: %s successfully dumped to %s' % (self.dbpath, fileout))
        return True


class Formdata():

    def __init__(self, table, id=None, parent=None):
        self.db = parent.db
        self.table = table
        self.fields = self.db.fields()
        self.data = None

    def fill(self, data):
        self.data = data

    def save(self):
        self.db.save(self.data)

if __name__ == '__main__':
    dbs = 'tst.sql3'
    tbl = 'ta'
    tbld = 'tb'
    dicl = odi([('id', 2), ('epo', 'Mayr'), ('ono', 'Niko')])
    dicd = [odi([('id', 4), ('ej_id', 33), ('tsv2', 'testwe')]),
            odi([('id', 5), ('ta_id', 2), ('ej_id', 44), ('tsv2', 'testewee')])
            ]
    # print(save_master_d(db, tbl, tbld, dic, dicd))
    # print(fields(db, 'vdapx'))
    # print(select(db, 'select * from tb'))
    sqla = "INSERT INTO ej (ej) VALUES ('Fotismos')"
    sqlb = "UPDATE ej set ej='MAlakis' Where id=4"
    maindb = Db(dbs)
    print(maindb.dump())
    print(maindb.fields('koidd'))
    print(maindb.save(sqlb))
