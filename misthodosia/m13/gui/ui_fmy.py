# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\ted\Dropbox\prj\m13\gui\fmy.ui'
#
# Created: Fri Feb 15 17:09:22 2013
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(312, 188)
        self.b_makeFile = QtGui.QPushButton(Dialog)
        self.b_makeFile.setGeometry(QtCore.QRect(50, 110, 131, 23))
        self.b_makeFile.setObjectName(_fromUtf8("b_makeFile"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.t_xrisi = QtGui.QLineEdit(Dialog)
        self.t_xrisi.setGeometry(QtCore.QRect(70, 30, 61, 20))
        self.t_xrisi.setObjectName(_fromUtf8("t_xrisi"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.b_makeFile.setText(QtGui.QApplication.translate("Dialog", "Δημιουργία αρχείου", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Χρήση", None, QtGui.QApplication.UnicodeUTF8))
        self.t_xrisi.setText(QtGui.QApplication.translate("Dialog", "2012", None, QtGui.QApplication.UnicodeUTF8))

