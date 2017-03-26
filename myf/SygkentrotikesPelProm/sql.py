# -*- coding: utf-8 -*-
import sqlite3
import decimal


def grdec(poso=0):
    def isNum(value):  # Einai to value arithmos, i den einai ?
        try:
            float(value)
        except ValueError:
            return False
        else:
            return True

    PLACES = decimal.Decimal(10) ** (-1 * 2)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    tmp = str(tmp.quantize(PLACES))
    return tmp.replace('.', ',')


sqlxps = '''select afm as proafm, grdec(sum(aji)) as poso, grdec(sum(fpa)) as fpa,
 count(afm) as no, 'normal' as partype, '0' as miyp
from pp
where (teg='ΤΑΓ' or teg='ΛΟΙΠΑ1') and (dat between '%s' and '%s')
group by afm
order by afm;
'''

sqlxpsr = '''select afm as proafm, grdec(sum(aji) * -1) as poso,
 grdec(sum(fpa) * -1) as fpa, count(afm) as no, 'credit' as partype, '0' as miyp
from pp
where (teg='ΠΑΓ' or teg='ΛΟΙΠΑ1Π') and (dat between '%s' and '%s')
group by afm
order by afm;
'''

sqlotherxps = '''select grdec(sum(aji)) as poso, rdec(sum(fpa)) as tfpa
from pp
where teg='ΛΟΙΠΑ' and (dat between '%s' and '%s') and (fpa <> 0)
group by afm
order by afm;
'''

sqlrev = u'''select afm as pelafm, grdec(sum(aji)) as poso,
 grdec(sum(fpa)) as fpa, count(afm) as no, 'normal' as partype
from pp
where (teg='ΤΠΛ' or teg='ΤΠΥ')  and (dat between '%s' and '%s')
group by afm
order by afm;
'''

sqlrevr = u'''select afm as pelafm, grdec(sum(aji) * -1) as poso,
 grdec(sum(fpa) * -1) as fpa, count(afm) as no, 'credit' as partype
from pp
where (teg='ΠΙΣ' or teg='ΤΠΕ')  and (dat between '%s' and '%s')
group by afm
order by afm;
'''

sqllian = u'''select '' as tamNo, grdec(sum(aji)) as poso, grdec(sum(fpa)) as fpa
from pp
where (teg='ΑΠΛ' or teg='ΑΠΥ' or teg='ΕΠΛ')  and dat between '%s' and '%s';'''


def getArrayOfDictionaries(sql, db):
    con = sqlite3.connect(db)
    con.create_function("grdec", 1, grdec)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    con.close()
    arrayOfDictionaries = []
    for row in rows:
        arrayOfDictionaries.append(dict(zip(row.keys(), row)))
    return arrayOfDictionaries

def getGroupedExpenses(apo, eos, db):
    sql1 = sqlxps % (apo, eos)
    sql2 = sqlxpsr % (apo, eos)
    normal = getArrayOfDictionaries(sql1, db)
    credit = getArrayOfDictionaries(sql2, db)
    lxps = sorted(normal + credit, key=lambda k: k['proafm'])
    return lxps


def getGroupedRevenues(apo, eos, db):
    sql1 = sqlrev % (apo, eos)
    sql2 = sqlrevr % (apo, eos)
    normal = getArrayOfDictionaries(sql1, db)
    credit = getArrayOfDictionaries(sql2, db)
    # lrevs = normal + credit
    lrevs = sorted(normal + credit, key=lambda k: k['pelafm'])
    return lrevs

def getGroupedCashRegisters(apo, eos, db):
    sql = sqllian % (apo, eos)
    return (getArrayOfDictionaries(sql, db))


if __name__ == "__main__":
    db = 'pp-pp.sql3'
    apo = '2015-12-01'
    eos = '2015-12-31'
    print(getGroupedExpenses(apo, eos, db))
