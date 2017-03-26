# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\ted\Dropbox\prj\m13\gui\print_rpt_misthodosia.ui'
#
# Created: Wed Mar 20 17:15:00 2013
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
        Dialog.resize(479, 324)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblMis = QtGui.QTableWidget(Dialog)
        self.tblMis.setAlternatingRowColors(True)
        self.tblMis.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tblMis.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblMis.setObjectName(_fromUtf8("tblMis"))
        self.tblMis.setColumnCount(0)
        self.tblMis.setRowCount(0)
        self.tblMis.verticalHeader().setSortIndicatorShown(True)
        self.verticalLayout.addWidget(self.tblMis)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.d_date = QtGui.QDateEdit(Dialog)
        self.d_date.setCalendarPopup(True)
        self.d_date.setObjectName(_fromUtf8("d_date"))
        self.horizontalLayout.addWidget(self.d_date)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.b_print = QtGui.QPushButton(Dialog)
        self.b_print.setObjectName(_fromUtf8("b_print"))
        self.horizontalLayout.addWidget(self.b_print)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Εκτύπωση μισθοδοσίας", None, QtGui.QApplication.UnicodeUTF8))
        self.tblMis.setSortingEnabled(True)
        self.b_print.setText(QtGui.QApplication.translate("Dialog", "Εκτύπωση", None, QtGui.QApplication.UnicodeUTF8))

