# -*- coding: utf-8 -*-

import sqlite3
import os
import datetime
import time
import json
# status VALUES
PIN_ERROR, DB_ERROR, NULL_VAL, ONE_VAL, MANY_VAL = range(5)


def jget(data, key):
    '''
    data: json from database
    key : the key to get value for
    creates a dictionary from json and tries to return
    key value if exists otherwise 0
    From dictionary to json we have to do: json.dumps(jdata)
    '''
    jdata = json.loads(data)
    val = jdata.get(key, 0)
    return val


def fixed_size(num, size):
    '''
    fixed_size(1, 2) returns '01'
    fixed_size(120, 2) returns '12'
    '''
    txt_num = str(num)
    len_txt = len(txt_num)
    if len_txt < size:
        return (size - len_txt) * '0' + txt_num
    elif len_txt > size:
        return txt_num[:size]
    else:
        return txt_num


def uid():
    time.sleep(.001)
    now = datetime.datetime.today()

    year1 = fixed_size(now.year, 4)
    # ignore the first two digits of year
    yearf = year1[2:]
    month = fixed_size(now.month, 2)
    day = fixed_size(now.day, 2)
    hour = fixed_size(now.hour, 2)
    mint = fixed_size(now.minute, 2)
    sec = fixed_size(now.second, 2)
    msec = fixed_size(now.microsecond, 3)
    fstr = '%s%s%s%s%s%s%s' % (yearf, month, day, hour, mint, sec, msec)
    return fstr


def nul2z(val):
    '''
    Instead of null returns 0. For sqlite use.
    '''
    if val:
        return val
    else:
        return 0


def grup(txtVal):
    '''
    Trasforms a string to uppercase special for Greek comparison
    '''
    ar1 = u"αάΆβγδεέΈζηήΉθιίϊΊκλμνξοόΌπρσςτυύΎφχψωώΏ"
    ar2 = u"ΑΑΑΒΓΔΕΕΕΖΗΗΗΘΙΙΙΙΚΛΜΝΞΟΟΟΠΡΣΣΤΥΥΥΦΧΨΩΩΩ"
    ftxt = u''
    for letter in txtVal:
        if letter in ar1:
            ftxt += ar2[ar1.index(letter)]
        else:
            ftxt += letter.upper()
    return ftxt


def dbScript(pin):
    '''
    Generic sql script execution
    input
        script : one or many sql expressions divided by ;
        db  : database name
    output:
        1 if no error , 0 if error
        text message
    '''
    script = pin.get('script', None)
    db = pin.get('db', None)

    if (not script) or (not db):
        return {'status': PIN_ERROR,
                'msg': 'dbScript: script and/or db name are empty'}

    try:
        con = sqlite3.connect(db)  # @UndefinedVariable
        cur = con.cursor()
        cur.executescript(script)
        con.commit()
        status = NULL_VAL
        msg = 'dbScript: Everything executed Fine !!'
    except sqlite3.Error, e:  # @UndefinedVariable
        if con:
            con.rollback()
        status = DB_ERROR
        msg = 'dbScript: %s' % e
    except Exception, e:
        print e
    finally:
        cur.close()
        con.close()
    return {'status': status, 'msg': msg}


def dbRows(pin):
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
    sql = pin.get('sql', None)
    db = pin.get('db', None)
    limit = pin.get('limit', None)

    if (not sql) or (not db):
        return {'status': PIN_ERROR,
                'rows': [[]],
                'columnNames': [],
                'rowNumber': 0,
                'columnNumber': 0,
                'msg': 'dbRows :script and/or db name are empty'}

    if not os.path.exists(db):
        return {'status': PIN_ERROR,
                'rows': [[]],
                'columnNames': [],
                'rowNumber': 0,
                'columnNumber': 0,
                'msg': 'dbRows : Path %s not exists' % db}

    status = DB_ERROR
    msg = 'dbRows :Something bad happened !!'

    columnNames = []

    if limit:
        sql += ' limit(%s)' % limit
    try:
        con = sqlite3.connect(db)  # @UndefinedVariable
        # hook functions here
        con.create_function("grup", 1, grup)
        con.create_function("nul2z", 1, nul2z)
        con.create_function('jget', 2, jget)

        rowNum = 0
        colNum = 0
        cur = con.cursor()
        cur.execute(sql)
        columnNames = [t[0] for t in cur.description]
        colNum = len(columnNames)
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
            msg = 'dbRows: Success , %s records' % rowNum

    except sqlite3.Error, e:  # @UndefinedVariable
        rws = []
        status = DB_ERROR
        msg = 'dbRows: %s' % e

    return {
        'rows': rws,
        'columnNames': columnNames,
        'status': status,
        'msg': msg,
        'rowNumber': rowNum,
        'columnNumber': colNum
        }


