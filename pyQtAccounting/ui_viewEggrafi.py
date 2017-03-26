# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\prj\pyQtAccounting\viewEggrafi.ui'
#
# Created: Thu Jan 12 21:18:10 2012
#      by: PyQt4 UI code generator 4.8.5
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
        Dialog.resize(800, 600)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Εγγραφή", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setText(QtGui.QApplication.translate("Dialog", "Ημερομηνία", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Παραστατικό", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.tParastatiko = QtGui.QLineEdit(Dialog)
        self.tParastatiko.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tParastatiko.setObjectName(_fromUtf8("tParastatiko"))
        self.gridLayout.addWidget(self.tParastatiko, 1, 1, 1, 3)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Περιγραφή", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.tPerigrafi = QtGui.QLineEdit(Dialog)
        self.tPerigrafi.setObjectName(_fromUtf8("tPerigrafi"))
        self.gridLayout.addWidget(self.tPerigrafi, 2, 1, 1, 3)
        self.tNo = QtGui.QLineEdit(Dialog)
        self.tNo.setMaximumSize(QtCore.QSize(100, 16777215))
        self.tNo.setObjectName(_fromUtf8("tNo"))
        self.gridLayout.addWidget(self.tNo, 0, 2, 1, 1)
        self.tdate = QtGui.QLineEdit(Dialog)
        self.tdate.setMaximumSize(QtCore.QSize(120, 16777215))
        self.tdate.setObjectName(_fromUtf8("tdate"))
        self.gridLayout.addWidget(self.tdate, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tDetail = QtGui.QTableWidget(Dialog)
        self.tDetail.setAlternatingRowColors(True)
        self.tDetail.setObjectName(_fromUtf8("tDetail"))
        self.tDetail.setColumnCount(0)
        self.tDetail.setRowCount(0)
        self.tDetail.horizontalHeader().setStretchLastSection(True)
        self.tDetail.verticalHeader().setDefaultSectionSize(20)
        self.tDetail.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tDetail)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.bNewLine = QtGui.QPushButton(Dialog)
        self.bNewLine.setText(QtGui.QApplication.translate("Dialog", "Νέα γραμμή", None, QtGui.QApplication.UnicodeUTF8))
        self.bNewLine.setAutoDefault(False)
        self.bNewLine.setObjectName(_fromUtf8("bNewLine"))
        self.horizontalLayout.addWidget(self.bNewLine)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.txtYpol = QtGui.QLineEdit(Dialog)
        self.txtYpol.setMinimumSize(QtCore.QSize(100, 0))
        self.txtYpol.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtYpol.setFont(font)
        self.txtYpol.setText(QtGui.QApplication.translate("Dialog", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.txtYpol.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtYpol.setObjectName(_fromUtf8("txtYpol"))
        self.horizontalLayout.addWidget(self.txtYpol)
        self.bSave = QtGui.QPushButton(Dialog)
        self.bSave.setText(QtGui.QApplication.translate("Dialog", "Αποθήκευση", None, QtGui.QApplication.UnicodeUTF8))
        self.bSave.setAutoDefault(False)
        self.bSave.setObjectName(_fromUtf8("bSave"))
        self.horizontalLayout.addWidget(self.bSave)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass

