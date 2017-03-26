# -*- coding: utf-8 -*-
import decimal
import random

def dec(poso=0, decimals=2):
    """ use : Given a number, it returns a decimal with a specific number
        of decimals
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or
                int ..)
            2.decimals : The number of decimals (default 2)
        output: A decimal number
        """
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


def triades(txt, separator='.'):
    '''
    Help function to split digits to thousants ( 123456 becomes 123.456 )
    '''
    ltxt = len(txt)
    rem = ltxt % 3
    precSpace = 3 - rem
    stxt = ' ' * precSpace + txt
    a = []
    while len(stxt) > 0:
        a.append(stxt[:3])
        stxt = stxt[3:]
    a[0] = a[0].strip()
    fval = ''
    for el in a:
        fval += el + separator
    return fval[:-1]


def grd(poso, decimals=2):
    '''
    Returns string with Greek Formatted decimal (12345.67 becomes 12.345,67)
    '''
    prosimo = ''
    strposo = str(poso)
    if len(strposo) > 0:
        if strposo[0] in '-':
            prosimo = '-'
            strposo = strposo[1:]
    timi = '%s' % dec(strposo, decimals)
    intpart, decpart = timi.split('.')
    final = triades(intpart) + ',' + decpart
    if dec(poso) == dec(0):
        prosimo = ''
    if final[0] == '.':
        final = final[1:]
    return prosimo + final

'''
Για τη λογιστική θα πρέπει να ορίσουμε την έννοια των διαφορετικού τύπου λογαριασμών

0. Λογαριασμοί Τάξεως# -*- coding: utf-8 -*-
1. Λογαριασμοί Παγίων
2. Λογαριασμοί Αποθεμάτων
3. Λογαριασμοί Απαιτήσεων
4. Λογαριασμοί Κεφαλαίου
5. Λογαριασμοί Υποχρεώσεων
6. Λογαριασμοί Εξόδimport decimalων
7. Λογαριασμοί Εξόδων
8. Λογαριασμοί Αποτελεσμάτων
'''


class Tran():
    def __init__(self, no, dat, par, per):
        self.no = no
        self.dat = dat
        self.par = par
        self.per = per
        self._lines = []
        self._lineno = 0
        self._txr = dec(0)
        self._tpi = dec(0)

    def ypol(self):
        if self._txr > self._tpi:
            return (1, self._txr - self._tpi)
        elif self._txr < self._tpi:
            return (-1, self._tpi - self._txr)
        else:
            return (0, 0)

    def newline(self, lmos, xr, pi):
        self._lines.append([lmos, dec(xr), dec(pi)])
        self._lineno += 1
        self._txr += dec(xr)
        self._tpi += dec(pi)

    def transfer(self, lmoxr, lmopi, poso):
        self.newline(lmoxr, poso, 0)
        self.newline(lmopi, 0, poso)

    def boundx(self, lmo1, lmo2, pc, poso):
        self.newline(lmo1, poso, 0)
        val = dec(dec(poso) * dec(pc / 100.0))
        self.newline(lmo2, val, 0)
        return val

    def boundp(self, lmo1, lmo2, pc, poso):
        self.newline(lmo1, 0, poso)
        val = dec(dec(poso) * dec(pc / 100.0))
        self.newline(lmo2, 0, val)
        return val

    def final(self, lmos):
        if self._lineno == 0:
            return None
        ypt, yp = self.ypol()
        if ypt == 1:
            self.newline(lmos, 0, yp)
        elif ypt == -1:
            self.newline(lmos, yp, 0)


    def __str__(self):
        tmpl = 'Tran no: %s\nDate   : %s\nPar    : %s\nPer    : %s\n'
        lmpl = '%20s %16s %16s \n'
        st = tmpl % (self.no, self.dat, self.par, self.per)
        for line in self._lines:
            st += lmpl % (line[0], grd(line[1]), grd(line[2]))
        st += lmpl % ('-' * 20, '-' * 16, '-' * 16)
        st += lmpl % ('Totals', grd(self._txr), grd(self._tpi))
        return st


