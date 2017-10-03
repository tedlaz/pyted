#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
from ui_edytorEN import Ui_notatnik
from ui_mkKey import Ui_mkKeyDlg
import krypto as kr
import os


class thread1(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.timer = QtCore.QBasicTimer()
        self.step = 0
        self.par = parent

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        kr.krypto(self.par.filename, self.par.numlines)
        self.emit(QtCore.SIGNAL("madeKey( QString )"), 'ok')


class makeKey(QtGui.QDialog):
    def __init__(self, parent=None):
        self.par = parent
        QtGui.QWidget.__init__(self, parent)
        self.dui = Ui_mkKeyDlg()
        self.dui.setupUi(self)
        self.filename = ''
        self.numlines = 0
        self.keymaker = thread1(self)
        QtCore.QObject.connect(self.dui.bFilename, QtCore.SIGNAL("clicked()"), self.make_key)
        self.connect(self.keymaker, QtCore.SIGNAL("madeKey ( QString ) "), self.made)
        self.made = False

    def make_key(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getSaveFileName(self, u'όνομα αρχείου κλειδιού',os.path.dirname('%s' % self.par.kryptoKey))
        self.dui.txtFilename.setText(self.filename)

    def made(self, txt):
        QtGui.QMessageBox.information(self, u"pyKrypto ", u'Το κλειδί δημιουργήθηκε')
        self.par.kryptoKey = self.filename
        self.par.ui.txtKeyFile.setText(self.filename)
        QtGui.QDialog.accept(self)

    def accept(self):
        if len(self.filename) == 0:
            QtGui.QMessageBox.information(self, u"pyKrypto ", u'Πρέπει να δώσετε όνομα αρχείου')
            return
        self.numlines = int(self.dui.doubleSpinBox.value())
        self.keymaker.start()
        for i in range(self.numlines):
            self.dui.progressBar.setValue(i*100 / self.numlines)


class StartQT4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        self.settings = QtCore.QSettings()
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_notatnik()
        self.ui.setupUi(self)
        self.result = ''
        self.kryptoKey = self.settings.value("keypath", defaultValue=QtCore.QVariant('')).toString()
        self.messagePath = self.settings.value("msgpath", QtCore.QVariant('')).toString()
        self.ui.txtKeyFile.setText(self.kryptoKey)
        QtCore.QObject.connect(self.ui.button_openkey, QtCore.SIGNAL("clicked()"), self.file_dialog)
        QtCore.QObject.connect(self.ui.button_save, QtCore.SIGNAL("clicked()"), self.file_save)
        QtCore.QObject.connect(self.ui.button_open, QtCore.SIGNAL("clicked()"), self.file_open)
        QtCore.QObject.connect(self.ui.button_makeKey, QtCore.SIGNAL("clicked()"), self.create_key)

    def file_dialog(self):
        fd = QtGui.QFileDialog(self)
        filename = fd.getOpenFileName(self, u"Επιλογή κλειδιού",os.path.dirname('%s' % self.kryptoKey))
        from os.path import isfile
        if isfile(filename):
            self.ui.txtKeyFile.setText(filename)
            self.kryptoKey = filename
            self.settings.setValue("keypath", QtCore.QVariant(self.kryptoKey))
            self.settings.sync()

    def create_key(self):
        dlg = makeKey(self)
        dlg.show()

    def noKey_message(self):
        QtGui.QMessageBox.information(self, u"pyKrypto - Λάθος", u"Πρέπει να δημιουργήσετε ή να επιλέξετε κλειδί.")

    def file_open(self):
        self.ui.txtEdit.setPlainText('')
        if len(self.kryptoKey) == 0:
            self.noKey_message()
            return
        fd = QtGui.QFileDialog(self)
        fname = fd.getOpenFileName(self, u"Άνοιγμα κωδικοποιημένου μυνήματος", self.messagePath)
        fp = os.path.dirname('%s' % fname)
        if len(fp) < 1 :
            return
        k = kr.krypto(self.kryptoKey)
        self.ui.txtEdit.setPlainText(k.dekrypto(fname).decode('utf-8'))
        self.settings.setValue("msgpath", QtCore.QVariant(fp))
        self.settings.sync()
        self.messagePath = fp

    def file_save(self):
        if len(self.kryptoKey) == 0:
            self.noKey_message()
            return
        fd = QtGui.QFileDialog(self)
        saveFile = fd.getSaveFileName(self, u"Αποθήκευση κωδικοποιημένου αρχείου",self.messagePath)
        fp = os.path.dirname('%s' % saveFile)
        if len(fp) < 1 :
            return
        lines = self.ui.txtEdit.toPlainText().split('\n')
        self.settings.setValue("msgpath", QtCore.QVariant(fp))
        self.settings.sync()
        self.messagePath = fp
        k = kr.krypto(self.kryptoKey)
        k.kryptoLines(lines, saveFile)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("ntaccountants")
    app.setOrganizationDomain("ntaccountants.gr")
    app.setApplicationName("pyKrypto")
    myapp = StartQT4()
    myapp.show()
    sys.exit(app.exec_())
