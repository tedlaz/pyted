# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\ted\Dropbox\prj\m13\gui\tables.ui'
#
# Created: Wed Mar 06 21:57:52 2013
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
        Dialog.resize(590, 463)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.c_tables = QtGui.QComboBox(Dialog)
        self.c_tables.setMinimumSize(QtCore.QSize(150, 0))
        self.c_tables.setObjectName(_fromUtf8("c_tables"))
        self.horizontalLayout.addWidget(self.c_tables)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tb_table = QtGui.QTableView(Dialog)
        self.tb_table.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.tb_table.setObjectName(_fromUtf8("tb_table"))
        self.verticalLayout.addWidget(self.tb_table)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Πίνακες Εφαρμογής", None, QtGui.QApplication.UnicodeUTF8))