def dbCommit(pin):
    """
    For insert or Update records returns last inserted id
    input
        sql : sql code to run
        db  : database name
        params : parameters
    output:
        last inserted id or 0 (error)
        text message
    """

    sql = pin.get('sql', None)
    db = pin.get('db', None)
    params = pin.get('params', None)

    if (not sql) or (not db):
        return {'status': PIN_ERROR,
                'msg': 'dbRows :script and/or db name are empty'}

    if not os.path.exists(db):
        return {'status': PIN_ERROR,
                'msg': 'dbCommit: Path %s not exists' % db}

    last_id = None
    status = DB_ERROR
    msg = 'dbCommit: Something bad happened !!'

    try:
        con = sqlite3.connect(db)  # @UndefinedVariable
        cur = con.cursor()
        if params:
            cur.execute(sql, params)  # sql with ? instead of %s
        else:
            cur.execute(sql)
        last_id = cur.lastrowid
        if not last_id:
            msg = 'dbCommit: Record updated !!!'
            status = ONE_VAL
        else:
            msg = 'dbCommit: Record saved with id=%s' % last_id
            status = ONE_VAL
        con.commit()
    except sqlite3.Error, e:  # @UndefinedVariable
        if con:
            con.rollback()
        status = DB_ERROR
        msg = 'dbCommit: %s' % e
    finally:
        cur.close()
        con.close()
    return {'lastId': last_id, 'status': status, 'msg': msg}


def key_value(pin):
    data = dbRows(pin)
    retdict = {}
    if data['columnNumber'] == 2 and data['rowNumber'] > 0:
        for line in data['rows']:
            retdict[line[0]] = line[1]
    return retdict


def key_value_print(pin):
    vals = key_value(pin)
    if not vals:
        print('No Values')
        return
    for key in vals:
        print('%s : %s' % (key, vals[key]))


def zread(key, db):
    '''
    Returns value from key.
    Assumes existense of table z(param, val)
    '''
    # print 'zread key: %s, db: %s' % (key, db)
    sql = "SELECT val FROM z WHERE param='%s'" % key
    result = dbRows({'sql': sql, 'db': db})
    if result['rowNumber'] == 1:
        return result['rows'][0][0]
    else:
        return ''


def tst():
    assert nul2z(None) == 0
    assert nul2z(12) == 12
    assert nul2z('tst') == 'tst'
    assert grup(u'αάσςεέοόΌfab') == u'ΑΑΣΣΕΕΟΟΟFAB'

    db = 'tst.db'
    id = uid()
    sqlCreate = "CREATE table if not exists tst (id INTEGER PRIMARY KEY, per TEXT); "
    sqlInsert = "INSERT INTO tst(id, per) VALUES(%s, 'testing insert');" % id
    sqlUpdate = "UPDATE tst SET per = 'new value' WHERE id = %s" % id
    sqlSelect = "SELECT * FROM tst"
    print(dbScript({'script': sqlCreate, 'db': db}))
    print(dbCommit({'sql': sqlInsert, 'db': db}))
    print(dbRows({'sql': sqlSelect, 'db': db}))
    print(dbCommit({'sql': sqlUpdate, 'db': db}))
    print(dbRows({'sql': sqlSelect, 'db': db}))
    print(dbRows({'sql': sqlSelect, 'db': 'a.db'}))
    sql2 = "CREATE TABLE IF NOT EXISTS jt(id INTEGER PRIMARY KEY, tx TEXT, data TEXT);"
    sql2s = "SELECT tx, sum(jget(data, 'poso')) as poso FROM jt group by tx;"
    print(dbScript({'script': sql2, 'db': db}))
    print(dbCommit({'sql': '''INSERT INTO jt VALUES(1, 'a', '{"poso": 100, "ika": "Εδώ"}')''', 'db': db}))
    print(dbCommit({'sql': '''INSERT INTO jt VALUES(2, 'a', '{"poso": 30, "ika": "Eκεί"}')''', 'db': db}))
    print(dbCommit({'sql': '''INSERT INTO jt VALUES(3, 'b', '{"poso": 30, "ika": "Eκεί"}')''', 'db': db}))
    print(dbRows({'sql': sql2s, 'db': db}))
    os.remove(db)

if __name__ == '__main__':
    tst()
