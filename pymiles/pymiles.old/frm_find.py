# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

import table_widget as dtw


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

        self.canInsertNewRecord = pin.get('canInsertNewRecord', 1)
        self.parent = parent

        self.colwidths = []

        self.table = dtw.Table_widget(self.pin, self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setMinimumSize(500, 100)

        self.table.cellDoubleClicked.connect(self.sendVals)
        self.array = []

    def newRecord(self):
        self.table.newRecord()

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

if __name__ == '__main__':
    import sys
    from u_db import Dbmanager
    APP = QtGui.QApplication([])
    DLG = Ffind(Dbmanager('tst.sql3').table_rpr("dia"))
    DLG.show()
    SEX = APP.exec_()
    if DLG.array:
        print(u'%s' % DLG.array[0])
    sys.exit(SEX)
