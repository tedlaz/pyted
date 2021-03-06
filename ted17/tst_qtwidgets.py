"""Testing my pyqt widgets"""
from PyQt5 import QtGui as Qg
from PyQt5 import QtCore as Qc
from PyQt5 import QtWidgets as Qw
import sys
import os
import ted17 as tqt


def qfl(label, widget):
    return [Qw.QLabel(label), widget]


class Test(Qw.QDialog):
    """Testing my controls"""
    def __init__(self, dbf, parent=None):
        super().__init__()
        self.dbf = dbf
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.setWindowTitle(u'Δοκιμή qted')
        self.flds = [qfl('CheckBox', tqt.wChekcBox(2, self)),
                     qfl('Date', tqt.wDat('', self)),
                     qfl('DateEmpty', tqt.wDatEmpty('', self)),
                     qfl('Integer', tqt.wInt(145, self)),
                     qfl('Integer Spin', tqt.wIntSpin(12, self)),
                     qfl('Numeric', tqt.wNum(123.45, self)),
                     qfl('NumericSpin', tqt.wNumOld(11.23, self)),
                     qfl('Text', tqt.wText('This is just text', self)),
                     #  qfl('TextButton', tqt.wTxtButton('62.04.05',
                     #                                   sq1,
                     #                                   sq9, self.db, self)),
                     qfl('TextButton', tqt.wTxtButton('1', 'par', self)),
                     qfl('Combo', tqt.wTxtCombo(3, [[1, u'Ενα'],
                                                    [2, u'Δύο'],
                                                    [3, u'Τρία']], self)),
                     qfl('TextLine', tqt.wTxtLine('Ted Lazaros', self)),
                     qfl('TextLineNumbers', tqt.wTxtLineNum(123123123, self)),
                     qfl('WeekDays', tqt.wWeekdays([1, 1, 1, 0, 0, 0, 1],
                                                   self)),
                     qfl('YesNo', tqt.wYesNo(False, [u'Όχι', u'Ναί'], self))
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
    a = tqt.dec.dec('2356.00')
    dbf = 'tst_qtwidgets.db'
    app = Qw.QApplication(sys.argv)
    ui = Test(dbf)
    ui.show()
    sys.exit(app.exec_())
