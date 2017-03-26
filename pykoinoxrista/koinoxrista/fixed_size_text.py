# -*- coding: utf-8 -*-

from pymiles.utils.txt_num import dec

aleft, aright = range(2)


class TextNum():

    def val(self, strvalue):
        return strvalue

    def str(self, value):
        return u'%s' % value


class Int():

    def val(self, value):
        return int(value)

    def str(self, strvalue):
        return u'%s' % strvalue


class Num():

    def __init__(self, dec=2):
        self.decimals = dec

    def val(self, strvalue):
        div = -1 * self.decimals
        ak = strvalue[:div]
        de = strvalue[div:]
        return dec('%s.%s' % (ak, de), self.decimals)

    def str(self, value):
        stval = u'%s' % dec(value, self.decimals)
        stval = stval.replace('.', '')
        stval = stval.replace(',', '')
        return stval


class DatYYYMMDD():

    def val(self, value):
        year = value[:4]
        month = value[4:6]
        date = value[6:8]
        return '-'.join([year, month, date])

    def str(self, strvalue):  # strvalue must be iso date
        year, month, date = strvalue.split('-')
        return u'%s%s%s' % (year, month, date)


class DatDDMMYYYY():

    def val(self, value):
        year = value[4:8]
        month = value[2:4]
        date = value[:2]
        return '-'.join([year, month, date])

    def str(self, strvalue):  # strvalue must be iso date
        year, month, date = strvalue.split('-')
        return u'%s%s%s' % (date, month, year)


class col():

    def __init__(self, size, align=aleft, filler=' ', typ=TextNum()):
        self.size = size
        self.alingment = align
        self.filler = str(filler)
        self.type = typ

    def write(self, value):
        val = u'%s' % self.type.str(value)
        if len(val) > self.size:
            if self.alingment == aleft:
                val = val[:self.size]
            else:
                print('error in size !!!')
                return ''
        lendif = self.size - len(val)
        if self.alingment == aleft:
            return val + self.filler * lendif
        elif self.alingment == aright:
            return u'%s' % (self.filler * lendif + val)

    def read(self, value):
        lval = len(value) - 1
        if self.alingment == aleft:
            for i in range(lval):
                if value[lval-i] == self.filler:
                    value = value[:-1]
                else:
                    return self.type.val(value.strip())
            return ''
        elif self.alingment == aright:
            for i in range(lval):
                if value[0] == self.filler:
                    value = value[1:]
                else:
                    return self.type.val(value.strip())
            return ''


class row():

    def __init__(self, head, cols=[], term='\n'):
        self.head = col(1).write(head)
        self.cols = cols
        self.term = term

    def len(self):
        al = len(self.head)
        for col in self.cols:
            al += col.size
        al += len(self.term)
        return al

    def add(self, val):
        self.cols.append(val)

    def read(self, value):
        lenv = len(value)
        assert lenv == self.len()
        valarr = []
        valarr.append(int(value[:len(self.head)]))
        value = value[len(self.head):]
        for col in self.cols:
            cval = value[:col.size]
            valarr.append(col.read(cval))
            value = value[col.size:]
        return valarr

    def write(self, valuearr):
        st = self.head
        assert len(valuearr) == len(self.cols)
        for i, col in enumerate(self.cols):
            st += col.write(valuearr[i])
        st += self.term
        return st

ftn = TextNum()
fin = Int()
fnu = Num()
fdy = DatYYYMMDD()
fdd = DatDDMMYYYY()


def ctxt(size):
    return col(size, aleft, ' ', ftn)


def cnum(size):
    return col(size, aright, '0', fnu)


def cdmy(size=8):
    return col(size, aleft, ' ', fdd)


def cymd(size=8):
    return col(size, aleft, ' ', fdy)


def ctextnumeric(size):
    return col(size, aleft, ' ', fin)


def cinteger(size):
    return col(size, aright, '0', fin)


class dfile():

    def __init__(self, head, rows, eof):
        self.header = ''
        self.rows = ''
        self.eof = eof

    def read(self, flines):
        for line in flines:
            pass

    def write(self,rows):
        st = ''
        for row in rows:
            pass


if __name__ == '__main__':
    # import sys
    # reload(sys)
    # sys.setdefaultencoding("utf-8")

    r1 = row(2)
    r1.add(cnum(14))
    r1.add(cnum(14))
    r1.add(cnum(14))
    r1.add(cnum(13))
    r1.add(cnum(13))
    r1.add(cnum(13))
    r1.add(cnum(12))
    r1.add(cnum(11))
    r1.add(ctxt(27))
    r1.add(cdmy(8))
    r1.add(cymd(8))

    val = r1.write([20220.98,
                    3575.14,
                    16645.84, 0, 0, 0, 0, 0,
                    'kala', '2015-01-01', '2015-01-01'])
    print(val)
    arrs = r1.read(val)
    print(arrs)
    print(arrs[1] + 1)
    aa = col(14, 1, '0', Num())
    fv = aa.write(20220.98)
    print(fv)
