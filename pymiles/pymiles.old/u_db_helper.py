# -*- coding: utf-8 -*-
import u_db_select as udbselect
import u_db_save as udbsave
import u_db_sql as usql


def table_vals(dbpath, table, asdic=True):
    # Returns all records from table
    return udbselect.select(dbpath, usql.select_tbl(table), asdic)


def table_val(dbpath, table, id_):
    # SELECT * FROM table WHERE id=id_
    return udbselect.select(dbpath, usql.select_tbl_id(table, id_))


def table_where(dbpath, table, wheredic, asdic=True):
    # SELECT * FROM table WHERE grup(fld1) LIKE %val1% AND grup(fld2) ...
    sql = usql.select_where(table, wheredic)
    return udbselect.select(dbpath, sql, asdic)


def table_fkey(dbpath, table, keyval, asdic=True):
    sql = "SELECT * FROM %s WHERE %s=%s" % (table, keyval[0], keyval[1])
    return udbselect.select(dbpath, sql, asdic)


def sql_where(dbpath, sql, wheredic):
    # SELECT * FROM table WHERE grup(fld1) LIKE %val1% AND grup(fld2) ...
    sql = usql.select_sql_where(sql, wheredic)
    return udbselect.select(dbpath, sql, False)


def save_listdic(dbpath, table, listdic):
    # listdict : a list of INSERT or UPDATE sql
    sql = usql.save_list(table, listdic)
    return udbsave.save(dbpath, sql)


def select(dbpath, sql):
    return udbselect.select(dbpath, sql)


def select_list(dbpath, sql):
    return udbselect.select(dbpath, sql, False)


if __name__ == '__main__':
    db = 'tst.sql3'
    sql = "SELECT * FROM eid"
    # print(udbs.select(db, sql))
    # print(table_val(db, 'eid', 0))
    wher = {'eidp': u'κ', 'eidk': '0'}
    # print(table_vals(db, 'eid'))
    print(table_where(db, 'eid', wher))
