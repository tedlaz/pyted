# -*- coding: utf-8 -*-
from PyQt4 import QtGui, Qt, QtCore
# from pymiles.utils.logger import log
from pymiles.gui.fields.selector import qtfield
from pymiles.sqlite.db_select import select
from pymiles.sqlite.db_sql import save as sqlsave
from pymiles.sqlite.db_save import save as dbsave


class Fdata_table(QtGui.QDialog):

    def __init__(self, parent, table, id_=None):
        QtGui.QDialog.__init__(self, parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.setMinimumWidth(400)

        assert(table is not None)
        assert(parent is not None)
        self.meta = self.parent().meta
        self.db = self.parent().db
        self.data = {}
        assert(self.db is not None)

        assert(table in self.meta._tables)
        self.table = table
        # Set window title by tlabel
        self.setWindowTitle(self.meta.tlabel(self.table))
        self.id = id_ or 0

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        flayout = QtGui.QFormLayout()
        self.qtfields = {}
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
        self.last_inserted_id = None

    def populate(self, id_):
        sqlg = "SELECT * FROM %s WHERE id=%s" % (self.table, id_)
        dictdata = select(self.db, sqlg)
        assert(dictdata['rownum'] == 1)  # Must have one and only one record
        self.data = dictdata['rows'][0]
        for fld in self.meta.table_fields(self.table):
            self.qtfields[fld].set(self.data[fld])

    def save(self):
        fields = self._get_updated_fields()
        if not fields:
            self.accept()
            return
        if 'id' not in fields:
            fields.append('id')
        dicforsql = {}
        for field in fields:
            dicforsql[field] = self.qtfields[field].get()
        sqls = sqlsave(self.table, dicforsql)
        self.last_inserted_id = dbsave(self.db, [sqls, ])
        self.accept()

    def _get_updated_fields(self):
        if not self.data:
            return self.meta.table_fields(self.table)
        updated_fields = []
        for fld in self.meta.table_fields(self.table):
            # print(self.data[fld], self.qtfields[fld].get())
            if str(self.data[fld]) != self.qtfields[fld].get():
                updated_fields.append(fld)
        return updated_fields
