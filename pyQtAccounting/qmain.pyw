#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 18 Φεβ 2011

@author: tedlaz
'''
# import sip
#sip.setapi('QString', 2)

import sys

from PyQt4 import QtGui, QtCore

import qIsozygio as isoz
import qImerologio as imer
import qinserteggrafi as ineggr

from ui_main import Ui_MainWindow
import dlgifs as ifs

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class fMain(QtGui.QMainWindow):
    def __init__(self, parent=None):
        self.settings = QtCore.QSettings()
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.ui.statusbar.showMessage(u'Χωρίς εταιρία')
        self.makeConnections()
        self.db = '%s' % self.settings.value("db_path", defaultValue=QtCore.QVariant('')).toString()
        #self.ui.statusbar.showMessage(self.db)
        self.setWindowTitle(self.db)
        #self.createTrayIcon()
        #icon = QtGui.QIcon()
        #icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/eurod")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.trayIcon.setIcon(icon)
        #self.trayIcon.show()
    def makeConnections(self):
        QtCore.QObject.connect(self.ui.bOpenIsozygio,QtCore.SIGNAL("clicked()"), self.openIsozygio)
        QtCore.QObject.connect(self.ui.action_isozygio,QtCore.SIGNAL("triggered()"),self.openIsozygio)
        QtCore.QObject.connect(self.ui.bOpenImerologio,QtCore.SIGNAL("clicked()"), self.openImerologio)
        QtCore.QObject.connect(self.ui.bInsertTransaction,QtCore.SIGNAL("clicked()"), self.insertTransaction)
        QtCore.QObject.connect(self.ui.action_eggrafi,QtCore.SIGNAL("triggered()"),self.insertTransaction)
        QtCore.QObject.connect(self.ui.action_open,QtCore.SIGNAL("triggered()"),self.fileOpen)
        QtCore.QObject.connect(self.ui.action_exit,QtCore.SIGNAL("triggered()"),self.close)
        QtCore.QObject.connect(self.ui.bifsprint,QtCore.SIGNAL("clicked()"), self.printifsdlg)
        QtCore.QObject.connect(self.ui.action_ifsPrint,QtCore.SIGNAL("triggered()"), self.printifsdlg)
        QtCore.QObject.connect(self.ui.btree,QtCore.SIGNAL("clicked()"), self.openTree)
    def openIsozygio(self):
        #self.ui.statusbar.showMessage(u'Βάση δεδομένων : ted.sql3')
        if self.db:
            fIsoz = isoz.fIsozygio(parent=self)
            #fIsoz.setModal(True)
            fIsoz.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            fIsoz.show()
            fIsoz.raise_()
            fIsoz.activateWindow()
    def openTree(self):
        import qtree
        if self.db:
            fTree = qtree.fTree(parent=self)
            fTree.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            fTree.show()
    def openImerologio(self):
        #self.ui.statusbar.showMessage(u'Βάση δεδομένων : ted.sql3')
        if self.db:
            fImer = imer.fImerologio(parent=self)
            fImer.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            fImer.show()
            fImer.raise_()
            fImer.activateWindow()
    def printifsdlg(self):
        dlgPrintIfs = ifs.fPrintIfs(parent=self)
        dlgPrintIfs.show()
    def fileOpen(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, u'Επιλογή Βάσης Δεδομένων',self.db,"DbFiles (*.sql3)")
        if fname:
            self.db = '%s' % fname
            self.settings.setValue("db_path",QtCore.QVariant(self.db))
            #self.ui.statusbar.showMessage(self.db)
            self.setWindowTitle(self.db)

    def insertTransaction(self):
        fInsertTransaction = ineggr.fInsertEggrafi(parent=self)
        fInsertTransaction.show()
    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.ui.action_open)
        self.trayIconMenu.addAction(self.ui.action_isozygio)
        self.trayIconMenu.addAction(self.ui.action_eggrafi)
        self.trayIconMenu.addAction(self.ui.action_ifsPrint)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.ui.action_exit)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            QtGui.QMessageBox.information(self, "Systray",
                    "The program will keep running in the system tray. To "
                    "terminate the program, choose <b>Quit</b> in the "
                    "context menu of the system tray entry.")
            self.hide()
            event.ignore()

if __name__ == "__main__":
    import os
    if '__file__' in globals():
        path = os.path.dirname(os.path.abspath(__file__))
    elif hasattr(sys, 'frozen'):
        path = os.path.dirname(os.path.abspath(sys.executable))  # for py2exe
    else:  # should never happen
        path = os.getcwd()

    os.chdir(path)
    sys.path = [path] + [p for p in sys.path if not p == path]

    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("ntaccountants")
    app.setOrganizationDomain("ntaccountants.gr")
    app.setApplicationName("pyAccounting")
    myApp = fMain()
    myApp.show()
    sys.exit(app.exec_())
