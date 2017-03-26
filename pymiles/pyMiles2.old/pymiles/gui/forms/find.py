# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from pymiles.gui.forms import table_widget as dtw
import edit_record as er


class Ffind(QtGui.QDialog):

    '''
    Form returning search values
    sql: search sql
    db : Current DB
    insTbl : 0 for no insert button, 1 for insert button
    parent:
    '''

    def __init__(self, pin, parent=None):
        super(Ffind, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.pin = pin
        self.setWindowTitle(pin.get('tablelbl', 'set Title Here'))
        self.meta = self.pin['meta']
        self.db = self.pin['db']
        self.tbl = self.pin['table']
        self.canInsertNewRecord = pin.get('canInsertNewRecord', 1)

        self.colwidths = []

        self.table = dtw.Table_widget(self.pin, self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setMinimumSize(500, 100)

        btn = QtGui.QPushButton('New Record', self)
        layout.addWidget(btn)
        btn.clicked.connect(self.new_record)
        btn.setFocusPolicy(QtCore.Qt.NoFocus)

        self.table.cellDoubleClicked.connect(self.sendVals)
        self.array = []

    def new_record(self):
        a = er.Fdata_table(self, self.tbl)
        if a.exec_() == QtGui.QDialog.Accepted:
            self.array.append(a.last_inserted_id)
            self.accept()

    def keyPressEvent(self, ev):
        '''
        use enter or return for fast selection nad form close ...
        '''
        if (ev.key() == QtCore.Qt.Key_Enter or
                ev.key() == QtCore.Qt.Key_Return):
            self.sendVals(self.table.currentRow(), self.table.currentColumn())
        QtGui.QDialog.keyPressEvent(self, ev)

    def val(self):
        return self.array

    def sendVals(self, x, y):
        for colu in range(self.table.columnCount()):
            try:
                self.array.append(self.table.item(x, colu).text())
            except:
                pass
        self.accept()
