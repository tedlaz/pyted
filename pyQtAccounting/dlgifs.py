# -*- coding: utf-8 -*-
'''
Created on Dec 13, 2011

@author: tedlaz
'''
from PyQt4 import QtGui
from ui_dlgifs import Ui_dlgifs

class fPrintIfs(QtGui.QDialog):
    def __init__(self, args=None,parent=None,lmos='', per=''):
        super(fPrintIfs, self).__init__(parent)
        self.parent = parent
        if self.parent:
            self.db = self.parent.db
        else:
            self.db = None
        self.ui = Ui_dlgifs()
        self.ui.setupUi(self)
        self.ui.bprn.clicked.connect(self.printToPdf)
        self.pdfDir = ''
    def printToPdf(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                "QFileDialog.getExistingDirectory()",
                self.pdfDir, options)
        if directory:
            self.pdfDir = directory
        if self.db: 
            import rep_ifs as rif
            rif.makePdf(self.ui.lapo.text(),self.ui.leos.text(),self.db,self.pdfDir,self.ui.tameio.text())
        self.accept()
if __name__ == '__main__':
    pass