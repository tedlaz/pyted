# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\ted\Dropbox\prj\m13\gui\calcmis.ui'
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
        Dialog.resize(551, 207)
        self.t_xrisi = QtGui.QLineEdit(Dialog)
        self.t_xrisi.setGeometry(QtCore.QRect(80, 10, 113, 20))
        self.t_xrisi.setObjectName(_fromUtf8("t_xrisi"))
        self.t_period = QtGui.QLineEdit(Dialog)
        self.t_period.setGeometry(QtCore.QRect(80, 40, 113, 20))
        self.t_period.setObjectName(_fromUtf8("t_period"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 51, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 51, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.b_calc = QtGui.QPushButton(Dialog)
        self.b_calc.setGeometry(QtCore.QRect(80, 140, 75, 23))
        self.b_calc.setObjectName(_fromUtf8("b_calc"))
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(210, 10, 131, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox_2 = QtGui.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(210, 40, 131, 22))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 51, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.t_typos = QtGui.QLineEdit(Dialog)
        self.t_typos.setGeometry(QtCore.QRect(80, 70, 113, 20))
        self.t_typos.setObjectName(_fromUtf8("t_typos"))
        self.cb_1 = QtGui.QComboBox(Dialog)
        self.cb_1.setGeometry(QtCore.QRect(210, 70, 301, 22))
        self.cb_1.setObjectName(_fromUtf8("cb_1"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Υπολογισμός Μισθοδοσίας", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Χρήση", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Περίοδος", None, QtGui.QApplication.UnicodeUTF8))
        self.b_calc.setText(QtGui.QApplication.translate("Dialog", "Υπολογισμός", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "2012", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "2013", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(0, QtGui.QApplication.translate("Dialog", "Ιανουάριος", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(1, QtGui.QApplication.translate("Dialog", "Φεβρουάριος", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(2, QtGui.QApplication.translate("Dialog", "Μάρτιος", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(3, QtGui.QApplication.translate("Dialog", "Απρίλιος", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(4, QtGui.QApplication.translate("Dialog", "Μάϊος", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(5, QtGui.QApplication.translate("Dialog", "Ιούνιος", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(6, QtGui.QApplication.translate("Dialog", "Ιούλιος", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(7, QtGui.QApplication.translate("Dialog", "Αύγουστος", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(8, QtGui.QApplication.translate("Dialog", "Σεπτέμβριος", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(9, QtGui.QApplication.translate("Dialog", "Οκτώβριος", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(10, QtGui.QApplication.translate("Dialog", "Νοέμβριος", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.setItemText(11, QtGui.QApplication.translate("Dialog", "Δεκέμβριος", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Τύπος", None, QtGui.QApplication.UnicodeUTF8))
        self.t_typos.setText(QtGui.QApplication.translate("Dialog", "1", None, QtGui.QApplication.UnicodeUTF8))

