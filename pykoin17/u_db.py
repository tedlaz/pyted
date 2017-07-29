# -*- coding: utf-8 -*-

import sqlite3
import os
from logger import log
from u_dict import merge_dict_to_listdic
from collections import OrderedDict as odi

def isdb_ok(db):
    '''
    Basic check for all (almost) functions here
    '''
    if db == ':memory:':
        return True
    if not db:
        log.info('isdb_ok: db parameter is empty')
        return False
    if not os.path.exists(db):
        log.info('isdb_ok: Path %s does not exist' % db)
        return False
    return True


def is_list1_in_list2(list1, list2, ignore_id=False):
    '''
    IF every element of list1 belongs to list2 returs True.
    Otherwise returns False
    id is a special case , we can just ignore it
    with ignore_id=True
    '''
    if not list1 or not list2:
        return False
    for el in list1:
        if ignore_id:
            if el == 'id':
                continue
        if el not in list2:
            return False
    return True


def sql_insert(dic, fields, table):
    '''
    Returns sql of the form:
    'INSERT INTO TABLE(...) VALUES (...);'
    dic : dict of values {'fld1': 'val1', 'fld2': 'val2', ...}
    fields : list of fields ['fld1', 'fld2', ...]
    table : table name
    '''
    if not dic:
        log.info('sql_insert: dic is empty')
        return ''
    if not fields:
        log.info('sql_insert: fields is empty')
        return ''
    if not table:
        log.info('sql_insert: table is empty')
        return ''
    sql = "INSERT INTO %s (%s) VALUES (%s);"
    pfields = ''
    pvalues = ''
    for fld in fields:
        if fld == 'id':
            continue
        pfields += '%s, ' % fld
        pvalues += "'%s', " % dic[fld]
    pfields = pfields[:-2]
    pvalues = pvalues[:-2]
    return sql % (table, pfields, pvalues)


def sql_update(dic, fields, table):
    sql = "UPDATE %s set %s WHERE id=%s;"
    pfld_val = ''
    for fld in fields:
        if fld == 'id':
            continue
        pfld_val += "%s='%s', " % (fld, dic[fld])
    pfld_val = pfld_val[:-2]
    return sql % (table, pfld_val, dic['id'])


def sql_many(db, table, listdict, transactional=True):
    '''
    Creates script of the form:
    "
    INSERT INTO table(...) VALUES(...);
    'UPDATE table SET ... WHERE id=id;
    "
    If transactional is True wraps sql with BEGIN TRANSACTION;, COMMIT;
    '''
    sqllist = sql_many_list(db, table, listdict)
    if not sqllist:
        return ''
    sql = ''
    if transactional:
        sql = "BEGIN TRANSACTION;\n"
    for sqlel in sqllist:
        sql += '%s\n' % sqlel
    if transactional:
        sql += "COMMIT;"
    return sql


def sql_many_list(db, table, listdict):
    '''
    Creates list of sql from listdict of the form:
    [
    '[INSERT] INTO table (...) VALUES(...)',
     'UPDATE table SET ... WHERE id=id,
     ...
    ]
    if dict from listdict has key='id' and value of key > 0
    update otherwise insert
    '''
    if not isdb_ok(db):
        return []

    if not table:
        log.info('sql_many: empty table')
        return ''

    fields = fields_of_table(db, table)  # Get table fields

    if not fields:
        log.info('sql_many: no fields for table %s' % table)
        return []

    lst = []
    for dic in listdict:
        keys = dic.keys()
        if not is_list1_in_list2(fields, keys, True):
            msg = 'sql_many: not all fields(%s) in keys(%s)'
            log.info(msg % (fields, keys))
            return []
        if dic.get('id', 0) == 0:
            lst.append('%s' % sql_insert(dic, fields, table))
        else:
            lst.append('%s' % sql_update(dic, fields, table))
    return lst


