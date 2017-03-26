import ted_util as tu
import ted_sqlite as ts
fil = 'tdf.sql3'

a1 = {'ikas': float(tu.dec(20.3456)), 'sk': 30, 'sg': 24, 'ted': 112.22}
a2 = {'ska': 12, 'ika': 12}
a3 = {'ted': 123, 'sk': 13.5, 'ika': 1}

sqlc = "create table if not exists test(id INTEGER PRIMARY KEY, xr, per, typ, erg, js);"
sqli = "insert into test values (null, ?, ?, ?, ?, ?);"
sqls = "select xr, per, typ, erg, p0(js, 'ted') as sk from test"
# ts.script_on_new_db(fil, sqlc)
ts.insertp(fil, sqli, ('2015', '01', '01', 'ted', ts.jd(a1)))
ts.insertp(fil, sqli, ('2015', '01', '01', 'popi', ts.jd(a2)))
ts.insertp(fil, sqli, ('2015', '01', '01', 'nikos', ts.jd(a3)))
vls = ts.select_with_functions(fil, sqls)

for li in vls:
    print("{xr} {per} {typ} {erg} {sk}".format(**li))
