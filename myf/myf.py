# -*- coding: utf-8 -*-
'''
myf module
'''
import decimal
import xml.etree.ElementTree as et


'''
Ημερομηνία ΑΦΜ Αξια ΦΠΑ Νορμαλ/inverse ypoxreos
'''


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


def coma2dot(text):
    "Coma to dot"
    return text.replace(',', '.')


class Myf():
    def __init__(self, fname):
        self.tree = et.parse(fname)
        self.root = self.tree.getroot()
        self.pack = self.root.find('package')

    def getpol(self):
        parr = []
        pol = self.pack.find('groupedRevenues')
        for el in pol.findall('revenue'):
            afm = el.find('afm').text
            amount = coma2dot(el.find('amount').text)
            tax = coma2dot(el.find('tax').text)
            note = el.find('note').text
            invoices = el.find('invoices').text
            parr.append([afm, amount, tax, note, invoices])
        return parr

    def getpolt(self):
        tval = dec(0)
        tfpa = dec(0)
        for el in self.getpol():
            if el[3] == 'normal':
                tval += dec(el[1])
                tfpa += dec(el[2])
            else:
                tval -= dec(el[1])
                tfpa -= dec(el[2])
        return tval, tfpa

    def getpollian(self):
        parr = []
        pol = self.pack.find('groupedCashRegisters')
        for el in pol.findall('cashregister'):
            cashreg_id = el.find('cashreg_id').text
            amount = coma2dot(el.find('amount').text)
            tax = coma2dot(el.find('tax').text)
            parr.append([cashreg_id, amount, tax])
        return parr

    def getpolliant(self):
        tval = dec(0)
        tfpa = dec(0)
        for el in self.getpollian():
            tval += dec(el[1])
            tfpa += dec(el[2])
        return tval, tfpa

    def getpoliseist(self):
        tval1, tfpa1 = self.getpolt()
        tval2, tfpa2 = self.getpolliant()
        return tval1 + tval2, tfpa1 + tfpa2

    def getag(self):
        parr = []
        ag = self.pack.find('groupedExpenses')
        for el in ag.findall('expense'):
            afm = el.find('afm').text
            amount = coma2dot(el.find('amount').text)
            tax = coma2dot(el.find('tax').text)
            note = el.find('note').text
            invoices = el.find('invoices').text
            nonObl = el.find('nonObl').text
            parr.append((afm, amount, tax, note, invoices))
        return parr

    def getagt(self):
        tval = dec(0)
        tfpa = dec(0)
        for el in self.getag():
            if el[3] == 'normal':
                tval += dec(el[1])
                tfpa += dec(el[2])
            elif el[3] == 'credit':
                # print(el, el[1], el[2])
                tval -= dec(el[1])
                tfpa -= dec(el[2])
        return tval, tfpa

    def getexp(self):
        parr = [[0, 0]]
        el = self.pack.find('otherExpenses')
        if el:
            amount = coma2dot(el.find('amount').text)
            tax = coma2dot(el.find('tax').text)
            parr.append([amount, tax])
        return parr

    def getexpt(self):
        el = self.getexp()[0]
        return dec(el[0]), dec(el[1])

    def getagorest(self):
        tv1, tfpa1 = self.getagt()
        tv2, tfpa2 = self.getexpt()
        return tv1 + tv2, tfpa1 + tfpa2


def printanalytic(xmlfile):
    myf = Myf(xmlfile)

    print('GroupedExpenses analytika')
    fstr = '%9s %12s %11s %6s %4s'
    val = 0
    vat = 0
    tim = 0
    for el in myf.getag():
        tim += int(el[4])
        if el[3] == 'normal':
            val += dec(el[1])
            vat += dec(el[2])
        else:
            val -= dec(el[1])
            vat -= dec(el[2])
        print(fstr % el)
    print(fstr % ('Synola', val, vat, '', tim))


def printmyf(xmlfile):
    myf = Myf(xmlfile)
    print('Esoda')
    print('poliseis %12s %12s' % myf.getpolt())
    print('Lianiki  %12s %12s' % myf.getpolliant())
    print('---------------------------------------')
    print('pol.Syno %12s %12s' % myf.getpoliseist())
    print('Ejoda')
    print('Agores   %12s %12s' % myf.getagt())
    print('Loipa ej %12s %12s' % myf.getexpt())
    print('---------------------------------------')
    print('agores   %12s %12s' % myf.getagorest())
    # for el in myf.getag():
    #     print(el)


def file2txt(afile):
    txt = ''
    try:
        with open(afile) as fl:
            txt = fl.read()
    except:
        pass
    return txt

if __name__ == '__main__':
    printmyf('/home/tedlaz/tedfiles/prj/samaras2016d/myf/091767623-2016-4.xml')
    # printmyf('s2.xml')
    # printmyf('s3.xml')
    # printmyf('s4.xml')
    # printanalytic('s1.xml')
    # print(file2txt('grpexpn.sql'))
