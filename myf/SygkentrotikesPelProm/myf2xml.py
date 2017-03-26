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


def dec(poso=0):
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
    return str(tmp.quantize(PLACES))

def d1(poso=0, decimals=2):
    def isNum(value):  # Einai to value arithmos, i den einai ?
        try:
            float(value)
        except ValueError:
            return False
        else:
            return True

    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


def dbselect(sql, db):
    con = sqlite3.connect(db)
    con.create_function("grdec", 1, grdec)
    con.create_function("dec1", 1, dec)
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

xxmain = '<?xml version="1.0" encoding="UTF-8"?>\n<packages>\n{package}\n</packages>'
xtpack = '''  <package actor_afm="{afm}" month="{minas}" year="{etos}" branch="{parar}">\n{data} </package>'''
xtcash = '''    <groupedCashRegisters action="{xtype}">\n{data}    </groupedCashRegisters>\n'''
xtrevs = '''    <groupedRevenues action="{xtype}">\n{data}    </groupedRevenues>\n'''
xtexps = '''    <groupedExpenses action="{xtype}">\n{data}    </groupedExpenses>\n'''
xtothe = '''    <otherExpenses>\n      <amount>{val}</amount>\n      <tax>{tax}</tax>\n      <date>{imnia}</date>\n    </otherExpenses>\n'''
xlcash = '''      <cashregister>\n        <cashreg_id>{tamNo}</cashreg_id>\n        <amount>{val}</amount>\n        <tax>{tax}</tax>\n        <date>{imnia}</date>\n      </cashregister>\n'''
xlreve = '''      <revenue>\n        <afm>{tafm}</afm>\n        <amount>{val}</amount>\n        <tax>{tax}</tax>\n        <invoices>{nu}</invoices>\n        <note>{pt}</note>\n        <date>{imnia}</date>\n      </revenue>\n'''
xlexpe = '''      <expense>\n        <afm>{tafm}</afm>\n        <amount>{val}</amount>\n        <tax>{tax}</tax>\n        <invoices>{nu}</invoices>\n        <note>{pt}</note>\n        <nonObl>{miyp}</nonObl>\n        <date>{imnia}</date>\n      </expense>\n'''


grType = ['replace', 'incremental']
parType = ['credit', 'normal']
miYpoxreos = ['0', '1']

sqlp = """select
myfc, typ, tafm,
grdec(sum(tposo)) as val,
grdec(sum(tfpa)) as tax,
dec1(sum(aji)) as daji,
dec1(sum(fpa)) as dfpa,
count(id) as nu,
partype as pt
from myf
where dat between '{papo}' and '{peos}'
group by myfc, tafm, partype
order by typ, myfc, tafm, partype desc;"""


