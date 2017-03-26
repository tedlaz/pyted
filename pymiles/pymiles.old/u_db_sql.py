# -*- coding: utf-8 -*-

from u_logger import log
from u_txt_num import grup


def _insert(tbl, dic):
    '''
    tbl : table name
    dic : dict of values {'fld1': 'val1', 'fld2': 'val2', ...}
    Returns sql text of the form:
    'INSERT INTO TABLE(...) VALUES (...);'
    '''
    if not dic:
        log.error('_insert: dic is empty')
        return ''
    if not tbl:
        log.error('_insert: table is empty')
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
    tbl : tablename
    dic : dict of values {'fld1': 'val1', 'fld2': 'val2', ...}
    Returns sql text of the form:
    'UPDATE <tbl> SET fld1=val1, fld2=val2 WHERE id=?'
    '''
    if 'id' not in dic.keys():
        log.error("_update: dic must contain a key value = id")
        return ''
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
    tbl : tablename
    dic : dict of values {'fld1': 'val1', 'fld2': 'val2', ...}
    if id=0 or no id call _insert, otherwise call _update
    '''
    id = dic.get('id', 0)
    if id == '':
        id = 0
    if id == 0:
        return _insert(tbl, dic)
    else:
        return _update(tbl, dic)


def save_list(tbl, listdic):
    '''
    tbl : tablename
    listdic : a list of dictionaries like
    [
      {'fld1': 'val01', 'fld2': 'val02', ...},
      {'fld1': 'val11', 'fld2': 'val12', ...},
      ...
    ]
    From a tablename=tbl and a list of dictionaries holding table row values,
    create a list of save sql (update or insert) of the form:
    [
      'INSERT ...',
      'UPDATE ...',
      ...
    ]
    '''
    sql_list = []
    for dic in listdic:
        sql_list.append(save(tbl, dic))
    return sql_list


def save_many(tbl, listdic):
    '''
    tbl : tablename
    listdic : a list of dictionaries like
    [
      {'fld1': 'val01', 'fld2': 'val02', ...},
      {'fld1': 'val11', 'fld2': 'val12', ...},
      ...
    ]
    From a list of sql like save_list, create a text sql script of the form:
    '
    INSERT ...;
    UPDATE ...;
    INSERT ...;
    ..........;
    '
    '''
    sql = ''
    for el in save_list(tbl, listdic):
        sql += '%s\n' % el
    return sql


def save_many_tran(tbl, listdic):
    "Text sql script from save_many function in a transaction"
    sql = "BEGIN TRANSACTION;\n"
    sql += save_many(tbl, listdic)
    sql += "COMMIT;"
    return sql


def save_one_many(tblone, dicone, tblman, ldicma):
    '''
    tblone : tablename of master
    dicone : dictionary of master table values
    tblman : tablename of details
    ldicma : list of dictionaries of details
    Returns touple of the form:
    (
        "SELECT OR INSERT .......",  // Master data
        [
            "SELECT OR INSERT ...",  // Detail lines
            "SELECT OR INSERT ..."
        ]
    )
    '''
    master_id = dicone.get('id', 0)
    detail_id_name = tblone + '_id'
    # Every row dict should have detail_id_name
    for row in ldicma:
        did = row.get(detail_id_name, 0)
        if did == '0':
            did = 0
        if did == 0:
            if master_id:
                row[detail_id_name] = master_id
            else:
                row[detail_id_name] = '{idval}'
                if row['id']:
                    log.error('save_one_many: Only new records allowed')
                    return ('', '')
        else:
            if did != master_id:
                tst = 'save_one_many: %s(%s) sould be same as master_id(%s)'
                log.error(tst % (detail_id_name, did, master_id))
                return ('', '')
    sqlmaster = save(tblone, dicone)
    sqldetail = save_list(tblman, ldicma)
    return (sqlmaster, sqldetail)


def select_tbl(tbl):
    return "SELECT * FROM %s" % tbl


def select_tbl_id(tbl, id):
    return "SELECT * FROM %s WHERE id=%s" % (tbl, id)


def select_where(tbl, field_val={}):
    sql1 = "SELECT * FROM %s WHERE " % tbl
    for key in field_val.keys():
        sql1 += "grup(%s) LIKE '%%%s%%' AND " % (key, grup(field_val[key]))
    sql1 = sql1[:-4]
    return sql1


def select_sql_where(sql, field_val={}):
    sql1 = "%s WHERE " % sql
    if not field_val:
        return sql1
    for key in field_val.keys():
        sql1 += "grup(%s) LIKE '%%%s%%' AND " % (key, grup(field_val[key]))
    sql1 = sql1[:-4]
    return sql1

