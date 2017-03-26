# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\prj\pyQtAccounting\dlgifs.ui'
#
# Created: Tue Dec 13 18:12:03 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dlgifs(object):
    def setupUi(self, dlgifs):
        dlgifs.setObjectName(_fromUtf8("dlgifs"))
        dlgifs.resize(435, 103)
        dlgifs.setWindowTitle(QtGui.QApplication.translate("dlgifs", "Ημερήσιο Φύλλο Συναλλαγών", None, QtGui.QApplication.UnicodeUTF8))
        self.lapo = QtGui.QLineEdit(dlgifs)
        self.lapo.setGeometry(QtCore.QRect(120, 10, 113, 22))
        self.lapo.setObjectName(_fromUtf8("lapo"))
        self.leos = QtGui.QLineEdit(dlgifs)
        self.leos.setGeometry(QtCore.QRect(120, 40, 113, 22))
        self.leos.setObjectName(_fromUtf8("leos"))
        self.label = QtGui.QLabel(dlgifs)
        self.label.setGeometry(QtCore.QRect(30, 10, 53, 16))
        self.label.setText(QtGui.QApplication.translate("dlgifs", "Από", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(dlgifs)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 53, 16))
        self.label_2.setText(QtGui.QApplication.translate("dlgifs", "Έως", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.bprn = QtGui.QPushButton(dlgifs)
        self.bprn.setGeometry(QtCore.QRect(290, 10, 131, 51))
        self.bprn.setText(QtGui.QApplication.translate("dlgifs", "Εκτύπωση", None, QtGui.QApplication.UnicodeUTF8))
        self.bprn.setObjectName(_fromUtf8("bprn"))
        self.tameio = QtGui.QLineEdit(dlgifs)
        self.tameio.setGeometry(QtCore.QRect(120, 70, 113, 22))
        self.tameio.setText(QtGui.QApplication.translate("dlgifs", "38.00.0000", None, QtGui.QApplication.UnicodeUTF8))
        self.tameio.setObjectName(_fromUtf8("tameio"))
        self.label_3 = QtGui.QLabel(dlgifs)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 91, 16))
        self.label_3.setText(QtGui.QApplication.translate("dlgifs", "Λ/μός Ταμίου", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(dlgifs)
        QtCore.QMetaObject.connectSlotsByName(dlgifs)

    def retranslateUi(self, dlgifs):
        pass

