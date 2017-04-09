'''
Module db_sql_create.py
Creates insert, update, delete sql from dictionaries
'''


def dic2sql(table, adic):
    '''
    Returns sql (insert, update, delete)
    table : The table name
    adic  : dictionary with key names same with table field names
    Returns :
     if id  = 0, insert sql
     if id != 0, update sql
     if there is a key in adic with name _d_(value unimportant) delete sql
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
    if '_d_' in adic:
        sql = 'DELETE FROM %s WHERE id=%s;'
        return sql % (table, adic['id'])
    if (adic['id'] == 0) or (adic['id'] == '') or (adic['id'] is None):
        sql = "INSERT INTO %s (%%s) VALUES (%%s);" % table
        return sql % (', '.join(fields), ', '.join(values))
    else:
        sql = "UPDATE %s SET %s WHERE id=%s;"
        return sql % (table, ', '.join(ufldva), adic['id'])


def dic2sql_md(tmaster, tdetail, adic, id_at_end=True):
    '''
    Returns sql inside transaction (insert, update, delete)
     for master-detail tables. It uses dic2sql
    tmaster : master table name
    tdetail : detail table name
    adic    : dictionary to translate to sql. Keys represent
              table fields
    id_at_end : if foreign key looks like id_* then False
                if foreign key looks like *_id then True
    '''
    sql = dic2sql(tmaster, adic) + '\n'
    if id_at_end:
        fkey = '%s_id'
    else:
        fkey = 'id_%s'
    for el in adic['zlines']:
        if (adic['id'] == 0) or (adic['id'] == '') or (adic['id'] is None):
            el[fkey % tmaster] = ('(SELECT MAX(id) FROM %s)' % tmaster)
            assert el.get('id', 0) == 0
        else:
            el[fkey % tmaster] = adic['id']
        # if master is marked for deletion do the same to detail
        if '_d_' in adic:
            el['_d_'] = 1
            assert 'id' in el
        sql += dic2sql(tdetail, el) + '\n'
    return 'BEGIN TRANSACTION;\n' + sql + 'COMMIT;'


if __name__ == '__main__':
    # Insert transaction
    adic = {'epo': 'Laz', 'ono': 'Ted',
            'zlines': [{'v': 1, 'k': 2}, {'v': 4, 'k': 5}]}
    print(dic2sql_md('tm', 'tmd', adic))
    # Update transaction
    bdic = {'id': 65, 'epo': 'Laz', 'ono': 'Ted',
            'zlines': [{'v': 1, 'k': 2}, {'v': 4, 'k': 5}]}
    print(dic2sql_md('tm', 'tmd', bdic))
    # Mixed transaction
    cdic = {'id': 85, 'epo': 'Laz', 'ono': 'Ted',
            'zlines': [{'id': 34, 'v': 1, 'k': 2, '_d_': 1}, {'v': 4, 'k': 5},
                       {'id': 15, 'v': 8, 'k': 9}]}
    # Delete transaction
    edic = {'id': 10, 'epo': 'Laz', 'ono': 'Ted', '_d_': 1,
            'zlines': [{'id': 65, 'v': 1, 'k': 2}, {'id': 66, 'v': 4, 'k': 5}]}
    print(dic2sql_md('tm', 'tmd', edic))
    # Using dic2sql insert, update, delete
    print(dic2sql('erg', {'epo': 'Lazaros', 'el_id': 34}))
    print(dic2sql('erg', {'id': 0, 'epo': 'Lazaros', 'el_id': 34}))
    print(dic2sql('erg', {'id': 20, 'epo': 'Lazaros', 'el_id': 34}))
    print(dic2sql('erg', {'id': 20, 'epo': 'Lazaros', 'el_id': 34, '_d_': 1}))
