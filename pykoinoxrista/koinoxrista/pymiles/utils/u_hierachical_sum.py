# -*- coding: utf-8 -*-

sqlx = '''
SELECT
    lmo.lmo,
    lmo.lmop,
    sum(CASE WHEN tr.dat<'{apo}'  THEN trd.xr END) as bxr,
    sum(CASE WHEN tr.dat<'{apo}'  THEN trd.pi END) as bpi,
    sum(CASE WHEN tr.dat>='{apo}' AND tr.dat<='{eos}' THEN trd.xr END) as pxr,
    sum(CASE WHEN tr.dat>='{apo}' AND tr.dat<='{eos}' THEN trd.pi END) as ppi,
    sum(CASE WHEN tr.dat>'{eos}'  THEN trd.xr END) as axr,
    sum(CASE WHEN tr.dat>'{eos}'  THEN trd.pi END) as api
FROM trd
INNER JOIN lmo ON lmo.id=trd.id_lmo
INNER JOIN tr ON tr.id=trd.id_tr
GROUP BY lmo.lmo
'''

sqle = '''
SELECT
    lmo.lmo,
    lmo.lmop,
    sum(CASE WHEN tr.dat>='{y}-01-01' AND tr.dat<='{y}-01-31' THEN trd.xr END) as xr01,
    sum(CASE WHEN tr.dat>='{y}-01-01' AND tr.dat<='{y}-01-31' THEN trd.pi END) as pi01,
    sum(CASE WHEN tr.dat>='{y}-02-01' AND tr.dat<='{y}-02-29' THEN trd.xr END) as xr02,
    sum(CASE WHEN tr.dat>='{y}-02-01' AND tr.dat<='{y}-02-29' THEN trd.pi END) as pi02,
    sum(CASE WHEN tr.dat>='{y}-03-01' AND tr.dat<='{y}-03-31' THEN trd.xr END) as xr03,
    sum(CASE WHEN tr.dat>='{y}-03-01' AND tr.dat<='{y}-03-31' THEN trd.pi END) as pi03,
    sum(CASE WHEN tr.dat>='{y}-04-01' AND tr.dat<='{y}-04-30' THEN trd.xr END) as xr04,
    sum(CASE WHEN tr.dat>='{y}-04-01' AND tr.dat<='{y}-04-30' THEN trd.pi END) as pi04,
    sum(CASE WHEN tr.dat>='{y}-05-01' AND tr.dat<='{y}-05-31' THEN trd.xr END) as xr05,
    sum(CASE WHEN tr.dat>='{y}-05-01' AND tr.dat<='{y}-05-31' THEN trd.pi END) as pi05,
    sum(CASE WHEN tr.dat>='{y}-06-01' AND tr.dat<='{y}-06-30' THEN trd.xr END) as xr06,
    sum(CASE WHEN tr.dat>='{y}-06-01' AND tr.dat<='{y}-06-30' THEN trd.pi END) as pi06,
    sum(CASE WHEN tr.dat>='{y}-07-01' AND tr.dat<='{y}-07-31' THEN trd.xr END) as xr07,
    sum(CASE WHEN tr.dat>='{y}-07-01' AND tr.dat<='{y}-07-31' THEN trd.pi END) as pi07,
    sum(CASE WHEN tr.dat>='{y}-08-01' AND tr.dat<='{y}-08-31' THEN trd.xr END) as xr08,
    sum(CASE WHEN tr.dat>='{y}-08-01' AND tr.dat<='{y}-08-31' THEN trd.pi END) as pi08,
    sum(CASE WHEN tr.dat>='{y}-09-01' AND tr.dat<='{y}-09-31' THEN trd.xr END) as xr09,
    sum(CASE WHEN tr.dat>='{y}-09-01' AND tr.dat<='{y}-09-31' THEN trd.pi END) as pi09,
    sum(CASE WHEN tr.dat>='{y}-10-01' AND tr.dat<='{y}-10-31' THEN trd.xr END) as xr10,
    sum(CASE WHEN tr.dat>='{y}-10-01' AND tr.dat<='{y}-10-31' THEN trd.pi END) as pi10,
    sum(CASE WHEN tr.dat>='{y}-11-01' AND tr.dat<='{y}-11-31' THEN trd.xr END) as xr11,
    sum(CASE WHEN tr.dat>='{y}-11-01' AND tr.dat<='{y}-11-31' THEN trd.pi END) as pi11,
    sum(CASE WHEN tr.dat>='{y}-12-01' AND tr.dat<='{y}-12-31' THEN trd.xr END) as xr12,
    sum(CASE WHEN tr.dat>='{y}-12-01' AND tr.dat<='{y}-12-31' THEN trd.pi END) as pi12
FROM trd
INNER JOIN lmo ON lmo.id=trd.id_lmo
INNER JOIN tr ON tr.id=trd.id_tr
GROUP BY lmo.lmo
'''


