# -*- coding: utf-8 -*-
'''
Created on 15 Φεβ 2013

@author: tedlaz
'''



from PyQt4 import QtCore, QtGui
import utils.dbutils as dbutils 
from utils.tedutils import caps  
#import classwizard_rc

import zipfile



class Test(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Test, self).__init__(parent)

        self.setWindowTitle(u"Δοκιμαστικό παράθυρο")
        
        self.mb = QtGui.QComboBox()
        self.mb.addItems(self.populate())
        self.mb.setMaximumSize(300, 20)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.mb)
        self.setLayout(layout)
        
        
    def populate(self):
        zf = zipfile.ZipFile('osyk/osyk.zip')
        vec = []
        for lin in  zf.read('dn_eid.txt').split("\n"):
            sp = lin.split('|')
            if len(sp) > 1:
                vec.append(caps(sp[1].decode('CP1253')))
        vec.sort()
        return vec
        
    def accept(self):
        print '%s %s %s' % (self.field('epon'),self.field('coType'),self.field('fname'))
        file = open('newDb.sql')
        script = u''
        for lines in file:
            script += '%s' % lines.decode('utf-8')
        dbutils.executeScript(script, self.field('fname'))
        sqlCo = "INSERT INTO  m12_co  VALUES (1,'%s','','',1,'','','','','','','','','','')" % self.field('epon')
        dbutils.commitToDb(sqlCo, self.field('fname'))
        #self.parent.
        sqlCoy = u"INSERT INTO m12_coy VALUES (1,1,'Κεντρικό','%s')" % self.field('kad')
        dbutils.commitToDb(sqlCoy, self.field('fname'))
        #self.parent.db = self.field('fname')
        #self.parent.onStartOrFileOpen()






if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = Test()
    #wizard.setGeometry(80,80,100,100)
    #wizard.setMaximumSize(300, 300)
    wizard.show()
    sys.exit(app.exec_())
