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


class Myf():

    def __init__(self, db, afm):
        self.db = db
        self.afm = afm

    def _getData(self, sql):
        '''
        Get a list of dictionaries from Database
        '''
        con = sqlite3.connect(self.db)
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

    def _getSql(self, afile):
        # Get sql text from file
        txt = ''
        try:
            with open(afile) as fl:
                txt = fl.read()
        except:
            pass
        return txt

    def getGroupedRevenues(self, apo, eos):
        sqlNormal = self._getSql('grouprevennormal.sql') % (apo, eos)
        sqlCredit = self._getSql('grouprevencredit.sql') % (apo, eos)
        normal = self._getData(sqlNormal)
        credit = self._getData(sqlCredit)
        lrevs = sorted(normal + credit, key=lambda k: k['pelafm'])
        return lrevs

    def getGroupedCashRegisters(self, apo, eos):
        sql = self._getSql('groupcashregister.sql') % (apo, eos)
        return self._getData(sql)

    def getGroupedExpenses(self, apo, eos):
        sqlNormal = self._getSql('groupexpennormal.sql') % (apo, eos)
        sqlCredit = self._getSql('groupexpencredit.sql') % (apo, eos)
        normal = self._getData(sqlNormal)
        credit = self._getData(sqlCredit)
        lxps = sorted(normal + credit, key=lambda k: k['proafm'])
        return lxps

    def getOtherExpenses(self, apo, eos):
        return {}

    def tst(self, poso, fpa):
        poso = float(poso)
        fpa = float(fpa)
        kath = poso /(1.0 + fpa)
        print(grdec(kath), grdec(poso-kath))


if __name__ == '__main__':
    myf = Myf('./SygkentrotikesPelProm/pp-pp.sql3', '123123123')
    print(myf.getGroupedCashRegisters('2015-01-01', '2015-12-31'))
    print(myf.tst(12.3, .23))
