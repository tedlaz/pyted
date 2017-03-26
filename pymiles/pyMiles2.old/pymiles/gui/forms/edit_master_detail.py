# -*- coding: utf-8 -*-
from PyQt4 import QtGui, Qt, QtCore
# from pymiles.utils.logger import log
from pymiles.gui.fields.selector import qtfield
from pymiles.sqlite.db_select import select
from pymiles.sqlite.db_sql import save_one_many as sqlom
from pymiles.sqlite.db_save import save_one_many as saveom
from pymiles.utils.txt_num import isNum, dec


class Master_detail(QtGui.QDialog):

    def __init__(self, parent, table, id_=None):
        QtGui.QDialog.__init__(self, parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.setMinimumWidth(800)

        assert(table is not None)
        assert(parent is not None)
        self.meta = self.parent().meta
        self.db = self.parent().db
        self.data = {}
        self.datad = []
        assert(self.db is not None)

        assert(table in self.meta._tables)
        self.table = table
        self.ptable = '%s_d' % table  # if master is tbl detail is tbl_d
        self.confield = '%s_id' % table  # We must have a field tbl_id in tbl_d
        assert(self.ptable in self.meta._tables)
        # Set window title by tlabel
        self.setWindowTitle(self.meta.tlabel(self.table))
        self.id = id_ or 0

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        flayout = QtGui.QFormLayout()
        self.qtfields = {}
        self.qtgfields = []
        for fld in self.meta.table_fields(self.table):
            typos = self.meta.ftype(fld)
            label = self.meta.flabel(fld)
            self.qtfields[fld] = qtfield(typos, self, fld)
            if fld != 'id':
                flayout.addRow(QtGui.QLabel(label), self.qtfields[fld])
            else:
                self.qtfields[fld].setVisible(False)
        self.lay.addLayout(flayout)
        # grid here
        self.grid = QtGui.QTableWidget(self)
        self.lay.addWidget(self.grid)

        self.gfields = self.meta.table_fields(self.ptable)
        self.glabels = self.meta.labels_from_fields(self.gfields)

        self.grid.setColumnCount(len(self.gfields))
        self.grid.setHorizontalHeaderLabels(self.glabels)
        for i, field in enumerate(self.gfields):
            if field == 'id' or field == self.confield:
                self.grid.setColumnHidden(i, True)

        self.blayout = QtGui.QHBoxLayout()
        self.lay.addLayout(self.blayout)
        bta = QtGui.QPushButton('add new line')
        self.blayout.addWidget(bta)
        bta.clicked.connect(self.add_empty_grid_line)

        btn = QtGui.QPushButton('Save and exit')
        self.blayout.addWidget(btn)
        btn.clicked.connect(self.savevals)

        bta.setFocusPolicy(QtCore.Qt.NoFocus)
        btn.setFocusPolicy(QtCore.Qt.NoFocus)

        if id_:
            self.populate(id_)

    def populate(self, id_):
        sqlg = "SELECT * FROM %s WHERE id=%s" % (self.table, id_)
        sqlp = "SELECT * FROM %s WHERE %s=%s"
        sqlpar = sqlp % (self.ptable, self.confield, id_)
        dictdata = select(self.db, sqlg)
        assert(dictdata['rownum'] == 1)
        self.data = dictdata['rows'][0]
        for fld in self.meta.table_fields(self.table):
            self.qtfields[fld].set(self.data[fld])
        dedata = select(self.db, sqlpar)
        self.datad = dedata['rows']
        self.grid.setRowCount(dedata['rownum'])
        self.qtgfields = []
        for i, line in enumerate(self.datad):
            lineqt = {}
            for j, field in enumerate(self.gfields):
                lineqt[field] = qtfield(self.meta.ftype(field), self, field)
                lineqt[field].set(self.datad[i][field])
                self.grid.setCellWidget(i, j, lineqt[field])
            self.qtgfields.append(lineqt)
        self.grid.setColumnWidth(2, 400)

    def add_empty_grid_line(self):
        rows = self.grid.rowCount()
        self.grid.setRowCount(rows + 1)
        lineqt = {}
        for i, field in enumerate(self.gfields):
            lineqt[field] = qtfield(self.meta.ftype(field), self, field)
            self.grid.setCellWidget(rows, i, lineqt[field])
            if field == 'id' or field == self.confield:
                lineqt[field].setVisible(False)
        self.qtgfields.append(lineqt)
        self.datad.append({})

    def savevals(self):
        fields = self._get_updated_fields()
        lines = self._get_updated_lines()
        dicone = {}
        for field in fields:
            dicone[field] = self.qtfields[field].get()
        if 'id' not in dicone:
            dicone['id'] = self.data['id']
        ldicma = []
        for i, line in enumerate(lines):
            if not line:
                continue
            if 'id' not in line:
                line.append('id')
            ldic = {}
            for field in line:
                ldic[field] = self.qtgfields[i][field].get()
            ldicma.append(ldic)
        lsql = sqlom(self.table, dicone, self.ptable, ldicma)
        print('---->', lsql)
        saveom(self.db, lsql)
        self.accept()

    def _get_updated_fields(self):
        if not self.data:
            return self.meta.table_fields(self.table)
        updated_fields = []
        for fld in self.meta.table_fields(self.table):
            # print(self.data[fld], self.qtfields[fld].get())
            dfld = self.data[fld]
            qfld = self.qtfields[fld].get()
            if isNum(dfld):
                dfld = str(dec(dfld))
            if isNum(qfld):
                qfld = str(dec(qfld))
            if dfld != qfld:
                updated_fields.append(fld)
        return updated_fields

    def _get_updated_lines(self):
        updated_lines = []
        for i, dline in enumerate(self.datad):
            if not dline:
                updated_lines.append(self.meta.table_fields(self.ptable))
                continue
            updated_fields = []
            for fld in self.meta.table_fields(self.ptable):
                dfld = self.datad[i][fld]
                qfld = self.qtgfields[i][fld].get()
                if isNum(dfld):
                    dfld = str(dec(dfld))
                if isNum(qfld):
                    qfld = str(dec(qfld))
                if dfld != qfld:
                    updated_fields.append(fld)
            updated_lines.append(updated_fields)
        print(updated_lines)
        return updated_lines
