# -*- coding: utf-8 -*-
import sqlite3
import os
from u_logger import log
from u_txt_num import grup, nul2z


def select(dbpath, sql, rows_as_dic=True):
    '''
    A select for every situation !!!
    Returns dictionary
    {
    'fields': columnNames,    List with field names.
    'labels': labels,         List with field labels
    'rows': listval,          List with rows as dictionary or as list
                              according to row_as_dic value.
    'rownum': number_of_rows, Integer holding number of rows.
    'as_dic': rows_as_dic     True if 'rows' is dictionary, False else.
    }
    '''
    if not os.path.exists(dbpath):
        log.error('select(): dbpath %s not exists' % dbpath)
        return {}
    if len(sql) < 10:
        log.error('select(): Wrong sql-> %s' % sql)
        return {}
    if sql[:6].upper() != 'SELECT':
        log.error('select(): sql (%s ) is not SELECT' % sql)
    try:
        con = sqlite3.connect(dbpath)
        # hook functions here
        con.create_function("grup", 1, grup)
        con.create_function("nul2z", 1, nul2z)
        # con.create_function('jget', 2, jget)
        cur = con.cursor()
        cur.execute(sql)
        columnNames = [t[0] for t in cur.description]
        rows = cur.fetchall()
    except sqlite3.Error as sqe:
        log.error('select(): %s' % sqe)
        rows = [[]]
        cur.close()
        con.close()
        return {}
    cur.close()
    con.close()
    listval = []
    number_of_rows = len(rows)
    for row in rows:
        if rows_as_dic:
            tdic = {}  # odi()  # Ordered dict
            for i, col in enumerate(row):
                tdic[columnNames[i]] = col
            listval.append(tdic)
        else:
            tlist = []
            for col in row:
                tlist.append(col)
            listval.append(tlist)

    log.debug('select(%s): Completed ;-)' % sql)
    return {'fields': columnNames,
            'rows': listval,
            'rownum': number_of_rows,
            'as_dic': rows_as_dic}
