# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from frm_data import Fdata
# from fld_selector import makefld
from frm_seq import Fsequencial
import u_db_helper as dbh
# from u_logger import log


class Dsequential(QtGui.QDialog):

    def __init__(self, tables, table, val, parent):
        QtGui.QDialog.__init__(self, parent)
        self.tables = tables
        self.table = table
        self.db = parent.db
        self.val = val
        frm = Fsequencial(self.tables,
                          self.table,
                          val,
                          'one',
                          True,
                          [],
                          self)
        layo = QtGui.QVBoxLayout()
        layo.addWidget(frm)
        self.setLayout(layo)
        self.setWindowTitle(frm.title)


class anitem(QtGui.QTableWidgetItem):

    def __init__(self, val, fld, tables, db):
        QtGui.QTableWidgetItem.__init__(self)
        self.setText(val)
        self.fld = fld
        self.tables = tables
        self.db = db

    def set(self, val):
        if self.fld[-3:] == '_id':
            ptable = self.fld[:-3]
            rpv = ptable + '_rp'
            psql = self.tables[ptable]['rpr']
            sql = "%s WHERE id=%s" % (psql, val)
            result = dbh.select(self.db, sql)
            self.setText(result['rows'][0][rpv])
        else:
            self.setText(val)

    def get(self):
        return self.text


class Fgridv(Fdata):

    def create_gui(self):
        self.setMinimumWidth(800)
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        self.grid = QtGui.QTableWidget(self)
        self.layout.addWidget(self.grid)

        # Get data dimensions (How many columns , rows)
        self.grid.setColumnCount(len(self.meta['fields']))

        # Set column titles
        labels = []
        for i, fld in enumerate(self.meta["order"]):
            labels.append(self.meta["fields"][fld]['lbl'])
            if fld in self.invisible_fields:
                self.grid.setColumnHidden(i, True)
        self.grid.setHorizontalHeaderLabels(labels)
        self.grid.setColumnWidth(0, 30)
        # Create widgets
        for i in range(len(self.data['rows'])):
            self.add_row()
        self.grid.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.grid.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.grid.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.grid.cellDoubleClicked.connect(self.sendVals)
        # Create bottom buttons
        if not self.visible_buttons:
            return
        layout = QtGui.QHBoxLayout()
        b_ok_lbl = u'Αποθήκευση'

        self.b_ok = QtGui.QPushButton(b_ok_lbl)
        self.b_cancel = QtGui.QPushButton(u'Ακύρωση')
        self.b_add = QtGui.QPushButton(u'Νέα εγγραφή')
        layout.addWidget(self.b_cancel)
        layout.addWidget(self.b_add)
        self.b_add.setFocusPolicy(0)
        self.b_cancel.setFocusPolicy(0)
        self.b_ok.setFocusPolicy(0)
        layout.addWidget(self.b_ok)
        self.layout.addLayout(layout)
        self.b_ok.clicked.connect(self.resizegrid)
        self.b_add.clicked.connect(self.add_row)
        self.b_cancel.clicked.connect(self.closeit)
        self.grid.resizeColumnsToContents()

    def add_row(self):
        trows = self.grid.rowCount()
        self.grid.setRowCount(trows + 1)
        self.widgets.append({})
        for j, fld in enumerate(self.meta["order"]):
            self.widgets[trows][fld] = anitem('', fld, self.tables, self.db)
            self.grid.setItem(trows, j, self.widgets[trows][fld])

    def keyPressEvent(self, ev):
        '''
        use enter or return for fast selection nad form close ...
        '''
        if (ev.key() == QtCore.Qt.Key_Enter or
                ev.key() == QtCore.Qt.Key_Return):
            self.sendVals(self.grid.currentRow(), self.grid.currentColumn())
        QtGui.QWidget.keyPressEvent(self, ev)

    def sendVals(self, x, y):
        val = self.grid.item(x, 0).text()

        fff = Dsequential(self.tables, self.table, val, self)

        if fff.exec_() == 0:
            self.populate()

    def resizegrid(self):
        self.grid.resizeColumnsToContents()
