# -*- coding: utf-8 -*-

from dec import dec
import six
import sys


def fmt(rval, typsize):
    '''
    Επιστρέφει κείμενο σταθερού μεγέθους
    rval : Η τιμή για μετατροπή
    size : Το συνολικό μέγεθος του κειμένου    typ  : Είναι ο τύπος της τιμής.
           Μπορεί να έχει τις εξής τιμές:
           i     : integer ακέραιος (Γεμίζει από αριστερά με 0)
           n     : Numeric με δύο δεκαδικά (Γεμίζει από αριστερά με 0)
           d     : Date (Γεμίζει από αριστερά με κενά)
           Λοιπά : Όλα τα υπόλοιπα (Γεμίζει από δεξιά με κενά)
    '''

    typ = typsize[0]
    size = int(typsize[1:])

    if typ == 'n':  # Numeric Value with 2 decimals
        val = dec(rval)  # Make sure it has only 2 decimals
        val = '%s' % val
        val = val.replace('.', '')  # make it integer
        val = val.replace(',', '')  # make it integer
        ldif = size - len(val)
        assert ldif >= 0
        tmp = '%s%s' % ('0' * ldif, val)

    elif typ == 'i':
        assert int(rval) >= 0
        val = '%s' % rval
        ldif = size - len(val)
        assert ldif >= 0
        tmp = '%s%s' % ('0' * ldif, val)
        return tmp

    elif typ == 'd':  # Date
        val = '%s' % rval
        ldif = size - len(val)
        assert ldif >= 0
        tmp = '%s%s' % (' ' * ldif, val)

    else:  # Every other val including text
        val = '%s' % rval
        ldif = size - len(val)
        assert ldif >= 0
        tmp = '%s%s' % (val, ' ' * ldif)

    return tmp


def defmt(astr, typ):
    '''
    Από πεδίο κειμένου σταθερού μήκους επιστρέφει τιμή
    asrt : Το πεδίο κειμένου
    typ  : Ο τύπος του πεδίου (όπως παραπάνω)
    '''
    assert isinstance(astr, six.string_types)
    if typ == 'n':
        val = dec(astr) / dec(100)
    elif typ == 'i':
        val = int(astr)
    else:
        val = astr.strip()
    return val


class Fixedline():
    '''
    Documentation for class
    '''

    def __init__(self, ftypes):
        '''
        ftypes : ('1','i1', 'd12', 'i3')
        '''
        self.ltype = '%s' % ftypes[0]
        self.ltypelen = len(self.ltype)
        ltyp = 't%s' % self.ltypelen
        lftypes = list(ftypes[1:])
        lftypes.insert(0, ltyp)
        cftypes = tuple(lftypes)
        for el in cftypes:
            assert len(el) > 1
            assert int(el[1:]) > 0
        self.ftypes = cftypes

    def size(self):
        siz = 0
        for el in self.ftypes:
            siz += int(el[1:])
        return siz

    def line2text(self, dataarr):
        '''
        '''
        assert len(self.ftypes) == len(dataarr)
        txt = u''
        for i, el in enumerate(dataarr):
            txt += fmt(el, self.ftypes[i])
        return txt

    def text2line(self, txt):
        assert len(txt) == self.size()
        rarr = []
        i = 0
        for el in self.ftypes:
            typ = el[0]
            flen = int(el[1:])
            fs = flen + i
            rarr.append(defmt(txt[i:fs], typ))
            i = fs
        return rarr


class Fixedtext():
    '''
    Documentation here
    '''
    def __init__(self, fixedLines, lineterm='\n'):
        self.l = []
        self.seir = {}
        for i, el in enumerate(fixedLines):
            fline = Fixedline(el)
            self.l.append(fline)
            self.seir[fline.ltype] = i
        self.lineterm = lineterm

    def data2text(self, data):
        txt = ''
        for lin in data:
            txt += self.l[self.seir[lin[0]]].line2text(lin) + self.lineterm
        return txt[:-1]

    def data2file(self, data, filename, encodin='CP1253'):
        txt = self.data2text(data)
        if sys.version[0] == '2':
            with open(filename, 'w') as fil:
                fil.write(txt.encode(encodin))
        else:
            with open(filename, 'w', encoding=encodin) as fil:
                fil.write(txt)
        return True

    def text2data(self, text):
        farr = []
        for lin in text.split('\n'):
            # print('%s!' % lin)
            if lin[0] != 'E':
                farr.append(self.l[self.seir[lin[0]]].text2line(lin))
        return farr

    def file2data(self, txtfile, encodin='CP1253'):
        txt = ''
        if sys.version[0] == '2':
            with open(txtfile, 'r') as fil:
                txt = fil.read()
                txt = txt.decode(encodin)
        else:
            with open(txtfile, 'r', encoding=encodin) as fil:
                txt = fil.read()
        return self.text2data(txt)