def save(db, table, dic):
    '''
    Save a single record to database
    db    : Database name
    table : Table name
    dic   : values to save
    If dic contains key = 'id' with dic['id'] > 0 then
        executes update
    otherwise
        executes insert
    '''
    if not isdb_ok(db):
        return False

    if not table:
        log.info('save: empty table')
        return False

    fields = fields_of_table(db, table)
    if not fields:
        log.info('save: no fields for table %s' % table)
        return False
    keys = dic.keys()
    sql = ''
    if not is_list1_in_list2(fields, keys):
        log.info('save: not all fields (%s) in keys (%s)' % (fields, keys))
        return False
    if dic.get('id', 0) == 0:  # need to insert
        sql = sql_insert(dic, fields, table)
        last_id = _insert(db, sql)  # here is the actual insert
    else:  # need to update
        sql = sql_update(dic, fields, table)
        _update(db, sql)
        last_id = dic['id']
    return last_id


def save_many(db, table, listdict):
    '''
    Creates a transactional sql_may and executes it.
    '''
    sql = sql_many(db, table, listdict)
    return script(db, sql)


def save_master_det(db, master_table, dic, detail_table, lstdic):
    '''
    Save master / detail data in a single transaction
    '''
    if not isdb_ok(db):
        return False
    fkey = '%s_id' % master_table
    fldsmaster = fields_of_table(db, master_table)
    keysmaster = dic.keys()
    if not is_list1_in_list2(fldsmaster, keysmaster, True):
        log.info('save_master_det: Err1')
        return False
    if dic.get('id', 0) == 0:
        sqlmaster = sql_insert(dic, fldsmaster, master_table)
    else:
        sqlmaster = sql_update(dic, fldsmaster, master_table)
    try:
        con = sqlite3.connect(db)
    except sqlite3.Error as sqe:
        log.info('save_master_det: %s' % sqe)
        return False
    cur = con.cursor()
    last_id = None
    try:
        cur.execute(sqlmaster)
        last_id = cur.lastrowid
        if not last_id:
            last_id = dic['id']
        if not last_id:
            con.rollback()
            cur.close()
            con.close()
            return False
        merge_dict_to_listdic({fkey: last_id}, lstdic)
        sqldetail = sql_many_list(db, detail_table, lstdic)
        if sqldetail:
            for sqld in sqldetail:
                cur.execute(sqld)
        else:
            con.rollback()
            cur.close()
            con.close()
            log.info('save_master_det: rolled back :-(')
            return False
    except sqlite3.Error as sqe:
        log.info('save_master_det: %s' % sqe)
        con.rollback()
        log.info('save_master_det: rolled back :-(')
        cur.close()
        con.close()
        return False
    con.commit()
    cur.close()
    con.close()
    return True


def _insert(db, sql):
    '''
    A single insert
    '''
    if not isdb_ok(db):
        return None
    try:
        con = sqlite3.connect(db)
    except sqlite3.Error as sqe:
        log.info('_insert: %s' % sqe)
        return None
    cur = con.cursor()
    last_id = None
    try:
        cur.execute(sql)
        last_id = cur.lastrowid
        con.commit()
    except sqlite3.Error as sqe:
        log.info('_insert: %s' % sqe)
    finally:
        cur.close()
        con.close()
    return last_id


def _update(db, sql):
    '''
    A single update
    '''
    if not isdb_ok(db):
        return None
    try:
        con = sqlite3.connect(db)
    except sqlite3.Error as sqe:
        log.info('_update: %s' % sqe)
        return None
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except sqlite3.Error as sqe:
        log.info('_update: %s' % sqe)
    finally:
        cur.close()
        con.close()
    return True


def select(db, sql):
    '''
    A select
    '''
    if not isdb_ok(db):
        return []
    if not sql:
        log.info('select: parameter sql is empty')
        return []
    try:
        con = sqlite3.connect(db)
        # hook functions here
        # con.create_function("grup", 1, grup)
        # con.create_function("nul2z", 1, nul2z)
        # con.create_function('jget', 2, jget)

        cur = con.cursor()
        cur.execute(sql)
        columnNames = [t[0] for t in cur.description]
        rows = cur.fetchall()

    except sqlite3.Error as sqe:
        log.info('select: %s' % sqe)
        rows = [[]]
        cur.close()
        con.close()
        return []
    cur.close()
    con.close()
    listdict = []
    for row in rows:
        # tdic = {}
        tdic = odi()
        for i, col in enumerate(row):
            tdic[columnNames[i]] = col
        listdict.append(tdic)
    return listdict


