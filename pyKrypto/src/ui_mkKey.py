# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tedlaz/myProjects/pyKrypto/src/mkKey.ui'
#
# Created: Fri Feb  4 17:33:11 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_mkKeyDlg(object):
    def setupUi(self, mkKeyDlg):
        mkKeyDlg.setObjectName("mkKeyDlg")
        mkKeyDlg.resize(373, 213)
        self.verticalLayout = QtGui.QVBoxLayout(mkKeyDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bFilename = QtGui.QPushButton(mkKeyDlg)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/key"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bFilename.setIcon(icon)
        self.bFilename.setObjectName("bFilename")
        self.horizontalLayout.addWidget(self.bFilename)
        self.txtFilename = QtGui.QLineEdit(mkKeyDlg)
        self.txtFilename.setReadOnly(True)
        self.txtFilename.setObjectName("txtFilename")
        self.horizontalLayout.addWidget(self.txtFilename)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(mkKeyDlg)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(mkKeyDlg)
        self.doubleSpinBox.setDecimals(0)
        self.doubleSpinBox.setMinimum(5000.0)
        self.doubleSpinBox.setMaximum(500000.0)
        self.doubleSpinBox.setSingleStep(1000.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.horizontalLayout_2.addWidget(self.doubleSpinBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.progressBar = QtGui.QProgressBar(mkKeyDlg)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.buttonBox = QtGui.QDialogButtonBox(mkKeyDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(mkKeyDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), mkKeyDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), mkKeyDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(mkKeyDlg)

    def retranslateUi(self, mkKeyDlg):
        mkKeyDlg.setWindowTitle(QtGui.QApplication.translate("mkKeyDlg", "Δημιουργία κλειδιού", None, QtGui.QApplication.UnicodeUTF8))
        self.bFilename.setText(QtGui.QApplication.translate("mkKeyDlg", "Αρχείο", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("mkKeyDlg", "Γραμμές", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
