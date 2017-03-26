# -*- coding: utf-8 -*-
'''
Created on 3 Mar 2013

@author: tedlaz
'''

from PyQt4 import QtGui, Qt
import qt_table_report as tr
import dbutils as dbu
import dbmodel as model 

class printGridForm(QtGui.QDialog):
    def __init__(self, sql, tbl, db, parent):
        QtGui.QDialog.__init__(self)
        super(printGridForm, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        lines, headers, status, mssg = dbu.dbRows(sql,db)

        columnTypes = []
        colSizes = []
        colToSum = []
        colAlign = []
        for el in headers:
            if el == 'id':
                colSizes.append(3)
                colAlign.append(2)
                columnTypes.append(0)
            elif el[0] in 'st':
                colSizes.append(8)
                colAlign.append(0)
                columnTypes.append(0)
            elif el[0] in 'de':
                colSizes.append(7)
                colAlign.append(1)
                columnTypes.append(3)
            elif el[0] in 'z':
                colSizes.append(20)
                colAlign.append(0)
                columnTypes.append(0)
            else:
                colSizes.append(10)
                colAlign.append(1)
                columnTypes.append(0)
            colToSum.append(0)
             
        label = model.getTableLabelPlural(tbl)           
        f ={'orientation'  :0,  # 0:portait   1:landcape
            'pdfName'      :u'%s.pdf' % label,
            'fontFamily'   :'Times',  
            'ReportHeader1':label,
            'ReportHeader2':u'',
            'ReportHeader3':u'',
            'headerLabels':model.getLabels(headers),
            'columnSizes' :colSizes,
            'columnToSum' :colToSum,
            'columnTypes' :columnTypes,
            'columnAlign' :colAlign,
            'footerLine'  :True,
            'footerText'  :u'This is a footer text for testing',
            'footerPageNumberText':u'Σελίδα',
            'data'        :lines
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
    window = printGridForm()
    window.show()
    sys.exit(app.exec_())