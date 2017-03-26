# -*- coding: utf-8 -*-
import sql

mainXML = '<?xml version="1.0" encoding="UTF-8"?>\n<packages>\n{package}\n</packages>'
packageXML = '''  <package actor_afm="{coafm}" month="{minas}" year="{etos}" branch="{parartima}">\n{data} </package>'''
grType = ['replace', 'incremental']
grRevXML = '''    <groupedRevenues action="{grtype}">\n{revenues}    </groupedRevenues>\n'''
grExpXML = '''    <groupedExpenses action="{grtype}">\n{expenses}    </groupedExpenses>\n'''
grCasXML = '''    <groupedCashRegisters action="{grtype}">\n{tamiakes}    </groupedCashRegisters>\n'''
parType = ['credit', 'normal']
revXML = '''      <revenue>\n        <afm>{pelafm}</afm>\n        <amount>{poso}</amount>\n        <tax>{fpa}</tax>\n        <invoices>{no}</invoices>\n        <note>{partype}</note>\n        <date>{imnia}</date>\n      </revenue>\n'''
miYpoxreos = ['0', '1']
expXML = '''      <expense>\n        <afm>{proafm}</afm>\n        <amount>{poso}</amount>\n        <tax>{fpa}</tax>\n        <invoices>{no}</invoices>\n        <note>{partype}</note>\n        <nonObl>{miyp}</nonObl>\n        <date>{imnia}</date>\n      </expense>\n'''
casXML = '''      <cashregister>\n        <cashreg_id>{tamNo}</cashreg_id>\n        <amount>{poso}</amount>\n        <tax>{fpa}</tax>\n        <date>{imnia}</date>\n      </cashregister>\n'''
otherExpXML = '''    <otherExpenses>\n      <amount>{poso}</amount>\n      <tax>{fpa}</tax>\n      <date>{imnia}</date>\n    </otherExpenses>\n'''


#Το υποκατάστημα εφ'όσον στέλνουμε συγκεντρωτικά στοιχεία θα πρέπει να είναι κενό. Διαφορερικά 0 σημαίνει κεντρικό, 1 υποκατάστημα 1 κλπ
def main(data, afm, minas, etos, parartima=''):
    pack = packageXML.format(**{'coafm':afm, 'minas':minas, 'etos':etos, 'parartima':parartima, 'data':data})
    main = mainXML.format(**{'package':pack})
    return main


def revenues(lines, imnia):
    final   = ''
    details = ''
    for line in lines:
        line['imnia'] = imnia
        details += revXML.format(**line)
    if details:
        final += grRevXML.format(**{'grtype':grType[0], 'revenues': details})
    return final


def lianikes(lines, imnia):
    final   = ''
    details = ''

    for line in lines:
        line['imnia'] = imnia
        details += casXML.format(**line)

    if details:
        final += grCasXML.format(**{'grtype':grType[0], 'tamiakes': details})

    return final


def expenses(lines, imnia):
    final   = ''
    details = ''
    for line in lines:
        line['imnia'] = imnia
        details += expXML.format(**line)
    if details:
        final += grExpXML.format(**{'grtype':grType[0], 'expenses': details})
    return final


def otherExpenses(line, imnia):
    # line = {'poso':'1480,28', 'fpa':'145,03', 'imnia':'2014-09-30'}
    final   = ''
    details = ''
    if line:
        line['imnia'] = imnia
    else:
        return final

    final = otherExpXML.format(**line)
    return final


def makexml(eos, lrev, lxps, lian, loth, afm):
    year, month, day = eos.split('-')
    month = str(int(month))
    revs = revenues(lrev, eos)
    exps = expenses(lxps, eos)
    lian = lianikes(lian, eos)
    otherex = otherExpenses(loth, eos)
    xmldata = revs+exps+lian+otherex
    return main(xmldata, afm, month, year)


def makexmlFromDb(apo, eos, db, afm):
    lrev = sql.getGroupedRevenues(apo, eos, db)
    lian = sql.getGroupedCashRegisters(apo, eos, db)
    lxps = sql.getGroupedExpenses(apo, eos, db)
    loth = {}
    return makexml(eos, lrev, lxps, lian, loth, afm)


if __name__ == "__main__":
    print(makexmlFromDb('2015-10-01', '2015-12-31', 'pp-pp.sql3', '091767623'))
