# -*- coding: utf-8 -*-

import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import sys
import tedqt as qted
#from PyQt5.QtCore import pyqtSlot


class Test(Qw.QDialog):
    def __init__(self, db, parent=None):
        super().__init__()
        sq1 = "SELECT id || ' ' || lmp FROM lm WHERE id='%s'"
        sq9 = "SELECT id, id || ' ' || lmp as val FROM lm WHERE grup(val) LIKE '%%%s%%'"
        self.db = db
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.setWindowTitle(u'Δοκιμή qted')
        self.flds = [[Qw.QLabel('CheckBox'), qted.wChekcBox(2,self)],
                     [Qw.QLabel('Date'), qted.wDat('2015-01-01', self)],
                     [Qw.QLabel('DateEmpty'), qted.wDatEmpty('2015-01-02', self)],
                     [Qw.QLabel('Integer'), qted.wInt(145, self)],
                     [Qw.QLabel('Integer Spin'), qted.wIntSpin(12, self)],
                     [Qw.QLabel('Numeric'), qted.wNum(123.45, self)],
                     [Qw.QLabel('NumericSpin'), qted.wNumOld(11.23, self)],
                     [Qw.QLabel('Text'), qted.wText('This is just text', self)],
                     [Qw.QLabel('TextButton'), qted.wTxtButton('', sq1, sq9, self.db, self)],
                     [Qw.QLabel('Combo'), qted.wTxtCombo(3, [[1,u'Ενα'], [3, u'Τρία']], self)],
                     [Qw.QLabel('TextLine'), qted.wTxtLine('Ted Lazaros', self)],
                     [Qw.QLabel('TextLineNumbers'), qted.wTxtLineNum(123123123, self)],
                     [Qw.QLabel('WeekDays'), qted.wWeekdays([1,1,1,0,0,0,1], self)],
                     [Qw.QLabel('YesNo'), qted.wYesNo(False, [u'Όχι', u'Ναί'], self)],
                    ]
        layout = Qw.QFormLayout()
        for el in self.flds:
            layout.addRow(el[0], el[1])
        btn = Qw.QPushButton(u'Επιστροφή Τιμών')
        layout.addRow(Qw.QLabel(''), btn)
        self.setLayout(layout)
        btn.clicked.connect(self.getVals)
        btn.setFocusPolicy(Qc.Qt.NoFocus)
        self.flds[8][1].valNotFound.connect(self.test_slot)

    @Qc.pyqtSlot(str)
    def test_slot(self, val):
        Qw.QMessageBox.critical(self, u"Λάθος", u'Η τιμή %s δεν υπάρχει' % val)

    def getVals(self):
        ast = ''
        for el in self.flds:
            ast += '%s : %s\n' % (el[0].text(), el[1].get())
        Qw.QMessageBox.information(self, u"Τιμές πεδίων", ast)


if __name__ == '__main__':
    dbf = '/home/tedlaz/pyted/tederp/tst.db'
    sq1 = ''
    sq9 = ''
    app = Qw.QApplication(sys.argv)
    ui = Test(dbf)
    ui.show()
    sys.exit(app.exec_())
