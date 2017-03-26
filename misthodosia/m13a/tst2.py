# -*- coding: utf-8 -*-
'''
Created on 7 Μαϊ 2013

@author: tedlaz
'''
from PyQt4 import QtGui,Qt


class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        super(dlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        self.makeConnections()
        
    def makeConnections(self):
        #QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"),self.show1)
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