"""
Module data2text.py
Create a fixed length text file with data
Read back from file and store values to dicts
"""
import utils as ul
LEFT, CENTER, RIGHT = range(3)


class ColSizeException(Exception):
    pass


class RowException(Exception):
    pass


class DocException(Exception):
    pass


class Col():
    def __init__(self, name, size, filler=' ', align=LEFT):
        """Template to create a fixed size text field
           align
        """
        assert len(filler) == 1
        assert type(size) is int
        assert type(align) is int
        self.name = name
        self.size = size
        self.filler = filler
        self.align = align

    def txt(self, val):
        tstr = str(val)
        ltstr = len(tstr)
        size_differene = self.size - ltstr
        if size_differene < 0:
            est = 'Col size (%s) is small for value %s (%s)'
            raise ColSizeException(est % (self.size, tstr, ltstr))
        if self.align == LEFT:
            formatter = '{:%s<%s}' % (self.filler, self.size)
        elif self.align == CENTER:
            formatter = '{:%s^%s}' % (self.filler, self.size)
        elif self.align == RIGHT:
            formatter = '{:%s>%s}' % (self.filler, self.size)
        else:
            formatter = '{:%s>%s}' % (self.filler, self.size)
        return formatter.format(tstr)

    def txt2val(self, txtval):
        if self.align == LEFT:
            return txtval.rstrip(self.filler)
        elif self.align == CENTER:
            return txtval.strip(self.filler)
        elif self.align == RIGHT:
            return txtval.lstrip(self.filler)
        else:
            return txtval.lstrip(self.filler)


class ColCap(Col):
    def txt(self, val):
        return super().txt(ul.grup(val))


class ColDec(Col):
    def __init__(self, name, size, decs=2):
        super().__init__(name, size, '0', RIGHT)
        self.decs = decs

    def txt(self, val):
        return super().txt(ul.dec2text_flat(val, self.decs))

    def txt2val(self, txtval):
        tval = super().txt2val(txtval)
        return ul.dec(tval[:-self.decs] + '.' + tval[-self.decs:], self.decs)


class ColCalc(ColDec):
    def __init__(self, name, size, row2point, col2point, decs=2):
        super().__init__(name, size, decs)
        self.row2point = row2point
        self.col2point = col2point


class Row():
    def __init__(self, identifier):
        self._id = str(identifier)
        self._lenid = len(self._id)
        self._colnames = []
        self._cols = {}

    def acol(self, col):
        """Add a Col object to self._cols"""
        self._colnames.append(col.name)
        self._cols[col.name] = col

    @property
    def id(self):
        return self._id

    @property
    def len(self):
        val = len(self._id)
        for elm in self._cols:
            val += self._cols[elm].size
        return val

    def txt(self, data=''):
        ttx = self._id
        for elm in self._colnames:
            ttx += self._cols[elm].txt(data[elm])
        return ttx

    def txt2dic(self, txtrow):
        assert len(txtrow) == self.len
        assert txtrow.startswith(self._id)
        tdic = {}
        eos = self._lenid
        tdic['row_id'] = txtrow[:self._lenid]
        apo = self._lenid
        for elm in self._colnames:
            eos += self._cols[elm].size
            tdic[elm] = self._cols[elm].txt2val(txtrow[apo:eos])
            apo = eos
        return tdic

    def iscompatible(self, dic):
        assert isinstance(dic, dict)
        for key in self._colnames:
            if key not in dic:
                return False
        return True

    def __repr__(self):
        atx = '(OBJ Row id=%s:' % self._id
        for elm in self._colnames:
            atx += ' %s(%s)' % (elm, self._cols[elm].size)
        return atx + ')'


class Doc():
    def __init__(self, list_of_rows=None):
        self.rowtypes = {}
        if list_of_rows:
            assert isinstance(list_of_rows, list)
            for elm in list_of_rows:
                self.add_rowtype(elm)
        self.lines = []

    def add_rowtype(self, row):
        assert isinstance(row, Row)
        if row.id not in self.rowtypes.keys():
            self.rowtypes[row.id] = row
        else:
            raise DocException('rowtype %s is already in Doc' % row)

    def add_row(self, row_id, rowdic):
        row_id = str(row_id)
        assert row_id in self.rowtypes
        if self.rowtypes[row_id].iscompatible(rowdic):
            self.lines.append({'id': row_id, 'data': rowdic})
        else:
            raise RowException('Dic %s is not combatible ' % rowdic)

    def calc_sum(self, rowid, column):
        val = 0
        for lin in self.lines:
            if lin['id'] == rowid:
                val += ul.dec(lin['data'].get(column, 0))
        return val

    def calc_totals(self):
        # search in lines
        for lin in self.lines:
            # search in columns
            for key in lin['data'].keys():
                if isinstance(self.rowtypes[lin['id']]._cols[key], ColCalc):
                    vli = self.rowtypes[lin['id']]._cols[key].row2point
                    vlc = self.rowtypes[lin['id']]._cols[key].col2point
                    val = self.calc_sum(vli, vlc)
                    lin['data'][key] = val

    @property
    def txt(self):
        self.calc_totals()
        ftx = []
        for elm in self.lines:
            ftx.append(self.rowtypes[elm['id']].txt(elm['data']))
        return '\n'.join(ftx)

    def txt2dics(self, ftxt):
        farr = []
        for lin in ftxt.split('\n'):
            for key in self.rowtypes.keys():
                if lin.startswith(key):
                    farr.append(self.rowtypes[key].txt2dic(lin))
        return farr

    def save2file(self, filename, encoding):
        with open(filename, 'w', encoding=encoding) as sfile:
            sfile.write(self.txt)

    def from_file(self, filename, encoding):
        txtdata = ''
        with open(filename, encoding=encoding) as sfile:
            txtdata = sfile.read()
        return self.txt2dics(txtdata)
