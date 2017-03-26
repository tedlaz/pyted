# -*- coding: utf-8 -*-
'''
Created on 18 Φεβ 2011

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore, Qt
from utils import dbutils, qtutils
import os
import gui.res_rc

class ButtonLineEdit(QtGui.QLineEdit):
    '''
    QlineEdit with button and sql based values
    '''
    #buttonClicked = QtCore.pyqtSignal(bool)
    
    def __init__(self, parent=None, sql=None, titles=None, db=None):
        super(ButtonLineEdit, self).__init__(parent)
        
        
        
        self.idValue = 0
        self.sql    = sql
        self.titles = titles
        self.db = db
        
        self.button = QtGui.QToolButton(self)
        iconFind = QtGui.QIcon()
        iconFind.addPixmap(QtGui.QPixmap(":/pr/find"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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

        a = qtutils.fFind(self.sql, self.titles.split(' '), [10,300], self.db ,parent=self)
        
        if a.exec_() == QtGui.QDialog.Accepted:
            self.idValue = a.array[0]
            self.setText(a.array[1])
            
        QtGui.QLineEdit.focusInEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusIn))
        
class TableParameters():
    def __init__(self,tableName, db, parameterdb):
        self.db = db
        self._sqlTable  = "SELECT id, tname, tper FROM tbl WHERE tname='%s'" % tableName
        self._tname = dbutils.getDbOneRow(self._sqlTable,parameterdb)
        self._sqlFields = "SELECT fname, fper, ftyp, frequired, fsql, ftitles, sqlUpdate FROM tbl_d WHERE tbl_id='%s'" % self._tname[0]
        self._fieldNames = dbutils.getDbRows(self._sqlFields, parameterdb)
        
        self.numberOfFields = len(self._fieldNames)
        self.tableLabel = self._tname[2]
        self.tableName  = self._tname[1]
        
        self.sqlCreate()
        
    def sqlCreate(self):
        selSql   = 'SELECT '
        tailSel  ="FROM %s " % self.tableName
        tailSel += "WHERE id=%s"
        
        insSql = 'INSERT INTO %s (' % self.tableName
        tailSql = " VALUES ("
        
        updSql = "UPDATE %s SET " % self.tableName
        tailUpd = "WHERE id=%s" 
        
        for i in range(self.numberOfFields):
            if i == (self.numberOfFields - 1):
                selSql += '%s ' % self._fieldNames[i][0]
                insSql += "%s)" % self._fieldNames[i][0]
                tailSql += "'%s')"
                updSql += "%s=" % self._fieldNames[i][0]
                updSql += "'%s' "
            else:
                selSql += '%s, ' % self._fieldNames[i][0]
                insSql += "%s, " % self._fieldNames[i][0]
                tailSql += "'%s',"
                updSql += "%s=" % self._fieldNames[i][0]
                updSql += "'%s', "
                
        self.sqlInsert = insSql + tailSql
        self.sqlSelect = selSql + tailSel
        self.sqlUpdate = updSql + tailUpd      
 
    def formFieldsCreate(self,labels,flds,gridLayout):
        
        today = QtCore.QDate.currentDate()
        
        for i in range(self.numberOfFields):
            labels.append(QtGui.QLabel(self._fieldNames[i][1]))
            
            if self._fieldNames[i][2] == 'text':
                flds.append(QtGui.QLineEdit())
                
            elif self._fieldNames[i][2] == 'date':
                te = QtGui.QDateEdit()
                te.setCalendarPopup(True)
                te.setDate(today)
                flds.append(te)
                
            elif self._fieldNames[i][2] == 'dec':
                flds.append(QtGui.QDoubleSpinBox())
                
            elif self._fieldNames[i][2] == 'int':
                sb = QtGui.QSpinBox()
                sb.setMinimum(0)
                sb.setMaximum(2050)
                flds.append(sb)            
                
            elif self._fieldNames[i][2] == 'fkey':
                #self.idvals[self._fieldNames[i][0]] = 0
                le = ButtonLineEdit(sql=self._fieldNames[i][4],titles=self._fieldNames[i][5], db=self.db) #MyLineEdit() #QtGui.QLineEdit()
                #le.textEdited.connect(functools.partial(self.con,i))
                le.setReadOnly(True)
                flds.append(le)
                
            else:
                flds.append(QtGui.QLineEdit())
                
            labels[i].setBuddy(flds[i])
            gridLayout.addWidget(labels[i],i,0)
            gridLayout.addWidget(flds[i],i,1)
            
    def getFieldParameters(self):
        if self._fieldNames:
            return self._fieldNames
        else:
            return None
        
    def checkSql(self):
        return 'line 150 : SQL Strings\n %s\n %s\n %s\n' % (self.sqlSelect,self.sqlInsert,self.sqlUpdate)
      
    def __str__(self):
        st  = 'Line 153 : Parameters for table : %s\n' % self.tableName
        for row in self._fieldNames:
            for col in row:
                st += ' %s ' % col
            st += '\n'  
        return st 

StyleSheet1 = """
QComboBox { color: darkblue; font-weight: bold; }
QLineEdit { color: darkgreen; font-weight: bold; }
QDateEdit { color: darkblue; }
QLineEdit[yellowback="true"] {
    background-color: rgb(255, 255, 127);
    color: darkblue;
}
"""
StyleSheet2 = """
QLineEdit { background-color: rgb(255, 255, 192); }
QDateEdit { background-color: rgb(255, 255, 192); }
"""       
class fmasterDetail(QtGui.QDialog):

    def __init__(self, args=None, parent=None, tableName=None,id1=0,pardb=None):
        super(fmasterDetail, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        if parent:
            self.db = parent.db
        else:
            self.db = 'c:/ted/mis.sql3'  
                  
        gridLayout = QtGui.QGridLayout() # Layout for master
        
        self.setStyleSheet(StyleSheet2) 
        
        self.tablePars = TableParameters(tableName,self.db,pardb)

        self.masterLabels = [] #Array with master Labels
        self.masterFields = [] #Array with Master Fields
        
        self.tablePars.formFieldsCreate(self.masterLabels, self.masterFields, gridLayout)
        
        
        self.quitButton = QtGui.QPushButton(u'Ακύρωση')
        spacer = QtGui.QSpacerItem(100,60,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        
        self.saveButton = QtGui.QPushButton(u'Αποθήκευση')
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.quitButton)
        buttonLayout.addItem(spacer)
        buttonLayout.addWidget(self.saveButton)
        layout = QtGui.QVBoxLayout()
        layout.addLayout(gridLayout)
        
        #self.grid = QtGui.QTableWidget()
        #layout.addWidget(self.grid)
        
        layout.addLayout(buttonLayout)
        
        self.setLayout(layout)
        
        self.setWindowTitle(self.tablePars.tableLabel)
        
        self.id = int(id1)
        
        QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL("clicked()"),self.saveToDb)
        QtCore.QObject.connect(self.quitButton, QtCore.SIGNAL("clicked()"),self.exit)
        
        if self.id:
            self.populateFormFields()
        
    def populateFormFields(self):
        rowVal = dbutils.getDbOneRow(self.tablePars.sqlSelect % self.id, self.db)
        if rowVal:
            for i in range(self.tablePars.numberOfFields):
                
                if self.tablePars._fieldNames[i][2] == 'date':
                    yr,mn,dt = rowVal[i].split('-')
                    qd = QtCore.QDate()
                    qd.setDate(int(yr),int(mn),int(dt))
                    self.masterFields[i].setDate(qd)
                    
                elif self.tablePars._fieldNames[i][2] == 'dec':
                    self.masterFields[i].setValue(rowVal[i]) 
        
                elif self.tablePars._fieldNames[i][2] == 'fkey':
                    self.masterFields[i].idValue = str(rowVal[i])
                    
                    if self.tablePars._fieldNames[i][6]:
                        sqlForField = self.tablePars._fieldNames[i][6] % rowVal[i]
                        sqlWhere = ''
                    else:
                        sqlForField = self.tablePars._fieldNames[i][4]
                        
                        if 'WHERE' in sqlForField:
                            sqlWhere = " AND id=%s" % rowVal[i]
                        else:
                            sqlWhere = " WHERE id=%s" % rowVal[i]
                            
                    fkSql = sqlForField + sqlWhere
                    print 'Line 252 : fksql = %s' % fkSql
                    v = dbutils.getDbOneRow(fkSql, self.db)
                    self.masterFields[i].setText(v[1]) 
                    
                elif self.tablePars._fieldNames[i][2] == 'int':
                    self.masterFields[i].setValue(rowVal[i])
        
                else:
                    self.masterFields[i].setText('%s' % rowVal[i])
        
    def saveToDb(self):
        varr = []
        errors = 0
        errorLog = ''
        
        for i in range(self.tablePars.numberOfFields):
            
            if self.tablePars._fieldNames[i][2] == 'date':
                val = self.masterFields[i].date().toString('yyyy-MM-dd')
                
            elif self.tablePars._fieldNames[i][2] == 'fkey':
                val = self.masterFields[i].idValue
                if val == 0:
                    errors += 1
                    errorLog += u'Συμπληρώστε δεδομένα για %s\n' % self.masterLabels[i].text()
                
            elif self.tablePars._fieldNames[i][2] == 'dec':
                val = self.masterFields[i].value()
                if val <= 0:
                    errors += 1
                    errorLog += u'Συμπληρώστε δεδομένα για %s\n' % self.masterLabels[i].text()
                    
            elif self.tablePars._fieldNames[i][2] == 'int':
                val = self.masterFields[i].value()    
                            
            else:
                val = self.masterFields[i].text()
            
            if self.tablePars._fieldNames[i][3]:
                if len('%s' % val) == 0:
                    errors += 1
                    errorLog += u'Συμπληρώστε δεδομένα για %s\n' % self.masterLabels[i].text()

            varr.append(val)
            
        if self.id == 0:
            sqlToExecute = self.tablePars.sqlInsert % tuple(varr)
        else:
            varr.append(self.id)
            sqlToExecute = self.tablePars.sqlUpdate % tuple(varr)
        print 'Line 302 : sqlToExecute: %s' % sqlToExecute
        if errors:
            QtGui.QMessageBox.warning(self,u'Προσοχή υπάρχουν λάθη',errorLog)
        else:
            if self.db:
                insNo = dbutils.commitToDb(sqlToExecute, self.db)
                if insNo:
                    QtGui.QMessageBox.warning(self,u'Μια χαρά',u'Η εγγραφή αποθηκευτηκε με αριθμό : %s' % insNo)
                    self.id = insNo
                    #self.LineEditid.setText('%s' % self.id)
                    self.accept()
                else:
                    QtGui.QMessageBox.warning(self,u'Μια χαρά',u'Η εγγραφή με αριθμό : %s Ενημερώθηκε' % self.id)
                    self.accept()
            else:
                QtGui.QMessageBox.warning(self,u'Πρόβλημα',u'Δεν υπάρχει Βάση Δεδομένων')
                
    def exit(self):
        self.reject()
        ''' 
        Σχόλια

       '''      
        
def test():
    import sys
    app = QtGui.QApplication(sys.argv)
    form = fmasterDetail(sys.argv,tableName='m12_co',id1=1,pardb='../mispar.sql3')
    form.show()
    app.exec_()
    
if __name__ == '__main__':
    tblnms = TableParameters('m12_par','c:/ted/mis.sql3',parameterdb='../mispar.sql3')
    print tblnms
    print tblnms.checkSql()
    test()