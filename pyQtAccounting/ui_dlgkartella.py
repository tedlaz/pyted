# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\prj\pyQtAccounting\dlgkartella.ui'
#
# Created: Wed Dec 21 12:36:09 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dlgkartella(object):
    def setupUi(self, dlgkartella):
        dlgkartella.setObjectName(_fromUtf8("dlgkartella"))
        dlgkartella.resize(449, 77)
        dlgkartella.setWindowTitle(QtGui.QApplication.translate("dlgkartella", "Καρτέλλα λογαριασμού", None, QtGui.QApplication.UnicodeUTF8))
        self.apo = QtGui.QLineEdit(dlgkartella)
        self.apo.setGeometry(QtCore.QRect(120, 10, 113, 22))
        self.apo.setText(QtGui.QApplication.translate("dlgkartella", "2011-01-01", None, QtGui.QApplication.UnicodeUTF8))
        self.apo.setObjectName(_fromUtf8("apo"))
        self.eos = QtGui.QLineEdit(dlgkartella)
        self.eos.setGeometry(QtCore.QRect(120, 40, 113, 22))
        self.eos.setText(QtGui.QApplication.translate("dlgkartella", "2011-12-31", None, QtGui.QApplication.UnicodeUTF8))
        self.eos.setObjectName(_fromUtf8("eos"))
        self.label = QtGui.QLabel(dlgkartella)
        self.label.setGeometry(QtCore.QRect(30, 10, 53, 16))
        self.label.setText(QtGui.QApplication.translate("dlgkartella", "Από", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(dlgkartella)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 53, 16))
        self.label_2.setText(QtGui.QApplication.translate("dlgkartella", "Έως", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.bprn = QtGui.QPushButton(dlgkartella)
        self.bprn.setGeometry(QtCore.QRect(290, 0, 151, 71))
        self.bprn.setText(QtGui.QApplication.translate("dlgkartella", "Εκτύπωση", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/pdf")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bprn.setIcon(icon)
        self.bprn.setIconSize(QtCore.QSize(60, 60))
        self.bprn.setObjectName(_fromUtf8("bprn"))

        self.retranslateUi(dlgkartella)
        QtCore.QMetaObject.connectSlotsByName(dlgkartella)

    def retranslateUi(self, dlgkartella):
        pass

import resources_rc
