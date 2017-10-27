import inspect


class Field():
    _type = 'fld'
    _sql = ''
    _name = 'Basic Field'

    def __init__(self, lbl='', unique=False):
        self._lbl = lbl
        self._unique = unique

    def __repr__(self):
        return self._type

    def label(self):
        if self._lbl:
            return self._lbl
        else:
            return
    def sql(self, name):
        return '%s %s' % (name, self._sql)


class Text(Field):
    _name = 'Text Field'
    _sql = 'TEXT'


class Integer(Field):
    _name = 'Integer field'
    _sql = 'INTEGER'


class Numeric(Field):
    _name = 'Numeric field'
    _sql = 'NUMERIC'


class Model():
    _name = 'Base Model'

    def labels(self):
        flds = [m[0] for m in inspect.getmembers(self) if str(m[1]) == 'fld']
        lbls = {}
        for el in flds:
            fld = self.__getattribute__(el)
            if fld._lbl:
                lbls[el] = fld._lbl
            else:
                lbls[el] = el
        return lbls

    def sql_create_table(self):
        sql = "CREATE TABLE %s (\n" % self.__class__.__name__.lower()
        sql += "id INTEGER NOT NULL PRIMARY KEY,\n"

        fields = []
        att = [m[0] for m in inspect.getmembers(self) if str(m[1]) == 'fld']
        for atr in att:
            fields.append('%s' % self.__getattribute__(atr).sql(atr))
        tfields = ',\n'.join(fields)
        print(sql + tfields + ')')


class Eee(Model):
    epo = Text('Επώνυμο')
    ono = Text()
    age = Integer()


if __name__ == '__main__':
    Eee().sql_create_table()
    print(Eee().labels())
