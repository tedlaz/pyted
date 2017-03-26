# -*- coding: utf-8 -*-

from PyQt4 import QtGui, Qt
from pymiles.sqlite.db_select import select


class Combo(QtGui.QComboBox):

    def __init__(self, parent, name, val=None):
        super(Combo, self).__init__(parent)
        assert(parent is not None)
        assert(name.endswith('_id'))
        assert(len(name) > 3)
        assert(name in self.parent().meta._flbl.keys())
        self.name = name
        self.populate()
        self.set(val)  # val must be a valid id

    def get(self):
        return self.index2id[self.currentIndex()]

    def set(self, id_):
        if id_:
            self.setCurrentIndex(self.id2index[id_])

    def populate(self):
        """
        Here we
        1.get values from Database
        2.fill Combo
        3.set current index to initial value
        """
        self.index2id = {}
        self.id2index = {}
        table = self.name[:-3]  # Take out _id from field and get tablename
        sqlr = self.parent().meta.rpr(table) + ' ORDER BY rpr'
        vals = select(self.parent().db, sqlr, False)['rows']
        for i, el in enumerate(vals):
            self.addItem('%s' % el[1])
            self.index2id[i] = el[0]
            self.id2index[el[0]] = i

