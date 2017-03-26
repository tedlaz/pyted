# -*- coding: utf-8 -*-
'''
Created on ${date}

@author: ${user}
'''
from PyQt4 import QtGui,QtCore,Qt
import sys, os

           
class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        super(dlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        self.setupGui()
        self.makeConnections()
        self.setWindowTitle("put Title Here")
        
    def setupGui(self):
        #gfile = '%s/%s' %(sys.path[0],'m13.gif')
        #self.movie = WigglyWidget()
        #self.setGeometry(100, 100, size.width(), size.height())
        self.txtlb = QtGui.QLabel(u'Δοκιμαστικό κείμενο \nγια τους κάλους και καλά κρασιά ρε\n φίλε και τα πάντα όλα')
        
        layout = QtGui.QVBoxLayout()
        #layout.addWidget(self.movie)
        layout.addWidget(self.txtlb)
        self.setLayout(layout)
        self.setMinimumSize(400, 300)
        
    def makeConnections(self):
        pass
        
    def show1(self):
        #dlg.dlg(parent=self).show
        pass
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()