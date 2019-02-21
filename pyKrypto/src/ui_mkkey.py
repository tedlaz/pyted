# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mkkey.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mkKeyDlg(object):
    def setupUi(self, mkKeyDlg):
        mkKeyDlg.setObjectName("mkKeyDlg")
        mkKeyDlg.resize(439, 250)
        self.verticalLayout = QtWidgets.QVBoxLayout(mkKeyDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(mkKeyDlg)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(mkKeyDlg)
        self.doubleSpinBox.setDecimals(0)
        self.doubleSpinBox.setMinimum(5000.0)
        self.doubleSpinBox.setMaximum(500000.0)
        self.doubleSpinBox.setSingleStep(1000.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.horizontalLayout_2.addWidget(self.doubleSpinBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bFilename = QtWidgets.QPushButton(mkKeyDlg)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/key"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bFilename.setIcon(icon)
        self.bFilename.setObjectName("bFilename")
        self.horizontalLayout.addWidget(self.bFilename)
        self.txtFilename = QtWidgets.QLineEdit(mkKeyDlg)
        self.txtFilename.setReadOnly(True)
        self.txtFilename.setObjectName("txtFilename")
        self.horizontalLayout.addWidget(self.txtFilename)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.progressBar = QtWidgets.QProgressBar(mkKeyDlg)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.buttonBox = QtWidgets.QDialogButtonBox(mkKeyDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(mkKeyDlg)
        self.buttonBox.accepted.connect(mkKeyDlg.accept)
        self.buttonBox.rejected.connect(mkKeyDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(mkKeyDlg)
        mkKeyDlg.setTabOrder(self.doubleSpinBox, self.bFilename)
        mkKeyDlg.setTabOrder(self.bFilename, self.txtFilename)
        mkKeyDlg.setTabOrder(self.txtFilename, self.buttonBox)

    def retranslateUi(self, mkKeyDlg):
        _translate = QtCore.QCoreApplication.translate
        mkKeyDlg.setWindowTitle(_translate("mkKeyDlg", "Key creator"))
        self.label.setToolTip(_translate("mkKeyDlg", "Number of lines"))
        self.label.setText(_translate("mkKeyDlg", "Lines"))
        self.doubleSpinBox.setToolTip(_translate("mkKeyDlg", "Number of lines"))
        self.bFilename.setStatusTip(_translate("mkKeyDlg", "File name for the new key"))
        self.bFilename.setText(_translate("mkKeyDlg", "File name"))


import resources_rc
