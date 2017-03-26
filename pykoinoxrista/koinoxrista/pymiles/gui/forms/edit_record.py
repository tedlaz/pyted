# -*- coding: utf-8 -*-
from PyQt4 import QtGui, Qt, QtCore
from pymiles.gui.fields.selector import qtfield
from databind import Databind


class Fdata_table(QtGui.QDialog, Databind):

    def __init__(self, parent, table, id_=None):
        QtGui.QDialog.__init__(self, parent)
        Databind.__init__(self, parent, table, id_)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.setMinimumWidth(400)

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)
        flayout = QtGui.QFormLayout()

        for fld in self.meta.table_fields(self.table):
            typos = self.meta.ftype(fld)
            label = self.meta.flabel(fld)
            self.qtfields[fld] = qtfield(typos, self, fld)
            if fld != 'id':
                flayout.addRow(QtGui.QLabel(label), self.qtfields[fld])
            else:
                self.qtfields[fld].setVisible(False)
        self.lay.addLayout(flayout)
        btn = QtGui.QPushButton('Save and exit')
        self.lay.addWidget(btn)
        btn.clicked.connect(self.save)
        btn.setFocusPolicy(QtCore.Qt.NoFocus)
        if id_:
            self.populate(id_)