def select_table(db, tablename):
    '''
    Returns all records of table tablename
    '''
    if not tablename:
        log.info('select_table: tablename is empty')
        return []
    sql = 'SELECT * FROM %s' % tablename
    return select(db, sql)


def select_one(db, tablename, id):
    '''
    Returns just one record or {}
    '''
    sql = "SELECT * FROM %s WHERE id=%s" % (tablename, id)
    result = select(db, sql)
    if result:
        return result[0]
    else:
        return {}


def select_list(db, tmaster, tdetail, id):
    '''
    Returns a list of dictionaries from tdetail
    filtered by tmaster_id=id
    db      : database
    tmaster : master table name
    tdetail : detail table name
    id      : id to filter tdetail records
    '''
    sql = "SELECT * FROM %s WHERE %s_id=%s" % (tdetail, tmaster, id)
    return select(db, sql)


def select_master_detail(db, tmaster, tdetail, id):
    '''
    tmaster : master table
    tdetail : detail table. Must have foreign key pointing to tmaster with
               name tmaster_id
    id      : The id of the master record.
              Returns dict in the form {'id': 1, ... ,'i_i': [{}, {}, ..]}
              i_i key contains list with tdetail records.
    '''
    if not isdb_ok(db):
        return {}

    fdic = select_one(db, tmaster, id)
    if fdic:
        resd = select_list(db, tmaster, tdetail, id)
    else:
        return {}
    fdic['%s_list' % tdetail] = resd
    return fdic


def select_master_detail_deep(db, tmaster, tdetail, id):
    if not isdb_ok(db):
        return {}
    master = select_deep(db, tmaster, id)
    sqld = "SELECT id FROM %s WHERE %s_id=%s" % (tdetail, tmaster, id)
    # Βρίσκουμε τα id των παιδιών
    resd = select(db, sqld)
    detail = []
    for dic in resd:
        detail.append(select_deep(db, tdetail, dic['id'], tmaster))
    master['i_i'] = detail
    return master


def select_deep(db, table, id, tmaster=None):
    '''
    Select a record from database (db) , table (table) with id = (id)
    Scans the record keys and if key is of the form <name>_id substitudes
    value with record from table <name> and id = <name>_id
    '''
    if not isdb_ok(db):
        return {}
    sqlm = "SELECT * FROM %s WHERE id=%s" % (table, id)
    res = select(db, sqlm)
    if not res:
        return {}
    else:
        res1 = res[0]
    keys = res1.keys()
    if tmaster:
        popval = tmaster + '_id'
        if popval in keys:
            keys.pop(keys.index(popval))
    for key in keys:
        if '_id' in key:
            new_table = key[:-3]
            new_id = res1[key]
            res1[key] = select_deep(db, new_table, new_id)
    return res1


def fields_of_table(db, table):
    '''
    Returns a list with table fields
    '''
    if not isdb_ok(db):
        return []
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute('SELECT * FROM %s LIMIT 1' % table)
        fields = [t[0] for t in cur.description]
    except sqlite3.Error as sqe:
        log.info('fields_of_table: %s' % sqe)
        return []
    cur.close()
    con.close()
    return fields


def script(db, sql, newDb=False):
    '''
    sql   : A set of sql commands (create, insert or update)
    '''
    if not newDb:
        if not isdb_ok(db):
            return False
    else:
        log.info('script: creating database %s' % db)
    if not sql:
        return False
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.executescript(sql)
        con.commit()
    except sqlite3.Error as sqe:
        log.info('script: %s' % sqe)
        con.rollback()
        cur.close()
        con.close()
        return False
    cur.close()
    con.close()
    return True


def main():
    db = 'tst.sql3'
    print(select_master_detail(db, 'dia', 'dapx',1))


if __name__ == '__main__':
    main()
