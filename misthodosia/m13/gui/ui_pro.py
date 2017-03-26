# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\ted\Dropbox\prj\m13\gui\pro.ui'
#
# Created: Thu Mar 28 22:38:32 2013
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
        Dialog.resize(600, 377)
        Dialog.setMinimumSize(QtCore.QSize(264, 297))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.t_tabl = QtGui.QTableWidget(Dialog)
        self.t_tabl.setObjectName(_fromUtf8("t_tabl"))
        self.t_tabl.setColumnCount(0)
        self.t_tabl.setRowCount(0)
        self.t_tabl.horizontalHeader().setVisible(True)
        self.t_tabl.horizontalHeader().setSortIndicatorShown(True)
        self.t_tabl.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.t_tabl)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.b_printPreview = QtGui.QPushButton(Dialog)
        self.b_printPreview.setObjectName(_fromUtf8("b_printPreview"))
        self.horizontalLayout.addWidget(self.b_printPreview)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.b_newRec = QtGui.QPushButton(Dialog)
        self.b_newRec.setAutoFillBackground(False)
        self.b_newRec.setStyleSheet(_fromUtf8("background-color: rgb(0, 170, 255);\n"
"color: rgb(255, 255, 0);"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/pr/tst")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_newRec.setIcon(icon)
        self.b_newRec.setObjectName(_fromUtf8("b_newRec"))
        self.horizontalLayout.addWidget(self.b_newRec)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Γενική Φόρμα", None, QtGui.QApplication.UnicodeUTF8))
        self.t_tabl.setSortingEnabled(True)
        self.b_printPreview.setText(QtGui.QApplication.translate("Dialog", "Εκτύπωση", None, QtGui.QApplication.UnicodeUTF8))
        self.b_newRec.setText(QtGui.QApplication.translate("Dialog", "Νέα Εγγραφή", None, QtGui.QApplication.UnicodeUTF8))

import res_rc
