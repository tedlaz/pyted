# -*- coding: utf-8 -*-


# dic : OrderedDict
# tbl : table name
from collections import OrderedDict as odi


def _insert(tbl, dic):
    '''
    Returns sql of the form:
    'INSERT INTO TABLE(...) VALUES (...);'
    dic : dict of values {'fld1': 'val1', 'fld2': 'val2', ...}
    table : table name
    '''
    if not dic:
        print('sql_insert: dic is empty')
        return ''
    if not tbl:
        print('sql_insert: table is empty')
        return ''
    sql = "INSERT INTO %s (%s) VALUES (%s);"
    pfields = ''
    pvalues = ''
    for fld in dic.keys():
        if fld == 'id':
            continue
        pfields += '%s, ' % fld
        pvalues += "'%s', " % dic[fld]
    pfields = pfields[:-2]
    pvalues = pvalues[:-2]
    return sql % (tbl, pfields, pvalues)


def _update(tbl, dic):
    '''
    Update sql. dic must contain key='id'
    '''
    sql = "UPDATE %s set %s WHERE id=%s;"
    pfld_val = ''
    for fld in dic.keys():
        if fld == 'id':
            continue
        pfld_val += "%s='%s', " % (fld, dic[fld])
    pfld_val = pfld_val[:-2]
    return sql % (tbl, pfld_val, dic['id'])


def save(tbl, dic):
    '''
    Insert or Update according to id
    if id=0 or no id insert otherwise update
    '''
    id = dic.get('id', 0)
    if id == 0:
        return _insert(tbl, dic)
    else:
        return _update(tbl, dic)


def save_list(tbl, listdic):
    sql_list = []
    for dic in listdic:
        sql_list.append(save(tbl, dic))
    return sql_list


def save_many(tbl, listdic):
    sql = ''
    for el in save_list(tbl, listdic):
        sql += '%s\n' % el
    return sql


def save_many_tran(tbl, listdic):
    sql = "BEGIN TRANSACTION;\n"
    sql += save_many(tbl, listdic)
    sql += "COMMIT;"
    return sql


def select(tbl):
    return "SELECT * FROM %s" % tbl


def select_one(tbl, id):
    return "SELECT * FROM %s WHERE id=%s" % (tbl, id)


if __name__ == '__main__':
    dic = odi([('id', 0), ('epo', 'Laz'), ('ono', 'Ted')])
    tbl = 'emp'
    print(save(tbl, dic))
