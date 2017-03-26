#!/usr/bin/python3
# -*- coding: utf-8 -*-

import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import sys
import os
import tedqt as qted
from tedutil.dec import dec
from tedutil import db as s2d
from lmocreate import mlmo
from suds.client import Client  # To setup run : sudo pip install suds-jurko

cpath = os.path.dirname(os.path.abspath(__file__))


def vatol(afm, countryCode='EL'):
    '''
    VAT Check online
    using SOAP client
    returns dictionary with:
    countryCode, vatNumber, requestDate, valid, name, address
    '''
    url = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    result = {'valid': False}
    try:
        client = Client(url, timeout=10)
        result = client.service.checkVat(countryCode, afm)
    except:
        result['conError'] = True
    return result


class Insert_form(Qw.QDialog):
    def __init__(self, db, dicval=None, parent=None):
        super().__init__()
        self.db = db
        self._ui()
        self._style()
        if dicval:
            self.setvals(dicval)

    def _style(self):
        self.style_data = ''
        with open(os.path.join(cpath, 'qdark.qss'), 'r') as afile:
            self.style_data = afile.read()
        self.setStyleSheet(self.style_data)

    def _ui(self):
        self.setWindowTitle(u'Νέα Εγγραφή')
        p1 = "SELECT id || ' ' || epo FROM syn WHERE id='%s'"
        p9 = "SELECT id, id || ' ' || epo as val FROM syn WHERE grup(val) LIKE '%%%s%%'"
        self.flds = {'id': qted.wIntSpin(),
                     'dat': qted.wDat(),
                     'par': qted.wTxtLine(),
                     'trp': qted.wTxtLine()
                     }

        mainLayout = Qw.QVBoxLayout(self)
        glay = Qw.QGridLayout()

        glay.addWidget(Qw.QLabel(u'Ημερομηνία'), 0, 0)
        glay.addWidget(self.flds['dat'], 0, 1)

        glay.addWidget(Qw.QLabel(u'Παραστατικό'), 1, 0)
        glay.addWidget(self.flds['par'], 1, 1)

        glay.addWidget(Qw.QLabel(u'Περιγραφή'), 2, 0)
        glay.addWidget(self.flds['trp'], 2, 1)

        self.bAddLine = Qw.QPushButton(u'Νέα γραμμή')
        glay.addWidget(self.bAddLine, 3, 0)

        mainLayout.addLayout(glay)

        self.tbl = Qw.QTableWidget(self)
        # self.tbl.setStyleSheet(dbf.tblStyle)
        # self.tbl.setItemDelegate(ValidatedItemDelegate())
        # self.tbl.verticalHeader().setDefaultSectionSize(25)
        self.tbl.setAlternatingRowColors(True)

        hds = [u'id', u'Λογαριασμός', u'Χρέωση', u'Πίστωση']
        self.tbl.setColumnCount(len(hds))
        self.tbl.hideColumn(0)
        self.tbl.setHorizontalHeaderLabels(hds)
        self.tbl.setColumnWidth(1, 450)  # Μέγεθος στήλης λογαριασμών
        mainLayout.addWidget(self.tbl)

        self.ffld = {'txr': qted.wNum(),
                     'tpi': qted.wNum(),
                     'typ': qted.wNum()}

        alr = Qc.Qt.AlignRight | Qc.Qt.AlignTrailing | Qc.Qt.AlignVCenter

        for el in self.ffld:
            self.ffld[el].setAlignment(alr)
            self.ffld[el].setReadOnly(True)

        flay = Qw.QGridLayout()
        flay.addWidget(Qw.QLabel(u'Χρέωση'), 0, 0)
        flay.addWidget(Qw.QLabel(u'Πίστωση'), 0, 1)
        flay.addWidget(Qw.QLabel(u'Υπόλοιπο'), 0, 2)
        flay.addWidget(self.ffld['txr'], 1, 0)
        flay.addWidget(self.ffld['tpi'], 1, 1)
        flay.addWidget(self.ffld['typ'], 1, 2)
        sp = Qw.QSpacerItem(110, 20, Qw.QSizePolicy.Expanding, Qw.QSizePolicy.Minimum)
        flay.addItem(sp, 1, 3)
        self.bSave = Qw.QPushButton(u'Αποθήκευση')
        flay.addWidget(self.bSave, 0, 4, 2, 1)
        mainLayout.addLayout(flay)

        self.setLayout(mainLayout)
        self.resize(800, 400)

        self.bAddLine.clicked.connect(self.addRow)
        self.bSave.clicked.connect(self.dbSave)
        self.bAddLine.setFocusPolicy(Qc.Qt.NoFocus)
        self.bSave.setFocusPolicy(Qc.Qt.NoFocus)
        # self.tbl.cellClicked.connect(self.cChanged)
        self.addRow()
        self.addRow()

    def keyPressEvent(self, ev):
        # Block escape key from closing form
        if ev.key() != Qc.Qt.Key_Escape:
            Qw.QDialog.keyPressEvent(self, ev)

    def dblxr(self):
        pass

    def setvals(self, dic):
        for key in dic:
            if key != 'zlines':
                self.flds[key].set(dic[key])
        self.tbl.setRowCount(0)
        for i, el in enumerate(dic['zlines']):
            self.addRow()
            self.tbl.cellWidget(i, 0).set(el['id'])
            self.tbl.cellWidget(i, 1).set(el['id_lmo'])
            self.tbl.cellWidget(i, 2).set(el['xr'])
            self.tbl.cellWidget(i, 3).set(el['pi'])
        self.calcTotals()
        self.setWindowTitle(u'Εγγραφή %s' % dic['id'])

    def calcTotals(self):
        txr = tpi = dec(0)
        for i in range(self.tbl.rowCount()):
            txr += dec(self.tbl.cellWidget(i, 2).get())
            tpi += dec(self.tbl.cellWidget(i, 3).get())
        self.ffld['txr'].set(txr)
        self.ffld['tpi'].set(tpi)
        self.ffld['typ'].set(txr - tpi)

    def reset(self):  # Μηδενισμός φόρμας
        self.flds['par'].set('')
        # self.flds['per'].set('')
        for i in range(self.tbl.rowCount()):
            self.tbl.cellWidget(i, 2).set(0)
            self.tbl.cellWidget(i, 3).set(0)
        self.calcTotals()

    def addRow(self):
        rid = self.tbl.rowCount()  # Number of rows
        self.tbl.setRowCount(rid + 1)

        sq1 = "SELECT lmo || ' ' || lmop FROM lmo WHERE id='%s'"
        sq9 = "SELECT id, lmo || ' ' || lmop as val FROM lmo WHERE grup(val) LIKE '%%%s%%'"
        self.tbl.setCellWidget(rid, 0, qted.wIntSpin())
        self.tbl.setCellWidget(rid, 1, qted.wTxtButton('', sq1, sq9, self.db, self.tbl))
        self.tbl.setCellWidget(rid, 2, qted.wNum(parent=self.tbl))
        self.tbl.setCellWidget(rid, 3, qted.wNum(parent=self.tbl))
        # self.tbl.cellWidget(rowidx, 2).doubleClicked.connect(self.tst)

        self.tbl.cellWidget(rid, 2).editingFinished.connect(self.calcTotals)
        self.tbl.cellWidget(rid, 3).editingFinished.connect(self.calcTotals)

    def tst(self):
        print(self.tbl.currentRow())

    def dic(self):
        d = {}
        for el in self.flds:
            d[el] = self.flds[el].get()
        d['zlines'] = []

        for i in range(self.tbl.rowCount()):
            # Εάν έχουμε μηδενική τιμή αγνοούμε τη γραμμή
            d1 = {}
            d1['id'] = self.tbl.cellWidget(i, 0).get()
            if (self.tbl.cellWidget(i, 2).get() == 0 and
                    self.tbl.cellWidget(i, 3).get() == 0):
                if d1['id'] > 0:
                    d1['_d_'] = 1  # mark for deletion
                else:
                    continue

            d1['id_lmo'] = self.tbl.cellWidget(i, 1).get()
            d1['xr'] = self.tbl.cellWidget(i, 2).get()
            d1['pi'] = self.tbl.cellWidget(i, 3).get()
            d['zlines'].append(d1)
        return d

    def verrors(self):
        msg = u''
        if len(self.flds['par'].get()) < 3:
            msg += u'Το παραστατικό πρέπει να έχει τιμή\n'
        if (self.ffld['txr'].get() == 0) and (self.ffld['tpi'].get() == 0):
            msg += u'Το άρθρο πρέπει να έχει γραμμές με τιμές\n'
        if self.ffld['typ'].get() != 0:
            msg += u'Το άρθρο πρέπεινα είναι ισοσκελισμένο'
        return msg

    def dbSave(self):
        errs = self.verrors()
        if len(errs) > 1:
            Qw.QMessageBox.critical(self, u"Παρακαλώ διορθώστε τα παρακάτω", '%s' % errs)
            return
        try:
            sql = s2d.md2sql('tr', 'trd', self.dic(), False)
            # print(sql)
            s2d.execute_script(self.db, sql)
            res = '%s' % s2d.rowst(self.db, "SELECT MAX(id) FROM tr;")[0][0]
        except Exception as e:
            Qw.QMessageBox.critical(self, u"Πρόβλημα", '%s' % e)
            return
        mainid = self.flds['id'].get()
        if mainid == 0:
            Qw.QMessageBox.information(self, u"Επιτυχία", 'Αριθμός εγγραφής %s' % res)
            self.reset()
            self.flds['par'].setFocus(True)
        else:
            Qw.QMessageBox.information(self, u"Επιτυχία", 'H eγγραφή %s ενημερώθηκε' % mainid)


if __name__ == '__main__':
    DBPATH = '/home/tedlaz/tedfiles/prj/samaras16c/gl201609.sql3'
    adic = s2d.db2dic(DBPATH, 95, 'tr', 'trd', id_at_end=False)
    print(adic)
    app = Qw.QApplication(sys.argv)
    ui = Insert_form(DBPATH, adic)
    ui.show()
    sys.exit(app.exec_())
