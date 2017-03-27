"""
Form transaction edit (insert, update, delete)
"""
import os
import sys
import PyQt5.QtCore as Qc
# import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw

from tedutil.dec import dec
from tedutil import db as tdb
import tedqt as tq

CPATH = os.path.dirname(os.path.abspath(__file__))
IM = [[1, u'Απογραφών/Ισολογισμών'], [2, u'Γενικό Ημερολόγιο']]
SQL1 = "SELECT lmo || ' ' || lmop FROM lmo WHERE id='%s'"
SQL9 = ("SELECT id, lmo || ' ' || lmop as val FROM lmo "
        "WHERE grup(val) LIKE '%%%s%%' "
        "ORDER BY val")


class Fedit(Qw.QDialog):
    signal_updated = Qc.pyqtSignal()

    def __init__(self, db, trid=None, templid=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.idv = trid
        self._ui()
        self._connections()
        if trid:
            self._setvals(trid)
        elif templid:  # Use another record as template
            self._settmpl(templid)
        else:
            # Add two rows to new transaction (Minimum one debit, one credit)
            self._addRow()
            self._addRow()

    def _ui(self):
        self.setWindowTitle(u'Νέα εγγραφή λογιστικής(%s)' % self.db)
        mainLayout = Qw.QVBoxLayout(self)
        glay = Qw.QGridLayout()
        flay = Qw.QGridLayout()
        mainLayout.addLayout(glay)
        self.tbl = Qw.QTableWidget(self)
        self.tbl.setAlternatingRowColors(True)
        mainLayout.addWidget(self.tbl)
        mainLayout.addLayout(flay)
        self.flds = {'id': tq.wIntSpin(),
                     'im_id': tq.wTxtCombo(2, IM),
                     'dat': tq.wDat(),
                     'par': tq.wTxtLine(),
                     'per': tq.wTxtLine()
                     }
        glay.addWidget(Qw.QLabel(u'Ημερολόγιο'), 0, 0)
        glay.addWidget(self.flds['im_id'], 0, 1)
        glay.addWidget(Qw.QLabel(u'Ημερομηνία'), 1, 0)
        glay.addWidget(self.flds['dat'], 1, 1)
        glay.addWidget(Qw.QLabel(u'Παραστατικό'), 2, 0)
        glay.addWidget(self.flds['par'], 2, 1)
        glay.addWidget(Qw.QLabel(u'Περιγραφή'), 3, 0)
        glay.addWidget(self.flds['per'], 3, 1)
        self.bAddLine = Qw.QPushButton(u'Νέα γραμμή')
        glay.addWidget(self.bAddLine, 4, 0)
        hds = [u'id', u'Λογαριασμός', u'Περιγραφή', u'Χρέωση', u'Πίστωση']
        self.tbl.setColumnCount(len(hds))
        self.tbl.hideColumn(0)
        self.tbl.setHorizontalHeaderLabels(hds)
        self.tbl.setColumnWidth(1, 450)  # Μέγεθος στήλης λογαριασμών
        self.ffld = {'txr': tq.wNum(),
                     'tpi': tq.wNum(),
                     'typ': tq.wNum()}
        alr = Qc.Qt.AlignRight | Qc.Qt.AlignTrailing | Qc.Qt.AlignVCenter
        for el in self.ffld:
            self.ffld[el].setAlignment(alr)
            self.ffld[el].setReadOnly(True)
        flay.addWidget(Qw.QLabel(u'Χρέωση'), 0, 0)
        flay.addWidget(Qw.QLabel(u'Πίστωση'), 0, 1)
        flay.addWidget(Qw.QLabel(u'Υπόλοιπο'), 0, 2)
        flay.addWidget(self.ffld['txr'], 1, 0)
        flay.addWidget(self.ffld['tpi'], 1, 1)
        flay.addWidget(self.ffld['typ'], 1, 2)
        sp = Qw.QSpacerItem(110, 20, Qw.QSizePolicy.Expanding,
                            Qw.QSizePolicy.Minimum)
        flay.addItem(sp, 1, 3)
        self.bSave = Qw.QPushButton(u'Αποθήκευση')
        flay.addWidget(self.bSave, 1, 4)
        self.bAddLine.setFocusPolicy(Qc.Qt.NoFocus)
        self.bSave.setFocusPolicy(Qc.Qt.NoFocus)
        self.resize(800, 600)
        self.setMinimumSize(800, 400)

    def _addSame(self):
        self.accept()
        newform = Fedit(self.db, None, self.idv)
        newform.exec_()

    def _connections(self):
        self.bAddLine.clicked.connect(self._addRow)
        self.bSave.clicked.connect(self._dbSave)

    def _addRow(self):
        rid = self.tbl.rowCount()  # Number of rows
        self.tbl.setRowCount(rid + 1)

        self.tbl.setCellWidget(rid, 0, tq.wIntSpin())
        self.tbl.setCellWidget(rid, 1, tq.wTxtButton('', SQL1, SQL9, self.db,
                                                     self.tbl))
        self.tbl.setCellWidget(rid, 2, tq.wTxtLine(parent=self.tbl))
        self.tbl.setCellWidget(rid, 3, tq.wNum(parent=self.tbl))
        self.tbl.setCellWidget(rid, 4, tq.wNum(parent=self.tbl))
        # Connect xr, pi fields
        self.tbl.cellWidget(rid, 3).editingFinished.connect(self._calcTotals)
        self.tbl.cellWidget(rid, 4).editingFinished.connect(self._calcTotals)

    def _setvals(self, vid):
        """
        Get values from database and set the to form fields for editing
        """
        dic = tdb.db2dic(self.db, vid, 'tr', 'trd', id_at_end=True)
        for key in dic:
            if key != 'zlines':
                self.flds[key].set(dic[key])
        self.tbl.setRowCount(0)
        for i, el in enumerate(dic['zlines']):
            self._addRow()
            self.tbl.cellWidget(i, 0).set(el['id'])
            self.tbl.cellWidget(i, 1).set(el['lmo_id'])
            self.tbl.cellWidget(i, 2).set(el['per2'])
            self.tbl.cellWidget(i, 3).set(el['_xr'])
            self.tbl.cellWidget(i, 4).set(el['_pi'])
        self._calcTotals()
        self.setWindowTitle(u'Εγγραφή %s (%s)' % (dic['id'], self.db))

    def _settmpl(self, vid):
        """
        Initialize transaction using existing transaction as template.
        """
        dic = tdb.db2dic(self.db, vid, 'tr', 'trd', id_at_end=True)
        self.flds['per'].set(dic['per'])
        self.flds['im_id'].set(dic['im_id'])
        self.tbl.setRowCount(0)
        for i, el in enumerate(dic['zlines']):
            self._addRow()
            self.tbl.cellWidget(i, 1).set(el['lmo_id'])
            self.tbl.cellWidget(i, 2).set(el['per2'])
            self.tbl.cellWidget(i, 3).set(el['_xr'])
            self.tbl.cellWidget(i, 4).set(el['_pi'])
        self._calcTotals()

    def _calcTotals(self):
        """
        Calculate totals of the form
        """
        txr = tpi = dec(0)
        for i in range(self.tbl.rowCount()):
            txr += dec(self.tbl.cellWidget(i, 3).get())
            tpi += dec(self.tbl.cellWidget(i, 4).get())
        self.ffld['txr'].set(txr)
        self.ffld['tpi'].set(tpi)
        self.ffld['typ'].set(txr - tpi)

    def _reset(self):
        """
        Reset form's data and get prepared for another new transaction
        """
        self.flds['par'].set('')
        # self.flds['per'].set('')
        for i in range(self.tbl.rowCount()):
            self.tbl.cellWidget(i, 3).set(0)
            self.tbl.cellWidget(i, 4).set(0)
        self._calcTotals()

    def keyPressEvent(self, ev):
        """Block escape key from closing form"""
        if ev.key() != Qc.Qt.Key_Escape:
            Qw.QDialog.keyPressEvent(self, ev)

    def dic(self):
        d = {}
        for el in self.flds:
            d[el] = self.flds[el].get()
        d['zlines'] = []

        for i in range(self.tbl.rowCount()):
            # Εάν έχουμε μηδενική τιμή αγνοούμε τη γραμμή
            d1 = {}
            d1['id'] = self.tbl.cellWidget(i, 0).get()
            if (self.tbl.cellWidget(i, 3).get() == 0 and
                    self.tbl.cellWidget(i, 4).get() == 0):
                if d1['id'] > 0:
                    d1['_d_'] = 1  # mark for deletion
                else:
                    continue

            d1['lmo_id'] = self.tbl.cellWidget(i, 1).get()
            d1['per2'] = self.tbl.cellWidget(i, 2).get()
            d1['_xr'] = self.tbl.cellWidget(i, 3).get()
            d1['_pi'] = self.tbl.cellWidget(i, 4).get()
            d['zlines'].append(d1)
        return d

    def _verrors(self):
        self._calcTotals()
        msg = u''
        if len(self.flds['par'].get()) < 3:
            msg += u'Δεν έχετε δώσει αριθμό παραστατικού\n'
        if (self.ffld['txr'].get() == 0) and (self.ffld['tpi'].get() == 0):
            msg += u'Μηδενικά άρθρα δεν επιτρέπονται\n'
        if self.ffld['typ'].get() != 0:
            msg += u'Το άρθρο πρέπει να είναι ισοσκελισμένο'
        return msg

    def _dbSave(self):
        errs = self._verrors()
        if len(errs) > 1:
            Qw.QMessageBox.critical(self,
                                    u"Για διόρθωση",
                                    '%s' % errs)
            return
        try:
            sql = tdb.md2sql('tr', 'trd', self.dic(), True)
            tdb.execute_script(self.db, sql)
            res = '%s' % tdb.rowst(self.db, "SELECT MAX(id) FROM tr;")[0][0]
        except Exception as e:
            Qw.QMessageBox.critical(self, u"Πρόβλημα", '%s' % e)
            return
        mainid = self.flds['id'].get()
        if mainid == 0:
            Qw.QMessageBox.information(self,
                                       u"Επιτυχία",
                                       'Αριθμός εγγραφής %s' % res)
            self._reset()
            self.flds['par'].setFocus(True)
        else:
            Qw.QMessageBox.information(self,
                                       u"Επιτυχία",
                                       'H eγγραφή %s ενημερώθηκε' % mainid)
        self.signal_updated.emit()


if __name__ == '__main__':
    DBPATH = '/home/tedlaz/pyted/tedaccounting/tst.aba'
    app = Qw.QApplication(sys.argv)
    ui = Fedit(DBPATH, 10)
    ui.show()
    sys.exit(app.exec_())