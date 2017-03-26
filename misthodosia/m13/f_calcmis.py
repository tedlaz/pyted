# -*- coding: utf-8 -*-
'''
Created on 18 Νοε 2012

@author: tedlaz
'''
from PyQt4 import QtGui,Qt
from utils import dbutils, widgets
import datetime

class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        super(dlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        if parent:
            self.db = parent.db
        else:
            self.db = 'c:/ted/mis.sql3'

        xrisiLabel = QtGui.QLabel(u"Χρήση:")
        xrisi = widgets.DbComboBox(dbutils.getDbRows("SELECT id, xrisi FROM m12_xrisi", self.db))
        xrisiLabel.setBuddy(xrisi)

        perLabel = QtGui.QLabel(u"Περίοδος Μισθοδοσίας:")
        per = widgets.DbComboBox(dbutils.getDbRows("SELECT id, periodp FROM m12_period", self.db))
        perLabel.setBuddy(per)

        typLabel = QtGui.QLabel(u"Τύπος Μισθοδοσίας:")
        typ = widgets.DbComboBox(dbutils.getDbRows("SELECT id, mistp FROM m12_mist", self.db))
        typLabel.setBuddy(typ)

        bcalc =  QtGui.QPushButton(u'Υπολογισμός')

        def calcmis():
            from utils import calcMisthodosia as cm
            imnia = datetime.datetime.now().isoformat()[:10]
            #print self.cb_1dict[self.ui.cb_1.currentText().__str__()]
            xrid  = xrisi.getValue()
            perid = per.getValue()
            mistid= typ.getValue()
            cm.makeMis(xrid, perid, mistid, imnia, self.db)
            self.accept()

        bcalc.clicked.connect(calcmis)
        glayout = QtGui.QGridLayout()

        glayout.addWidget(xrisiLabel,0,0)
        glayout.addWidget(xrisi,0,1)

        glayout.addWidget(perLabel,1,0)
        glayout.addWidget(per,1,1)

        glayout.addWidget(typLabel,2,0)
        glayout.addWidget(typ,2,1)

        vlayout = QtGui.QVBoxLayout()
        vlayout.addLayout(glayout)
        vlayout.addWidget(bcalc)

        self.setLayout(vlayout)
        self.setWindowTitle(u'Υπολογισμός Μισθοδοσίας')

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()
