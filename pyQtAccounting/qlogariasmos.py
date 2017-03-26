#!/usr/bin/env python
#coding=utf-8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

import sys
from PyQt4.QtCore import (QString, Qt, SIGNAL)
from PyQt4.QtGui import (QApplication, QDialog, QFont, QFontMetrics, QFileDialog,
        QHBoxLayout, QPainter, QPrinter, QLabel, QPushButton, QTableWidget, QPixmap,
        QTableWidgetItem, QLineEdit, QGridLayout, QVBoxLayout,QMessageBox,QIcon )

import accounting as ac
import dlgkartella as kartella

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class fKartella(QDialog):
    def __init__(self, args=None,parent=None, lmos='38.00.00.0000'):
        super(fKartella, self).__init__(parent)
        self.pateras = parent
        self.lmos = lmos
        if self.pateras:
            self.db = parent.db
        else:
            self.db = None
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        #QMessageBox.information(self, u"pyKrypto ", self.db)
        #self.populateTable()        
        
        #Header fields and layout
        lblAA    = QLabel('Λογαριασμός')
        self.aa  = QLineEdit()

        lblPer   = QLabel('Περιγραφή')
        self.per = QLineEdit()
        
        layHeader = QGridLayout()
        layHeader.addWidget(lblAA,0,0)
        layHeader.addWidget(self.aa,0,1)
        layHeader.addWidget(lblPer,3,0)
        layHeader.addWidget(self.per,3,1)
        
        #Footer Layout
        self.pdf  = QPushButton("Εκτύπωση")
        iconPdf = QIcon()
        iconPdf.addPixmap(QPixmap(_fromUtf8(":/print")), QIcon.Normal, QIcon.Off)
        self.pdf.setIcon(iconPdf)
        self.tXr  = QLineEdit()
        self.tPi  = QLineEdit()
        self.tYp  = QLineEdit()
        self.tXr.setAlignment(Qt.AlignRight)
        self.tPi.setAlignment(Qt.AlignRight)
        self.tYp.setAlignment(Qt.AlignRight)
        layFooter = QHBoxLayout()
        layFooter.addWidget(self.pdf)
        layFooter.addStretch()
        layFooter.addWidget(self.tXr)
        layFooter.addWidget(self.tPi)
        layFooter.addWidget(self.tYp)
        
        #Buttons for save or Just quit
        #bSave = QPushButton("Go for it")
        #bQuit = QPushButton("Abort")
        buttonLayout = QHBoxLayout()
        #buttonLayout.addWidget(bQuit)
        buttonLayout.addStretch()
        #buttonLayout.addWidget(bSave)
        
        #Final Layout
        layout = QVBoxLayout()
        layout.addLayout(layHeader)
        layout.addWidget(self.table)
        layout.addLayout(layFooter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        
        #Connections
        self.connect(self.aa,SIGNAL("returnPressed ()"),self.getKartella)
        self.connect(self.pdf, SIGNAL("clicked()"),self.pdfDlg)
        #self.connect(self.table,SIGNAL("cellDoubleClicked(int,int)"),self.dummy)
        #self.connect(bQuit, SIGNAL("clicked()"), self.accept)
        self.setWindowTitle(u"Λ/μός %s" % self.lmos)
        self.setMinimumSize(900, 600)
        self.aa.setText(lmos)
        self.getKartella()

    def pdfDlg(self):
        dlgPrintIso = kartella.fPrintKartella(parent=self,lmos=self.lmos)
        dlgPrintIso.show()    
    def getFileName(self):
        fd = QFileDialog(self)
        self.filename = fd.getOpenFileName()
        self.txtFileName.setText(self.filename)
        
    def getKartella(self):
        id, per = ac.returnId(self.aa.text(),self.db)
        self.per.setText(per)
        self.table.setRowCount(0)
        lines = ac.kinisi(id,self.db)    
        headers = [u'No',u'Ημερομηνία',u'Παραστατικό',u'Περιγραφή',u'Χρέωση',u'Πίστωση',u'Υπόλοιπο']
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        txr = 0
        tpi = 0
        typ = 0
        for line in lines:
            self.setLine(line)
            txr += line[3]
            tpi += line[4]
        typ = txr-tpi
        self.tXr.setText(QString("%L1").arg(float(txr),0,"f",2))
        self.tPi.setText(QString("%L1").arg(float(tpi),0,"f",2))
        self.tYp.setText(QString("%L1").arg(float(typ),0,"f",2))
        self.table.resizeColumnsToContents()
            
    def printViaQPainter(self,f):
        from os.path import isfile
        if isfile(f):
            lines = open(f)
        else:
            return
        a = f.split('.')
        #s = a[-1]
        fname = ''
        for i in range(len(a)-1) :
            fname += a[i]
        fname += '.pdf'
        self.printer = QPrinter()
        self.printer.setPageSize(QPrinter.A4)
        self.printer.setOutputFileName(fname)
        self.printer.setOutputFormat(QPrinter.PdfFormat)
        if self.cmbOrientation.currentText() == 'landscape':
            self.printer.setOrientation(QPrinter.Landscape)
        pageRect = self.printer.pageRect()
        LeftMargin = 15

        sansFont = QFont("Courier", 10)
        sansLineHeight = QFontMetrics(sansFont).height()
        painter = QPainter(self.printer)
        #page = 1
        y = 20
        for line in lines:
            painter.save()
            painter.setFont(sansFont)
            y += sansLineHeight
            x = LeftMargin
            try:
                painter.drawText(x,y,line[:-1].decode('utf-8'))
            except:
                painter.drawText(x,y,'CodePage error !!!')
            if y > (pageRect.height() - 54) :
                self.printer.newPage()
                y = 20
            painter.restore()
        lines.close()
        self.accept()
            
    def setLine(self,item):
        rc = self.table.rowCount()
        self.table.setRowCount(rc+1)
        self.table.setItem(rc,0,strItem('%s' % item[6]))
        self.table.setItem(rc,1,strItem(item[0]))
        self.table.setItem(rc,2,strItem(item[1]))
        self.table.setItem(rc,3,strItem(item[2]))
        self.table.setItem(rc,4,numItem(item[3]))
        self.table.setItem(rc,5,numItem(item[4]))
        self.table.setItem(rc,6,numItem(item[5]))
        
def numItem(no,decimals=2):
    item = QTableWidgetItem(QString("%L1").arg(float(no),0,"f",decimals))
    item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
    return item

def strItem(str):
    item = QTableWidgetItem(str)
    return item

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = fKartella(sys.argv)
    form.show()
    app.exec_()
