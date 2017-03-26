# -*- coding: utf-8 -*-
'''
Created on 3 Mar 2013

@author: tedlaz
'''

from PyQt4 import QtGui, Qt
import qt_table_report as tr
class testprn1(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        f ={'orientation'  :1,
            'pdfName'      :'test.pdf',
            'fontFamily'   :'Helvetica',  
            'ReportHeader1':u'TEST TEPORT',
            'ReportHeader2':u'Period : January 2012',
            'ReportHeader3':u'',
            'headerLabels':[u'Name',u'Year',u'Value'],
            'columnSizes' :[10,10,10],
            'columnToSum' :[0,0,1],
            'columnTypes' :[0,3,2],
            'columnAlign' :[0,1,2],
            'footerLine'  :True,
            'footerText'  :u'This is a footer text for testing',
            'footerPageNumberText':u'Page',
            'data'        :[['ted','1963-02-10',10.21],] *80
            }
        
        self.rep = tr.qtTableReport(f)
        tstButton = QtGui.QPushButton('test')
        tstButton.clicked.connect(self.onClick)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(tstButton)
        self.setLayout(layout)
        self.onClick()
        
    def onClick(self):
        self.rep.printPreview()
        self.accept()

if __name__ == '__main__':
    
    import sys

    app = QtGui.QApplication(sys.argv)
    window = testprn1()
    window.show()
    sys.exit(app.exec_())