class Myf2xml():
    def __init__(self, db, coafm):
        self.db = db  # Database με δεδομένα εσόδων εξόδων
        self.coafm = coafm  # ΑΦΜ εταιρείας
        # self.parartima = parartima  # Παράρτημα που αφορά

    def xml(self, apo, eos, parartima='', xmltype='replace'):
        '''
        xmltype : replace (default) or incremental
        '''
        sql = sqlp.format(papo=apo, peos=eos)
        data = dbselect(sql, self.db)

        lcash = ''
        lreve = ''
        lexpe = ''
        tothe = ''
        esval = d1(0)
        esfpa = d1(0)
        exval = d1(0)
        exfpa = d1(0)
        oesval = d1(0)
        oesfpa = d1(0)
        oexval = d1(0)
        oexfpa = d1(0)
        ca0 = d1(0)
        ca1 = d1(0)
        re0 = d1(0)
        re1 = d1(0)
        ex0 = d1(0)
        ex1 = d1(0)
        ot0 = d1(0)
        ot1 = d1(0)
        for lin in data:
            if lin['typ'] == 1:
                esval += d1(lin['daji'])
                esfpa += d1(lin['dfpa'])
            else:
                exval += d1(lin['daji'])
                exfpa += d1(lin['dfpa'])

            lin['imnia'] = eos

            if lin['myfc'] == 'cash':
                lin['tamNo'] = ''
                lcash += xlcash.format(**lin)
                ca0 += d1(lin['daji'])
                ca1 += d1(lin['dfpa'])
            elif lin['myfc'] == 'rev':
                lreve += xlreve.format(**lin)
                re0 += d1(lin['daji'])
                re1 += d1(lin['dfpa'])
            elif (lin['myfc'] == 'exp') and (lin['tafm'] != '000'):
                lin['miyp'] = '0'
                lexpe += xlexpe.format(**lin)
                ex0 += d1(lin['daji'])
                ex1 += d1(lin['dfpa'])
            elif (lin['myfc'] == 'exp') and (lin['tafm'] == '000'):
                tothe = xtothe.format(**lin)
                ot0 = d1(lin['daji'])
                ot1 = d1(lin['dfpa'])
            else:
                if lin['typ'] == 1:
                    oesval += d1(lin['daji'])
                    oesfpa += d1(lin['dfpa'])
                else:
                    oexval += d1(lin['daji'])
                    oexfpa += d1(lin['dfpa'])
        tcash = ''
        trevs = ''
        texps = ''
        if lcash:
            tcash = xtcash.format(xtype=xmltype, data=lcash)
        if lreve:
            trevs = xtrevs.format(xtype=xmltype, data=lreve)
        if lexpe:
            texps = xtexps.format(xtype=xmltype, data=lexpe)

        pdata = trevs + texps + tcash + tothe

        year, mm, day = eos.split('-')
        mm = str(int(mm))

        tpack = ''
        if pdata:
            tpack = xtpack.format(afm=self.coafm,
                                   minas=mm,
                                   etos=year,
                                   parar=parartima,
                                   data=pdata)
        print('MYF apo %s eos %s' % (apo, eos))
        print('Synolika Esoda : %12s fpa : %12s' % (esval, esfpa))
        print('Synolika Exoda : %12s fpa : %12s' % (exval, exfpa))
        print('\nSE MYF')
        print('Poliseis lian  : %12s fpa : %12s' % (ca0, ca1))
        print('Poliseis Xond  : %12s fpa : %12s' % (re0, re1))
        print('-' * 48)
        print('Poliseis Total : %12s fpa : %12s\n' % (ca0 + re0, ca1 + re1))
        print('Agores         : %12s fpa : %12s' % (ex0, ex1))

        print('Agores koybas  : %12s fpa : %12s' % (ot0, ot1))
        print('-' * 48)
        print('Agores Total   : %12s fpa : %12s\n' % (ex0 + ot0, ex1 + ot1))
        fpad = self.dfpa(apo, eos, parartima)
        print('FPA mi ekpipt  : %31s' % fpad)
        print('Agores Final   : %12s fpa : %12s\n' % (ex0 + ot0 - fpad, ex1 + ot1 + fpad))
        print('Ektos Myf')
        print('Synolika Esoda : %12s fpa : %12s' % (oesval, oesfpa))
        print('Synolika Exoda : %12s fpa : %12s' % (oexval, oexfpa))
        return xxmain.format(package=tpack)

    def dfpa(self, apo, eos, parartima=''):
        sql = """SELECT sum(abs(tfpa)) - sum(abs(fpa)) as fpad
                 from myf where dat between '{apo}' and '{eos}'
                 and typ=2;"""
        fpadelta = dbselect(sql.format(apo=apo, eos=eos), self.db)[0]['fpad']
        return d1(fpadelta)

    def xml2file(self, apo, eos, fname, parartima='', xmltype='replace'):
        xmldata = self.xml(apo, eos, parartima, xmltype)
        with open(fname, 'w') as afile:
            afile.write(xmldata)

if __name__ == "__main__":
    m2x = Myf2xml('pp-pp.sql3', '091767623')
    #m2x.xml('2015-01-01', '2015-12-31')
    #print(m2x.dfpa('2015-01-01', '2015-12-31'))
    m2x.xml2file('2015-04-01', '2015-06-30', '/home/tedlaz/20152.xml')
