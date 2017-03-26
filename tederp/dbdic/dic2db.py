# -*- coding: utf-8 -*-
import sqlite3


def _d2sql(adic, table, masterfld=None, masterid=None):
    '''
    Creates insert or update sql from a dictionary
    table : Table name
    adic  : Dictionary with keys corresponding to table's fields
    Returns update or insert sql according id
    if (id = 0 or id = '' or id = None) returns insert sql
    if id <> 0 returns update sql
    '''
    fields = []  #
    values = []
    ufldva = []
    adic['id'] = adic.get('id', 0)
    for el in adic.keys():
        if el == 'id':
            continue
        if el == 'zlines':
            # Το κλειδί zlines παραβλέπεται γιατί εάν υπάρχει, αναφέρεται
            # σε πίνακα details
            continue
        fields.append(el)
        # Εδώ γίνεται η εισαγωγή του parent κλειδιού την ώρα της εγγραφής
        if '(SELECT MAX(id) FROM' in ('%s' % adic[el]):
            values.append("%s" % adic[el])
        else:
            values.append("'%s'" % adic[el])
        ufldva.append("%s='%s'" % (el, adic[el]))

    if adic['id'] == 0 or adic['id'] == '' or adic['id'] == None:
        sql = "INSERT INTO %s (%%s) VALUES (%%s);" % table
        return sql % (', '.join(fields), ', '.join(values))
    else:
        if masterfld:
            sql = "UPDATE %s SET %s WHERE id='%s' AND %s='%s';"
            return sql % (table, ', '.join(ufldva), adic['id'], masterfld, masterid)
        else:
            sql = "UPDATE %s SET %s WHERE id='%s';"
            return sql % (table, ', '.join(ufldva), adic['id'])


def _md2sql(adic, tmaster, tdetail=None):
    '''
    Master-Detail to sql
    '''
    if not tdetail:
        return _d2sql(adic, tmaster)
    sql = _d2sql(adic, tmaster) + '\n'
    for el in adic['zlines']:
        if adic['id'] == 0 or adic['id'] == '' or adic['id'] == None:
            el['%s_id' % tmaster] = ('(SELECT MAX(id) FROM %s)' % tmaster)
            sql += _d2sql(el, tdetail) + '\n'
        else:
            masterfld = '%s_id' % tmaster
            masterid = adic['id']
            el[masterfld] = masterid
            sql += _d2sql(el, tdetail, masterfld, masterid) + '\n'
    return 'BEGIN TRANSACTION;\n' + sql + 'COMMIT;\n'


def confsql(adic, tmaster):
    '''
    Returns back data from tables just to make sure everything is ok
    '''
    asql = 'SELECT * FROM %s WHERE %%s;' % tmaster
    aval = []
    for ele in adic.keys():
        if ele == 'id':
            continue
        if ele == 'zlines':
            continue
        aval.append("%s='%s'" % (ele, adic[ele]))
    return asql % ' and '.join(aval)


def _execute_script(sqlscript, dbf, confirmsql):
    con = sqlite3.connect(dbf)
    con.row_factory = sqlite3.Row
    con.executescript(sqlscript)
    cur = con.cursor()
    cur.execute(confirmsql)
    rows = cur.fetchall()
    cur.close()
    con.close()
    return dict(zip(rows[0].keys(), rows[0]))


def dic2db(dbf, adic, tmaster, tdetail=None):
    '''
    Create master and/or detail sql in a transaction and run it
    against database dbf
    '''
    csql = confsql(adic, tmaster)
    return _execute_script(_md2sql(adic, tmaster, tdetail), dbf, csql)


if __name__ == '__main__':
    ad = {'par_id': 1, 'cat_id': 7, 'typ_id': 'normal', 'ori_id': 'ell', 'id': 87,
          'dat': '2016-10-05', 'pno': u'ΤΔΑ109',  'afm': '046949583', 'pli_id': 1,
          'per': 'test',
          'zlines': [{'lm_id': '20.01', 'pfpa': 13, 'val': 50, 'fpa': 26, 'id': 0},
                     {'lm_id': '20.01', 'pfpa': 23, 'val': 210, 'fpa': 48, 'id': 4},
                    ]
          }
    db = '/home/tedlaz/pyted/tederp/tst.db'
    print(_md2sql(ad,'ki', 'kid'))
    #print(dic2db(db, ad, 'ki', 'kid'))
