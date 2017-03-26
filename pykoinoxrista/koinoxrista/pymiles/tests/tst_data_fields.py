# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from pymiles.gui.fields.selector import qtfield
from pymiles.sqlite.db_meta import Metadb


class tstform(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)
        self.db = 'tst.sql3'
        self.meta = Metadb()
        self.fields = []
        self.fl = QtGui.QFormLayout()
        self.addfield('BOOLEAN', 'Boolean')
        self.addfield('DATE', 'Date')
        self.addfield('DATEN', 'Daten')
        self.addfield('INTEGER', 'Integer')
        self.addfield('INTEGERS', 'Integer Spin')
        self.addfield('NUMERIC', 'Numeric')
        self.addfield('NUMERICS', 'Numeric spin')
        self.addfield('TEXT', 'Text')
        self.addfield('IDBUTTON', 'tr_id')
        self.addfield('IDCOMBO', 'tr_id')
        self.addfield('VARCHAR', 'Textline')
        self.addfield('VARCHARN', 'Textline number')
        self.addfield('WEEKDAYS', 'Weekdays')

        main_layout.addLayout(self.fl)
        btn = QtGui.QPushButton('Print Values and exit')
        main_layout.addWidget(btn)
        btn.clicked.connect(self.showvals)
        self.setWindowTitle('Testing data fields')

    def addfield(self, typ, name):
        fld = qtfield(typ, self, name)
        self.fields.append(fld)
        self.fl.addRow(QtGui.QLabel(name), fld)

    def showvals(self):
        for el in self.fields:
            print(el.get())
        self.accept()

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    app = QtGui.QApplication([])
    main = tstform()
    main.setMinimumSize(200, 100)
    main.show()
    s = app.exec_()
    sys.exit(s)
