#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from decimal import Decimal as dec
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
from tedqt import f_table
from tedutil import db
import qacc
import isozygio as iso

cpath = os.path.dirname(os.path.abspath(__file__))


class Isozygio_form(Qw.QDialog):
    def __init__(self, dbpath, parent=None):
        super().__init__()
        self.db = dbpath
        self.setWindowTitle(u'Ισοζύγιο Λογαριασμών (%s)' % self.db)
        self._ui()
        self._style()

    def fillData(self):
        sql1 = "select * from vtr_trd"
        # dbpath = '/home/tedlaz/prj/samaras16c/gl201609.sql3'
        sa = {0: 'm', 1: 'm2', 2: 'm3', 3: 'm4', 4: 'm6', 5: 'y', 6: 's'}
        per = sa[self.flds['per'].currentIndex()]
        head, lines = iso.isoz_list(self.db, sql1, per)
        self.setHeaders(head)
        self.addRows(lines)

    def _style(self):
        self.style_data = ''
        with open(os.path.join(cpath, 'qdark.qss'), 'r') as afile:
            self.style_data = afile.read()
        self.setStyleSheet(self.style_data)

    def _ui(self):
        self.flds = {'per': Qw.QComboBox()}
        self.flds['per'].addItem(u'Μήνας')
        self.flds['per'].addItem(u'Δίμηνο')
        self.flds['per'].addItem(u'Τρίμηνο')
        self.flds['per'].addItem(u'Τετράμηνο')
        self.flds['per'].addItem(u'Εξάμηνο')
        self.flds['per'].addItem(u'Έτος')
        self.flds['per'].addItem(u'Σαιζόν')
        self.flds['per'].setCurrentIndex(2)  # Προεπιλογή το Τρίμηνο
        self.flds['per'].currentIndexChanged.connect(self.fillData)

        mainLayout = Qw.QVBoxLayout(self)
        glay = Qw.QGridLayout()
        glay.addWidget(Qw.QLabel(u'Περίοδος'), 0, 0)
        glay.addWidget(self.flds['per'], 0, 1)

        # self.bAddLine = Qw.QPushButton(u'Ενημέρωση')
        # glay.addWidget(self.bAddLine, 0, 2)

        mainLayout.addLayout(glay)

        self.tbl = Qw.QTableWidget(self)
        self.tbl.verticalHeader().setVisible(False)
        self.tbl.setSelectionMode(Qw.QAbstractItemView.SingleSelection)
        self.tbl.setSelectionBehavior(Qw.QAbstractItemView.SelectRows)
        # self.tbl.setStyleSheet(dbf.tblStyle)
        # self.tbl.setItemDelegate(ValidatedItemDelegate())
        # self.tbl.verticalHeader().setDefaultSectionSize(25)
        self.tbl.setAlternatingRowColors(True)

        mainLayout.addWidget(self.tbl)
        alr = Qc.Qt.AlignRight | Qc.Qt.AlignTrailing | Qc.Qt.AlignVCenter
        self.setLayout(mainLayout)
        self.resize(1000, 700)
        # self.bAddLine.clicked.connect(self.fillData)
        self.tbl.cellDoubleClicked.connect(self.dblCl)
        self.fillData()

    def dblCl(self, i, j):
        import kartella
        lmos = self.tbl.item(i, 0).text()
        lmpe = self.tbl.item(i, 1).text()
        rows, lbls = kartella.kartella(lmos, self.db)
        titl = u'Καρτέλλα λογαριασμού %s (%s)' % (lmos, lmpe)
        dlg1 = f_table.Form_find(lbls, rows, titl, self, False)
        dlg1.valselected.connect(self.vls)
        dlg1.show()
        # Qw.QMessageBox.information(self, u"tst", '%s %s %s' % (i, j, rows))

    def vls(self, val):
        # Qw.QMessageBox.information(self, u"Επιτυχία", 'Αριθμός εγγραφής %s' % val)
        adic = db.db2dic(self.db, int(val), 'tr', 'trd', id_at_end=False)
        editform = qacc.Insert_form(self.db, adic, self)
        editform.exec_()

    def setHeaders(self, headers=[]):
        if not headers:
            return
        self.tbl.setColumnCount(len(headers))
        self.tbl.setHorizontalHeaderLabels(headers)

    def addRows(self, rows=[[]]):
        if not rows:
            return
        self.tbl.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                if type(col) is dec:
                    item = Qw.QTableWidgetItem(iso.dec2gr(col))
                    item.setTextAlignment(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
                else:
                    item = Qw.QTableWidgetItem('%s' % col)
                self.tbl.setItem(i, j, item)
        self.tbl.resizeColumnsToContents()  # .resizeRowsToContents()


if __name__ == '__main__':
    db16 = '/home/tedlaz/tedfiles/prj/samaras2016d/2016.sql3'
    db15 = '/home/tedlaz/prj/samaras15/gl2015.sql3'
    dbm = '/home/tedlaz/MEGAsync/gastst.sql3'
    kms = '/home/tedlaz/Downloads/kms/kms.sql3'
    app = Qw.QApplication(sys.argv)
    ui = Isozygio_form(db16)
    ui.show()
    sys.exit(app.exec_())
