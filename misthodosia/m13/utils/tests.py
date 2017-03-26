# -*- coding: utf-8 -*-
'''
Created on 5 Φεβ 2013

@author: tedlaz
'''
from PyQt4 import QtCore, QtGui
import sys, os
from utils import qtutils, dbutils

class dataTypes():
    def __init__(self,dtypName):
        self.typeNames = ['text','fkey','date','int','dec']
        if dtypName in self.typeNames:
            self.typeName = dtypName
        else:
            self.typeName = self.typeNames[0]
            
    def setVal(self,val):
        if self.typeName == self.typeNames[0]:
            pass
    
class ButtonLineEditDataProvider():
    def __init__(self,sql='SELECT id, epon FROM m12_fpr', titles='id aaaa', sizes=[30,300], db='/ted/mis.sql3'):
        self.sql    = sql
        self.titles = titles.split(' ')
        self.sizes  = sizes
        self.db     = db
        

        
class ButtonLineEdit(QtGui.QLineEdit):
    '''
    QlineEdit with button and sql based values
    '''
    
    def __init__(self, parent=None, dataProvider=None):
        super(ButtonLineEdit, self).__init__(parent)
        
        self.dataProvider = dataProvider
        
        self.idValue = 0

        self.setReadOnly(True)
        self.button = QtGui.QToolButton(self)
        
        iconFind = os.path.join(os.path.dirname(__file__), 'icon_find.jpg')
        self.button.setIcon(QtGui.QIcon(iconFind))
        
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        
        self.button.clicked.connect(self.clicked)#self.buttonClicked.emit)

        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth*2 + 2),max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth*2 + 2))

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width(),(self.rect().bottom() - buttonSize.height() + 1)/2)
        super(ButtonLineEdit, self).resizeEvent(event)
        
            
    def clicked(self):

        a = qtutils.fFind(self.dataProvider.sql, self.dataProvider.titles, self.dataProvider.sizes, self.dataProvider.db ,parent=self)
        
        if a.exec_() == QtGui.QDialog.Accepted:
            self.idValue = a.array[0]
            self.setText(a.array[1])
            
        QtGui.QLineEdit.focusInEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusIn))

class myTableWidgetDataProvider():
    
    def __init__(self,tableName,parameterDb):
        self._sqlTable  = "SELECT id, tname, tper FROM tbl WHERE tname='%s'" % tableName
        self._tname = dbutils.getDbOneRow(self._sqlTable,parameterDb)
        self._sqlFields = "SELECT fname, fper, ftyp, frequired, fsql, ftitles, sqlUpdate FROM tbl_d WHERE tbl_id='%s'" % self._tname[0]
        self._fields=['id',]
        self._headers=['id',]
        self._colTypes=['text',] 
        self._isRequired=[0,]
        self._fkeySql=['',]
        self._fkeyTitles=['',]  
        self._fsqlUpdate=['',]
              
        for row in dbutils.getDbRows(self._sqlFields, parameterDb):
            self._fields.append(row[0])
            self._headers.append(row[1])
            self._colTypes.append(row[2]) 
            self._isRequired.append(row[3])
            self._fkeySql.append(row[4])
            self._fkeyTitles.append(row[5])
            self._fsqlUpdate.append(row[6])  
        
