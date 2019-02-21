# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edytoren.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_notatnik(object):
    def setupUi(self, notatnik):
        notatnik.setObjectName("notatnik")
        notatnik.resize(750, 493)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/key"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        notatnik.setWindowIcon(icon)
        notatnik.setStatusTip("")
        self.centralwidget = QtWidgets.QWidget(notatnik)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_makeKey = QtWidgets.QPushButton(self.centralwidget)
        self.button_makeKey.setIcon(icon)
        self.button_makeKey.setObjectName("button_makeKey")
        self.horizontalLayout.addWidget(self.button_makeKey)
        self.button_openkey = QtWidgets.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/filenew.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_openkey.setIcon(icon1)
        self.button_openkey.setObjectName("button_openkey")
        self.horizontalLayout.addWidget(self.button_openkey)
        self.txtKeyFile = QtWidgets.QLineEdit(self.centralwidget)
        self.txtKeyFile.setReadOnly(True)
        self.txtKeyFile.setObjectName("txtKeyFile")
        self.horizontalLayout.addWidget(self.txtKeyFile)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.txtEdit = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.txtEdit.setFont(font)
        self.txtEdit.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.txtEdit.setObjectName("txtEdit")
        self.verticalLayout.addWidget(self.txtEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_open = QtWidgets.QPushButton(self.centralwidget)
        self.button_open.setIcon(icon1)
        self.button_open.setObjectName("button_open")
        self.horizontalLayout_2.addWidget(self.button_open)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_save = QtWidgets.QPushButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/filesaveas.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_save.setIcon(icon2)
        self.button_save.setObjectName("button_save")
        self.horizontalLayout_2.addWidget(self.button_save)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/filequit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        notatnik.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(notatnik)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 29))
        self.menubar.setObjectName("menubar")
        notatnik.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(notatnik)
        self.statusbar.setObjectName("statusbar")
        notatnik.setStatusBar(self.statusbar)

        self.retranslateUi(notatnik)
        self.pushButton_2.clicked.connect(notatnik.close)
        QtCore.QMetaObject.connectSlotsByName(notatnik)

    def retranslateUi(self, notatnik):
        _translate = QtCore.QCoreApplication.translate
        notatnik.setWindowTitle(_translate("notatnik", "pyKrypto"))
        self.button_makeKey.setToolTip(_translate("notatnik", "Generate new key file"))
        self.button_makeKey.setText(_translate("notatnik", "New key"))
        self.button_openkey.setToolTip(_translate("notatnik", "Use existing key file"))
        self.button_openkey.setText(_translate("notatnik", "Select key"))
        self.button_open.setToolTip(_translate("notatnik", "Message to decrypt"))
        self.button_open.setText(_translate("notatnik", "Open message"))
        self.button_save.setToolTip(_translate("notatnik", "Save encrypted message to a file"))
        self.button_save.setText(_translate("notatnik", "Save message"))
        self.pushButton_2.setStatusTip(_translate("notatnik", "Exit application"))
        self.pushButton_2.setText(_translate("notatnik", "Exit"))


import resources_rc
