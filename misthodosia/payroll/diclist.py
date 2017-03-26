# -*- coding: utf-8 -*-

import sys


class Diclist():
    '''
    Dictionary and list at the same time

    '''
    def __init__(self, vals=None):
        self._arr = []
        self._dic = {}
        if vals:
            self.setMany(vals)

    def keys(self):
        '''
        Returns a tuple with the keys
        '''
        return tuple(self._arr)

    def len(self):
        '''
        Returns the length
        '''
        return len(self._arr)

    def add(self, key, val):
        '''
        Adds a new value for new key only
        '''
        if key in self._arr:
            raise ValueError('The key already exists')
        else:
            self._arr.append(key)
            self._dic[key] = val

    def setMany(self, vals):
        '''
        Inserts many values. For double keys last inserted overlaps older.
        '''
        for lin in vals:
            assert len(lin) == 2
            self.add(lin[0], lin[1])

    def list(self):
        '''
        Returns data as a list
        '''
        lst = []
        for el in self._arr:
            lst.append(self._dic[el])
        return lst

    def dic(self):
        '''
        Returns data as a normal dic
        '''
        dic = {}
        for el in self._arr:
            dic[el] = self._dic[el]
        return dic

    def odic(self):
        '''
        Returns data as an ordered dic
        '''
        from collections import OrderedDict as od
        tod = od()
        for el in self._arr:
            tod[el] = self._dic[el]
        return tod

    def get(self, key):
        '''
        Returns value by key. If key not exists returns None
        '''
        if key in self._arr:
            return self._dic[key]
        else:
            return None

    def getById(self, no):
        '''
        Returns value by id. If id is out of size returns None
        '''
        if no > len(self._arr):
            return None
        else:
            return self._dic[self._arr[no]]

    def set(self, key, val):
        '''
        Sets value by key. If key is already present
        it changes old value with new
        '''
        if key not in self._arr:
            self._arr.append(key)
        self._dic[key] = val

    def setById(self, aa, val):
        '''
        Sets value by id. If id is out of size, does nothing
        '''
        assert int(aa) >= 0
        if aa < self.len():
            self._dic[self._arr[aa]] = val

    def __str__(self):
        st = ''
        for el in self._arr:
            st += '%s : %s\n' % (el, self._dic[el])
        if sys.version[0] == '2':
            return st.encode('utf-8')
        else:
            return st


class Fieldtmpl():
    '''
    Field template
    '''

    def __init__(self, name, typ='t', size=30):
        self.name = name
        self.typ = typ
        self.size = size

    def __str__(self):
        return 'name: %s\ntyp: %s\nsize: %s' % (self.name, self.typ, self.size)


class Rowtmpl():
    '''
    Row template
    '''

    def __init__(self):
        self._fields = ['epo', 'ono']
        self._types = ['']


if __name__ == '__main__':
    ft = Fieldtmpl('epo')
    print(ft)
    vals = (('pat', 'Kostas'), ('mit', 'Stav'))
    tran = {'pat': u'Πατρώνυμο', 'mit': u'Μητρώνυμο'}
    aa = Diclist(vals)
    aa.set('epo', 'Laz')
    aa.set('ono', 'Ted')
    print(aa.get('epo'))
    print(aa.get('etos'))
    aa.set('epo', u'Λάζαρος')
    aa.set('etos', 1963)
    print(aa.get('etos'))
    aa.set('etos', 1962)
    print(aa.getById(0))
    print(aa.keys())
    print(aa.len())
    print(aa.list())
    print(aa)
    print(aa.dic())
    print(aa.odic())
    for el in aa.odic():
        print('%s %s ' % (el, aa.get(el)))

    print(aa.get('malakia'))
