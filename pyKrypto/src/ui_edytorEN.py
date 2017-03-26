# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tedlaz/myProjects/pyKrypto/src/edytorEN.ui'
#
# Created: Mon Feb 21 11:10:26 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_notatnik(object):
    def setupUi(self, notatnik):
        notatnik.setObjectName("notatnik")
        notatnik.resize(750, 493)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/key"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        notatnik.setWindowIcon(icon)
        notatnik.setStatusTip("")
        self.centralwidget = QtGui.QWidget(notatnik)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_makeKey = QtGui.QPushButton(self.centralwidget)
        self.button_makeKey.setIcon(icon)
        self.button_makeKey.setObjectName("button_makeKey")
        self.horizontalLayout.addWidget(self.button_makeKey)
        self.button_openkey = QtGui.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/filenew.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_openkey.setIcon(icon1)
        self.button_openkey.setObjectName("button_openkey")
        self.horizontalLayout.addWidget(self.button_openkey)
        self.txtKeyFile = QtGui.QLineEdit(self.centralwidget)
        self.txtKeyFile.setReadOnly(True)
        self.txtKeyFile.setObjectName("txtKeyFile")
        self.horizontalLayout.addWidget(self.txtKeyFile)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.txtEdit = QtGui.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setWeight(50)
        font.setBold(False)
        self.txtEdit.setFont(font)
        self.txtEdit.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.txtEdit.setObjectName("txtEdit")
        self.verticalLayout.addWidget(self.txtEdit)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_open = QtGui.QPushButton(self.centralwidget)
        self.button_open.setIcon(icon1)
        self.button_open.setObjectName("button_open")
        self.horizontalLayout_2.addWidget(self.button_open)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_save = QtGui.QPushButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/filesaveas.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_save.setIcon(icon2)
        self.button_save.setObjectName("button_save")
        self.horizontalLayout_2.addWidget(self.button_save)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/filequit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        notatnik.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(notatnik)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 23))
        self.menubar.setObjectName("menubar")
        notatnik.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(notatnik)
        self.statusbar.setObjectName("statusbar")
        notatnik.setStatusBar(self.statusbar)

        self.retranslateUi(notatnik)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), notatnik.close)
        QtCore.QMetaObject.connectSlotsByName(notatnik)

    def retranslateUi(self, notatnik):
        notatnik.setWindowTitle(QtGui.QApplication.translate("notatnik", "pyKrypto", None, QtGui.QApplication.UnicodeUTF8))
        self.button_makeKey.setText(QtGui.QApplication.translate("notatnik", "Δημιουργία κλειδιού", None, QtGui.QApplication.UnicodeUTF8))
        self.button_openkey.setText(QtGui.QApplication.translate("notatnik", "Κλειδί..", None, QtGui.QApplication.UnicodeUTF8))
        self.button_open.setText(QtGui.QApplication.translate("notatnik", "Μύνημα", None, QtGui.QApplication.UnicodeUTF8))
        self.button_save.setText(QtGui.QApplication.translate("notatnik", "Αποθήκευση", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("notatnik", "Τερματισμός", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
