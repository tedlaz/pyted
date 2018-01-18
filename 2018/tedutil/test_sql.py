from tedutil import sqlite as sql


if __name__ == '__main__':
    dd1 = sql.DataFromSqlite(('epo', 'ono'), (('laz', 'ted'), ('daz', 'pop')))
    print(dd1)
    print(dd1.as_list_of_dics)
    print(dd1.as_dict_of_dics)
    dd2 = sql.DataFromSqlite((), ())
    print(dd2)
    print(sql.create_sql('erg', ('id', 'epo', 'ono'), (1, 'ted', 'laz'), 2))
    print(dd1.first_row_only)