#!/usr/bin/env python
#coding=utf-8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

import sys
from PyQt4.QtCore import (QString, Qt, SIGNAL)
from PyQt4.QtGui import (QApplication, QDialog, QFont, QFontMetrics, QFileDialog,QSplitter,
        QHBoxLayout, QPainter, QPrinter, QLabel, QPushButton, QTableWidget,QPixmap,QAbstractItemView,
        QTableWidgetItem, QLineEdit, QGridLayout, QVBoxLayout, QMessageBox,QIcon )

import accounting as ac

import dlgiso as iso
import qt_utils as ut

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class fImerologio(QDialog):
    def __init__(self, args=None,parent=None):
        super(fImerologio, self).__init__(parent)
        self.parent = parent
        if self.parent:
            self.db = parent.db
        else:
            self.db =None
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)  
        self.table.setSortingEnabled(True)  # Εδώ ορίζεται το σορτάρισμα ...    
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.tabled = QTableWidget()
        self.tabled.setAlternatingRowColors(True)  
        self.tabled.setSortingEnabled(True)  # Εδώ ορίζεται το σορτάρισμα ...    
        self.tabled.verticalHeader().setVisible(False)
        self.tabled.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabled.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        #Header fields and layout
        lblAA    = QLabel(u'Ημερολόγιο κινήσεων')
        
        layHeader = QGridLayout()
        layHeader.addWidget(lblAA,0,0)
        
        
        #Buttons for save or Just quit
        bRefresh = QPushButton("Ανανέωση")
        iconRe = QIcon()
        iconRe.addPixmap(QPixmap(_fromUtf8(":/resync")), QIcon.Normal, QIcon.Off)
        bRefresh.setIcon(iconRe)
        bPdf     = QPushButton("Εκτύπωση")
        iconPdf = QIcon()
        iconPdf.addPixmap(QPixmap(_fromUtf8(":/print")), QIcon.Normal, QIcon.Off)
        bPdf.setIcon(iconPdf)
        #bQuit = QPushButton("Abort")
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(bPdf)
        buttonLayout.addStretch()
        buttonLayout.addWidget(bRefresh)
        
        #Final Layout
        layout = QVBoxLayout()
        layout.addLayout(layHeader)
        sp = QSplitter(Qt.Vertical)
        sp.addWidget(self.table)
        sp.addWidget(self.tabled)
        #layout.addWidget(self.table)
        #layout.addWidget(self.tabled)
        layout.addWidget(sp)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        
        #Connections
        self.connect(bRefresh, SIGNAL("clicked()"),self.getIsoz)
        self.connect(self.table,SIGNAL("currentCellChanged(int, int,int,int)"),self.sendVals)
        self.setWindowTitle(u"Ημερολόγιο κινήσεων")
        self.setMinimumSize(900, 600)
        self.getIsoz()
    def sendVals(self,x,y,a,b):
        val = self.table.item(x, 0).text()
        sqld='select logistiki_tran_d.id,code,per,per2,xr,pi from logistiki_tran_d inner join logistiki_lmo on logistiki_lmo.id=logistiki_tran_d.lmos_id where tran_id=%s order by logistiki_tran_d.id' % val
        headers = ['id',u'Κωδικός',u'Λογαριασμός',u'Περ2',u'Χρέωση',u'Πίστωση']
        siz   = [8,100,350,100,100,100]
        coltyp= [0,0,0,0,1,1] 
        ut.populateTableWidget(self.tabled, sqld, headers, self.db,coltyp,siz)
    def pdfDlg(self):
        dlgPrintIso = iso.fPrintIso(parent=self)
        dlgPrintIso.show()

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
        lines = tr.im()
        headers = [u'aa',u'Ημερομηνία',u'Παρ/κό',u'Περιγραφή',u'Ποσό']
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
     
        for line in lines:
            self.setLine(line)

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
        self.table.setItem(rc,0,strItem('%s' % item[0]))
        self.table.setItem(rc,1,strItem(item[1]))
        self.table.setItem(rc,2,strItem(item[2]))
        self.table.setItem(rc,3,strItem(item[3]))
        self.table.setItem(rc,4,numItem(item[4]))

def setItems(val,types):
    if types == '0':
        return numItem(val)
    elif types == '9':
        return strItem(val)
    else:
        return None
            
def numItem(no):
    item = QTableWidgetItem(QString("%L1").arg(float(no),0,"f",2))
    item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
    return item

def strItem(st):
    item = QTableWidgetItem(st)
    return item

if __name__ == "__main__":
    print(setItems(100,'0'))
    