# -*- coding: utf-8 -*-


class Fields():

    def __init__(self, fields, labels):
        self._fields = fields
        self._labels = labels

    def __repr__(self):
        return 'Fields %s' % self._fields

    def __len__(self):
        return len(self._fields)

    def __iter__(self):
        return self._fields.__iter__()

    def label(self, field):
        if field in self._fields:
            return self._labels(sef._fields.index('field'))

    def __getitem__(self, position):
        return self._fields[position]

class Records():

    def __init__(self, fields, labels, records):
        self._fields = fields
        self._labels = labels
        self._records = records
        self.ylen = len(fields)

    def _checklabels(self):
        diff = len(self._labels) - len(self._fields)
        if diff > 0:
            raise ValueError
        elif diff < 0:
            pass

    def __repr__(self):
        return 'Records %s %s %s' % (self._fields, self._labels, self._records)

    def __len__(self):
        return len(self._records)

    def __iter__(self):
        return self._records.__iter__()

    def __getitem__(self, position):
        return self._records[position]

    def get_fields(self):
        return self._fields

    def get_labels(self):
        return self._labels

    def get(self, col=0, row=0):
        if len(self._records) == 0:
            return ''
        return self._records[row][col]

    def get_by_name(self, fldname, row=0):
        if len(self._records) == 0:
            return ''
        if fldname in self._fields:
            return self._records[row][self._fields.index(fldname)]
        else:
            return ''

    def get_col(self, col=0):
        if len(self._records) == 0:
            return []
        if col > self.ylen - 1:
            return []
        tlst = []
        for el in self._records:
            tlst.append(el[col])
        return tlst

    def get_col_by_name(self, fldname):
        if len(self._records) == 0:
            return []
        if fldname in self._fields:
            tlist = []
        for i in range(len(self._records)):
            tlist.append(self.get_by_name(fldname, i))
        return tlist


if __name__ == '__main__':
    arec = Records(['id', 'epo'], ['id', 'epo'], [[1, 'Laz'], [2, 'Daz']])
    print(arec, len(arec))
    if arec:
        print('ok')
    for el in arec:
        print(el)
    print(arec[0])
    print(arec.get_by_name('id', 1))
    print(arec.get_col(1))
    print(arec.get(1, 1))
    print(arec.get_col_by_name('epo'))
