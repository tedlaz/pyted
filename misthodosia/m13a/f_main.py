#! /usr/bin/env python
# -*- coding: utf-8 -*-
#Θεόδωρος Λάζαρος
import sip
sip.setapi(u'QDate', 2)
sip.setapi(u'QDateTime', 2)
sip.setapi(u'QString', 2)
sip.setapi(u'QTextStream', 2)
sip.setapi(u'QTime', 2)
sip.setapi(u'QUrl', 2)
sip.setapi(u'QVariant', 2)

from PyQt4 import QtCore, QtGui, Qt

import res_rc
import sys
import os
import utils_db
import report_table
#import imports


def isMisDB(db): # check if db is payroll db
    
    if utils_db.getDbOneRow('SELECT * FROM m12_co',db):
        return True
    else:
        return False

def coText(db):
    '''
    Returns text with Company Name , etc ...
    '''
    sql = "SELECT cop || ' ' || ono FROM m12_co WHERE id=1"
    coname = utils_db.getDbSingleVal(sql, db)
    if coname:
        return "%s" % coname.strip()
    else:
        return "Λάθος Αρχείο"
        
def findPlugins(pluginExtension='.py'):
    pluginDir = os.path.join(sys.path[0],'plugins').replace('\\','/')
    sys.path.insert(1,pluginDir)
    print sys.path
    os.chdir(pluginDir)
    pluginFiles = []
    for file1 in os.listdir("."):
        if file1.endswith(pluginExtension):
            ffil = file1[:-3]
            impstr = 'import %s as pl1963' % ffil
            exec(impstr)
            #Εδώ να μπεί κριτήριο εάν θα είναι το plugin εμφανήσιμο στο menou ή όχι !!
            pluginFiles.append([pluginDir,ffil,pl1963.name,pl1963.namp,pl1963.pname,pl1963.pnamp])
    return pluginFiles