def sqlapeos(dt, sf, apo, eos, re, n2z=False):
    '''
    dt : date field
    sf : numeric field to sum
    apo: Date >=
    eos: Date <=
    re : result field name
    '''
    sql = "sum(CASE WHEN {dt}>='{apo}' AND {dt}<='{eos}' THEN {sf} END') as {re}"
    sql = sql.format(dt=dt, sf=sf, apo=apo, eos=eos, re=re)
    if n2z:
        sql = 'nul2z(%s)' % sql
    return sql

def sql_month(dt, sf, etos, n2z=False):
    da = []
    da.append(('%s-01-01' % etos, '%s-01-31' % etos, '%s01' % sf))
    da.append(('%s-02-01' % etos, '%s-02-29' % etos, '%s02' % sf))
    da.append(('%s-03-01' % etos, '%s-03-31' % etos, '%s03' % sf))
    da.append(('%s-04-01' % etos, '%s-04-30' % etos, '%s04' % sf))
    da.append(('%s-05-01' % etos, '%s-05-31' % etos, '%s05' % sf))
    da.append(('%s-06-01' % etos, '%s-06-30' % etos, '%s06' % sf))
    da.append(('%s-07-01' % etos, '%s-07-31' % etos, '%s07' % sf))
    da.append(('%s-08-01' % etos, '%s-08-31' % etos, '%s08' % sf))
    da.append(('%s-09-01' % etos, '%s-09-30' % etos, '%s09' % sf))
    da.append(('%s-10-01' % etos, '%s-10-31' % etos, '%s10' % sf))
    da.append(('%s-11-01' % etos, '%s-11-30' % etos, '%s11' % sf))
    da.append(('%s-12-01' % etos, '%s-12-31' % etos, '%s12' % sf))
    sql = ''

    for el in da:
        sql += '%s,\n' % sqlapeos(dt, sf, el[0], el[1], el[2], n2z)
    return sql[:-2]


def sql_dim(dt, sf, etos, n2z=False):
    da = []
    da.append(('%s-01-01' % etos, '%s-02-29' % etos, '%s1di' % sf))
    da.append(('%s-03-01' % etos, '%s-04-30' % etos, '%s2di' % sf))
    da.append(('%s-05-01' % etos, '%s-06-30' % etos, '%s3di' % sf))
    da.append(('%s-07-01' % etos, '%s-08-31' % etos, '%s4di' % sf))
    da.append(('%s-09-01' % etos, '%s-10-31' % etos, '%s5di' % sf))
    da.append(('%s-11-01' % etos, '%s-12-31' % etos, '%s6di' % sf))
    sql = ''

    for el in da:
        sql += '%s,\n' % sqlapeos(dt, sf, el[0], el[1], el[2], n2z)
    return sql[:-2]


def sql_trim(dt, sf, etos, n2z=False):
    da = []
    da.append(('%s-01-01' % etos, '%s-03-31' % etos, '%s1tr' % sf))
    da.append(('%s-04-01' % etos, '%s-06-30' % etos, '%s2tr' % sf))
    da.append(('%s-07-01' % etos, '%s-09-30' % etos, '%s3tr' % sf))
    da.append(('%s-10-01' % etos, '%s-12-31' % etos, '%s4tr' % sf))
    sql = ''

    for el in da:
        sql += '%s,\n' % sqlapeos(dt, sf, el[0], el[1], el[2], n2z)
    return sql[:-2]


def sql_apo_eos(sql, tapo, teos):
    return sql.format(apo=tapo, eos=teos)


def sql_etos(sql, etos='2014'):
    return sql.format(y=etos)

def adddic(d1, d2):
    f = {}
    for key in d1.keys():
        f[key] = d1[key] + d2[key]
    return f


def zerodic(d1):
    f = {}
    for key in d1.keys():
        f[key] = 0
    return f


def calc(datadic, levels=[1, 2, 5, 8]):
    for key in datadic.keys():
        f = {}
        for bkey in datadic[key].keys():
            f[bkey] = datadic[key][bkey]
        for level in levels:
            hkey = key[:level]
            datadic[hkey] = adddic(datadic.get(hkey, zerodic(f)), f)
        datadic['0'] = adddic(datadic.get('0', zerodic(f)), f)
    return datadic


if __name__ == '__main__':
    vals = {'38.00.00.0000': {'val1': 100, 'val2': 20},
            '38.03.00.0000': {'val1': 15, 'val2': 130},
            '38.03.00.0001': {'val1': 11, 'val2': 111},
            '50.00.00.0000': {'val1': 110, 'val2': 67}}
    tval = calc(vals)
    for key in sorted(tval.keys()):
        print(key, tval[key])

    print(sql_apo_eos(sqlx, '2014-01-01', '2014-12-31'))

    print(sql_etos(sqle, '2014'))
    print(sql_month('dat', 'pi', '2015', n2z=False))
    print(sql_dim('dat', 'pi', '2015', n2z=False))
    print(sql_trim('dat', 'pi', '2015', n2z=False))
