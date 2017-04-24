# -*- coding: utf-8 -*-
'''
Δημιουργία τρίμηνων xml αρχείων συγκεντρωτικών καταστάσεων Πελατών-Προμηθευτών
Προυποθέσεις:
Θα πρέπει να υπάρχει δημιουργημένο αρχείο sqlite με τα δεδομένα χρήσης
(ac-elee2sqlite πρόγραμμα)και να έχει γίνει μια βασική επεξεργασία για τις
εγγραφές που περιλαμβάνονται και αποκλείονται.
Για τις συγκεντρωτικές λιανικής θα πρέπει το πεδίο afm να είναι κενό.
Το ίδιο ισχύει για τις συγκεντρωτικές εξόδων (κουβάς).
'''
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
xtothe = '''    <otherExpenses>\n      <amount>{maj}</amount>\n      <tax>{mfpa}</tax>\n      <date>{dmonth}</date>\n    </otherExpenses>\n'''
xlcash = '''      <cashregister>\n        <cashreg_id></cashreg_id>\n        <amount>{maj}</amount>\n        <tax>{mfpa}</tax>\n        <date>{dmonth}</date>\n      </cashregister>\n'''
xlreve = '''      <revenue>\n        <afm>{afm}</afm>\n        <amount>{maj}</amount>\n        <tax>{mfpa}</tax>\n        <invoices>{no}</invoices>\n        <note>{note}</note>\n        <date>{dmonth}</date>\n      </revenue>\n'''
xlexpe = '''      <expense>\n        <afm>{afm}</afm>\n        <amount>{maj}</amount>\n        <tax>{mfpa}</tax>\n        <invoices>{no}</invoices>\n        <note>{note}</note>\n        <nonObl>0</nonObl>\n        <date>{dmonth}</date>\n      </expense>\n'''

grType = ['replace', 'incremental']
parType = ['credit', 'normal']
miYpoxreos = ['0', '1']

sqlt = '''select
case
  when dat between '{etos}-01-01' and '{etos}-03-31' then 0
  when dat between '{etos}-04-01' and '{etos}-06-30' then 1
  when dat between '{etos}-07-01' and '{etos}-09-30' then 2
  when dat between '{etos}-10-01' and '{etos}-12-31' then 3
  else 9
end as trimino,
case
  when dat between '{etos}-01-01' and '{etos}-03-31' then '{etos}-03-31'
  when dat between '{etos}-04-01' and '{etos}-06-30' then '{etos}-06-30'
  when dat between '{etos}-07-01' and '{etos}-09-30' then '{etos}-09-30'
  when dat between '{etos}-10-01' and '{etos}-12-31' then '{etos}-12-31'
  else '000-00-00'
end as dmonth,
case
  when length(afm) = 0 and eee=1 and typ=1 then '3.cashregister'
  when length(afm) = 9 and eee=1 and typ=1 then '1.revenue'
  when length(afm) = 0 and eee=1 and typ=2 then '4.expensegroup'
  when length(afm) = 9 and eee=1 and typ=2 then '2.expense'
  else '0.ektos'
end as typos,
eee, typ, afm,note, count(aji) as no, dec1(sum(aji)) as taj, dec1(sum(fpa)) as tfpa,  grdec(sum(maji)) as maj, grdec(sum(mfpa)) as mfpa
from ee
group by trimino, typos, eee, typ, afm, note
order by trimino, typos, eee, typ, afm, note
'''


