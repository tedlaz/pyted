# -*- coding: utf-8 -*-


import record


def maxv(ar1, ar2):
    maxa = []
    assert len(ar1) == len(ar2)
    for i, el in enumerate(ar1):
        if el >= ar2[i]:
            maxa.append(el)
        else:
            maxa.append(ar2[i])
    return maxa


class Table():
    def __init__(self, name, rect, data=None):
        self._name = name
        self._recd = record.Record(rect)
        self._data = []
        self._maxid = 0
        self._maxrc = [5] * self._recd.ln
        if data:
            assert self._recd.chckmany(data)
            for lin in data:
                self.addrec(lin)

    def addrec(self, rec):
        rec = list(rec)
        if self._recd.chckone(rec):
            if rec[0] <= 0:
                rec[0] = self._maxid + 1
            if self._maxid < rec[0]:
                self._maxid = rec[0]
            self._data.append(rec)
            self._rsiz(rec)
            print('all ok')
            return True
        else:
            print('Not ok')
            return False

    def _rsiz(self, rec):
        szs = []
        for el in rec:
            szs.append(len(str(el)))
        self._maxrc = maxv(szs, self._maxrc)

    def __str__(self):
        linesize = (sum(self._maxrc) + self._recd.ln)
        tmpl = ''
        fst = '\n' + '=' * linesize + '\n'
        for el in self._maxrc:
            tmpl += '{:' + str(el) + '} '
        tmpl += '\n'
        fst += tmpl.format(*self._recd._fields)
        fst += '-' * linesize + '\n'
        for lin in self._data:
            fst += tmpl.format(*lin)
        fst += '=' * linesize + '\n'
        return fst

if __name__ == '__main__':
    datai = [[0, 'Ted', 'Lazaros', '1963-02-10'],
             [0, 'Popi', 'Dazea', '1968-10-22']]
    record1 = ('stono', 'stepo', 'd_gen')
    tb = Table('tst', record1, datai)
    tb.addrec((0, 'Nik', 'Mav', '2014-01-01'))
    tb.addrec((0, 'George', 'Benson', '2001-01-10'))
    tb.addrec((0, 'Xrysiida', 'Panagiotoy', '1903-12-04'))
    print(tb._recd.sqlc('tst'))
    print(tb._data)
    print(tb._maxid)
    print(maxv([2, 5, 4], [1, 6, 3]))
    print(tb._maxrc)
    print(tb)
