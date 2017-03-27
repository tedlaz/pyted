#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from decimal import Decimal as deci
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
from tedqt import f_table
from tedqt import f_find
from tedutil import db
from tedutil import dec
import qedit
import isozygio as iso
import kartella

cpath = os.path.dirname(os.path.abspath(__file__))


class Fisozygio(Qw.QDialog):
    signal_updated = Qc.pyqtSignal()

    def __init__(self, dbpath, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db = dbpath
        self.setWindowTitle(u'Ισοζύγιο Λογαριασμών (%s)' % self.db)
        self._ui()

    def fillData(self):
        sql1 = "select * from vtr"
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
        self.flds['per'].setMinimumWidth(160)
        mainLayout = Qw.QVBoxLayout(self)
        glay = Qw.QGridLayout()
        glay.addWidget(Qw.QLabel(u'Περίοδος : '), 0, 0)
        glay.addWidget(self.flds['per'], 0, 1)
        sp = Qw.QSpacerItem(110, 20, Qw.QSizePolicy.Expanding,
                            Qw.QSizePolicy.Minimum)
        glay.addItem(sp, 0, 2)
        mainLayout.addLayout(glay)
        self.tbl = Qw.QTableWidget(self)
        self.tbl.verticalHeader().setVisible(False)
        self.tbl.setSelectionMode(Qw.QAbstractItemView.SingleSelection)
        self.tbl.setSelectionBehavior(Qw.QAbstractItemView.SelectRows)
        self.tbl.setAlternatingRowColors(True)
        mainLayout.addWidget(self.tbl)
        alr = Qc.Qt.AlignRight | Qc.Qt.AlignTrailing | Qc.Qt.AlignVCenter
        self.setLayout(mainLayout)
        self.resize(1000, 700)
        self.tbl.cellDoubleClicked.connect(self.dblCl1)
        self.fillData()

    def contextMenuEvent(self, event):
        menu = Qw.QMenu(self)
        a_clyp = menu.addAction(u"Κλείσιμο υπολοίπου")
        a_info = menu.addAction(u"Πληροφορίες λογαριασμού")
        # Action.triggered.connect(self.make_new)
        menu.exec_(event.globalPos())

    def dblCl(self, i, j):
        lmos = self.tbl.item(i, 0).text()
        lmpe = self.tbl.item(i, 1).text()
        rows, lbls = kartella.kartella(lmos, self.db)
        titl = u'Καρτέλλα λογαριασμού %s (%s)' % (lmos, lmpe)
        dlg1 = f_table.Form_find(lbls, rows, titl, self, False)
        dlg1.valselected.connect(self.vls)
        dlg1.show()

    def dblCl1(self, i, j):
        lmos = self.tbl.item(i, 0).text()
        lmpe = self.tbl.item(i, 1).text()
        if i > self.tbl.rowCount() - 4:
            return
        titl = u'Καρτέλλα λογαριασμού %s (%s)' % (lmos, lmpe)
        sql = ("select id, dat, lmo, lmop, par, xr, pi "
               "from vtr "
               "where lmo like '%s%%' "
               "order by dat, lmo, id;") % lmos
        lbl = ['id', 'Ημνία', 'Λογαριασμός', 'περιγραφή', 'παραστατικό',
               'χρέωση', 'πίστωση', 'Υπόλοιπο']
        dlg1 = f_find.Find(self.db, sql, lbl, self, None, False, titl)
        dlg1.signal_selected_id.connect(self.vls)
        dlg1.signal_make_new.connect(self.newv)
        self.signal_updated.connect(dlg1.slot_updated)
        dlg1.show()

    def newv(self, templateid):
        editform = qedit.Fedit(self.db, None, templateid, self)
        if self.parent:
            editform.signal_updated.connect(self.parent.slot_updated)
        else:
            editform.signal_updated.connect(self.slot_updated)
        editform.exec_()

    def vls(self, val):
        editform = qedit.Fedit(self.db, val, None, self)
        if self.parent:
            editform.signal_updated.connect(self.parent.slot_updated)
        else:
            editform.signal_updated.connect(self.slot_updated)
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
                if type(col) is deci:
                    item = Qw.QTableWidgetItem(dec.dec2gr2(col))
                    item.setTextAlignment(Qc.Qt.AlignRight |
                                          Qc.Qt.AlignVCenter)
                else:
                    item = Qw.QTableWidgetItem('%s' % col)
                self.tbl.setItem(i, j, item)
        self.tbl.resizeColumnsToContents()  # .resizeRowsToContents()

    @Qc.pyqtSlot()
    def slot_updated(self):
        self.fillData()
        self.signal_updated.emit()


if __name__ == '__main__':
    DBPATH = '/home/tedlaz/pyted/tedaccounting/tst.aba'
    # DBPATH = '/home/tedlaz/tedfiles/prj/samaras2016d/2016.sql3'
    app = Qw.QApplication(sys.argv)
    ui = Fisozygio(DBPATH)
    ui.show()
    sys.exit(app.exec_())
