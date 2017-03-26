# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\ted\Dropbox\prj\m13\gui\apd.ui'
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
        Dialog.resize(460, 274)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblXrisiTrimino = QtGui.QTableWidget(Dialog)
        self.tblXrisiTrimino.setObjectName(_fromUtf8("tblXrisiTrimino"))
        self.tblXrisiTrimino.setColumnCount(0)
        self.tblXrisiTrimino.setRowCount(0)
        self.verticalLayout.addWidget(self.tblXrisiTrimino)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.b_makeFile = QtGui.QPushButton(Dialog)
        self.b_makeFile.setObjectName(_fromUtf8("b_makeFile"))
        self.horizontalLayout.addWidget(self.b_makeFile)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Δημιουργία Αρχείου Α.Π.Δ.", None, QtGui.QApplication.UnicodeUTF8))
        self.b_makeFile.setText(QtGui.QApplication.translate("Dialog", "Δημιουργία αρχείου", None, QtGui.QApplication.UnicodeUTF8))

