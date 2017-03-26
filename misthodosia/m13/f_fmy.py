# -*- coding: utf-8 -*-
'''
Created on 18 Νοε 2012

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore

from gui import ui_print_rpt_misthodosia
from utils.fmy_etoys import makeFMYFile

sqlmis = '''
SELECT m12_xrisi.id , m12_xrisi.xrisi, sum(m12_misd.val)>0 as t
FROM m12_xrisi
INNER JOIN m12_mis ON m12_mis.xrisi_id=m12_xrisi.id
INNER JOIN m12_misd ON m12_misd.mis_id=m12_mis.id
GROUP BY m12_xrisi.id
'''
class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        super(dlg, self).__init__(parent)

        self.ui = ui_print_rpt_misthodosia.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.d_date.setDate(QtCore.QDate.currentDate())
        self.makeConnections()

        if parent:
            self.db = parent.db
        else:
            self.db = ''
        self.appSettings = parent.settings
        self.populate()
        self.setWindowTitle(u'Δημιουργία αρχείου ΦΜΥ')
        self.ui.b_print.setText(u'Δημιουργία αρχείου')

    def populate(self):
        from utils.qtutils import populateTableWidget
        headers = [u'ΑΑ',u'Χρήση',u'none']
        populateTableWidget(self.ui.tblMis,sqlmis,headers,self.db,colWidths =[10,250,1])

    def makeConnections(self):
        QtCore.QObject.connect(self.ui.b_print, QtCore.SIGNAL("clicked()"),self.makeFile)

    def makeFile(self):
        from qtprint import qt_beb1_report
        misid =  self.ui.tblMis.item(self.ui.tblMis.currentRow(),1).text()
        if misid:
            defaultPdfName = 'JL10'
            direct = '%s' % self.appSettings.value("save_path", defaultValue='')
            fName = QtGui.QFileDialog.getExistingDirectory(self,u"Περιοχή αποθήκευσης",direct)
            self.appSettings.setValue("save_path",fName)
            fName = '%s/%s' % (fName,defaultPdfName)
            fName = fName.replace('\\','/')

            printDate = self.ui.d_date.date().toString('dd/MM/yyyy')
            co, vols  = makeFMYFile(fName,misid,self.db,u'%s' % printDate)
            win = qt_beb1_report.Window(co,vols,parent=self)
            win.printAsPdf('%s.pdf'%fName)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()
