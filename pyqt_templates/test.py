from qted import *


def qfl(label, widget):
    return [Qw.QLabel(label), widget]


class Test(Qw.QDialog):
    """Testing my controls"""
    def __init__(self, dbf, parent=None):
        super().__init__()
        self.dbf = dbf
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        self.setWindowTitle(u'Δοκιμή qted')
        self.flds = [qfl('TCheckBox', TCheckbox(2, self)),
                     qfl('TDate', TDate('2014-01-20', self)),
                     qfl('TDateEmpty', TDateEmpty('2015-10-21', self)),
                     qfl('TInteger', TInteger(145, self)),
                     qfl('TIntegerSpin', TIntegerSpin(12, self)),
                     qfl('TNumericSpin', TNumericSpin(123.45, self)),
                     qfl('TNumeric', TNumeric(11.23, self)),
                     qfl('TText', TText('This is just text', self)),
                     qfl('TTextButton', TTextButton('2', 'par', self.dbf, self)),
                     qfl('TCombo', TCombo(13,
                                          [[1, u'Ενα'],
                                           [2, u'Δύο'],
                                           [13, u'Τρία'],
                                           [14, u'Τέσσερα']
                                           ],
                                          self)),
                     qfl('TextLine', TTextLine('Ted Lazaros', self)),
                     qfl('TextLineNum', TTextlineNum(123123123, self)),
                     qfl('WeekDays', TWeekdays([1, 1, 1, 0, 0, 0, 1], self)),
                     qfl('YesNoCombo',
                         TYesNoCombo(False, [u'Όχι', u'Ναί'], self))
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
    import sys
    dbf0 = '/home/tedlaz/prj/pyted/pyqt_templates/tst_qtwidgets.db'
    app = Qw.QApplication(sys.argv)
    ui = Test(dbf0)
    ui.show()
    # sys.exit(app.exec_())
    # app = Qw.QApplication([])
    dialog = FTable(dbf0, 'pro', 2)
    dialog.show()
    appex = app.exec_()
    sys.exit(appex)