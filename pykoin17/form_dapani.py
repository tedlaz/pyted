# -*- coding: utf-8 -*-
'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''
# from PyQt5 import QtGui as Qg
from PyQt5 import QtCore as Qc
from PyQt5 import QtWidgets as Qw
import u_db


class Form_dapani(Qw.QDialog):

    '''
    Διαχείριση διαμερισμάτων
    '''

    def __init__(self, dbf, did=None, parent=None):
        super().__init__(parent)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.setWindowTitle(u'Δαπάνη')
        # self.setMinimumSize(800, 400)
        self.dbf = dbf
        self.id = did
        mainlayout = Qw.QVBoxLayout()
        self.setLayout(mainlayout)

        self.dfld = ['dap', ]
        self.labels = []
        self.fields = []
        self.labels.append(Qw.QLabel('Δαπάνη'))
        self.fields.append(Qw.QLineEdit())

        flayout = Qw.QFormLayout()
        for i, _ in enumerate(self.labels):
            flayout.insertRow(i, self.labels[i], self.fields[i])
        mainlayout.addLayout(flayout)

        self.bcanel = Qw.QPushButton(u'Ακύρωση', self)
        self.bcanel.setFocusPolicy(Qc.Qt.NoFocus)
        self.bdel = Qw.QPushButton(u'Διαγραφή', self)
        self.bdel.setFocusPolicy(Qc.Qt.NoFocus)
        self.bsave = Qw.QPushButton(u'Αποθήκευση', self)
        self.bsave.setFocusPolicy(Qc.Qt.NoFocus)
        blayout = Qw.QHBoxLayout()
        blayout.addWidget(self.bcanel)
        blayout.addWidget(self.bdel)
        blayout.addWidget(self.bsave)
        mainlayout.addLayout(blayout)
        self._connect()
        self.fill_widgets()

    def _connect(self):
        self.bcanel.clicked.connect(self.on_cancel)
        self.bdel.clicked.connect(self.on_delete)
        self.bsave.clicked.connect(self.on_save)

    def on_cancel(self):
        self.close()

    def on_delete(self):
        if not self.id:
            return
        sqld = ("DELETE FROM dap WHERE id='%s';\n"
                "DELETE FROM xiliosta WHERE dap_id='%s';")
        u_db.script(self.dbf, sqld % (self.id, self.id))
        self.accept()

    def on_save(self):
        sqli = 'INSERT INTO dap VALUES (null, %s);'
        sqlu = "UPDATE dap SET %s WHERE id='%s';"
        vals = []
        if not self.id:
            for wid in self.fields:
                vals.append("'%s'" % wid.text())
            fsql = sqli % ','.join(vals)
            u_db.script(self.dbf, fsql)
            self.accept()
        else:
            for i, fld in enumerate(self.dfld):
                vals.append("%s='%s'" % (fld, self.fields[i].text()))
            fsql = sqlu % (','.join(vals), self.id)
            u_db.script(self.dbf, fsql)
            self.accept()

    def fill_widgets(self):
        if not self.id:  # Αν δεν υπάρχει id τότε μην κάνεις τίποτα
            return
        sql = "SELECT * FROM dap WHERE id='%s'" % self.id

        diam = u_db.select(self.dbf, sql)
        for i, el in enumerate(diam[0]):
            if i == 0:
                continue
            self.fields[i-1].setText('%s' % diam[0][el])


if __name__ == '__main__':
    import sys
    app = Qw.QApplication([])
    dialog = Form_dapani('zzz.sql3')
    dialog.show()
    appex = app.exec_()
    sys.exit(appex)