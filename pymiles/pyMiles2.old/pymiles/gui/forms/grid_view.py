# -*- coding: utf-8 -*-
from PyQt4 import QtGui, Qt, QtCore
from pymiles.sqlite.db_select import select
from pymiles.gui.forms.edit_record import Fdata_table
from pymiles.gui.forms.edit_master_detail import Master_detail
from pymiles.gui.forms.grid_items import tblitem


class Grid_table_view(QtGui.QDialog):

    def __init__(self, parent, table):
        QtGui.QDialog.__init__(self, parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        assert(table is not None)
        assert(parent is not None)
        self.meta = self.parent().meta
        self.db = self.parent().db
        assert(self.db is not None)
        assert(table in self.meta._tables)
        self.table = table
        self.tfields = self.meta.table_fields(self.table)
        self.tlabels = self.meta.labels_from_fields(self.tfields)
        self.setWindowTitle(self.meta.tlabel(self.table, True))

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.grid = QtGui.QTableWidget(self)

        self.lay.addWidget(self.grid)

        self.grid.verticalHeader().setStretchLastSection(False)
        self.grid.verticalHeader().setVisible(False)

        self.grid.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.grid.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.grid.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.grid.setAlternatingRowColors(True)
        altcolor = "alternate-background-color: rgba(208,246,230);"
        self.grid.setStyleSheet(altcolor)
        self.grid.cellDoubleClicked.connect(self.openform)

        btn = QtGui.QPushButton('New Record', self)
        self.lay.addWidget(btn)
        btn.clicked.connect(self.new_record)
        self.populate()
        self.grid.sortItems(0)

    def populate(self):
        self.grid.setSortingEnabled(False)
        self.grid.setRowCount(0)
        sqlp = self.meta.sql_rpr(self.table)
        # print(sqlp)
        vals = select(self.db, sqlp)

        self.grid.setRowCount(vals['rownum'])
        self.grid.setColumnCount(len(self.tfields))
        self.grid.setHorizontalHeaderLabels(self.tlabels)
        for i, row in enumerate(vals['rows']):
            for j, field in enumerate(self.tfields):
                val = '%s' % vals['rows'][i][field]
                typ = self.meta._ftyp[field]
                item = tblitem(typ, val)
                # item = QtGui.QTableWidgetItem('%s' % vals['rows'][i][field])
                self.grid.setItem(i, j, item)
        self.grid.setSortingEnabled(True)
        self.grid.resizeColumnsToContents()

    def keyPressEvent(self, ev):
        '''
        use enter or return for fast selection nad form close ...
        '''
        if (ev.key() == QtCore.Qt.Key_Enter or
                ev.key() == QtCore.Qt.Key_Return):
            self.openform()
        # QtGui.QDialog.keyPressEvent(self, ev)

    def openform(self):
        id_ = self.grid.item(self.grid.currentRow(), 0).text()
        ptable = '%s_d' % self.table
        if ptable in self.meta._tables:
            a = Master_detail(self, self.table, id_)
        else:
            a = Fdata_table(self, self.table, id_)
        if a.exec_() == QtGui.QDialog.Accepted:
            self.populate()

    def new_record(self):
        ptable = '%s_d' % self.table
        if ptable in self.meta._tables:
            a = Master_detail(self, self.table)
        else:
            a = Fdata_table(self, self.table)
        if a.exec_() == QtGui.QDialog.Accepted:
            self.populate()

    def sizeHint(self):
        return QtCore.QSize(800, 600)
