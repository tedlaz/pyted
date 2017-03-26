# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\ted\Dropbox\prj\m13\gui\fpr.ui'
#
# Created: Tue Feb 19 13:04:05 2013
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
        Dialog.resize(263, 442)
        Dialog.setMinimumSize(QtCore.QSize(263, 442))
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setMinimumSize(QtCore.QSize(256, 101))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.b_save = QtGui.QPushButton(self.groupBox)
        self.b_save.setGeometry(QtCore.QRect(20, 60, 75, 23))
        self.b_save.setObjectName(_fromUtf8("b_save"))
        self.verticalLayout.addWidget(self.groupBox)
        self.tableView = QtGui.QTableView(Dialog)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Εισαγωγή Φυσικού Προσώπου", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Δοκιμαστικό", None, QtGui.QApplication.UnicodeUTF8))
        self.b_save.setText(QtGui.QApplication.translate("Dialog", "Αποθήκευση", None, QtGui.QApplication.UnicodeUTF8))

