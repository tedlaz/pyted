import sqlite3
from dec import dec


SQLPARN = "SELECT *, 'parn' as ptyp FROM parn WHERE xrisi='%s' AND minas='%s'"
SQLPARA = "SELECT *, 'para' as ptyp FROM para WHERE xrisi='%s' AND minas='%s'"
SQLPARY = "SELECT *, 'pary' as ptyp FROM pary WHERE xrisi='%s' AND minas='%s'"

'''
SELECT pro_id, max(sdat), substr(sdat, 1, 7) as etmon
FROM sym
WHERE etmon <= '2016-11'
GROUP BY pro_id
;
'''


def erg_data(ergid, year, month, dbf):
    '''
    Get tactical employee data for specific year, month
    '''
    assert month > 0
    assert month <= 12
    assert year > 2000
    pass


def getvals(sql, dbf):
    '''
    Get Values From Database
    Returns a list of dictionaries
    '''
    # print(sql)
    con = sqlite3.connect(dbf)
    cur = con.cursor()
    query = cur.execute(sql)
    colname = [d[0] for d in query.description]
    rlist = [dict(zip(colname, r)) for r in query.fetchall()]
    cur.close()
    con.close()
    return rlist


def getpar(xrisi, minas, dbf):
    '''
    Get parousies and organise per erg_id
    '''
    par = getvals(SQLPARN % (xrisi, minas), dbf)
    par += getvals(SQLPARA % (xrisi, minas), dbf)
    par += getvals(SQLPARY % (xrisi, minas), dbf)
    fdic = {}
    for dic in par:
        eid = dic['pro_id']
        fdic[eid] = fdic.get(eid, [])
        fdic[eid].append(dic)
    return fdic


def get_erg_data(erg, xrisi, minas, dbf):
    '''
    Get tactical data for ergnos
    '''
    return {'typ': 'imsth',
            'apod': 40,
            'nmeres':25,
            'kpk': 101,
            'pikae': 16,
            'pika': 35.00,
            'nwdays': 6,
            'nwhours': 40}


def calcmis(xrisi, minas, dbf):
    '''
    Calculate misthodosia
    '''
    fdic = getpar(xrisi, minas, dbf)
    print(fdic)
    for ergid in fdic:
        edata = get_erg_data(ergid, xrisi, minas, dbf)
        if edata['typ'] == 'misth':
            misthos = dec(edata['apod'])
            imsthio = dec(edata['apod'] / edata['nmeres'])
            ormisth = dec(imsthio * dec(edata['nwdays']) / dec(edata['nwhours']))
        elif edata['typ'] == 'imsth':
            misthos = dec(edata['apod'] * edata['nmeres'])
            imsthio = dec(edata['apod'])
            ormisth = dec(imsthio * dec(edata['nwdays']) / dec(edata['nwhours']))
        else:
            misthos = dec(0)
            imsthio = dec(0)
            ormisth = dec(0)
        print(imsthio)
        totalm = dec(0)
        for lin in fdic[ergid]:
            ptyp = lin['ptyp']
            if ptyp == 'parn':
                if edata['typ'] == 'misth':
                    apod = dec(dec(edata['apod']) * dec(lin['meres']) / dec(edata['nmeres']))

                elif edata['typ'] == 'imsth':
                    apod = dec(imsthio * dec(lin['meres']))
                print('Taktikes Apodoxes   : %s' % apod)
            elif ptyp == 'para':
                # imeromisthio * meres<3 / 2 + imeromisthio * meres>3
                apod = dec(dec(imsthio) * dec(lin['merl3']) / dec(2.0) + dec(imsthio) * dec(lin['merm3']))
                print('Apodoxes Astheneias : %s' % apod)
            totalm += apod
        print('Total Apod          : %s' % totalm)


if __name__ == '__main__':
    DBF = '/home/tedlaz/tedfiles/prj/mis2017'
    calcmis(2016, 12, DBF)
