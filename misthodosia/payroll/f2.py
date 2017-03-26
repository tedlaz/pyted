# -*- coding: utf-8 -*-
import decimal


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


def tst1():
    tml1 = '{:>10} {:>12}\n'
    tml2 = '{:<10} {:<12}\n'
    tml3 = '{:^10} {:^12}\n'
    ar = [19, 23]
    print(tml1.format(*ar))
    print(tml2.format(*ar))
    print(tml3.format(*ar))


class F2():
    def __init__(self):
        self.v = {}
        self._addzero(range(301, 312))
        self._addzero(range(331, 338))
        self._addzero(range(351, 359))
        self._addzero(range(371, 379))
        self._addzero(range(341, 346))
        self._addzero([401, 402, 403, 404])
        self._addzero([411, 412, 413, 420])
        self._addzero([501, 502, 503, 511, 512, 513])
        self._addzero([35700, 35713, 35716, 35723, 35724])
        self._addzero([37700, 37713, 35716, 37723, 37724])
        self._addzero([601, 611])

    def _addzero(self, rng):
        for i in rng:
            self.v[i] = dec(0)

    def calc(self, vl):
        d100 = dec(100)
        for el in vl.keys():
            if el in self.v.keys():
                self.v[el] = dec(vl[el])
        self.v[331] = dec(self.v[301] * dec(13) / d100)
        self.v[332] = dec(self.v[302] * dec(24) / d100)
        self.v[333] = dec(self.v[303] * dec(23) / d100)
        self.v[334] = dec(self.v[304] * dec(8) / d100)
        self.v[335] = dec(self.v[305] * dec(4) / d100)
        self.v[336] = dec(self.v[306] * dec(16) / d100)
        self.v[307] = self._sum(range(301, 307))
        self.v[337] = self._sum(range(331, 337))
        self.v[311] = self._sum(range(307, 311))

        self.v[371] = dec(self.v[351] * dec(13) / d100)
        self.v[372] = dec(self.v[352] * dec(24) / d100)
        self.v[373] = dec(self.v[353] * dec(23) / d100)
        self.v[374] = dec(self.v[354] * dec(8) / d100)
        self.v[375] = dec(self.v[355] * dec(4) / d100)
        self.v[376] = dec(self.v[356] * dec(16) / d100)

        self.v[37713] = dec(self.v[35713] * dec(13) / d100)
        self.v[37723] = dec(self.v[35723] * dec(23) / d100)
        self.v[37724] = dec(self.v[35724] * dec(24) / d100)
        c377 = self.v[37713] + self.v[37723] + self.v[37724]
        if c377 > self.v[377]:
            fd = c377 - self.v[377]
            print(u'Το ΦΠΑ εξόδων είναι μικρότερο κατά %s' % fd)
        if c377 < self.v[377]:
            fd = self.v[377] - c377
            print(u'Το ΦΠΑ εξόδων είναι μεγαλύτερο κατά %s' % fd)
        self.v[357] = self.v[35713] + self.v[35716] + self.v[35723] + self.v[35724]

        self.v[358] = self._sum(range(351, 358))
        self.v[378] = self._sum(range(371, 378))
        self._finalize()

    def _finalize(self):
        self.v[404] = self._sum([401, 402, 403])
        self.v[413] = self._sum([411, 412])

        self.v[420] = self.v[378] + self.v[404] - self.v[413]

        if self.v[337] > self.v[420]:
            self.v[511] = self.v[337] - self.v[420]
        else:
            self.v[501] = self.v[420] - self.v[337]

        if self.v[601] > self.v[501]:
            d = self.v[601] - self.v[501]
            self.v[402] += d
            self._finalize()
        if self.v[601] < self.v[501]:
            d = self.v[501] - self.v[601]
            self.v[412] += d
            self._finalize()

        if self.v[611] > self.v[511]:
            d = self.v[611] - self.v[511]
            self.v[412] += d
            self._finalize()

        if self.v[611] < self.v[511]:
            d = self.v[511] - self.v[611]
            self.v[402] += d
            self._finalize()

    def _sum(self, rang):
        tot = dec(0)
        for i in rang:
            tot += dec(self.v[i])
        return tot

    def __str__(self):
        st = ''
        stf = '{:4} {:>12} {:4} {:>12}\n'
        sta = '{:4} {:>12}\n'
        for i in range(301, 308):
            st += stf.format(i, grd(self.v[i]), i+30, grd(self.v[i+30]))
        for i in range(308, 312):
            st += sta.format(i, grd(self.v[i]))
        st += '\n'
        for i in range(351, 359):
            st += stf.format(i, grd(self.v[i]), i+20, grd(self.v[i+20]))
        st += '\n'
        for i in [401, 402, 403]:
            st += sta.format(i, grd(self.v[i]))
        st += stf.format('', '', 404, grd(self.v[404]))
        for i in [411, 412]:
            st += sta.format(i, grd(self.v[i]))
        st += stf.format('', '', 413, grd(self.v[413]))
        st += stf.format('', '', 420, grd(self.v[420]))
        st += '\n'
        for i in [341, 342, 343, 344, 345]:
            st += sta.format(i, grd(self.v[i]))
        st += '\n'
        st += stf.format(501, grd(self.v[501]), 511, grd(self.v[511]))
        st += '\n 35700: %s\n' % grd(self.v[35700])
        return st


if __name__ == '__main__':
    # tst1()
    # clc({301: 10, 302: 100, 303: 1000})
    aa = F2()
    # print(aa.v)
    aa.calc({302: dec(572.1),
             303: 2661.72,
             309: 1497,
             342: 153,
             352: 715.47,
             353: 819.06,
             35723: 1704.91,
             377: 392.13,
             601: 3
             })
    print(aa)