class myTableWidget(QtGui.QTableWidget):
    
    def __init__(self,parent=None, vdataprovider=None):
        super(myTableWidget, self).__init__(parent)
        self.dataProvider = vdataprovider
        self.setColumnCount(len(self.dataProvider._headers))
        self.setHorizontalHeaderLabels(self.dataProvider._headers) 
        #self.setSortingEnabled(True)
        #self.addNewLine() 
        self.verticalHeader().setDefaultSectionSize(24)
        self.populateFormFields()
         
    def keyPressEvent(self,ev):
        
        if (ev.key()==QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            if self.currentColumn() < self.columnCount() - 1:
                self.setCurrentCell(self.currentRow(), self.currentColumn()+1)
            else:
                if (self.rowCount()-1 == self.currentRow()): #Εισαγωγή νέας γραμμής
                    self.addNewLine()
                    self.setCurrentCell(self.rowCount()-1, 0)
                else:
                    self.setCurrentCell(self.currentRow()+1, 0)

        
        QtGui.QTableWidget.keyPressEvent(self,ev)
        
        
    def addNewLine(self):
        self.setRowCount(self.rowCount() + 1)
        for i in range(self.columnCount()):
            if self.dataProvider._colTypes[i] == 'fkey':
                dpr = ButtonLineEditDataProvider(sql=self.dataProvider._fkeySql[i])
                a1 = ButtonLineEdit(dataProvider=dpr)
                #a1.setReadOnly(True)
                self.setCellWidget(self.rowCount()-1,i,a1)
            elif self.dataProvider._colTypes[i] == 'date':
                a1 = QtGui.QDateEdit()
                a1.setCalendarPopup(True)
                #a1.setDate(today)
                self.setCellWidget(self.rowCount()-1,i,a1)
            elif self.dataProvider._colTypes[i] == 'dec':
                a1 = QtGui.QDoubleSpinBox()
                a1.setAlignment(QtCore.Qt.AlignRight)
                self.setCellWidget(self.rowCount()-1,i,a1)
            elif self.dataProvider._colTypes[i] == 'int':
                a1 = QtGui.QSpinBox()
                self.setCellWidget(self.rowCount()-1,i,a1)
                
    def populateFormFields(self):
        rowVals = dbutils.getDbRows('SELECT * FROM m12_pard WHERE m12_pard.par_id=3', 'c:/ted/mis.sql3')
        if rowVals:
            for rowVal in rowVals:
                self.addNewLine()
                for i in range(self.columnCount()):
                
                    if self.dataProvider._colTypes[i] == 'date':
                        yr,mn,dt = rowVal[i].split('-')
                        qd = QtCore.QDate()
                        qd.setDate(int(yr),int(mn),int(dt))
                        #self.masterFields[i].setDate(qd)
                        self.cellWidget(self.rowCount()-1,i).setDate(qd)
                        
                    elif self.dataProvider._colTypes[i] == 'dec':
                        self.cellWidget(self.rowCount()-1,i).setValue(rowVal[i]) 
            
                    elif self.dataProvider._colTypes[i] == 'fkey':
                        self.cellWidget(self.rowCount()-1,i).idValue = str(rowVal[i])
                        
                        if self.dataProvider._fsqlUpdate[i]:
                            sqlForField = self.dataProvider._fsqlUpdate[i] % rowVal[i] 
                            sqlWhere = ''
                        else:
                            sqlForField = self.dataProvider._fkeySql[i]
                            
                            if 'WHERE' in sqlForField:
                                sqlWhere = " AND id=%s" % rowVal[i]
                            else:
                                sqlWhere = " WHERE id=%s" % rowVal[i]
                                
                        fkSql = sqlForField + sqlWhere
                        print 'Line 176 : fksql = %s' % fkSql
                        v = dbutils.getDbOneRow(fkSql, 'c:/ted/mis.sql3')
                        self.cellWidget(self.rowCount()-1,i).setText(v[1]) 
                        
                    elif self.dataProvider._colTypes[i] == 'int':
                        self.cellWidget(self.rowCount()-1,i).setValue(rowVal[i])
            
                    else:
                        self.setItem(self.rowCount()-1,i,QtGui.QTableWidgetItem('%s' % rowVal[i]))

    def resetLines(self):
        print 'Line 142 :\n%s ' % self.getData()
        #self.setRowCount(0)
        
    def getData(self):
        txtArr = ''
        for l in range(self.rowCount()):
            for c in range(self.columnCount()):
                if self.dataProvider._colTypes[c] == 'fkey':
                    txtArr += '%s %s ' %  (self.cellWidget(l, c).idValue,self.cellWidget(l, c).text())
                else:
                    if self.item(l, c):
                        txtArr += '%s ' % self.item(l, c).text()
            txtArr +='\n'
        return txtArr


class testDlg(QtGui.QDialog):
    def __init__(self,parent=None):
        super(testDlg, self).__init__(parent)
        dpr = myTableWidgetDataProvider('m12_pard','../mispar.sql3')
        self.myTable = myTableWidget(vdataprovider=dpr)
        
        gridLayout = QtGui.QGridLayout()
        
        l1 = QtGui.QLabel('test1 kai kala krasia')
        v1 = QtGui.QLineEdit()
        l2 = QtGui.QLabel('test2')
        v2 = QtGui.QLineEdit()
        gridLayout.addWidget(l1,0,0)
        gridLayout.addWidget(v1,0,1)
        gridLayout.setColumnStretch(2,2)
        gridLayout.addWidget(l2,1,0)
        gridLayout.addWidget(v2,1,1)
                
        buttonLayout = QtGui.QHBoxLayout()
        buttonTest   = QtGui.QPushButton('Test') 
        buttonTest.setAutoDefault(False)
        buttonAddLine= QtGui.QPushButton('AddLine')
        buttonAddLine.setAutoDefault(False)
        buttonLayout.addWidget(buttonTest)
        buttonLayout.addWidget(buttonAddLine)
        #Layouts
        layout = QtGui.QVBoxLayout()
        layout.addLayout(gridLayout)
        layout.addWidget(self.myTable)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        #connections
        buttonAddLine.clicked.connect(self.myTable.addNewLine)
        buttonTest.clicked.connect(self.myTable.resetLines)

isValSQL = '''
SELECT m12_par.id FROM m12_par
INNER JOIN m12_xrisi ON m12_xrisi.id=m12_par.xrisi_id
INNER JOIN m12_period ON m12_period.id=m12_par.period_id
WHERE m12_xrisi.xrisi='%s' AND m12_period.period='%s'
'''
insParSQL = "INSERT INTO m12_par (xrisi_id, period_id) VALUES (%s, %s)"
insPardSQL= "INSERT INTO m12_pard (par_id, pro_id, ptyp_id, pos) VALUES (%s, %s, %s, %s)"

def automaticInsert(xrisi='2012',period='01',db='c:/ted/mis.sql3'):
    from utils import variusSQL
    par = dbutils.getDbOneRow(isValSQL %(xrisi,period), db)
    if par:
        print u'Έχουν γίνει εγγραφές για την περίοδο %s %s' % (xrisi,period)
        return False
    xrisi_id = dbutils.getDbSingleVal("SELECT id FROM m12_xrisi WHERE xrisi='%s'" % xrisi, db)
    perio_id = dbutils.getDbSingleVal("SELECT id FROM m12_period WHERE period='%s'" % period, db)
    print xrisi_id, perio_id
    arr = dbutils.getDbRows(variusSQL.InsertParousiesSQL % (xrisi,period,xrisi,period), db)
    if not arr:
        print u'Δεν υπάρχουν εργαζόμενοι στην περίοδο %s %s' % (xrisi,period)
        return False
    for el in arr:
        for c in el:
            print c,
        print ''
    par_id = dbutils.commitToDb(insParSQL % (xrisi_id, perio_id), db)
    insArr = []
    for el in arr:
        insArr.append(dbutils.commitToDb(insPardSQL % (par_id,el[0],1,0),db))
    print insArr
a='''
CREATE TABLE "m12_apo" (
    "id" integer NOT NULL PRIMARY KEY,
    "apod" date NOT NULL,
    "pro_id" integer NOT NULL UNIQUE REFERENCES "m12_pro" ("id"),
    "apot" varchar(1) NOT NULL
)
'''    
def calcmis(data):
    
    if data['mtype'] == 'misthos':
        apodoxes = data['meres'] / data['symbasiMeres'] * data['misthos']
    elif data['mtype'] == 'imeromisthio':
        apodoxes = data['meres'] * data['imeromisthio']
    elif data['mtype'] == 'oromisthio':
        apodoxes = data['meres'] * data['oreaAnaMera'] * data['oromisthio']
    else:
        apodoxes = 0
        
    ika     = apodoxes * data['pika'] / 100
    ikaenos = apodoxes * data['pikaenos'] / 100
    ikaetis = ika - ikaenos
    
    forologiteo = apodoxes - ikaenos
    
    #fmy = fmy(forologiteo)
    #eea = eea(forologiteo)
    
    #kratiseisErgazomenoy = ikaenos + fmy + eea
    
if __name__ == '__main__':
    #app = QtGui.QApplication([])
    #adds = testDlg()
    #adds.show()
    #sys.exit(app.exec_())
    
    automaticInsert('2013','02')
    pass