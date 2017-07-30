# -*- coding: utf-8 -*-
'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''
from PyQt5 import QtGui as Qg
from PyQt5 import QtCore as Qc
from PyQt5 import QtWidgets as Qw


class FormTemplate(Qw.QDialog):
    '''Put docstring here
    '''
    def __init__(self, dbf, did=None, parent=None):
        '''
        :param dbf: Database file path
        :param did: The id of the record. None for new record.
        '''
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.setWindowTitle(u'Form template Δοκιμαστικό')
        # basic data here
        self._db = dbf
        self._id = did
        self._table = 'tsttable'  # For use in get set operations
        # Set main layout
        mainlayout = Qw.QVBoxLayout()
        self.setLayout(mainlayout)
        # Create form layout for data widgets
        formlayout = Qw.QFormLayout()
        mainlayout.addLayout(formlayout)
        # Create widgets here and add them to formlayout

        # ------------------------------------------------------
        # -------- Widgets here
        # ------------------------------------------------------

        # Create button layout
        buttonlayout = Qw.QHBoxLayout()
        mainlayout.addLayout(buttonlayout)
        # Create buttons
        self.bcancel = Qw.QPushButton(u'Ακύρωση', self)
        buttonlayout.addWidget(self.bcancel)
        self.bsave = Qw.QPushButton(u'Αποθήκευση', self)
        buttonlayout.addWidget(self.bsave)
        # Create connections
        self._connect()

    def _connect(self):
        self.bcancel.clicked.connect(self.close)
        self.bsave.clicked.connect(self.save2db)

    def validate(self):
        return False

    def save2db(self):
        if not self.validate():
            Qw.QMessageBox.critical(self, u"Λάθος", u'...')
            return
        sqli = 'INSERT INTO %s VALUES (null, self._table, %s);'
        sqlu = "UPDATE %s " % self._table
        sqlu += "SET %s WHERE id='%s';"
        vals = []
        if not self._id:
            for widget in self.fields:
                vals.append("'%s'" % widget.text())
            fsql = sqli % ','.join(vals)
        else:
            for i, fld in enumerate(self.dfld):
                vals.append("%s='%s'" % (fld, self.fields[i].text()))
            fsql = sqlu % (','.join(vals), self.id)
        u_db.script(self._db, fsql)
        self.accept()

    def fill_widgets(self):
        if not self.id:  # Αν δεν υπάρχει id τότε μην κάνεις τίποτα
            return
        sql = "SELECT * FROM %s WHERE id='%s'" % (self._table, self._id)
        diam = u_db.select(self._db, sql)
        for i, el in enumerate(diam[0]):
            if i == 0:
                continue
            self.fields[i-1].setText('%s' % diam[0][el])


if __name__ == '__main__':
    import sys
    app = Qw.QApplication([])
    dialog = FormTemplate('zzz.sql3')
    dialog.show()
    appex = app.exec_()
    sys.exit(appex)
