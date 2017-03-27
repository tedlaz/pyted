"""
Form transaction edit (insert, update, delete)
"""
import os
import sys
import PyQt5.QtCore as Qc
import PyQt5.QtWidgets as Qw
from tedutil import db as tdb
import tedqt as tq

CPATH = os.path.dirname(os.path.abspath(__file__))


class Fedit(Qw.QDialog):
    signal_updated = Qc.pyqtSignal()

    def __init__(self, db, lmoid=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.idv = lmoid
        self._ui()
        self._connections()
        if lmoid:
            self._setvals(lmoid)

    def _ui(self):
        self.setWindowTitle(u'Νέος Λογαριασμός λογιστικής(%s)' % self.db)
        mainLayout = Qw.QVBoxLayout(self)
        glay = Qw.QGridLayout()
        flay = Qw.QGridLayout()
        mainLayout.addLayout(glay)
        mainLayout.addLayout(flay)
        self.flds = {'id': tq.wIntSpin(),
                     'lmo': tq.wTxtLine(),
                     'lmop': tq.wTxtLine()
                     }
        glay.addWidget(Qw.QLabel(u'Κωδικός'), 0, 0)
        glay.addWidget(self.flds['lmo'], 0, 1)
        glay.addWidget(Qw.QLabel(u'Περιγραφή λογαριασμού'), 1, 0)
        glay.addWidget(self.flds['lmop'], 1, 1)

        sp = Qw.QSpacerItem(110, 20, Qw.QSizePolicy.Expanding,
                            Qw.QSizePolicy.Minimum)
        flay.addItem(sp, 0, 0)
        self.bSave = Qw.QPushButton(u'Αποθήκευση')
        flay.addWidget(self.bSave, 0, 1)
        self.bSave.setFocusPolicy(Qc.Qt.NoFocus)
        self.setMinimumSize(500, 140)

    def _connections(self):
        self.bSave.clicked.connect(self._dbSave)

    def _setvals(self, vid):
        """
        Get values from database and set the to form fields for editing
        """
        dic = tdb.db2dic(self.db, vid, 'lmo', None, id_at_end=True)
        for key in dic:
            self.flds[key].set(dic[key])
        self.setWindowTitle(u'Εγγραφή %s (%s)' % (dic['id'], self.db))

    def _reset(self):
        """
        Reset form's data and get prepared for another new transaction
        """
        self.flds['lmo'].set('')
        self.flds['lmop'].set('')

    def keyPressEvent(self, ev):
        """Block escape key from closing form"""
        if ev.key() != Qc.Qt.Key_Escape:
            Qw.QDialog.keyPressEvent(self, ev)

    def dic(self):
        d = {}
        for el in self.flds:
            d[el] = self.flds[el].get()
        d['zlines'] = []
        return d

    def _verrors(self):
        msg = u''
        if len(self.flds['lmo'].get()) < 3:
            msg += u'Δεν έχετε δώσει κωδικό λογαριασμού\n'
        if len(self.flds['lmop'].get()) < 3:
            msg += u'Δεν έχετε δώσει περιγραφή λογαριασμού\n'
        return msg

    def _dbSave(self):
        errs = self._verrors()
        if len(errs) > 1:
            Qw.QMessageBox.critical(self,
                                    u"Για διόρθωση",
                                    '%s' % errs)
            return
        try:
            sql = tdb.md2sql('lmo', None, self.dic(), True)
            tdb.execute_script(self.db, sql)
            res = '%s' % tdb.rowst(self.db, "SELECT MAX(id) FROM lmo;")[0][0]
        except Exception as e:
            Qw.QMessageBox.critical(self, u"Πρόβλημα", '%s' % e)
            return
        mainid = self.flds['id'].get()
        if mainid == 0:
            Qw.QMessageBox.information(self,
                                       u"Επιτυχία",
                                       'Αριθμός εγγραφής %s' % res)
            self._reset()
            self.flds['lmo'].setFocus(True)
        else:
            Qw.QMessageBox.information(self,
                                       u"Επιτυχία",
                                       'H eγγραφή %s ενημερώθηκε' % mainid)
        self.signal_updated.emit()


if __name__ == '__main__':
    DBPATH = '/home/tedlaz/pyted/tedaccounting/tst.aba'
    app = Qw.QApplication(sys.argv)
    ui = Fedit(DBPATH, 6)
    ui.show()
    sys.exit(app.exec_())
