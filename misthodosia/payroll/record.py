# -*- coding: utf-8 -*-


class Record():
    '''A short description Here ...

    input parameters
      put pars here

    returns
      returns here
    '''
    def __init__(self, fields):
        '''
        Add id field by default
        '''
        self._fields = ['id']
        for fld in fields:
            assert len(fld) >= 3
            assert self.isvalid(fld)
            if fld in self._fields:
                raise ValueError('Dublicate field %s' % fld)
            self._fields.append(fld)
        self.ln = len(self._fields)  # The number of fields

    def chckone(self, rec):
        assert isinstance(rec[0], int)
        if self.ln == len(rec):
            return True
        else:
            return False

    def chckmany(self, recs):
        for line in recs:
            if not self.chckone(line):
                return False
        return True

    def f2s(self, with_id=False):
        if with_id:
            return ', '.join(self._fields), ', '.join(['?'] * self.ln)
        else:
            return ', '.join(self._fields[1:]), ', '.join(['?'] * (self.ln - 1))

    def isvalid(self, field):
        if field == 'id':
            return True
        elif field[0] in 'ijndest':
            if field[1] in '_ut':
                return True
            else:
                return False
        else:
            return False

    def typ(self, field):  # j i n d e s t
        if field == 'id':
            return 'INTEGER PRIMARY KEY'
        elif field[0] == 'j':
            return 'INTEGER REFERENCES %s(id)' % field[2:]
        elif field[0] == 'i':
            return 'INTEGER NOT NULL DEFAULT 0'
        elif field[0] == 'n':
            return 'NUMERIC NOT NULL DEFAULT 0'
        elif field[0] == 'd':
            return "DATE NOT NULL DEFAULT '1900-01-01'"
        elif field[0] == 'e':
            return 'DATETIME'
        elif field[0] == 's':
            return "STRING NOT NULL DEFAULT ''"
        elif field[0] == 't':
            return "TEXT NOT NULL DEFAULT ''"
        else:
            return 'Unknown field type: %s' % field[0]

    def funique(self, field):
        un = ''
        if field != 'id':
            if field[1] == 'u':
                un = ' UNIQUE'
        return un

    def tunique(self, field):
        fnam = None
        if field != 'id':
            if field[1] == 't':
                fnam = field
        return fnam

    def sqlc(self, tbl):
        tuniq = []
        sql = 'CREATE TABLE %s (\n' % tbl
        for fld in self._fields:
            vuniq = self.tunique(fld)
            if vuniq:
                tuniq.append(vuniq)
            sql += '%s %s%s,\n' % (fld, self.typ(fld), self.funique(fld))
        if tuniq:
            sql += 'UNIQUE(%s)' % ','.join(tuniq)
        else:
            sql = sql[:-2]
        sql += '\n);'
        return sql

    def sqli(self, tbl):
        fls, marks = self.f2s()
        return 'INSERT INTO %s (%s) VALUES (%s);' % (tbl, fls, marks)

    def sqlu(self):
        pass

    def sqld(self):
        pass

    def __str__(self):
        tst = u''
        for el in self._fields:
            tst += '%s : %s\n' % (el, self.typ(el))
        return tst


if __name__ == '__main__':
    arec = Record(('i_pel',
                   'dtimnia',
                   'stafm',
                   'stpar',
                   'i_pi',
                   'n_poso',
                   'n_fpa'))
    print(arec.sqli('tstd'))
    print(arec.sqlc('spp'))
