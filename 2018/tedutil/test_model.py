from tedutil import model


if __name__ == '__main__':
    dbf = '/home/tedlaz/prj/pyted/2018/tedutil/aa.sql3'
    # tbl = 'ergazomenos'
    # tst = model.Model(dbf, tbl)
    # print(tst.fields)
    # print(tst.save({'id': '', 'val1': 'Δοκιμή', 'val2': ''}))
    # print(model.Model(dbf, 'mi_misthodosiatype').select_all_cols_rows)
    # print(sex.search('')[0])
    # erg = model.Model(dbf, 'mi_paroysiesdetails')
    # print(erg.fields)
    # print(erg.search_by_id(1))
    # oik = model.Model(dbf, 'oikogkat')
    # print(oik.search_by_id(1))
    # print(model.field_lbl(dbf, 'id'))
    # print(model.table_metadata(dbf, 'xrisi'))
    print(model.table_rpr(dbf, 'ergazomenos', 1))
    erg = model.Model(dbf, 'parartima')
    print(erg.rpr(1))
