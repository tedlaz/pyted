# -*- coding: utf-8 -*-
import sqlite3
import os
import json
from decimal import Decimal as dc

PATH = os.path.dirname(os.path.abspath(__file__))


class Db():
    def __init__(self, db=':memory:'):
        self.db = db

    def rowst(self, sql, withColumnNames=False):
        '''
        Get a list of tuples of rows [(), (), ...]
        '''
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(sql)
        if withColumnNames:
            columnNames = [t[0] for t in cur.description]
        rws = cur.fetchall()
        cur.close()
        con.close()
        if withColumnNames:
            return columnNames, rws
        else:
            return rws

    def rowsd(self, sql):
        '''
        Get a list of dictionaries [{}, {}, ...]
        '''
        con = sqlite3.connect(self.db)
        # con.create_function("grdec", 1, grdec)
        # con.create_function("dec1", 1, dec)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        con.close()
        arrayOfDictionaries = []
        for row in rows:
            arrayOfDictionaries.append(dict(zip(row.keys(), row)))
        return arrayOfDictionaries

    def columnames(self, sql):
        '''
        Get a list with column names
        '''
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(sql)
        columnNames = [t[0] for t in cur.description]
        cur.close()
        con.close()
        return columnNames

    def execute_script(self, sqlscript):
        con = sqlite3.connect(self.db)
        con.executescript(sqlscript)
        con.close()
        return True


def insert(table, adic, dbpath):
    sqlt = "INSERT INTO %s (%s) VALUES(%s);"
    fields = []
    values = []
    for key in adic:
        fields.append("%s" % key)
        values.append("'%s'" % adic[key])
    tfields = ', '.join(fields)
    tvalues = ', '.join(values)
    sql = sqlt % (table, tfields, tvalues)
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    cur.execute(sql)
    lastid = cur.lastrowid
    con.commit()
    cur.close()
    con.close()
    return lastid


def test():
    t = Db(os.path.join(PATH, 'tst.db'))
    sql = "select * from ki inner join kid on ki.id=kid.ki_id;"
    print(t.rowst(sql, True))
    # print('\n'.join(map(str, t.rowsd(sql))))
    # print(t.columnames(sql))


def sql_ins_upd(table, adic):
    '''
    Returns update or insert sql according id
    if id = 0 returns insert sql
    if id <> 0 returns update sql
    '''
    fields = []
    values = []
    ufldva = []
    adic['id'] = adic.get('id', 0)
    for el in adic.keys():
        if el == 'id':
            continue
        if el == 'zlines':
            continue
        fields.append(el)
        if '(SELECT MAX(id) FROM' in ('%s' % adic[el]):
            values.append("%s" % adic[el])
        else:
            values.append("'%s'" % adic[el])
        ufldva.append("%s='%s'" % (el, adic[el]))
    if (adic['id'] == 0) or (adic['id'] == '') or (adic['id'] is None):
        sql = "INSERT INTO %s (%%s) VALUES (%%s);" % table
        return sql % (', '.join(fields), ', '.join(values))
    else:
        sql = "UPDATE %s SET %s WHERE id=%s;"
        return sql % (table, ', '.join(ufldva), adic['id'])


def md2sql(tmaster, tdetail, adic, id_at_end=True):
    '''
    Master-Detail to sql
    '''
    sql = sql_ins_upd(tmaster, adic) + '\n'
    if id_at_end:
        fkey = '%s_id'
    else:
        fkey = 'id_%s'
    for el in adic['zlines']:
        if (adic['id'] == 0) or (adic['id'] == '') or (adic['id'] is None):
            el[fkey % tmaster] = ('(SELECT MAX(id) FROM %s)' % tmaster)
        else:
            el[fkey % tmaster] = adic['id']
        sql += sql_ins_upd(tdetail, el) + '\n'
    return 'BEGIN TRANSACTION;\n' + sql + 'COMMIT;\n'


def db2dic(tmaster, tdetail=None, anid=None):
    '''
    Returns dictionary from Database
    '''
    t = Db(os.path.join(PATH, 'tst.db'))
    det_id = '%s_id' % tmaster
    if anid:
        sql1 = "SELECT * FROM %s WHERE id='%s';" % (tmaster, anid)
    else:
        sql1 = "SELECT * FROM %s;" % tmaster
    master = t.rowsd(sql1)
    if tdetail:
        for el in master:
            sqlt = "SELECT * FROM %s WHERE %s='%s'"
            sql2 = sqlt % (tdetail, det_id, el['id'])
            det = t.rowsd(sql2)
            el['zlines'] = det
    return master


def getjson(tmaster, tdetail=None, eggrno=None):
    return json.dumps(db2dic(tmaster, tdetail, eggrno), ensure_ascii=False,
                      sort_keys=True,
                      indent=2,
                      separators=(',', ':'))


if __name__ == '__main__':
    ad = {'cat_id': 7, 'typ_id': 'normal', 'dat': '2016-10-04',
          'pno': u'ΤΔΑ105', 'ori_id': 'ell', 'afm': '046949583', 'pli_id': 1,
          'zlines': [{'lm_id': '20.01', 'pfpa': 13, 'val': 200, 'fpa': 26},
                     {'lm_id': '20.01', 'pfpa': 24, 'val': 200, 'fpa': 48},
                    ]
          }
    s = {'pli_id': 1,
         'afm': '046949947',
         'zlines': [{'lm_id': '70.00', 'val': dc('100.36'), 'pfpa': 0, 'fpa': dc('0.00')},
                    {'lm_id': '71.00', 'val': dc('100.12'), 'pfpa': 13, 'fpa': dc('13.02')},
                    {'lm_id': '73.00', 'val': dc('100.00'), 'pfpa': 24, 'fpa': dc('24.00')}
                    ],
         'pno': 'ΤΔΑ554',
         'cat_id': 7,
         'par_id': 1,
         'typ_id': 'normal',
         'ori_id': 'ell',
         'dat': '2016-10-01',
         'per': 'Πώληση 1'}
    # print(sql_ins_upd(tbl, ad))
    # print(md2sql(tbl, 'kid', ad))
    t = Db(os.path.join(PATH, 'tst.db'))
    # t.execute_script(md2sql('ki', 'kid', s))
    result = t.rowst("SELECT MAX(id) FROM ki;")[0][0]
    # aa = '\n'.join(map(str, sql2md(4)))
    print(getjson('ki', 'kid', result))
