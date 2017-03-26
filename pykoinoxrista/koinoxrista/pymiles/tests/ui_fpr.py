# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tedlaz/python_work/pyMiles/pymiles/tests/fpr.ui'
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
        Dialog.resize(391, 173)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.epo = Text_line(Dialog)
        self.epo.setObjectName(_fromUtf8("epo"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.epo)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.ono = Text_line(Dialog)
        self.ono.setObjectName(_fromUtf8("ono"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.ono)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.patr = Text_line(Dialog)
        self.patr.setObjectName(_fromUtf8("patr"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.patr)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.id = Text_line(Dialog)
        self.id.setEnabled(False)
        self.id.setObjectName(_fromUtf8("id"))
        self.horizontalLayout.addWidget(self.id)
        self.bsave = QtGui.QPushButton(Dialog)
        self.bsave.setObjectName(_fromUtf8("bsave"))
        self.horizontalLayout.addWidget(self.bsave)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Φυσικό Πρόσωπο", None))
        self.label_2.setText(_translate("Dialog", "Επώνυμο", None))
        self.label_3.setText(_translate("Dialog", "Όνομα", None))
        self.label_4.setText(_translate("Dialog", "Όνομα Πατέρα", None))
        self.bsave.setText(_translate("Dialog", "Αποθήκευση", None))

from pymiles.gui.fields.textline import Text_line
