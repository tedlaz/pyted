# -*- coding: utf-8 -*-
'''
Created on 18 Νοε 2012

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore

from gui import ui_fmy
from utils.fmy_etoys import makeFMYFile

class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        super(dlg, self).__init__(parent)
        
        self.ui = ui_fmy.Ui_Dialog()
        self.ui.setupUi(self)
        self.makeConnections()
        
        if parent:
            self.db = parent.db
        else:
            self.db = ''
        
    def makeConnections(self):
        QtCore.QObject.connect(self.ui.b_makeFile, QtCore.SIGNAL("clicked()"),self.makeFile)
    
    def makeFile(self):
        defaultPdfName = 'JL10'
        fName = QtGui.QFileDialog.getSaveFileName(self,u"Ονομα αρχείου",defaultPdfName)
        makeFMYFile(fName,self.ui.t_xrisi.text(),self.db)
        self.accept()
             
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()