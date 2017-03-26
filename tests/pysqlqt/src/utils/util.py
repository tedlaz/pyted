#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ted Lazaros
from pysqlqt import sqlite3_methods as sq3


def dict_from_db(sql, db):
    '''
    We need at least two columns from database.
    The first one becomes key and second one value
    to returning dictionary f
    '''
    result = sq3.dbRows({'sql': sql, 'db': db})
    f = {}
    if result['columnNumber'] < 2:
        return f
    for line in result['rows']:
        f[line[0]] = line[1]
    return f


def dict_with_def(dic, arr):
    '''
    Given a dictionary and an array returns a dictionary
    with key elements from array and values from dic if key exists
    otherwise array element
    '''
    f = {}
    for el in arr:
        f[el] = dic.get(el, el)
    return f


def lbls(fieldnames, db):
    '''
    Get field labels as dictionary with field names as keys.
    In case no label exists return field name.
    '''
    sql = 'SELECT fld, lbl FROM zfld'
    flabels = dict_from_db(sql, db)
    df = dict_with_def(flabels, fieldnames)
    return df


def dbrows_with_lbls(sql, db):
    '''
    We get a result dictionary, enrich it with labels (grlbl)
    and finally return it.
    '''
    result = sq3.dbRows({'sql': sql, 'db': db})
    if result['columnNames']:
        result['grlbl'] = lbls(result['columnNames'], db)
    return result


def compare_intervals(interval, control_interval):
    '''
    We have two intervals (pairs with start, end values where end >= start)
    We check first against second and we get 6 different positions as below:
    We also get True if they intersect , False otherwise.

    control_interval
    ---------------------|--------------------|-------------------------------

    interval
    1       |------|
    2       |------------------|
    3       |------------------------------------------|
    4                          |---------|
    5                          |-----------------------|
    6                                                  |------|
    '''
    d1, d2 = interval
    c1, c2 = control_interval
    assert d1 <= d2
    assert c1 <= c2
    if d2 < c1:
        return 1, False
    elif d1 < c1 and d2 >= c1 and d2 <= c2:
        return 2, True
    elif d1 < c1 and d2 > c2:
        return 3, True
    elif d1 >= c1 and d2 <= c2:
        return 4, True
    elif d1 >= c1 and d1 <= c2 and d2 > c2:
        return 5, True
    elif d1 > c2:
        return 6, False


if __name__ == '__main__':
    # db = 'doors.tst'
    # sql = 'select * from r_pro'
    # result = dbrows_with_lbls(sql, db)
    # print result
    in1 = ['2014-03-01', '2014-03-28']
    in2 = ['2014-02-10', '2014-02-23']
    print(compare_intervals(in2, in1))
    print(compare_intervals(in1, in2))
