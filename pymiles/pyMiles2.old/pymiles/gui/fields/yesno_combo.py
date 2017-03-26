# -*- coding: utf-8 -*-

from PyQt4 import QtGui


class Yes_no_combo(QtGui.QComboBox):

    def __init__(self, parent, val=0):
        super(Yes_no_combo, self).__init__(parent)
        assert(parent is not None)

        self.addItem('No')
        self.addItem('yes')
        self.set(val)

    def get(self):
        return str(self.currentIndex())

    def set(self, val):
        idx = 0
        if int(val) != 0:
            idx = 1
        self.setCurrentIndex(idx)
