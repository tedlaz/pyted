# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import sqlite3
import sys

def isNum(val): # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters : 
            1.value : the value to check against.
        output: True or False
    """
    if not val:
        return False
    value = '%s' % val
    value = value.replace(',','.')
    try: float(value)
    except ValueError: return False
    else: return True
    
def imBd(im):
    '''
    επιστρέφει ολογράφως αριθμητικες τιμές ημερών βδομάδας
    '''
    m = int(im)
    if   m == 1 : return u'μία(1)'
    elif m == 2 : return u'δύο(2)'
    elif m == 3 : return u'τρείς(3)'
    elif m == 4 : return u'τέσσερις(4)'
    elif m == 5 : return u'πέντε(5)'
    elif m == 6 : return u'έξι(6)'
    elif m == 7 : return u'επτά(7)'
    else:
        return u' '
        
def n(txt):
    '''
    Retuns empty space in case o null value
    '''
    if txt == None:
        return ' '
    else:
        return txt
        
def getData(sql,DB):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(sql)
    v1 = cur.fetchall()
    cur.close()
    con.close()
    return v1
    
def trimNull(v):
    val = []
    for i in v:
        for el in i:
            if (el) is None:
                val.append('')
            else:
                val.append(el)
    return val
    
def trimDate(dat):
    d=m=y=0
    if '/' in dat:
        d,m,y = dat.split('/')
    #print d,m,y
    return QtCore.QDate(int(y),int(m),int(d))
    
def populateTableWidget(tableWidget,sql,headers,db='tst.sql3',colTypes=[],colWidths =[]):
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
            
    tableWidget.setRowCount(0)
    lines = getData(sql,db)
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
    def __init__(self, args=None,parent=None):
        super(fFind, self).__init__(parent)
        self.parent = parent
        self.table = QtGui.QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle(u"Αναζήτηση " )
        self.setMinimumSize(400, 500)
        if len(args) > 2:
            self.populateTable(args[0],args[1],args[2])
        else:
            self.populateTable(args[0],args[1])
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
        
    def populateTable(self,sql,headers,colWidths=[]):
        populateTableWidget(self.table,sql,headers,colWidths=colWidths)
            
def createQtApp(mainClass,args=None):
    app = QtGui.QApplication(sys.argv)
    myApp = mainClass(args)
    myApp.show()
    sys.exit(app.exec_())