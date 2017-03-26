# -*- coding: utf-8 -*-
'''
Created on 13 Ιαν 2013

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore, Qt
from utils.tedutils import isNum
from utils import dbutils as dbu

def tableWidgetDefaults(twidget):
    '''
    Set default minimum size and without vertical headers  tableWidget
    '''
    twidget.verticalHeader().setDefaultSectionSize(20) #Εδώ ορίζουμε το πλάτος της γραμμής του grid
    twidget.verticalHeader().setStretchLastSection(False)
    twidget.verticalHeader().setVisible(False)
    
def populateTableWidget(tableWidget,sql,headers,db,colTypes=[],colWidths =[]):
    '''
    Function that rus sql on database db and fills the tablewidget with returning values
    '''
    def strItem(strv):
        st = '%s' % strv
        item = QtGui.QTableWidgetItem(st)
        return item
    
    def numItem(no):
        if isNum(no):
            no = '%s' % no
            no = no.replace(',','.')
            item = QtGui.QTableWidgetItem(QtCore.QString("%L1").arg(float(no),0,"f",2))
        else:
            item = strItem(no)
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        return item
    
    def setType(val,typos=0):
        if   typos == 0: #text
            return strItem(val)
        elif typos == 1: #Number
            return numItem(val)
        else:
            return val 
                  
    def setLine(line,typ=0):
        rc = tableWidget.rowCount()
        tableWidget.setRowCount(rc+1)
        colNo = 0
        for col in line:
            if colTypes == []:
                tableWidget.setItem(rc,colNo,setType(col,typ))
            else:
                tableWidget.setItem(rc,colNo,setType(col,colTypes[colNo]))
            colNo += 1
            
    def setColWidth():
        for i in range(len(colWidths)):
            tableWidget.setColumnWidth(i,colWidths[i])
            
    tableWidgetDefaults(tableWidget)
    tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)            
    tableWidget.setRowCount(0)
    lines = dbu.getDbRows(sql,db)
    tableWidget.setColumnCount(len(headers))
    tableWidget.setHorizontalHeaderLabels(headers)
    tableWidget.setColumnHidden(0,True)
    for line in lines:
        setLine(line)
    if colWidths == []:
        tableWidget.resizeColumnsToContents()
    else:
        setColWidth()

class fFind(QtGui.QDialog):
    def __init__(self, sql, headers, colwidths, db ,parent=None):
        QtGui.QDialog.__init__(self)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.parent = parent
        self.sql = sql
        self.headers = headers
        self.colwidths = colwidths
        self.db = db
        self.table = QtGui.QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        
        self.table.setAlternatingRowColors(True)
        #self.table.setStyleSheet("alternate-background-color: yellow;background-color: rgba(180,180,180);")
        self.table.setStyleSheet("alternate-background-color: rgba(241,246,180);")  
              
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle(u"Αναζήτηση " )
        self.setMinimumSize(400, 500)
        
        self.populateTable()
        self.connect(self.table,QtCore.SIGNAL("cellDoubleClicked(int, int)"),self.sendVals)
        self.array = []
        
    def keyPressEvent(self,ev):
        '''
        Χρησιμοποίηση του enter και του return για γρήγορη επιλογή και κλείσιμο της φόρμας ...
        '''
        if (ev.key()==QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            self.sendVals(self.table.currentRow(), self.table.currentColumn())
        QtGui.QDialog.keyPressEvent(self,ev)
        
    def val(self):
        return self.array
        
    def sendVals(self,x,y):
        for colu in range(self.table.columnCount()):
            self.array.append(self.table.item(x,colu).text())
        self.accept()
        
    def populateTable(self):
        populateTableWidget(self.table,self.sql,self.headers,self.db,colWidths=self.colwidths)

def populateTableWidgetFromList(tableWidget,listVal,headers,colTypes=[],colWidths =[]):
    '''
    Function that rus sql on database db and fills the tablewidget with returning values
    '''
    def strItem(strv):
        st = '%s' % strv
        item = QtGui.QTableWidgetItem(st)
        return item
    
    def numItem(no):
        if isNum(no):
            no = '%s' % no
            no = no.replace(',','.')
            item = QtGui.QTableWidgetItem(QtCore.QString("%L1").arg(float(no),0,"f",2))
        else:
            item = strItem(no)
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        return item
    
    def setType(val,typos=0):
        if   typos == 0: #text
            return strItem(val)
        elif typos == 1: #Number
            return numItem(val)
        else:
            return val 
                  
    def setLine(line,typ=0):
        rc = tableWidget.rowCount()
        tableWidget.setRowCount(rc+1)
        colNo = 0
        for col in line:
            if colTypes == []:
                tableWidget.setItem(rc,colNo,setType(col,typ))
            else:
                tableWidget.setItem(rc,colNo,setType(col,colTypes[colNo]))
            colNo += 1
            
    def setColWidth():
        for i in range(len(colWidths)):
            tableWidget.setColumnWidth(i,colWidths[i])
            
    tableWidgetDefaults(tableWidget)
    tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)            
    tableWidget.setRowCount(0)
    lines = listVal
    tableWidget.setColumnCount(len(headers))
    tableWidget.setHorizontalHeaderLabels(headers)
    #tableWidget.setColumnHidden(0,True)
    for line in lines:
        setLine(line)
    if colWidths == []:
        tableWidget.resizeColumnsToContents()
    else:
        setColWidth()
        
class fFindFromList(QtGui.QDialog):
    def __init__(self, listVal, headers, colwidths,parent=None):
        QtGui.QDialog.__init__(self)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        self.parent = parent
        self.list = listVal
        self.headers = headers
        self.colwidths = colwidths
        self.table = QtGui.QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        #self.table.setStyleSheet("alternate-background-color: yellow;background-color: rgba(180,180,180);")
        self.table.setStyleSheet("alternate-background-color: rgba(241,246,180);")
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSortIndicatorShown(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)
        
        #self.table.setToolTip(self.table.item(self.table.currentRow(), 1))
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle(u"Αναζήτηση " )
        self.setMinimumSize(400, 500)
        
        self.populateTable()
        self.connect(self.table,QtCore.SIGNAL("cellDoubleClicked(int, int)"),self.sendVals)
        self.array = []
        
    def keyPressEvent(self,ev):
        '''
        Χρησιμοποίηση του enter και του return για γρήγορη επιλογή και κλείσιμο της φόρμας ...
        '''
        if (ev.key()==QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            self.sendVals(self.table.currentRow(), self.table.currentColumn())
        QtGui.QDialog.keyPressEvent(self,ev)
        
    def val(self):
        return self.array
        
    def sendVals(self,x,y):
        for colu in range(self.table.columnCount()):
            self.array.append(self.table.item(x,colu).text())
        self.accept()
        
    def populateTable(self):
        populateTableWidgetFromList(self.table,self.list,self.headers,colWidths=self.colwidths)        

def test1():
    db = 'C:/ted/mis.sql3'
    sql = "SELECT id, epon,onom FROM m12_fpr"
    head = [u'AA',u'Επώνυμο',u'Όνομα']
    cw   = [10,100,100]
    import sys
    app = QtGui.QApplication(sys.argv)
    form = fFind(sql,head,cw,db)
    form.show()
    app.exec_()
    print form.array
    
def test2():
    from osyk import osyk
    kadList = osyk.cad_list()
    head = [u'ΚΑΔ',u'Περιγραφή']
    cw   = [35,300]   
    import sys
    app = QtGui.QApplication(sys.argv)
    form = fFindFromList(kadList,head,cw)
    form.show()
    app.exec_()
    print form.array                      
if __name__ == '__main__':
    test2()

    
    