from tedutil import model


if __name__ == '__main__':
    dbf = '/home/tedlaz/prj/django/src/db.sqlite3'
    tbl = 'tst'
    tst = model.Model(dbf, tbl)
    print(tst.fields)
    print(tst.save({'id': '', 'val1': 'Δοκιμή', 'val2': ''}))
    print(model.Model(dbf, 'mi_misthodosiatype').select_all_cols_rows)
    # print(sex.search('')[0])
    # erg = model.Model(dbf, 'mi_paroysiesdetails')
    # print(erg.fields)
    # print(erg.search_by_id(1))