def make_xml(database, xrisi, coafm, parartima='', xmltype='replace'):
    sql = sqlt.format(etos=xrisi)  # Δημιουργούμε την τελική sql
    data = dbselect(sql, database)  # Παίρνουμε τα δεδομένα απο την sqlite
    # Δημιουργούμε μεταβλητές για 4 τρίμηνα
    lcash = ['', '', '', '']
    lreve = ['', '', '', '']
    lexpe = ['', '', '', '']
    tothe = ['', '', '', '']
    # Αρχικοποιούμε τιμές για τα σύνολα
    esodaEktos = d1(0)
    fpaEsodonEktos = d1(0)
    ejodaEktos = d1(0)
    fpaEjodonEktos = d1(0)
    esodaMyf = d1(0)
    fpaEsodonMyf = d1(0)
    ejodaMyf = d1(0)
    fpaEjodonMyf = d1(0)
    for line in data:
        if line['eee'] == 0:  # Εκτός συγκεντρωτικής. Εδώ αθροίζουμε μόνο στα σύνολα
            if line['typ'] == 1:  # Έσοδα
                esodaEktos += d1(line['taj'])
                fpaEsodonEktos += d1(line['tfpa'])
            elif line['typ'] == 2:  # Έξοδα
                ejodaEktos += d1(line['taj'])
                fpaEjodonEktos += d1(line['tfpa'])
            else:
                print('error in line %' % line)
        elif line['eee'] == 1:  # Γραμμές συγκεντρωτικής
            if line['typ'] == 1:  # Έσοδα
                esodaMyf += d1(line['taj'])
                fpaEsodonMyf += d1(line['tfpa'])
                if line['typos'] == '1.revenue':
                    lreve[line['trimino']] += xlreve.format(**line)
                elif line['typos'] == '3.cashregister':
                    lcash[line['trimino']] += xlcash.format(**line)
                else:
                    print('error in line %' % line)
            elif line['typ'] == 2:  # Έξοδα
                ejodaMyf += d1(line['taj'])
                fpaEjodonMyf += d1(line['tfpa'])
                if line['typos'] == '2.expense':
                    lexpe[line['trimino']] += xlexpe.format(**line)
                elif line['typos'] == '4.expensegroup':
                    tothe[line['trimino']] += xtothe.format(**line)
            else:
                print('error in line %' % line)
        else:
            print('error in line %' % line)
        # Δημιουργούμε μεταβλητές για 4 τρίμηνα
        tcash = ['', '', '', '']
        trevs = ['', '', '', '']
        texps = ['', '', '', '']
        pdata = ['', '', '', '']
        tpack = ['', '', '', '']
        xmltr = ['', '', '', '']
    for i in range(4):
        if lcash[i]:
            tcash[i] = xtcash.format(xtype=xmltype, data=lcash[i])
        if lreve:
            trevs[i] = xtrevs.format(xtype=xmltype, data=lreve[i])
        if lexpe:
            texps[i] = xtexps.format(xtype=xmltype, data=lexpe[i])

        pdata[i] = '%s%s%s%s' % (trevs[i], texps[i], tcash[i], tothe[i])
        if pdata[i]:
            tpack[i] = xtpack.format(afm=coafm,
                                     minas=(i+1)*3,
                                     etos=xrisi,
                                     parar=parartima,
                                     data=pdata[i])
            xmltr[i] = xxmain.format(package=tpack[i])
            filename = '%s-%s-%s.xml' % (coafm, xrisi, i+1)
            with open(filename, 'w') as afile:
                afile.write(xmltr[i])
            print('file %s saved!!' % filename)

    print('Esoda ektos  : %14s fpa: %12s' % (esodaEktos, fpaEsodonEktos))
    print('Esoda se myf : %14s fpa: %12s' % (esodaMyf, fpaEsodonMyf))
    print('Synolo Esodon: %14s fpa: %12s' % (esodaEktos + esodaMyf, fpaEsodonEktos + fpaEsodonMyf))
    print('')
    print('Ejoda ektos  : %14s fpa: %12s' % (ejodaEktos, fpaEjodonEktos))
    print('Ejoda se myf : %14s fpa: %12s' % (ejodaMyf, fpaEjodonMyf))
    print('Synolo Ejodon: %14s fpa: %12s' % (ejodaEktos + ejodaMyf, fpaEjodonEktos + fpaEjodonMyf))
    return xmltr


if __name__ == '__main__':
    sql = sqlt.format(etos=2016)
    db = '/home/tedlaz/tedfiles/prj/samaras2016d/2016.sql3'
    #  print(dbselect(sql, db))
    make_xml(db, 2016, '091767623')
