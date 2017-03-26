# -*- coding: utf-8 -*-
from dec2str import dec2str as d2s


class Matrix():

    def __init__(self, rows=[], cols=[]):
        self.totaltitle = 'Total'
        self.minsize = len(self.totaltitle)
        self.rows = rows
        self.cols = cols
        self.vals = {}
        # Totals
        self.trows = {}
        for el in self.rows:
            self.trows[el] = 0
        self.tcols = {}
        for el in self.cols:
            self.tcols[el] = 0
        self.total = 0

    def addcol(self, col):
        if col not in self.cols:
            self.cols.append(col)
            self.tcols[col] = 0

    def addcolv(self, col, dval):
        self.addcol(col)
        for key in sorted(dval.keys()):
            self.addrow(key)
            self.setval(key, col, dval[key])
        self.rows.sort()
        self.cols.sort()

    def addrow(self, row):
        if row not in self.rows:
            self.rows.append(row)
            self.trows[row] = 0

    def setval(self, row, col, val):
        assert row in self.rows
        assert col in self.cols
        # Εάν η val είναι μηδέν, μην κάνεις τίποτα.
        if val == 0:
            return
        self.vals[row] = self.vals.get(row, {})
        self.vals[row][col] = self.vals[row].get(col, 0)

        # Εάν υπάρχει ήδη τιμή την αφαιρούμε από τα αθροίσματα
        if self.vals[row][col] != 0:
            oldv = self.vals[row][col]
            self.trows[row] -= oldv
            self.tcols[col] -= oldv
            self.total -= oldv
        self.vals[row][col] = val
        self.trows[row] += val
        self.tcols[col] += val
        self.total += val

    def getval(self, row, col):
        assert row in self.rows
        assert col in self.cols
        val1 = self.vals.get(row, {col: 0})
        return val1.get(col, 0)

    def getcol(self, col):
        val = []
        for row in self.rows:
            val.append(self.getval(row, col))
        return val

    def getcold(self, col):
        dval = {}
        for row in self.rows:
            dval[row] = self.getval(row, col)
        return dval

    def sumcol(self, col):
        assert col in self.cols
        return self.tcols[col]

    def colsize(self):
        csiz = {}
        for col in self.cols:
            csiz[col] = len(str(col))  # Αρχικό μέγεθος το όνομα της στήλης
            tsiz = len(d2s(self.sumcol(col)))
            if csiz[col] < tsiz:
                csiz[col] = tsiz
        return csiz

    def colformat(self):
        csiz = self.colsize()
        cformat = {}
        for key in csiz.keys():
            cformat[key] = '%%%ss  ' % csiz[key]
        return cformat

    def totalsformat(self):
        lent = len(d2s(self.total))
        if lent < self.minsize:
            lent = self.minsize
        return '%%%ss \n' % lent

    def rowtitlesformat(self):
        maxr = max([len(str(i)) for i in self.rows])
        if maxr < self.minsize:
            maxr = self.minsize
        return '%%%ss  ' % maxr

    def sumrow(self, row):
        assert row in self.rows
        return self.trows[row]

    def __str__(self):
        cformat = self.colformat()
        ttitl = self.totaltitle
        hrow = self.rowtitlesformat()
        htot = self.totalsformat()
        ast = hrow % ' '
        # print titles
        for col in self.cols:
            ast += cformat[col] % col
        ast += htot % ttitl
        for row in self.rows:
            ast += hrow % row
            for col in self.cols:
                ast += cformat[col] % d2s(self.getval(row, col))
            ast += htot % d2s(self.sumrow(row))
        ast += hrow % ttitl
        for col in self.cols:
            scol = self.sumcol(col)
            ast += cformat[col] % d2s(scol)
        ast += htot % d2s(self.total)
        return ast

if __name__ == '__main__':
    m = Matrix(['d1', 'd2', 'd3', 'd4', 'd5'], ['alpha', 'b', 'c'])
    m.setval('d1', 'alpha', 584526.78)
    m.setval('d1', 'c', 50)
    m.setval('d2', 'alpha', 662538.44)
    m.setval('d2', 'alpha', 5)
    m.setval('d3', 'b', 100.45)
    m.setval('d3', 'c', 80362.44)
    m.addcol('theta')
    m.addrow('d36')
    m.setval('d36', 'alpha', 765344.22)
    m.setval('d36', 'theta', 65)
    m.setval('d1', 'theta', 44)
    k = Matrix()
    k.addcolv('thermansi', {'d1': 275, 'd3': 340, 'd4': 300, 'd5': 85})
    k.addcolv('asanser', {'d1': 320, 'd2': 260, 'd4': 320, 'd5': 100})
    print(k)
    dist = k.getcold('asanser')
    from distd import distd
    print(distd(50, dist))

