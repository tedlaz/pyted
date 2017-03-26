# -*- coding: utf-8 -*-
'''
Created on Jan 10, 2012

@author: tedlaz
'''
#import sip
#sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from ui_viewEggrafi import Ui_Dialog
import qt_utils as ut

class fViewEggrafi(QtGui.QDialog):
    def __init__(self, args=None,parent=None,no=0):
        super(fViewEggrafi, self).__init__(parent)
        self.parent = parent
        self.no = no
        if self.parent:
            self.db = parent.db
        else:
            self.db =None
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.populate()
    def populate(self):
        if not self.db:
            return
        sql = 'select id,imnia,par,per from logistiki_tran where id=%s' % self.no
        sqld='select logistiki_tran_d.id,code,per,per2,xr,pi from logistiki_tran_d inner join logistiki_lmo on logistiki_lmo.id=logistiki_tran_d.lmos_id where tran_id=%s' % self.no
        master = ut.getData(sql, self.db)
        headers = ['id',u'Κωδικός',u'Λογαριασμός',u'Περ2',u'Χρέωση',u'Πίστωση']
        siz   = [8,100,350,100,100,60]
        coltyp= [0,0,0,0,1,1] 
        ut.populateTableWidget(self.ui.tDetail, sqld, headers, self.db,coltyp,siz)
        self.ui.tNo.setText(str(master[0][0]))
        self.ui.tdate.setText(master[0][1])
        self.ui.tParastatiko.setText(master[0][2])
        self.ui.tPerigrafi.setText(master[0][3])
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myApp = fViewEggrafi()
    myApp.show()
    sys.exit(app.exec_())