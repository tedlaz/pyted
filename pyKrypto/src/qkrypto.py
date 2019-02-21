#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import PyQt5 as q5
import PyQt5.QtWidgets as qw
from PyQt5.QtWidgets import QFileDialog as filed
from ui_edytoren import Ui_notatnik
from ui_mkkey import Ui_mkKeyDlg
import krypto as kr
import os

PNAM = "pyCrypto"
KEYFNAM = "Key file name"
KEYCREATED = "Key created"
SAVENC = "Save encrypted message"
MGNM = "You must give file name"
MUSTKEY = "You must create new or select existing key"
OPENEN = "Decrypt message"
KEYSEL = "Select key"


class thread1(q5.QtCore.QThread):
    thread1_finished = q5.QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        q5.QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.timer = q5.QtCore.QBasicTimer()
        self.step = 0
        self.par = parent

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        kr.krypto(self.par.filename, self.par.numlines)
        self.thread1_finished.emit('ok')


class MakeKey(qw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.par = parent
        self.ui = Ui_mkKeyDlg()
        self.ui.setupUi(self)
        self.filename = ''
        self.numlines = 0
        self.keymaker = thread1(self)
        self.ui.bFilename.clicked.connect(self.make_key)
        self.keymaker.thread1_finished.connect(self.key_created)
        self.made = False

    def make_key(self):
        self.filename, _ = filed.getSaveFileName(self, KEYFNAM, "", '')
        self.ui.txtFilename.setText(self.filename)

    def key_created(self, txt):
        qw.QMessageBox.information(self, PNAM, KEYCREATED)
        self.par.kryptoKey = self.filename
        self.par.ui.txtKeyFile.setText(self.filename)
        self.par.kryptoKey = self.filename
        self.par.settings.setValue("keypath", self.filename)
        qw.QDialog.accept(self)

    def accept(self):
        if len(self.filename) == 0:
            qw.QMessageBox.information(self, PNAM, MGNM)
            return
        self.numlines = int(self.ui.doubleSpinBox.value())
        self.keymaker.start()
        for i in range(self.numlines):
            self.ui.progressBar.setValue(i * 100 / self.numlines)


class MainWindow(q5.QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = q5.QtCore.QSettings()
        self.ui = Ui_notatnik()
        self.ui.setupUi(self)
        self.result = ''
        self.kryptoKey = self.settings.value("keypath", defaultValue='')
        self.messagePath = self.settings.value("msgpath", "")
        self.ui.txtKeyFile.setText(self.kryptoKey)
        self.ui.button_openkey.clicked.connect(self.file_open_key)
        self.ui.button_save.clicked.connect(self.file_save_message)
        self.ui.button_open.clicked.connect(self.file_open_message)
        self.ui.button_makeKey.clicked.connect(self.create_key)
        self.setWindowTitle("OneTimePad")

    def file_open_key(self):
        keydir = os.path.dirname('%s' % self.kryptoKey)
        filename, _ = filed.getOpenFileName(self, KEYSEL, keydir)
        from os.path import isfile
        if isfile(filename):
            self.ui.txtKeyFile.setText(filename)
            self.kryptoKey = filename
            self.settings.setValue("keypath", self.kryptoKey)
            self.settings.sync()

    def create_key(self):
        dlg = MakeKey(self)
        dlg.show()


    def noKey_message(self):
        qw.QMessageBox.error(self, PNAM, MUSTKEY)

    def file_open_message(self):
        self.ui.txtEdit.setPlainText('')
        if len(self.kryptoKey) == 0:
            self.noKey_message()
            return
        fname, _ = filed.getOpenFileName(self, OPENEN, self.messagePath)
        fp = os.path.dirname('%s' % fname)
        if len(fp) < 1 :
            return
        k = kr.krypto(self.kryptoKey)
        self.ui.txtEdit.setPlainText(str(k.dekrypto(fname)))
        self.settings.setValue("msgpath", fp)
        self.settings.sync()
        self.messagePath = fp

    def file_save_message(self):
        if len(self.kryptoKey) == 0:
            self.noKey_message()
            return
        saveFile, _ = filed.getSaveFileName(self, SAVENC ,self.messagePath)
        fp = os.path.dirname('%s' % saveFile)
        if len(fp) < 1 :
            return
        lines = self.ui.txtEdit.toPlainText().split('\n')
        self.settings.setValue("msgpath", fp)
        self.settings.sync()
        self.messagePath = fp
        k = kr.krypto(self.kryptoKey)
        k.kryptoLines(lines, saveFile)


if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    app.setOrganizationName("tedlaz")
    app.setOrganizationDomain("tedlaz.gr")
    app.setApplicationName(PNAM)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())
