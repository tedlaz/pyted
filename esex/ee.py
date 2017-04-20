#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ted Lazaros
"""

from PyQt4 import QtCore, QtGui
import sys
import os
from qtdb import dbforms as dbf
from qtdb import f_about
from qtdb import qtree as qtr
from qtdb import qinesoda as es
from qtdb import qinejoda as ej
from qtdb import res_rc
from qtdb import f2
from qtdb import minkat
import app_config


def isValidDB(db):  # check if db is payroll db
    '''
    if dbf.getDbOneRow('SELECT * FROM m12_co',db):
        return True
    else:
        return False
    '''
    return True


def coText(db):
    '''
    Returns text with Company Name , etc ...
    '''
    sql = "SELECT cop || ' ' || ono FROM co WHERE id=?"
    coname = dbf.getDbSingleVal(sql, ('1',), db)
    if coname:
        return "%s" % coname.strip()
    else:
        return u"Λάθος Αρχείο"


class fMain(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.settings = QtCore.QSettings()
        self.db = '%s' % self.settings.value("db_path", defaultValue=QtCore.QVariant('')).toString()
        # self.db = '%s' % self.settings.value("db_path", defaultValue='')
        self.createGui()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.makeConnections()

        self.exStatus()
        self.setWindowTitle(app_config.applicationTitle())
        self.onStartOrFileOpen()

    def createGui(self):
        frame = QtGui.QFrame(self)
        hlayout = QtGui.QHBoxLayout(frame)

        layout = QtGui.QVBoxLayout()
        self.stackw = QtGui.QStackedWidget()
        layout.addWidget(self.stackw)

        hlayout.addLayout(layout)
        self.setCentralWidget(frame)
        self.setMinimumSize(800, 600)

    def makeConnections(self):
        # self.treeWidget.clicked.connect(self.runPlugin)
        # self.stackw.doubleClicked.connect(self.runPlugin)
        pass

    def exBack(self):
        '''
        Function to go back to previus stack
        '''
        if self.stackw.count() > 1:
            forRemoval = self.stackw.currentWidget()
            self.stackw.removeWidget(forRemoval)
            forRemoval.setParent(None)
            # forRemoval.Delete()
            self.exStatus()
            self.setwinTitle()

    def exStatus(self):
        if self.stackw.count() > 1:
            self.execBack.setEnabled(True)
            self.addAct.setEnabled(self.stackw.currentWidget().canAdd())
            # self.prnAct.setEnabled(self.stackw.currentWidget().canPrint())
        else:
            self.execBack.setEnabled(False)
            self.addAct.setEnabled(False)
            self.execCancel.setEnabled(False)
            self.execSave.setEnabled(False)
            self.prnAct.setEnabled(False)

    def resetStackw(self):
        no = self.stackw.count()
        for i in range(no):
            forRemoval = self.stackw.currentWidget()
            self.stackw.removeWidget(forRemoval)
            forRemoval.setParent(None)
        self.exStatus()

    def createActions(self):
        self.addAct = QtGui.QAction(QtGui.QIcon(':/images/add.png'),
                                    u"Νέα εγγραφή",
                                    self,
                                    statusTip=u"Δημιουργία νέας εγγραφής",
                                    triggered=self.add)
        self.aboutAct = QtGui.QAction(QtGui.QIcon(':/images/info.png'),
                                      u"Περί της εφαρμογής",
                                      self,
                                      statusTip=u"Πληροφορίες για την εφαρμογή",
                                      triggered=self.about)
        self.coAct = QtGui.QAction(QtGui.QIcon(':/images/co.png'),
                                   u"Στοιχεία Επιχείρησης",
                                   self,
                                   statusTip=u"Στοιχεία Επιχείρησης",
                                   triggered=self.toDo)
        self.closeAct = QtGui.QAction(QtGui.QIcon(':/images/exit.png'),
                                      u"Έξοδος",
                                      self,
                                      statusTip=u"Έξοδος από την εφαρμογή",
                                      triggered=self.close)
        self.execBack = QtGui.QAction(QtGui.QIcon(':/images/back.png'),
                                      u"Επιστροφή",
                                      self,
                                      statusTip=u"Επιστροφή στην προηγούμενη οθόνη",
                                      triggered=self.exBack)
        self.execCancel = QtGui.QAction(QtGui.QIcon(':/images/editdelete.png'),
                                        u"Επιστροφή",
                                        self,
                                        statusTip=u"Έξοδος και επιστροφή στο αρχικό μενού",
                                        triggered=self.toDo)
        self.execSave = QtGui.QAction(QtGui.QIcon(':/images/filesave.png'),
                                      u"Αποθήκευση",
                                      self,
                                      statusTip=u"Αποθήκευση αλλαγών",
                                      triggered=self.toDo)
        self.openForm = QtGui.QAction(QtGui.QIcon(':/images/fileopen.png'),
                                      u"Άνοιγμα",
                                      self,
                                      statusTip=u"Άνοιγμα αρχείου επιχείρησης",
                                      triggered=self.fileOpen)
        self.prnAct = QtGui.QAction(QtGui.QIcon(':/images/print.png'),
                                    u"Εκτύπωση",
                                    self,
                                    statusTip=u"Εκτύπωση",
                                    triggered=self.prn)
        self.setAct = QtGui.QAction(QtGui.QIcon(':/images/set.png'),
                                    u"Επιλογές",
                                    self,
                                    statusTip=u"Επιλογές",
                                    triggered=self.toDo)
        self.newDbAct = QtGui.QAction(QtGui.QIcon(':/images/new.png'),
                                      u"&Nέο αρχείο",
                                      self,
                                      shortcut=QtGui.QKeySequence.New,
                                      statusTip=u"Δημιουργία νέου αρχείου επιχείρησης",
                                      triggered=self.newDB)
        self.closeDatAct = QtGui.QAction(QtGui.QIcon(':/images/par.png'),
                                         u"Ημ/νία κλειδώματος",
                                         self,
                                         statusTip=u"Μόνο μετά από αυτή την ημερομηνία μπορούν να γίνουν εγγραφές",
                                         triggered=self.closeDat)
        self.coDataAct = QtGui.QAction(QtGui.QIcon(':/images/set.png'),
                                       u"Στοιχεία επιχείρησης",
                                       self,
                                       statusTip=u"Στοιχεία επιχείρησης",
                                       triggered=self.coData)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(u"&Αρχείο")
        self.fileMenu.addAction(self.newDbAct)
        self.fileMenu.addAction(self.openForm)
        self.fileMenu.addAction(self.closeAct)
        self.parMenu = self.menuBar().addMenu(u"Παράμετροι")
        self.parMenu.addAction(self.coDataAct)
        self.parMenu.addAction(self.closeDatAct)
        self.helpMenu = self.menuBar().addMenu(u"Βοήθεια")
        self.helpMenu.addAction(self.aboutAct)

    def createToolBars(self):
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

    def createStatusBar(self):
        self.statusBar().showMessage(u"Έτοιμοι")

    def addPlugins(self):
        self.menuArray = app_config.fillTreeMenu()
        if not self.menuArray:
            return
        parents = []
        self.pfiles = {}
        for el in self.menuArray:
            if not (el[1] in parents):
                parents.append(el[1])
            if len(el) == 4:
                self.pfiles[el[2]] = [el[0], el[3]]
            else:
                self.pfiles[el[2]] = [el[0], el[3], el[4], el[2]]
        for parent in parents:
            p = QtGui.QTreeWidgetItem(self.treeWidget)
            p.setText(0, parent)
            for el in self.menuArray:
                if parent == el[1]:
                    p1 = QtGui.QTreeWidgetItem(p)
                    p1.setText(0, el[2])

    def runPlugin(self):
        selection = u'%s' % self.treeWidget.currentItem().text(0)
        dlg = None
        if selection not in self.pfiles:
            return
        if self.pfiles[selection][1] == 'tbl':
            table = self.pfiles[selection][0]
            dlg = dbf.ftableData(table, self.db, self, True)

        elif self.pfiles[selection][1] == 'frm':
            exestr = 'dlg = %s' % self.pfiles[selection][0]
            exec(exestr)

        elif self.pfiles[selection][1] == 'rpt':
            sql = self.pfiles[selection][2]
            dlg = dbf.fsqlData(sql,
                               self.db,
                               inPanel=True,
                               wtitle=self.pfiles[selection][3])
        self.addDialogOnStack(dlg)
        '''
        if dlg:
            self.stackw.addWidget(dlg)
            self.stackw.setCurrentIndex(self.stackw.count()-1)
            self.exStatus()
        '''

    def addDialogOnStack(self, dlg=None):
        if dlg:
            self.stackw.addWidget(dlg)
            self.stackw.setCurrentIndex(self.stackw.count()-1)
            self.exStatus()

    def newDB(self):
        fname = '%s' % QtGui.QFileDialog.getSaveFileName(self,
                u"%s Δημιουργία Νέου αρχείου" % app_config.applicationTitle(),
                os.path.dirname(self.db),
                u"Αρχείο (*.%s)" % app_config.dbExtension())
        sql = dbf.readFromRes(':sql/create.sql')

        if fname:
            dbf.executeScript(sql, fname)
            self.resetStackw()
            self.db = fname
            self.settings.setValue("db_path", self.db)
            self.onStartOrFileOpen()
            print(self.db)

    def openForm1(self):
        # import f_dialogTemplate
        '''
        frm = f_dialogTemplate.dlg(parent=self)
        #frm.show() #opens not in modal mode
        if frm.exec_() == QtGui.QDialog.Accepted: #modal mode
            print 'ok'
        '''
        pass

    def fileFromCommandLine(self, fname):
        pass
        '''if fname:
            self.db = '%s' % fname
            self.settings.setValue("db_path",self.db)#QtCore.QVariant(self.db))
            self.onStartOrFileOpen()
        '''

    def fileOpen(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,
                                                  u'Επιλογή Αρχείου',
                                                  self.db,
                                                  u"Αρχείο (*.%s)" % app_config.dbExtension())
        if fname:
            self.resetStackw()
            self.db = '%s' % fname
            self.settings.setValue("db_path", self.db)
            self.onStartOrFileOpen()

    def prn(self):
        self.stackw.currentWidget()._print()

    def add(self):
        self.stackw.currentWidget().newRecord()

    def onStartOrFileOpen(self):
        if os.path.isfile(self.db):
            if isValidDB(self.db):
                self.setwinTitle()
                self.treeWidget = QtGui.QTreeWidget()
                self.treeWidget.headerItem().setText(0, u'Κεντρικό Μενού')
                self.treeWidget.setMaximumSize(QtCore.QSize(190, 16777215))
                self.stackw.addWidget(self.treeWidget)
                self.treeWidget.doubleClicked.connect(self.runPlugin)
                self.addPlugins()
                return True
            else:
                QtGui.QMessageBox.critical(self, u'%s - Πρόβλημα !!!' % app_config.applicationTitle(), u'Λανθασμένο αρχείο')
                # self.ui.treeMis.setModel(None)
                self.db = ''
                self.setWindowTitle(u"%s -> ( ??? )" % app_config.applicationTitle())
                self.resetStackw()
                return False
        else:
            # self.ui.treeMis.setModel(None)
            self.setWindowTitle(u"%s -> ( ??? )" % app_config.applicationTitle())
            return False

    def setwinTitle(self):
        self.setWindowTitle(u"%s -> %s ( %s )" %(app_config.applicationTitle(), coText(self.db), self.db))

    def about(self):
        frm = f_about.dlg(txt=app_config.applicationTitle(),about=app_config.htmlAbout , parent=self)
        frm.exec_()

    def toDo(self):
        QtGui.QMessageBox.about(self,
                                u"Υπό κατασκευή",
                                u"Η εφαρμογή <b>M13</b> είναι "
                                u"υπό κατασκευή<br>"
                                u"Η ενέργεια που επιλέξατε "
                                u"δεν έχει υλοποιηθεί ακόμη.")

    def notOpen(self):
        QtGui.QMessageBox.critical(self, u"ΕΕ14",
        u"Δεν υπάρχει ανοικτό αρχείο εσόδων - εξόδων")

    def closeEvent1(self, event):
        reply = QtGui.QMessageBox.question(self, u'Επιβεβαίωση εξόδου',
                    u"Θέλετε να κλείσετε την εφαρμογή ;",
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def closeEvent(self, event):
        msgBox = QtGui.QMessageBox()
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

    def coData(self):
        frm = dbf.autoDialog('co', self.db, 1, self)
        frm.exec_()
        self.setwinTitle()

    def closeDat(self):
        frm = dbf.autoDialog('lk', self.db, 1, self)
        frm.exec_()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName(app_config.organizationName())
    app.setOrganizationDomain(app_config.organizationDomain())
    app.setApplicationName(app_config.applicationName())
    myApp = fMain()
    myApp.show()
    sys.exit(app.exec_())