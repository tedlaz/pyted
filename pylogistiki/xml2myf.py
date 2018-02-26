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

    def revenues_group(self):
        parr = []
        pol = self.pack.find('groupedRevenues')
        for el in pol.findall('revenue'):
            afm = el.find('afm').text
            amount = coma2dot(el.find('amount').text)
            tax = coma2dot(el.find('tax').text)
            note = el.find('note').text
            invoices = el.find('invoices').text
            parr.append({'afm': afm, 'amount': amount, 'tax': tax,
                         'note': note, 'invoices': invoices})
        return parr

    def revenues_group_total(self):
        tval = dec(0)
        tfpa = dec(0)
        for revenue in self.revenues_group():
            if revenue['note'] == 'normal':
                tval += dec(revenue['amount'])
                tfpa += dec(revenue['tax'])
            else:
                tval -= dec(revenue['amount'])
                tfpa -= dec(revenue['tax'])
        return tval, tfpa

    def revenues_cash(self):
        parr = []
        pol = self.pack.find('groupedCashRegisters')
        if not pol:
            return parr
        for el in pol.findall('cashregister'):
            cashreg_id = el.find('cashreg_id').text
            amount = coma2dot(el.find('amount').text)
            tax = coma2dot(el.find('tax').text)
            parr.append({'cashreg_id': cashreg_id, 'amount': amount,
                         'tax': tax})
        return parr

    def revenues_cash_total(self):
        tval = dec(0)
        tfpa = dec(0)
        for revenue_cash in self.revenues_cash():
            tval += dec(revenue_cash['amount'])
            tfpa += dec(revenue_cash['tax'])
        return tval, tfpa

    def revenues_all_total(self):
        tval1, tfpa1 = self.revenues_group_total()
        tval2, tfpa2 = self.revenues_cash_total()
        return tval1 + tval2, tfpa1 + tfpa2

    def expenses_group(self):
        parr = []
        ag = self.pack.find('groupedExpenses')
        for el in ag.findall('expense'):
            afm = el.find('afm').text
            amount = coma2dot(el.find('amount').text)
            tax = coma2dot(el.find('tax').text)
            note = el.find('note').text
            invoices = el.find('invoices').text
            # nonObl = el.find('nonObl').text
            parr.append({'afm': afm, 'amount': amount, 'tax': tax,
                         'note': note, 'invoices': invoices})
        return parr

    def expenses_group_total(self):
        tval = dec(0)
        tfpa = dec(0)
        for expense in self.expenses_group():
            if expense['note'] == 'normal':
                tval += dec(expense['amount'])
                tfpa += dec(expense['tax'])
            else:
                tval -= dec(expense['amount'])
                tfpa -= dec(expense['tax'])
        return tval, tfpa

    def expenses_other(self):
        parr = []
        elm = self.pack.find('otherExpenses')
        if elm:
            amount = coma2dot(elm.find('amount').text)
            tax = coma2dot(elm.find('tax').text)
            parr.append({'amount': amount, 'tax': tax})
        return parr

    def expenses_other_total(self):
        tval = dec(0)
        tfpa = dec(0)
        for expense in self.expenses_other():
            tval += dec(expense['amount'])
            tfpa += dec(expense['tax'])
        return tval, tfpa

    def expenses_all_total(self):
        tv1, tfpa1 = self.expenses_group_total()
        tv2, tfpa2 = self.expenses_other_total()
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


def printmyf(xmlfile, trimino):
    myf = Myf(xmlfile)
    print('Τρίμηνο: %s' % trimino)
    print('Έσοδα')
    print('Πωλήσεις %12s %12s' % myf.revenues_group_total())
    print('Λιανική  %12s %12s' % myf.revenues_cash_total())
    print('---------------------------------------')
    print('Σύνολο   %12s %12s' % myf.revenues_all_total())
    print('\nΈξοδα')
    print('Αγορές   %12s %12s' % myf.expenses_group_total())
    print('Λοιπά εξ %12s %12s' % myf.expenses_other_total())
    print('---------------------------------------')
    print('Σύνολο   %12s %12s' % myf.expenses_all_total())
    ramount, rtax = myf.revenues_all_total()
    eamount, etax = myf.expenses_all_total()
    print('Διαφορά  %12s %12s' % (ramount - eamount, rtax - etax))
    print('\n')


def file2txt(afile):
    txt = ''
    try:
        with open(afile) as fl:
            txt = fl.read()
    except:
        pass
    return txt


if __name__ == '__main__':
    printmyf('091767623-2017-1.xml', 1)
    printmyf('091767623-2017-2.xml', 2)
    printmyf('091767623-2017-3.xml', 3)
    printmyf('091767623-2017-4.xml', 4)