class fMain(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.settings = QtCore.QSettings()

        self.db = '%s' % self.settings.value("db_path", defaultValue='')
        self.createGui()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.makeConnections()
        
        self.exStatus()
        self.setWindowTitle(u"Μ13")
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
        #self.treeWidget.clicked.connect(self.runPlugin)
        #self.treeWidget.doubleClicked.connect(self.runPlugin)
        pass
    
    def exBack(self):
        if self.stackw.count() > 1:
            forRemoval =  self.stackw.currentWidget()
            self.stackw.removeWidget(forRemoval)
            forRemoval.setParent(None)
            #forRemoval.Delete() 
            self.exStatus()
            
    def exStatus(self):
        if self.stackw.count() > 1:
            self.execBack.setEnabled(True)
            self.addAct.setEnabled(self.stackw.currentWidget().canAdd())
            self.prnAct.setEnabled(self.stackw.currentWidget().canPrint())
        else:
            self.execBack.setEnabled(False)
            self.addAct.setEnabled(False)
            self.execCancel.setEnabled(False)
            self.execSave.setEnabled(False)
            self.prnAct.setEnabled(False)
            
    def resetStackw(self):
        no = self.stackw.count()
        for i in range(no):
            forRemoval =  self.stackw.currentWidget()
            self.stackw.removeWidget(forRemoval)
            forRemoval.setParent(None)
            sip.delete(forRemoval)
        self.exStatus()
        
    def createActions(self):
        
        self.addAct = QtGui.QAction(QtGui.QIcon(':/images/add.png'),u"Νέα εγγραφή", self,
                                     statusTip=u"Δημιουργία νέας εγγραφής",triggered=self.add)
        
        self.aboutAct = QtGui.QAction(QtGui.QIcon(':/images/info.png'),u"Περί της εφαρμογής", self,
                                     statusTip=u"Πληροφορίες για την εφαρμογή",triggered=self.about) 

        self.apolAct = QtGui.QAction(QtGui.QIcon(':/images/apol.png'),u"Απόλυση", self,
                                     statusTip=u"Απόλυση εργαζομένου",triggered=self.toDo)

        self.apoikAct = QtGui.QAction(QtGui.QIcon(':/images/oikap.png'),u"Οικιοθελής αποχώρηση", self,
                                     statusTip=u"Οικιοθελής αποχώρηση εργαζομένου",triggered=self.toDo)

        self.apsynAct = QtGui.QAction(QtGui.QIcon(':/images/synt.png'),u"Συνταξιοδότηση", self,
                                     statusTip=u"Αποχώρηση λόγω σύνταξης εργαζομένου",triggered=self.toDo)
                        
        self.coAct = QtGui.QAction(QtGui.QIcon(':/images/co.png'),u"Στοιχεία Επιχείρησης", self,
                                     statusTip=u"Στοιχεία Επιχείρησης",triggered=self.toDo)
        
        self.closeAct = QtGui.QAction(QtGui.QIcon(':/images/exit.png'),u"Έξοδος", self,
                                     statusTip=u"Έξοδος από την εφαρμογή",triggered=self.close)

        self.doyAct = QtGui.QAction(QtGui.QIcon(':/images/doy.png'),u"Υπουργείο Οικονομικών", self,
                                     statusTip=u"Υπουργείο Οικονομικών",triggered=self.toDo)
        
        self.ergAct = QtGui.QAction(QtGui.QIcon(':/images/employee.png'),u"Στοιχεία εργαζόμενων", self,
                                     statusTip=u"Στοιχεία εργαζομένων",triggered=self.toDo) 

        self.execBack = QtGui.QAction(QtGui.QIcon(':/images/back.png'),u"Επιστροφή", self,
                                     statusTip=u"Επιστροφή στην προηγούμενη οθόνη",triggered=self.exBack)

        self.execCancel = QtGui.QAction(QtGui.QIcon(':/images/editdelete.png'),u"Επιστροφή", self,
                                     statusTip=u"Έξοδος και επιστροφή στο αρχικό μενού",triggered=self.toDo)

        self.execSave = QtGui.QAction(QtGui.QIcon(':/images/filesave.png'),u"Αποθήκευση", self,
                                     statusTip=u"Αποθήκευση αλλαγών",triggered=self.toDo)
                        
        self.ikaAct = QtGui.QAction(QtGui.QIcon(':/images/ika.png'),u"ΙΚΑ", self,
                                     statusTip=u"Ιδρυμα Κοινωνικών Ασφαλίσεων",triggered=self.toDo)
 
        self.miscalcAct = QtGui.QAction(QtGui.QIcon(':/images/miscalc.png'),u"Μισθοδοσία", self,
                                     statusTip=u"Υπολογισμός Μισθοδοσίας",triggered=self.notOpen)
                
        self.newergAct = QtGui.QAction(QtGui.QIcon(':/images/newemployee.png'),u"Πρόσληψη εργαζομένου", self,
                                     statusTip=u"Εισαγωγή νέου εργαζόμενου",triggered=self.toDo)

        self.openForm = QtGui.QAction(QtGui.QIcon(':/images/fileopen.png'),u"Άνοιγμα", self,
                                     statusTip=u"Άνοιγμα αρχείου επιχείρησης",triggered=self.fileOpen)

        self.parAct = QtGui.QAction(QtGui.QIcon(':/images/par.png'),u"Παρουσίες", self,
                                     statusTip=u"Παρουσίες-Άδειες-Απουσίες Εργαζομένων",triggered=self.toDo)

        self.prnAct = QtGui.QAction(QtGui.QIcon(':/images/print.png'),u"Εκτύπωση", self,
                                     statusTip=u"Εκτύπωση",triggered=self.prn)
        
        self.setAct = QtGui.QAction(QtGui.QIcon(':/images/set.png'),u"Επιλογές", self,
                                     statusTip=u"Επιλογές",triggered=self.toDo)
                                                       
        self.newDbAct = QtGui.QAction(QtGui.QIcon(':/images/new.png'),u"&Nέο αρχείο", self, shortcut=QtGui.QKeySequence.New,
                                     statusTip=u"Δημιουργία νέου αρχείου επιχείρησης",triggered=self.newDB)
                
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(u"&Αρχείο")
        self.fileMenu.addAction(self.newDbAct)
        self.fileMenu.addAction(self.openForm)
        self.fileMenu.addAction(self.closeAct)
        
        self.parMenu = self.menuBar().addMenu(u"Παράμετροι")
        
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
        
        self.helpToolBar.addAction(self.setAct)
        self.helpToolBar.addAction(self.aboutAct)
        
        
    def createStatusBar(self):
        self.statusBar().showMessage(u"Έτοιμοι")
        
    def addPlugins(self):
        self.pluginArray = []
        self.pluginArray = findPlugins()
        if not self.pluginArray:
            return
        parents = []
        self.pfiles = {}
        for el in self.pluginArray:
            if not (el[5] in parents):
                parents.append(el[5])
            self.pfiles[el[3]] = el[1]
        for parent in parents:
            p = QtGui.QTreeWidgetItem(self.treeWidget)
            p.setText(0,parent)
            for el in self.pluginArray:
                if parent == el[5]:
                    p1 = QtGui.QTreeWidgetItem(p)
                    p1.setText(0,el[3])            
        
    def runPlugin(self):
        selection = self.treeWidget.currentItem().text(0)
        try:
            plugin = self.pfiles[selection]
            impstr = 'import %s as pl1963' % plugin
            exec(impstr)
            pl1963.run(self)
            self.stackw.setCurrentIndex(self.stackw.count()-1)
            print 'stackw.count = ',self.stackw.count()
            self.exStatus()
        except:
            pass
        
    def newDB(self):
        
        import f_newCoWizard
        wiz = f_newCoWizard.NewDbWizard(parent=self)   
        if wiz.exec_() == QtGui.QDialog.Accepted:
            self.resetStackw()
            self.db = wiz.field('fname')
            self.settings.setValue("db_path",self.db)
            self.onStartOrFileOpen()
                         
    def openForm1(self):
        import f_dialogTemplate
        frm = f_dialogTemplate.dlg(parent=self)
        #frm.show() #opens not in modal mode
        if frm.exec_() == QtGui.QDialog.Accepted: #modal mode
            print 'ok'             
             
    def fileFromCommandLine(self,fname):
        pass
        '''if fname:
            self.db = '%s' % fname
            self.settings.setValue("db_path",self.db)#QtCore.QVariant(self.db))
            self.onStartOrFileOpen()  
        ''' 
    def fileOpen(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, u'Επιλογή Εταιρείας',self.db,"DbFiles (*.m13)") 
        if fname:
            self.resetStackw()
            self.db = '%s' % fname
            self.settings.setValue("db_path",self.db)#QtCore.QVariant(self.db))
            self.onStartOrFileOpen()
            
    def prn(self):
        self.stackw.currentWidget()._print()
        
    def add(self):
        self.stackw.currentWidget()._add()
            
    def onStartOrFileOpen(self):
        if os.path.isfile(self.db):
            if isMisDB(self.db):
                self.setwinTitle()
                self.treeWidget = QtGui.QTreeWidget()
                self.treeWidget.headerItem().setText(0,u'Κεντρικό Μενού')
                self.treeWidget.setMaximumSize(QtCore.QSize(190, 16777215))
                self.stackw.addWidget(self.treeWidget)
                self.treeWidget.doubleClicked.connect(self.runPlugin)
                self.addPlugins()
                return True
            else:
                QtGui.QMessageBox.critical(self, u'Μ13 - Πρόβλημα !!!', u'Λανθασμένο αρχείο')
                #self.ui.treeMis.setModel(None)
                self.db = ''
                self.setWindowTitle("M13 - ( ??? )")
                self.resetStackw()
                return False
        else:
            #self.ui.treeMis.setModel(None)
            self.setWindowTitle("M13 - ( ??? )")
            return False
    def setwinTitle(self):
        self.setWindowTitle("M13 - %s ( %s )" %(coText(self.db),self.db)) 
                                    
    def about(self):
        import f_about
        frm = f_about.dlg(parent=self)
        frm.exec_()

    def toDo(self):
        QtGui.QMessageBox.about(self, u"Υπό κατασκευή",
        u"Η εφαρμογή <b>M13</b> είναι "
        u"υπό κατασκευή<br>"
        u"Η ενέργεια που επιλέξατε "
        u"δεν έχει υλοποιηθεί ακόμη.")
 
    def notOpen(self):
        QtGui.QMessageBox.critical(self, u"Μ13",
        u"Δεν υπάρχει ανοικτό αρχείο μισθοδοσίας")
               
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, u'Επιβεβαίωση εξόδου',
                    u"Θέλετε σίγουρα να κλείσετε ;", 
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
            
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("NT")
    app.setOrganizationDomain("NTDomain")
    app.setApplicationName("M13")
    myApp = fMain()
    myApp.show()
    sys.exit(app.exec_())