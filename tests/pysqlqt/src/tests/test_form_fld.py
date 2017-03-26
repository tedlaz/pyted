#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on May 4, 2015

@author: tedlaz
'''

import sys
import os
from PyQt4 import QtGui, Qt
from collections import OrderedDict
# find parent directory and add it to the path if not already
PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if PATH not in sys.path:
    sys.path.append(PATH)
from gui.data_fields import form_parameters as fp
import test_db as tdb


class Test_fld(QtGui.QDialog):
    def __init__(self, pin, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        lay = QtGui.QFormLayout()
        self.flds = OrderedDict()
        self.flds['id'] = fp.Integer({})
        self.flds['ButtonText'] = fp.ButtonText(tdb.button_text_value)
        self.flds['ButtonText2'] = fp.ButtonText2(tdb.button_text_value)
        self.flds['CheckBox'] = fp.CheckBox({'val': 1})
        self.flds['Date'] = fp.Date({})
        self.flds['DateOrEmpty'] = fp.DateOrEmpty({})
        self.flds['Integer'] = fp.Integer({'val': 123})
        self.flds['Numeric'] = fp.Numeric({'val': 123.32})
        self.flds['Text'] = fp.Text({'val': 'First line\nSecond line'})
        self.flds['TextLine'] = fp.TextLine({'val': 'Text Line'})
        self.flds['TextLineMasked'] = fp.TextLineMasked({'val': '1234'})
        self.flds['WeekDays'] = fp.WeekDays({'val': [1, 1, 1, 1, 1, 0, 0]})
        for key in self.flds:
            if key != 'id':
                lay.addRow(QtGui.QLabel(key), self.flds[key])
        button = QtGui.QPushButton('print')
        lay.addRow(QtGui.QLabel(''), button)
        button.clicked.connect(self.printa)
        button.setFocusPolicy(0)
        self.setLayout(lay)

    def printa(self):
        tmpstr = u''
        for key in self.flds:
            tmpstr += u'%s : %s\n' % (key, self.flds[key].get())
        QtGui.QMessageBox.about(self, u'Τιμές πεδίων', tmpstr)

    def get(self):
        vals = {}
        for key in self.flds:
            vals[key] = self.flds[key].get()
        return vals

if __name__ == '__main__':
    from sys import argv, exit
    tdb.create_tst_db()
    app = QtGui.QApplication(argv)
    form = Test_fld(None)
    form.show()
    s = app.exec_()
    tdb.delete_tst_db()
    exit(s)
