# -*- coding: utf-8 -*-
'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''

from PyQt4 import QtGui, QtCore, Qt
#from utils import dec as tu


class sortWidgetItem(QtGui.QTableWidgetItem):
    def __init__(self, text, sortKey):
        # call custom constructor with UserType item type
        QtGui.QTableWidgetItem.__init__(self,
                                        text,
                                        QtGui.QTableWidgetItem.UserType)
        self.sortKey = sortKey

    def __lt__(self, other):
        return self.sortKey < other.sortKey


class TableWidget(QtGui.QTableWidget):
    def __init__(self, pin, parent=None):
        super(TableWidget, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.rows = pin.get('rows', None)
        self.labels = pin.get('labels', None)

        self.parent = parent

        # Εδώ ορίζουμε το πλάτος της γραμμής του grid
        self.verticalHeader().setDefaultSectionSize(20)

        self.verticalHeader().setStretchLastSection(False)
        self.verticalHeader().setVisible(False)

        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.setAlternatingRowColors(True)
        self.setStyleSheet("alternate-background-color: rgba(208,246,230);")

        self.setSortingEnabled(True)
        self.populate()

    def _intItem(self, num):
        item = QtGui.QTableWidgetItem()
        item.setData(QtCore.Qt.DisplayRole, QtCore.QVariant(num))
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        return item

    def _numItem(self, num):
        item = sortWidgetItem(tu.strGrDec(num), num)
        item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        return item

    def _strItem(self, strv):
        st = '%s' % strv
        if st == 'None':
            st = ''
        item = QtGui.QTableWidgetItem(st)
        return item

    def _dateItem(self, strv):
        strv = '%s' % strv
        if len(strv) < 10:
            item = sortWidgetItem(strv, strv)
        else:
            y, m, d = strv.split('-')
            item = sortWidgetItem('%s/%s/%s' % (d, m, y), strv)
        return item

    def populate(self):
        self.setRowCount(0)
        self.setColumnCount(len(self.labels))
        self.setHorizontalHeaderLabels(self.labels)

        for line in self.rows:
            rc = self.rowCount()
            self.setRowCount(rc + 1)
            colNo = 0
            for col in line:
                '''
                if columnTypes[colNo] =='i': #Numeric values
                    self.setItem(rc,colNo,self._intItem(col))
                elif columnTypes[colNo] =='n':
                    self.setItem(rc,colNo,self._numItem(col))
                elif columnTypes[colNo] in 'de': #Date values
                    self.setItem(rc,colNo,self._dateItem(col))
                else: #Other values as text
                    self.setItem(rc,colNo,self._strItem(col))
                '''
                if tu.isNum(col):
                    if self.labels[colNo][:2] == 'id':
                        self.setItem(rc, colNo, self._intItem(col))
                    else:
                        self.setItem(rc, colNo, self._numItem(col))
                elif (len(col) == 10) and (col[4] == '-'):
                    self.setItem(rc, colNo, self._dateItem(col))
                else:
                    self.setItem(rc, colNo, self._strItem(col))
                colNo += 1
        self.resizeColumnsToContents()


def tstHeaders(arr):
    farr = []
    for el in arr:
        farr.append('fld.%s' % el)
    return farr

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    rows = [[1, 'ted'], [2, 'popi'],[3,u'Γιώργος']]
    labels = ['id', 'name']
    dlg1 = TableWidget({'rows': rows, 'labels': labels})
    dlg1.show()
    s = app.exec_()
    sys.exit(s)
