# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\prj\pyQtAccounting\dlgiso.ui'
#
# Created: Tue Dec 13 20:01:09 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dlgiso(object):
    def setupUi(self, dlgiso):
        dlgiso.setObjectName(_fromUtf8("dlgiso"))
        dlgiso.resize(435, 79)
        dlgiso.setWindowTitle(QtGui.QApplication.translate("dlgiso", "Εκτύπωση Ισοζυγίου", None, QtGui.QApplication.UnicodeUTF8))
        self.lapo = QtGui.QLineEdit(dlgiso)
        self.lapo.setGeometry(QtCore.QRect(120, 10, 113, 22))
        self.lapo.setText(QtGui.QApplication.translate("dlgiso", "2011-01-01", None, QtGui.QApplication.UnicodeUTF8))
        self.lapo.setObjectName(_fromUtf8("lapo"))
        self.leos = QtGui.QLineEdit(dlgiso)
        self.leos.setGeometry(QtCore.QRect(120, 40, 113, 22))
        self.leos.setText(QtGui.QApplication.translate("dlgiso", "2011-12-31", None, QtGui.QApplication.UnicodeUTF8))
        self.leos.setObjectName(_fromUtf8("leos"))
        self.label = QtGui.QLabel(dlgiso)
        self.label.setGeometry(QtCore.QRect(30, 10, 53, 16))
        self.label.setText(QtGui.QApplication.translate("dlgiso", "Από", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(dlgiso)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 53, 16))
        self.label_2.setText(QtGui.QApplication.translate("dlgiso", "Έως", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.bprn = QtGui.QPushButton(dlgiso)
        self.bprn.setGeometry(QtCore.QRect(290, 10, 131, 51))
        self.bprn.setText(QtGui.QApplication.translate("dlgiso", "Εκτύπωση", None, QtGui.QApplication.UnicodeUTF8))
        self.bprn.setObjectName(_fromUtf8("bprn"))

        self.retranslateUi(dlgiso)
        QtCore.QMetaObject.connectSlotsByName(dlgiso)

    def retranslateUi(self, dlgiso):
        pass

