# -*- coding: utf-8 -*-
'''
Created on Dec 13, 2011

@author: tedlaz
'''
from PyQt4 import QtGui
from ui_dlgiso import Ui_dlgiso

class fPrintIso(QtGui.QDialog):
    def __init__(self, args=None,parent=None,lmos='', per=''):
        super(fPrintIso, self).__init__(parent)
        self.parent = parent
        if self.parent:
            self.db = self.parent.db
            #print self.db
        else:
            self.db = None
        self.ui = Ui_dlgiso()
        self.ui.setupUi(self)
        self.ui.bprn.clicked.connect(self.printToPdf)
        self.pdfName = 'iso'
        
    def printToPdf(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,u"Ονομα αρχείου",self.pdfName,"PDF Files (*.pdf)")
        if fileName:
            self.pdfName = fileName
        if self.db: 
            import rep_is_apo_eos as isapoeos
            isapoeos.isozygioApoEos(self.ui.lapo.text(),self.ui.leos.text(),self.db,self.pdfName)
            #isapoeos.isozygioApoEos()
        self.accept()
if __name__ == '__main__':
    pass