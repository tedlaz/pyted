# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tedlaz/prj/tst.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(425, 307)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.epo = QtGui.QLineEdit(Dialog)
        self.epo.setObjectName(_fromUtf8("epo"))
        self.verticalLayout.addWidget(self.epo)
        self.ono = QtGui.QLineEdit(Dialog)
        self.ono.setObjectName(_fromUtf8("ono"))
        self.verticalLayout.addWidget(self.ono)
        self.vals = QtGui.QTextEdit(Dialog)
        self.vals.setObjectName(_fromUtf8("vals"))
        self.verticalLayout.addWidget(self.vals)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))

