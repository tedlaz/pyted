#!/usr/bin/env python
#coding=utf-8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

import sys
from PyQt4.QtCore import (QString, Qt, SIGNAL)
from PyQt4.QtGui import (QApplication, QDialog, QFont, QFontMetrics, QFileDialog,
        QHBoxLayout, QPainter, QPrinter, QLabel, QPushButton, QTableWidget,QPixmap,QAbstractItemView,
        QTableWidgetItem, QLineEdit, QGridLayout, QVBoxLayout, QMessageBox,QIcon )

import accounting as ac
import qlogariasmos as glmos
import dlgiso as iso

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class fIsozygio(QDialog):
    def __init__(self, args=None,parent=None):
        super(fIsozygio, self).__init__(parent)
        self.parent = parent
        if self.parent:
            self.db = parent.db
        else:
            self.db =None
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)        
        #Header fields and layout
        lblAA    = QLabel('Ισοζύγιο Λογαριασμών')
        
        layHeader = QGridLayout()
        layHeader.addWidget(lblAA,0,0)
        
        #Footer Layout
        self.tXr  = QLineEdit()
        self.tPi  = QLineEdit()
        self.tYp  = QLineEdit()
        self.tXr.setAlignment(Qt.AlignRight)
        self.tPi.setAlignment(Qt.AlignRight)
        self.tYp.setAlignment(Qt.AlignRight)
        layFooter = QHBoxLayout()
        layFooter.addStretch()
        layFooter.addWidget(self.tXr)
        layFooter.addWidget(self.tPi)
        layFooter.addWidget(self.tYp)
        
        #Buttons for save or Just quit
        bRefresh = QPushButton("Ανανέωση")
        iconRe = QIcon()
        iconRe.addPixmap(QPixmap(_fromUtf8(":/resync")), QIcon.Normal, QIcon.Off)
        bRefresh.setIcon(iconRe)
        bPdf     = QPushButton("Εκτύπωση")
        bPdf50   = QPushButton("Προμηθευτές")
        iconPdf = QIcon()
        iconPdf.addPixmap(QPixmap(_fromUtf8(":/print")), QIcon.Normal, QIcon.Off)
        bPdf.setIcon(iconPdf)
        #bQuit = QPushButton("Abort")
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(bPdf)
        buttonLayout.addWidget(bPdf50)
        buttonLayout.addStretch()
        buttonLayout.addWidget(bRefresh)
        
        #Final Layout
        layout = QVBoxLayout()
        layout.addLayout(layHeader)
        layout.addWidget(self.table)
        layout.addLayout(layFooter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        
        #Connections
        self.connect(bRefresh, SIGNAL("clicked()"),self.getIsoz)
        self.connect(bPdf, SIGNAL("clicked()"),self.pdfDlg)
        self.connect(bPdf50, SIGNAL("clicked()"),self.pdfDlg50)
        self.connect(self.table,SIGNAL("cellDoubleClicked(int,int)"),self.dummy)
        self.setWindowTitle("Ισοζύγιο ")
        self.setMinimumSize(900, 600)
        self.getIsoz()
    def pdfDlg(self):
        dlgPrintIso = iso.fPrintIso(parent=self)
        dlgPrintIso.show()
    def pdfDlg50(self):
        import rep_iso1 as ris
        fileName = QFileDialog.getSaveFileName(self,u"Ονομα αρχείου",'isTotal50.pdf',"PDF Files (*.pdf)")
        if fileName:
            ris.runReport(self.db, str(fileName))
    def dummy(self,x,y):
        glForm = glmos.fKartella(parent=self, lmos=self.table.item(x, 0).text())
        glForm.setAttribute(Qt.WA_DeleteOnClose)
        glForm.show()
        glForm.raise_()
        glForm.activateWindow()
    def getFileName(self):
        fd = QFileDialog(self)
        self.filename = fd.getOpenFileName()
        self.txtFileName.setText(self.filename)
        
    def getIsoz(self):
        #id, per = ac.returnId(self.aa.text())
        #self.per.setText(per)
        self.table.setRowCount(0)
        if self.parent:
            tr = ac.trans(self.parent.db)
        else:
            tr = None
        lines = tr.bs()
        headers = [u'Λογαριασμός',u'Περιγραφή',u'Χρέωση',u'Πίστωση',u'Υπόλοιπο']
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        txr = 0
        tpi = 0
        typ = 0        
        for line in lines:
            self.setLine(line)
            txr += line[2]
            tpi += line[3]
        typ = txr-tpi
        #self.tXr.setText(str(txr))
        self.tXr.setText(QString("%L1").arg(float(txr),0,"f",2))
        #self.tPi.setText(str(tpi))
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
        self.table.setItem(rc,0,strItem(item[0]))
        self.table.setItem(rc,1,strItem(item[1]))
        self.table.setItem(rc,2,numItem(item[2]))
        self.table.setItem(rc,3,numItem(item[3]))
        self.table.setItem(rc,4,numItem(item[4]))

def setItems(val,type):
    if type == '0':
        return numItem(val)
    elif type == '9':
        return strItem(val)
    else:
        return None
            
def numItem(no):
    item = QTableWidgetItem(QString("%L1").arg(float(no),0,"f",2))
    item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
    return item

def strItem(str):
    item = QTableWidgetItem(str)
    return item

if __name__ == "__main__":
    print(setItems(100,'0'))
    
