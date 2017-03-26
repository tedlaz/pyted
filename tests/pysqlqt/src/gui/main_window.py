#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ted Lazaros
from utils import config_parser as cp
from PyQt4 import QtCore, QtGui

import sys
import os
from recources import qrc_res
from recources import res_helpers
from utils import sqlite3_methods as sq3
from classes import info


class Main_window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.file_suffix = 'tst'
        self.app_key = 'tst167'  # This is unique for the application
        self.path = os.path.realpath(os.path.dirname(__file__))
        self.ini_file = os.path.join(info.PATH, 'config.ini')

        self.createGui()

        self.db = ''
        db_from_ini = cp.read_parameter('file_name', 'Main', self.ini_file)
        if self.verify_db(db_from_ini):
            self.db = db_from_ini
            self.set_title()

    def db_changed(self, new_db_file):
        txtdbfile = '%s' % new_db_file
        if txtdbfile == self.db:
            QtGui.QMessageBox.about(
                self, u"Προσοχή !!", u"Το αρχείο είναι ήδη ανοικτό")
            return False
        if new_db_file and self.verify_db(new_db_file):
            self.db = new_db_file
            self.set_title()
            cp.add_and_save('file_name', new_db_file, 'Main', self.ini_file)
            QtGui.QMessageBox.about(
                self, u"Εντάξει", u"Άνοιξε το αρχείο : %s" % self.db)
            return True
        else:
            QtGui.QMessageBox.about(
                self,
                u"Προσοχή!!",
                u"Το αρχείο : %s δεν είναι συμβατό." % self.db)
            return False

    def verify_db(self, dbname):
        if not dbname:
            return False
        app_key = sq3.zread('app_key', dbname)
        if app_key == self.app_key:
            # print(app_key)
            return True
        else:
            # print(app_key)
            return False

    def set_title(self):
        self.setWindowTitle(u'Application Title %s' % self.db)

    def createGui(self):
        frame = QtGui.QFrame(self)
        hlayout = QtGui.QHBoxLayout(frame)

        layout = QtGui.QVBoxLayout()
        self.stackw = QtGui.QStackedWidget()
        layout.addWidget(self.stackw)

        hlayout.addLayout(layout)
        self.setCentralWidget(frame)
        self.setMinimumSize(800, 600)

        # Create Actions
        self.newDbAct = QtGui.QAction(
            QtGui.QIcon(':/images/new.png'),
            u"&Nέο αρχείο",
            self,
            shortcut=QtGui.QKeySequence.New,
            statusTip=u"Δημιουργία νέου αρχείου",
            triggered=self.newDB)

        self.openForm = QtGui.QAction(
            QtGui.QIcon(':/images/fileopen.png'),
            u"Άνοιγμα",
            self,
            statusTip=u"Άνοιγμα αρχείου",
            triggered=self.fileOpen)

        self.execBack = QtGui.QAction(
            QtGui.QIcon(':/images/back.png'),
            u"Επιστροφή",
            self,
            statusTip=u"Επιστροφή στην προηγούμενη οθόνη",
            triggered=self.to_do)

        self.addAct = QtGui.QAction(
            QtGui.QIcon(':/images/add.png'),
            u"Νέα εγγραφή",
            self,
            statusTip=u"Δημιουργία νέας εγγραφής",
            triggered=self.to_do)

        self.aboutAct = QtGui.QAction(
            QtGui.QIcon(':/images/info.png'),
            u"Περί της εφαρμογής",
            self,
            statusTip=u"Πληροφορίες για την εφαρμογή",
            triggered=self.about)

        self.coAct = QtGui.QAction(
            QtGui.QIcon(':/images/co.png'),
            u"Στοιχεία Επιχείρησης",
            self,
            statusTip=u"Στοιχεία Επιχείρησης",
            triggered=self.to_do)

        self.closeAct = QtGui.QAction(
            QtGui.QIcon(':/images/exit.png'),
            u"Έξοδος",
            self,
            statusTip=u"Έξοδος από την εφαρμογή",
            triggered=self.close)

        self.execCancel = QtGui.QAction(
            QtGui.QIcon(':/images/editdelete.png'),
            u"Επιστροφή",
            self,
            statusTip=u"Έξοδος και επιστροφή στο αρχικό μενού",
            triggered=self.to_do)

        self.execSave = QtGui.QAction(
            QtGui.QIcon(':/images/filesave.png'),
            u"Αποθήκευση",
            self,
            statusTip=u"Αποθήκευση αλλαγών",
            triggered=self.to_do)

        self.prnAct = QtGui.QAction(
            QtGui.QIcon(':/images/print.png'),
            u"Εκτύπωση",
            self,
            statusTip=u"Εκτύπωση",
            triggered=self.to_do)

        self.setAct = QtGui.QAction(
            QtGui.QIcon(':/images/set.png'),
            u"Επιλογές",
            self,
            statusTip=u"Επιλογές",
            triggered=self.to_do)

        self.closeDatAct = QtGui.QAction(
            QtGui.QIcon(':/images/par.png'),
            u"Ημ/νία κλειδώματος",
            self,
            statusTip=u"Ελάχιστη Ημερομηνία εισαγωγής",
            triggered=self.to_do)

        self.coDataAct = QtGui.QAction(
            QtGui.QIcon(':/images/set.png'),
            u"Στοιχεία επιχείρησης",
            self,
            statusTip=u"Στοιχεία επιχείρησης",
            triggered=self.to_do)

        # Create Menus
        fileMenu = self.menuBar().addMenu(u"&Αρχείο")
        fileMenu.addAction(self.newDbAct)
        fileMenu.addAction(self.openForm)
        fileMenu.addAction(self.closeAct)
        parMenu = self.menuBar().addMenu(u"Παράμετροι")
        parMenu.addAction(self.coDataAct)
        parMenu.addAction(self.closeDatAct)
        helpMenu = self.menuBar().addMenu(u"Βοήθεια")
        helpMenu.addAction(self.aboutAct)

        # Create Toolbars
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newDbAct)
        self.fileToolBar.addAction(self.openForm)

        self.execToolBar = self.addToolBar("Exec")
        self.execToolBar.addAction(self.execBack)
        self.execToolBar.addAction(self.addAct)
        self.execToolBar.addAction(self.execSave)
        self.execToolBar.addAction(self.prnAct)
        self.execToolBar.addAction(self.execCancel)

        self.helpToolBar = self.addToolBar("Help")
        self.helpToolBar.addAction(self.coDataAct)
        self.helpToolBar.addAction(self.closeDatAct)
        self.helpToolBar.addAction(self.aboutAct)

        # Create Statusbar
        self.statusBar().showMessage(u"Έτοιμοι")

    def newDB(self):
        fname = QtGui.QFileDialog.getSaveFileName(
            self,
            u"Δημιουργία Νέου αρχείου",
            os.path.dirname('filename'),
            u"Αρχείο (*.%s)" % self.file_suffix)
        if '.' + self.file_suffix not in fname:
            fname = '%s.%s' % (fname, self.file_suffix)
        fname = str(fname)  # Be sure it is always python string
        sql = res_helpers.readFromRes(':sql/createdb.sql')
        result = sq3.dbScript({'script': sql, 'db': fname})
        if result['status'] == 2:
            self.db_changed(fname)
            return True
        else:
            return False

    def fileOpen(self):
        fname = QtGui.QFileDialog.getOpenFileName(
            self,
            u'Επιλογή Αρχείου',
            self.db,
            u"Αρχείο (*.%s)" % self.file_suffix)
        if fname:
            self.db_changed(str(fname))

    def openForm1(self):
        pass

    def fileFromCommandLine(self, fname):
        pass

    def prn(self):
        pass
        # self.stackw.currentWidget()._print()

    def add(self):
        self.stackw.currentWidget().newRecord()

    def setwinTitle(self):
        self.setWindowTitle('Test Title')

    def about(self):
        QtGui.QMessageBox.about(
            self,
            u'Περί της εφαρμογής',
            res_helpers.readFromRes(":/txt/about.html"))

    def to_do(self):
        QtGui.QMessageBox.about(
            self,
            u"Υπό κατασκευή",
            u"Η εφαρμογή <b>M13</b> είναι "
            u"υπό κατασκευή<br>"
            u"Η ενέργεια που επιλέξατε "
            u"δεν έχει υλοποιηθεί ακόμη.")

    def closeEvent(self, event):
        msgBox = QtGui.QMessageBox(self)
        msgBox.setText(u'Θέλετε να κλείσετε την εφαρμογή?')
        msgBox.setIcon(QtGui.QMessageBox.Question)
        msgBox.setWindowTitle(u'Επιβεβαίωση εξόδου')
        msgBox.addButton(QtGui.QPushButton(u'Ναί'), QtGui.QMessageBox.YesRole)
        msgBox.addButton(QtGui.QPushButton(u'Όχι'), QtGui.QMessageBox.NoRole)
        reply = msgBox.exec_()
        if reply == 0:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/images/app.png"))
    myApp = Main_window()
    myApp.show()
    sys.exit(app.exec_())