class Ledger():
    def __init__(self):
        self.transactions = []
        self.pp = []
        self.no = 0

    def add(self, trans):
        self.no += 1
        trans.no = self.no
        self.transactions.append(trans)

    def __str__(self):
        st = ''
        for tran in self.transactions:
            st += '%s \n' % tran.__str__()
        return st

    def autonum(self):
        for i, el in enumerate(self.transactions):
            el.no = i + 1

    def sort(self):
        self.transactions = sorted(self.transactions, key=lambda tr: tr.dat)
        self.autonum()

    def balance(self, apo=None, eos=None):
        bs = {}
        for tr in self.transactions:
            dat = tr.dat
            if apo:
                if dat >= apo:
                    pass
                else:
                    continue
            if eos:
                if dat <= eos:
                    pass
                else:
                    continue
            for lin in tr._lines:
                lmo = lin[0]
                xr = lin[1]
                pi = lin[2]
                oxr, opi = bs.get(lmo, [dec(0),dec(0)])
                bs[lmo] = [xr + oxr, pi + opi]
        return bs

    def prbal(self, apo=None, eos=None):
        sba = self.balance(apo, eos)
        tmpl = '%20s %16s %16s %16s'
        if not apo:
            apo = 'Arxi'
        if not eos:
            eos = 'Telos'
        print('Isozygio logariasmon apo:%s eos:%s' % (apo, eos))
        for lmo in sorted(sba.keys()):
            yp = grd(sba[lmo][0] - sba[lmo][1])
            print(tmpl % (lmo, grd(sba[lmo][0]), grd(sba[lmo][1]), yp))

    def kartella(self, lmos, apo=None, eos=None):
        lar = []
        llmo = len(lmos)
        for tran in self.transactions:
            dat = tran.dat
            par = tran.par
            if apo:
                if dat >= apo:
                    pass
                else:
                    continue
            if eos:
                if dat <= eos:
                    pass
                else:
                    continue
            for lin in tran._lines:
                if lmos == lin[0][:llmo]:
                    lar.append([dat, par, lin[1], lin[2], lin[0]])
        return lar

    def prkartella(self, lmos, apo=None, eos=None):
        tmpl = '%10s %12s %16s %16s %16s  (%s)'
        kart = self.kartella(lmos, apo, eos)
        if not apo:
            apo = 'Arxi'
        if not eos:
            eos = 'Telos'
        print('\nKartella logariasmoy %s apo:%s eos:%s' % (lmos, apo, eos))
        ypol = dec(0)
        for el in kart:
            ypol = ypol + el[2] - el[3]
            print(tmpl % (el[0], el[1], grd(el[2]), grd(el[3]), grd(ypol), el[4]))

    def ag1323(self, im, par, prom, p13, p23):
        tr = tran(0, im, par, 'Agores emporefmaton')
        if p13 != 0:
            tr.boundx('20.00.2013', '54.00.2013', 13, p13)
        if p23 != 0:
            tr.boundx('20.00.2023', '54.00.2023', 23, p23)
        tr.final(prom)
        self.add(tr)


    def ag1323m(self, im, par, promafm, p13, p23):
        prom ='50.00.%s' % promafm
        tr = Tran(0, im, par, 'Agores emporefmaton metritois')
        if p13 != 0:
            tr.boundx('20.01.2013', '54.00.2013', 13, p13)
        if p23 != 0:
            tr.boundx('20.01.2023', '54.00.2023', 23, p23)
        ty, ypol = tr.ypol()
        tr.final(prom)
        tr.transfer(prom, '38.00.0000', ypol)
        self.add(tr)


    def pol23(self, im, par, pelatisafm, poso):
        pelatis = '30.00.%s' % pelatisafm
        tr = Tran(0, im, par, 'poliseis 23%')
        tr.boundp('70.00.7023', '54.00.7023', 23, poso)
        tr.final(pelatis)
        self.add(tr)

    def pollian23(self, im, par, poso):
        tr = Tran(0, im, par, 'poliseis Lianikis 23%')
        tr.boundp('70.00.7123', '54.00.7123', 23, poso)
        tr.final('38.00.0000')
        self.add(tr)

    def pol13(self, im, par, pelatis, poso):
        tr = Tran(0, im, par, 'poliseis 13%')
        tr.boundp('70.00.7013', '54.00.7013', 13, poso)
        tr.final(pelatis)
        self.add(tr)

    def metaf(self, im, par, apo, se, poso):
        tr = Tran(0, im, par, 'Metafora posoy')
        tr.transfer(apo, se, poso)
        self.add(tr)


def randate(xrisi):
    minas = '%s' % random.randint(1, 12)
    mera = '%s' %random.randint(1, 31)
    if len(minas) == 1:
        minas = '0' + minas

    if len(mera) == 1:
        mera = '0' + mera
    if minas in ('04', '06', '09', '11') and mera == '31':
        mera = '30'
    if minas == '02' and int(mera) > 28:
        mera = '28'
    return '%s-%s-%s' % (xrisi, minas, mera)


if __name__ == '__main__':
    lg = Ledger()
    for i in range(100):
        r = random.randint(100000001, 100000030)
        v1 = random.randint(0, 99999) / 100.0
        v2 = random.randint(0, 99999) / 100.0
        lg.ag1323m(randate('2016'), 'tpy%s' % (i + 1), '%s' % r, v1, v2)
        print(i + 1)
    lg.pol23('2016-08-02', 'tpy1', '046949583', 100)
    lg.pol23('2016-01-03', 'tpy2', '123123456', 432)
    lg.pol23('2016-01-04', 'tpy3', '123123456', 541)
    lg.pol23('2016-02-07', 'tpy4', '123123456', 728)
    lg.pol23('2016-04-12', 'tpy5', '123123456', 445)
    lg.pol23('2016-07-02', 'tpy6', '123123456', 523)
    lg.pollian23('2016-01-01', 'tpy12', 104)
    lg.pollian23('2016-01-02', 'tpy13', 65)
    lg.pollian23('2016-01-03', 'tpy14', 247)
    lg.pollian23('2016-01-03', 'tpy15', 45)
    lg.pollian23('2016-01-04', 'tpy16', 32)
    lg.pol23('2016-07-03', 'tpy12', '301312312', 208.41)
    lg.metaf('2016-05-03', 'tpy12', '38.00.0000', '30.00.123123456', 256.34)
    lg.metaf('2016-04-14', 'tpy12', '38.00.0000', '30.00.123123456', 1212.78)
    # lg.add(metaf('2016-05-03', '50.00.0018', '38.00.0000', 289.85))
    # print(lg)
    lg.sort()
    print(lg)
    lg.prbal()
    lg.prkartella('50.00.100000048')
