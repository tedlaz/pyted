#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 18 Νοε 2012

@author: tedlaz
'''
import sip
sip.setapi(u'QDate', 2)
sip.setapi(u'QDateTime', 2)
sip.setapi(u'QString', 2)
sip.setapi(u'QTextStream', 2)
sip.setapi(u'QTime', 2)
sip.setapi(u'QUrl', 2)
sip.setapi(u'QVariant', 2)

import sys

from PyQt4 import QtGui, QtCore,Qt
from utils.commonData import coText
import os
from gui import ui_main
from utils import qtree
from utils import f_generic_grid
from utils import  variusSQL,dbutils 

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

def isMisDB(db): # check if db is payroll db
    try:
        print dbutils.getDbOneRow('SELECT * FROM m12_co',db)
        return True
    except:
        return False
    
class fMain(QtGui.QMainWindow):
    def __init__(self, parent=None):
        self.settings = QtCore.QSettings()
        QtGui.QMainWindow.__init__(self, parent)
        
        self.pardb='mispar.sql3'
        self.ui = ui_main.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.makeConnections()

        self.db = '%s' % self.settings.value("db_path", defaultValue='')#QtCore.QVariant('')).toString()
        self.savepath = '%s' % self.settings.value("save_path", defaultValue='')
        
        self.onStartOrFileOpen()
            
    def setwinTitle(self):
        self.setWindowTitle("M13 - %s ( %s )" %(coText(self.db),self.db))    
        
    def treeConnect(self):
        if self.db:
            try:
                model = qtree.makeModel(self.db)
                self.ui.treeMis.setModel(model)
                self.ui.treeMis.setColumnWidth(0,250)
                contexMenu = QtGui.QMenu(self.ui.treeMis)
                self.ui.treeMis.setContextMenuPolicy(Qt.Qt.ActionsContextMenu)
                a_1 = QtGui.QAction('Add',contexMenu)
                a_2 = QtGui.QAction('Delete',contexMenu)
                def tst():
                    QtGui.QMessageBox.critical(self, u'Δοκιμή !!!', u'και πάλι')
                a_1.triggered.connect(tst)
                self.ui.treeMis.addAction(a_1)
                self.ui.treeMis.addAction(a_2)
            except Exception:
                pass
            
    def onStartOrFileOpen(self):
        if os.path.isfile(self.db):
            if isMisDB(self.db):
                self.setwinTitle()
                self.treeConnect()
                return True
            else:
                QtGui.QMessageBox.critical(self, u'Μ13 - Πρόβλημα !!!', u'Λανθασμένο αρχείο')
                self.ui.treeMis.setModel(None)
                self.setWindowTitle("M13 - ( ??? )")
                return False
        else:
            self.ui.treeMis.setModel(None)
            self.setWindowTitle("M13 - ( ??? )")
            return False
        
    def makeConnections(self):
        self.ui.a_open.triggered.connect(self.fileOpen)
        self.ui.a_print_report.triggered.connect(self.f_rpt_misthodosiaOpen)
        self.ui.a_print_report_apod.triggered.connect(self.f_rpt_misthodosia_apodeikseisOpen)
        self.ui.a_pros.triggered.connect(self.f_proOpen)
        self.ui.a_pros_wizard.triggered.connect(self.f_proWizardOpen)
        #self.ui.a_pros.triggered.connect(self.f_fprOpen)
        self.ui.a_tables.triggered.connect(self.f_fprTables)
        self.ui.a_calcmis.triggered.connect(self.f_calcmisOpen)
        self.ui.a_fpr.triggered.connect(self.f_fprOpen)
        QtCore.QObject.connect(self.ui.a_fmyFiscal,QtCore.SIGNAL("triggered()"),self.f_fmyOpen)
        QtCore.QObject.connect(self.ui.a_apd,QtCore.SIGNAL("triggered()"),self.f_apdOpen)
        self.ui.pushButton.clicked.connect(self.f_proOpen)
        self.ui.a_par.triggered.connect(self.f_parOpen)
        self.ui.a_pard.triggered.connect(self.f_pardOpen)
        self.ui.a_exit.triggered.connect(self.close)
        self.ui.a_peri.triggered.connect(self.aboutApp)
        self.ui.a_sql.triggered.connect(self.dumpToSql)
        self.ui.a_new.triggered.connect(self.newDB)
        self.ui.a_xrisi.triggered.connect(self.f_xrisiOpen)
        self.ui.a_eid.triggered.connect(self.f_eidOpen)
        self.ui.a_ypok.triggered.connect(self.f_ypokOpen)
        self.ui.a_apol.triggered.connect(self.f_apolOpen)
        self.ui.a_auto_par.triggered.connect(self.f_calcparOpen)
            
    def fileOpen(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, u'Επιλογή Εταιρείας',self.db,"DbFiles (*.m13)")#(*.m13)")
        if fname:
            self.db = '%s' % fname
            self.settings.setValue("db_path",self.db)#QtCore.QVariant(self.db))
            self.onStartOrFileOpen()
            
    def fileFromCommandLine(self,fname):
        if fname:
            self.db = '%s' % fname
            self.settings.setValue("db_path",self.db)#QtCore.QVariant(self.db))
            self.onStartOrFileOpen()
            
    def newDB(self):
        
        import f_newDataFileWizard
        #f_newWizard.NewDbWizard(parent=self).show()
        wiz = f_newDataFileWizard.NewDbWizard(parent=self)   
        if wiz.exec_() == QtGui.QDialog.Accepted:
            self.db = wiz.field('fname')
            self.settings.setValue("db_path",self.db)
            self.onStartOrFileOpen()
         
            msb = QtGui.QMessageBox(self)
            msb.setTextFormat(QtCore.Qt.RichText)
            msb.setWindowTitle(u"Επιτυχία")
            msb.setText(u"Το αρχείο Δημιουργήθηκε και είναι ενεργό !!!</b><br/><br/><b>Μπορείτε να προχωρήσετε στην εισαγωγή εργαζομένων κλπ")
            msb.exec_() 
            
    def dumpToSql(self):
        if self.db:
            nam = self.db.split('.')
            dnam = '%s_dump' % nam[0] 
            print dnam
            fname = QtGui.QFileDialog.getSaveFileNameAndFilter(self, u'Επιλογή ονόματος αρχείου',dnam,u"SQL αρχείο (*.sql)") 
            if fname:
                dbutils.dumpToFile(fname[0], self.db)

    def f_rpt_misthodosiaOpen(self):
        import f_rpt_misthodosia
        if not self.db:
            return
        f_rpt_misthodosia.dlg(parent=self).show()

    def f_rpt_misthodosia_apodeikseisOpen(self):
        import f_rpt_misthodosia_apodeikseis
        if not self.db:
            return
        f_rpt_misthodosia_apodeikseis.dlg(parent=self).show()        
        
    def f_fprTables(self):
        import f_tables
        if not self.db:
            return
        f_tables.dlg(parent=self).show()
        
    def f_calcmisOpen(self):
        import f_calcmis
        if not self.db:
            return
        calcmi = f_calcmis.dlg(parent=self)
        if calcmi.exec_() == QtGui.QDialog.Accepted:
            self.treeConnect()
            
    def f_calcparOpen(self):
        import f_calcpar
        if not self.db:
            return
        f_calcpar.dlg(parent=self).show()
                     
    def f_fmyOpen(self):
        import f_fmy
        if not self.db:
            return
        f_fmy.dlg(parent=self).show()

    def f_apdOpen(self):
        import f_apd
        if not self.db:
            return
        f_apd.dlg(parent=self).show()
        
    def openForm(self,atbl,atitle,asql,aheaders):
        if not self.db:
            return
        form = f_generic_grid.dlg(sys.argv,parent=self,tbl=atbl,titl=atitle,sql=asql,headers=aheaders,pardb=self.pardb)
        form.show()
        
    def f_fprOpen(self):
        title= u'Φυσικά πρόσωπα'
        self.openForm('m12_fpr',title,variusSQL.fprSQL,variusSQL.fprSQLh)
    
    def f_proWizardOpen(self):
        import f_newEmployeeWizard
        wiz = f_newEmployeeWizard.NewEmpWizard(parent=self)   
        if wiz.exec_() == QtGui.QDialog.Accepted:
            print 'ok'
                        
    def f_proOpen(self):
        title= u'Προσλήψεις Εργαζομένων'
        self.openForm('m12_pro',title,variusSQL.proSQL,variusSQL.proSQLh)
        
    def f_parOpen(self):
        title= u'Παρουσίες Εργαζομένων'
        self.openForm('m12_par',title,variusSQL.parSQL,variusSQL.parSQLh)
                
    def f_pardOpen(self):
        title= u'Παρουσίες Αναλυτικά'
        self.openForm('m12_pard',title,variusSQL.pardSQL,variusSQL.pardSQLh)
        
    def f_xrisiOpen(self):
        title= u'Χρήσεις'
        self.openForm('m12_xrisi',title,variusSQL.xrisiSQL,variusSQL.xrisiSQLh)
 
    def f_eidOpen(self):
        title= u'Ειδικότητες'
        self.openForm('m12_eid',title,variusSQL.eidSQL,variusSQL.eidSQLh)

    def f_ypokOpen(self):
        title= u'Υποκαταστήματα'
        self.openForm('m12_coy',title,variusSQL.ypokSQL,variusSQL.ypokSQLh)

    def f_apolOpen(self):
        title= u'Αποχώρηση'
        self.openForm('m12_apo',title,variusSQL.apoSQL,variusSQL.apoSQLh)        
                                 
    def aboutApp(self):
        about = QtGui.QMessageBox(self)
        about.setTextFormat(QtCore.Qt.RichText)
        about.setWindowTitle(u"Περί της εφαρμογής M13")
        about.setText(u"<b>Μ13 έκδοση : 0.1</b><br/><br/> Δημιουργήθηκε από τον Θεόδωρο Λάζαρο</a>.<br/><br/>Άδεια χρήσης  :  <a href=\"http://www.gnu.org/licenses/gpl.html\"> GPL 3</a><br/><br/>Για περισσότερες πληροφορίες :<br/><a href=\"http://users.otenet.gr/~o6gnvw/\">Ted Lazaros Pages</a>")
        about.exec_() 
          
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, u'Επιβεβαίωση εξόδου',u"Θέλετε σίγουρα να κλείσετε ;", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("orgName")
    app.setOrganizationDomain("orgDomain")
    app.setApplicationName("appName")
    myApp = fMain()
    myApp.show()
    sys.exit(app.exec_())
