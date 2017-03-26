# -*- coding: utf-8 -*-
'''
Created on 18 Νοε 2012

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore

from gui import ui_apd
from utils.apd import makeAPDfile

sqlTrimino= '''
SELECT DISTINCT m12_trimino.id, xrisi,trimp
FROM m12_mis
INNER JOIN m12_xrisi on m12_xrisi.id=m12_mis.xrisi_id
INNER JOIN m12_period on m12_period.id = m12_mis.period_id
INNER JOIN m12_trimino on m12_trimino.id=m12_period.trimino_id
'''
sqlMinas = '''
SELECT DISTINCT m12_apdp.id, xrisi,trimp
FROM m12_mis
INNER JOIN m12_xrisi on m12_xrisi.id=m12_mis.xrisi_id
INNER JOIN m12_period on m12_period.id = m12_mis.period_id
INNER JOIN m12_apdp on m12_apdp.id=m12_period.id
ORDER BY xrisi DESC, m12_apdp.id DESC
'''
class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        super(dlg, self).__init__(parent)
        self.ui = ui_apd.Ui_Dialog()
        self.ui.setupUi(self)
        self.makeConnections()
        if parent:
            self.db = parent.db
        else:
            self.db = ''
        self.populate()

    def populate(self):
        from utils.qtutils import populateTableWidget
        headers = [u'αα',u'Χρήση',u'Μήνας']
        populateTableWidget(self.ui.tblXrisiTrimino,sqlMinas,headers,self.db,colWidths =[10,50,200])

    def makeConnections(self):
        QtCore.QObject.connect(self.ui.b_makeFile, QtCore.SIGNAL("clicked()"),self.makeFile)

    def makeFile(self):
        defaultPdfName = 'CSL01'
        xrisi =  self.ui.tblXrisiTrimino.item(self.ui.tblXrisiTrimino.currentRow(),1).text()
        trim  =  int(self.ui.tblXrisiTrimino.item(self.ui.tblXrisiTrimino.currentRow(),0).text())
        fName = QtGui.QFileDialog.getSaveFileName(self,u"Ονομα αρχείου",defaultPdfName)
        #xrisi = self.ui.t_xrisi.text()
        #trim  = int(self.ui.t_trimino.text())
        makeAPDfile(fName,xrisi,trim,self.db)
        self.accept()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()
