# -*- coding: utf-8 -*-
'''
Created on Dec 13, 2011

@author: tedlaz
'''
from PyQt4 import QtGui
from ui_dlgkartella import Ui_dlgkartella

class fPrintKartella(QtGui.QDialog):
    def __init__(self, args=None,parent=None,lmos='', per=''):
        super(fPrintKartella, self).__init__(parent)
        self.parent = parent
        self.lmos = lmos
        if self.parent:
            self.db = self.parent.db
            #print self.db
        else:
            self.db = None
        self.ui = Ui_dlgkartella()
        self.ui.setupUi(self)
        self.ui.bprn.clicked.connect(self.printToPdf)
        self.pdfName = 'kar'+self.lmos
        self.setWindowTitle(u'Εκτύπωση %s' % self.lmos)

    def printToPdf(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,u"Ονομα αρχείου",self.pdfName,"PDF Files (*.pdf)")
        if fileName:
            self.pdfName = fileName
        if self.db: 
            import rep_kartella as kartella
            kartella.kartellaLmoyApoEos(self.lmos,self.ui.apo.text(),self.ui.eos.text(),self.db,self.pdfName)
            #isapoeos.isozygioApoEos()
            from subprocess import call
            call(["C:/prg/SumatraPDFPortable/App/sumatrapdf/SumatraPDF.exe", '%s'% self.pdfName])
        self.accept()
if __name__ == '__main__':
    pass