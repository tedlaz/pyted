# -*- coding: utf-8 -*-
'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''

from PyQt4 import QtGui, QtCore

import table_widget as dtw


class FormFind(QtGui.QDialog):
    '''
    Form returning search values
    sql: search sql
    db : Current DB
    insTbl : 0 for no insert button, 1 for insert button
    parent:
    '''
    def __init__(self, pin, parent=None):
        super(FormFind, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        rows = pin.get('rows', None)
        labels = pin.get('labels', None)
        self.setWindowTitle(pin.get('title', 'set Title Here'))

        self.canInsertNewRecord = pin.get('canInsertNewRecord', 1)
        self.parent = parent

        self.colwidths = []

        self.table = dtw.TableWidget({'rows': rows, 'labels': labels}, self)

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
        if (ev.key() == QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
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
    APP = QtGui.QApplication([])
    RWS = [[1, u'Λάζαρος', u'Θεόδωρος'],
           [2, u'Δαζέα', u'Καλλιόπη']]
    LBL = [u'ΑΑ', u'Επώνυμο', u'Όνομα']
    DLG = FormFind({'titleg': u'Δοκιμαστική Φόρμα', 'rows': RWS, 'labels': LBL})
    DLG.show()
    SEX = APP.exec_()
    if DLG.array:
        print(u'%s' % DLG.array[1])
    sys.exit(SEX)
