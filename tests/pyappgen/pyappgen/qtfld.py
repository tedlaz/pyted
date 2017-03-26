# -*- coding: utf-8 -*-
'''
Created on 9 Ιαν 2014
@author: tedlaz
'''
from PyQt4 import QtGui, QtCore, Qt

import dbutils as dbu
import num_txt_etc as nte

import model

import res_rc

tblStyle = "alternate-background-color: rgba(208,246,230);"

def gLbl(fieldName,lbl): # Μάλλον να μεταφερθεί στο model
    if not lbl: return fieldName
    if fieldName in lbl:
        return lbl[fieldName]
    else:
        return fieldName
    
def getLabel(fieldName): # Μάλλον να μεταφερθεί στο model
    if fieldName in model.fields.fieldNamesArray:
        return model.fields.labelSmall[fieldName]
    elif fieldName == 'id':
        return u'ΑΑ'
    else:
        return fieldName
       
def gLblArray(fieldNames,lbl): # Μάλλον να μεταφερθεί στο model
    tmp = []
    for fieldName in fieldNames:
        tmp.append(getLabel(fieldName))
    return tmp

def gLblf(fieldName,flblf): # Μάλλον να μεταφερθεί στο model
    if not flblf: return fieldName
    if fieldName in flblf:
        return flblf[fieldName]
    else:
        return fieldName 
    
def readFromRes(resname):
    f = QtCore.QFile(resname)
    vstr = None
    if f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
        stream = QtCore.QTextStream(f)
        stream.setCodec('utf-8')
        vstr = u''
        while not stream.atEnd():
            vstr += u'%s\n' % stream.readLine().__str__()   
    f.close()
    return vstr

class sortWidgetItem(QtGui.QTableWidgetItem):
    def __init__(self, text, sortKey):
        #call custom constructor with UserType item type
        QtGui.QTableWidgetItem.__init__(self, text, QtGui.QTableWidgetItem.UserType)
        self.sortKey = sortKey
    def __lt__(self, other):
        return self.sortKey < other.sortKey
    
class dataTableWidget(QtGui.QTableWidget):
    def __init__(self, sql, tbl=None,db=None, parent=None, lbls=None):
        super(dataTableWidget, self).__init__(parent)
        
        self.parent = parent
        self.sql    = sql
        self.tbl    = tbl
        self.db     = db
        self.headers= None
        self.lbls   = lbls 
        self.verticalHeader().setDefaultSectionSize(20)     #Εδώ ορίζουμε το πλάτος της γραμμής του grid
        self.verticalHeader().setStretchLastSection(False)
        self.verticalHeader().setVisible(False)
        
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)            
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        
        self.setAlternatingRowColors(True)
        self.setStyleSheet(tblStyle)  
        
        self.setToolTip(u'Με δεξί πλήκτρο ποντικιού μενού για \n Διόρθωση εγγραφής \n Νέα εγγραφή')
        self.setSortingEnabled(True) 
        self.populate()

    def _intItem(self,num):
        item = QtGui.QTableWidgetItem()
        item.setData(QtCore.Qt.DisplayRole,QtCore.QVariant(num))
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        return item
    
    def _numItem(self,num):
        item = sortWidgetItem(nte.strGrDec(num),num)
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        return item
                    
    def _strItem(self,strv):
        st = '%s' % strv
        if st=='None' : st = ''
        item = QtGui.QTableWidgetItem(st)
        return item
    
    def _dateItem(self,strv):
        strv = '%s' % strv
        if len(strv) < 10:
            item = sortWidgetItem(strv,strv)
        else: 
            y,m,d = strv.split('-')
            item = sortWidgetItem('%s/%s/%s' % (d,m,y),strv)
        return item
    
    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)

        Action = menu.addAction(u"Διόρθωση Εγγραφής")
        Action.triggered.connect(self.openForEdit)
        Act2   = menu.addAction(u"Νέα εγγραφή")
        Act2.triggered.connect(self.newRecord)
        menu.exec_(event.globalPos())
        
    def openForEdit(self):
        frm = autoDialog(id=self.item(self.currentRow(),0).text(),tbl=self.tbl,db=self.db,parent=self)
        if frm.exec_() == QtGui.QDialog.Accepted:
            self.populate()
            
    def newRecord(self):
        frmnr = autoDialog(id=None,tbl=self.tbl,db=self.db,parent=self)
        if frmnr.exec_() == QtGui.QDialog.Accepted:
            self.populate()
                                         
    def populate(self):
        self.setRowCount(0)
        self.setSortingEnabled(False)
        lines, self.headers = dbu.getDbRows(self.sql,self.db)
        columnTypes = []
        for el in self.headers:
            columnTypes.append(el[0])
        self.setColumnCount(len(self.headers))
        self.setHorizontalHeaderLabels(gLblArray(self.headers,None))
        for line in lines:
            rc = self.rowCount()
            self.setRowCount(rc+1)
            colNo = 0
            for col in line:
                if columnTypes[colNo] =='i': #Numeric values
                    self.setItem(rc,colNo,self._intItem(col))
                elif columnTypes[colNo] =='n':
                    self.setItem(rc,colNo,self._numItem(col))
                elif columnTypes[colNo] in 'de': #Date values
                    self.setItem(rc,colNo,self._dateItem(col))
                else: #Other values as text
                    self.setItem(rc,colNo,self._strItem(col))
                colNo += 1
        self.resizeColumnsToContents() 
        self.setSortingEnabled(True)
        #self.sortByColumn(0,0)
                           
class fFind(QtGui.QDialog):
    '''
    Form returning search values
    sql: search sql
    db : Current DB
    insTbl : 0 for no insert button, 1 for insert button
    parent:
    '''
    def __init__(self, sql,db,tabl,canInsertNewRecord=1,parent=None):
        super(fFind, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        if db:
            self.lines, self.headers = dbu.getDbRows(sql,db)
        
        self.sql = sql
        self.db = db
        self.tbl= tabl
        self.canInsertNewRecord = canInsertNewRecord
        self.parent = parent
        self.colwidths = []     
        
        self.table = dataTableWidget(self.sql,self.tbl,self.db,self)

        layout = QtGui.QVBoxLayout()
                
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        self.setWindowTitle(model.tables.labelPlural[self.tbl])
        self.setMinimumSize(500, 100)
        
        self.connect(self.table,QtCore.SIGNAL("cellDoubleClicked(int, int)"),self.sendVals)
        self.array = []
   
    def newRecord(self):
        self.table.newRecord()
              
    def keyPressEvent(self,ev):
        '''
        use enter or return for fast selection nad form close ...
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

class fldb(QtGui.QCheckBox):
    """
    True or False field
    """

    def __init__(self, lbl,chkVal=False, isRequired=False,parent=None):
        super(fldb, self).__init__(parent)
        
        self.lbl = lbl
        self.parent = parent
        
        self.isReq = isRequired
        self.setV(chkVal)
            
    def setV(self,txtVal):
        if txtVal:
            self.setChecked(txtVal)
        else:
            self.setChecked(False)
            
    def getV(self):

        return self.checkState()
    
class flds(QtGui.QLineEdit):
    """
    String Field
    """
    def __init__(self, lbl,txtVal=None, isRequired=False,parent=None):
        super(flds, self).__init__(parent)
        
        self.lbl = lbl
        self.parent = parent
        
        self.isReq = isRequired
        self.setV(txtVal)
            
    def setV(self,txtVal):
        if txtVal:
            ttxtVal = '%s' % txtVal
            self.setText(ttxtVal.strip())
        else:
            self.setText('')
        self.setCursorPosition(0)
            
    def getV(self):
        tmpval = '%s' % self.text()
        return tmpval.strip()
    
class fldt(QtGui.QTextEdit):
    """
    Text field
    """
    def __init__(self, lbl,txtVal=None, isRequired=False,parent=None):
        super(fldt, self).__init__(parent)
        
        self.lbl = lbl
        self.parent = parent
        
        self.isReq = isRequired
        self.setMaximumHeight(100)
        self.setV(txtVal)
            
    def setV(self,txtVal):
        if txtVal:
            ttxtVal = '%s' % txtVal
            self.setText(ttxtVal.strip())
        else:
            self.setText('')
            
    def getV(self):
        tmpval = '%s' % self.toPlainText().replace("'","''")
        return tmpval.strip() 

class fldj(flds):
    '''
    Text field with numeric chars only.
    '''
    def __init__(self, lbl,txtVal=None, isRequired=False,parent=None):
        super(fldj, self).__init__(lbl,txtVal, isRequired,parent)
        rval = QtCore.QRegExp('(\d*)([1-9])(\d*)')
        self.setValidator(QtGui.QRegExpValidator(rval))        
       
class fldd(QtGui.QDateEdit):
    '''
    Date values
    '''
    def __init__(self, lbl,sqliteDate=None, parent=None):
        super(fldd, self).__init__(parent)
        
        self.lbl = lbl
        self.parent = parent
        
        self.setCalendarPopup(True)
        self.setV(sqliteDate)
            
    def setV(self,sqliteDate):   
        if sqliteDate:
            if len(sqliteDate) > 10:
                sqliteDate = sqliteDate[:10]
            yr,mn,dt = sqliteDate.split('-')
            qd = QtCore.QDate()
            qd.setDate(int(yr),int(mn),int(dt))
            self.setDate(qd)
        else:
            self.setDate(QtCore.QDate.currentDate())
            
    def getV(self):
        return self.date().toString('yyyy-MM-dd')
  
class flde(QtGui.QToolButton):
    '''
    Date or empty string values
    '''
    def __init__(self, lbl,sqliteDate=None, parent=None):
        super(flde, self).__init__(parent) 
        
        self.lbl    = lbl
        self.parent = parent
        
        self.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.setMenu(QtGui.QMenu(self))
        self.cal = QtGui.QCalendarWidget()
        self.action = QtGui.QWidgetAction(self)
        self.action.setDefaultWidget(self.cal)
        self.menu().addAction(self.action)
        self.cal.clicked.connect(self.menuCalendar)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        self.setToolTip(u'Με δεξί κλικ ποντικιού μηδενίζει την ημερομηνία')
        
    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.RightButton:
            self.setText('')
        else:
            QtGui.QToolButton.mousePressEvent(self, event)
            
    def menuCalendar(self):
        self.setText(self.cal.selectedDate().toString('dd/MM/yyyy'))
        self.menu().hide()
                
    def setV(self, sqliteDate):
        if len(sqliteDate) == 0: return
        y,m,d = sqliteDate.split('-')
        self.setText('%s/%s/%s' %(d,m,y))
        
    def getV(self):
        if len(self.text()) == 0: return ''
        d,m,y = self.text().split('/')
        return '%s-%s-%s' % (y,m,d)
      
BLANK, GREEN = range(2)

class fldw(QtGui.QWidget):
    '''
    Weekdays selection ( [1,1,1,1,1,0,0] 7 values 0 or 1, one per weekday)
    '''
    def __init__(self,lbl,vals=[1,1,1,1,1,0,0],parent=None,dayNames=u'ΔΕ ΤΡ ΤΕ ΠΕ ΠΑ ΣΑ ΚΥ'):
        super(fldw, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding))
       
        self.lbl = lbl
        self.parent = parent
        
        self.setV(vals) # Δημιουργεί το self.grid
        self.selected = [0, 0]
        self.dayNames = dayNames.split()
        self.setMinimumSize(QtCore.QSize(170, 20))
        self.setMaximumSize(QtCore.QSize(170, 20))
        self.setToolTip(u'Επιλέξτε τις Εργάσιμες ημέρες\nΜε δεξί κλικ μηδενίστε')
        
    def sizeHint(self):
        return QtCore.QSize(170, 20)

        
    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.LeftButton:
            xOffset = self.width() / 7
            yOffset = xOffset #self.height()
            if event.x() < xOffset:       x = 0
            elif event.x() < 2 * xOffset: x = 1
            elif event.x() < 3 * xOffset: x = 2
            elif event.x() < 4 * xOffset: x = 3 
            elif event.x() < 5 * xOffset: x = 4
            elif event.x() < 6 * xOffset: x = 5
            else: x = 6
            
            if event.y() < xOffset:       y = 0
    
            #print event.x(), event.y()
            cell = self.grid[x]
            if cell == BLANK:
                cell = GREEN
            else:
                cell = BLANK
            self.grid[x] = cell
            self.selected = [x, 0]
            self.update()
            
        elif event.button() == Qt.Qt.RightButton:
            self.reset()
            
    def paintEvent(self, event=None):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        xOffset = self.width() / 7
        yOffset = self.height() # / 7 
        for x in range(7):
            cell = self.grid[x]
            rect = QtCore.QRectF(x * xOffset, 0 , xOffset, yOffset).adjusted(0.5, 0.5, -0.5, -0.5)
            color = None
            painter.drawRect(rect.adjusted(2, 2, -2, -2))
            if cell == GREEN:
                color = Qt.Qt.green
            if color is not None:
                painter.save()
                painter.setPen(Qt.Qt.black)
                painter.setBrush(color)
                #painter.drawEllipse(rect.adjusted(2, 2, -2, -2))
                painter.drawRect(rect.adjusted(2, 2, -2, -2))
                color = Qt.Qt.black
                painter.restore()
                
            painter.setPen(Qt.Qt.black)
            painter.drawText(rect.adjusted(6, 3, -3, -3),self.dayNames[x])
            painter.drawRect(rect)
        #print self.getValues()
        
    def getV(self,strVal=True): # strval : Εάν η επιστρεφόμενη τιμή είναι string ή array
        if strVal:
            st = '['
            for i in range(7):
                if i == 6:
                    st += '%s]' % self.grid[i]
                else:
                    st += '%s,' % self.grid[i]
            return st
        else:
            return self.grid
        
    def setV(self,darr=[0,0,0,0,0,0,0]):
        'Set values to days vector. But first checks for proper array length and type'
        darr = '%s' % darr
        tmparr = eval(darr)  
        if len(tmparr) == 7:
            self.grid = tmparr
        else:
            self.grid = [0,0,0,0,0,0,0]
        self.update() 
              
    def reset(self):
        'Set everything to Null'
        self.setV([0,0,0,0,0,0,0])
        
    def set5days(self):
        'Set Standard five days week'
        self.setV([1,1,1,1,1,0,0])

class fldi(QtGui.QSpinBox):
    '''
    Integer values (eg 123)
    '''
    def __init__(self, lbl,intVal=0, parent=None):
        super(fldi, self).__init__(parent)
        
        self.lbl = lbl
        self.parent = parent
        
        self.setMinimum(0)
        self.setMaximum(999999999)
        self.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

        self.setV(intVal)    

    def getV(self):
        return '%s' % self.value()
    
    def setV(self,val):
        if val:
            self.setValue(int(val))
        else:
            self.setValue(0)
    
class fldn(QtGui.QDoubleSpinBox):
    '''
    Numeric (decimal 2 ) values (eg 999,99)
    '''
    def __init__(self, lbl,intVal=0, parent=None):
        super(fldn, self).__init__(parent)
        
        self.lbl = lbl
        self.parent = parent
        
        self.setMinimum(-99999999999)
        self.setMaximum(99999999999)
        self.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        
        self.setV(intVal)
            
    def getV(self):
        val = '%s' % self.value()
        if val[-2:] =='.0':
            val = val[:-2]
        return  val
    
    def setV(self,val):
        if val:
            self.setValue(val)
        else:
            self.setValue(0)

class fldc(QtGui.QComboBox):
    '''
    ComboBox with two values . One not visible for storing one human readable
    '''
    #fld%s(u'%s',sql,parent=self))" % (typ,el)
    def __init__(self, lbl, sql, parent=None, tbl=None):#cdata = [[1,'val1'],[2,'val2']], parent=None):
        super(fldc, self).__init__(parent)
        
        self.lbl = lbl
        self.sql = sql
        self.tbl = tbl
        self.parent = parent
        
        self.id=[]
        
        self.setData()#(cdata)
        
    def setData(self):
        vals = dbu.getDbRows(model.reprFlds(self.tbl), self.parent.db ,False)
        #model.reprFlds(self.tbl)
        for el in vals:
            tmp = u''
            for i in range(len(el)):
                if i == 0:
                    self.id.append(el[i])
                else:
                    tmp += u'%s ' % el[i]
            self.addItem(tmp)
                
    def setDataOld(self, cdata=[[]]):
        for el in cdata:
            self.id.append(el[0])
            self.addItem(el[1])
                
    def setV(self, val):
        for i in range(len(self.id)):
            if self.id[i] == val:
                self.setCurrentIndex(i)
    
    def getV(self):   
        return self.id[self.currentIndex()]
    
class fldz(QtGui.QLineEdit):
    '''
    QlineEdit with button and sql based values
    Παράμετροι
    sql     = Το sql που μας δίνει τα δεδομένα του παράθυρου επιλογής
    titles  = Επικεφαλίδες για το table του παράθυρου επιλογής (string με διαχωριστικό το |)
    db      = Η διαδρομή του αρχείου μισθοδοσίας
    sizes   = Τα πλάτη των στηλών του παράθυρου επιλογής
    idVal   = Το πρωτεύον κλειδί που άμα πάρει αρχική τιμή μας εμφανίζει συγκεκριμένη εγγραφή 
    '''
    
    def __init__(self, lbl,sql=None,idVal=None, sql1=None, parent=None,tbl=None):
        super(fldz, self).__init__(parent)
        
        self.lbl = lbl
        self.parent = parent
        
        self.tbl    = lbl
        self.sql    = sql
        self.sql1   = sql1 # SQL ειδικά για το setValue ...
        self.tbl    = tbl
        self.titles = []
        
        self.setV(idVal)
        
        self.setReadOnly(True)
        self.button = QtGui.QToolButton(self)
        
        iconFind = QtGui.QIcon()
        iconFind.addPixmap(QtGui.QPixmap(":images/icon_find.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button.setIcon(QtGui.QIcon(iconFind))
        
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.setFocusPolicy(Qt.Qt.NoFocus)
        self.button.clicked.connect(self.clicked)

        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth*2 + 2),max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth*2 + 2))
                
    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width(),(self.rect().bottom() - buttonSize.height() + 1)/2)
        super(fldz, self).resizeEvent(event)
    '''    
    def keyPressEvent(self,ev):
        if (ev.key()==QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            self.clicked()
    '''
                
    def clicked(self):
        a = fFind(self.sql, self.parent.db, self.tbl, parent=self.parent)
        
        if a.exec_() == QtGui.QDialog.Accepted:
            self.idValue = a.array[0]
            self.setV(self.idValue)
            
            #ttxt = ''
            #for i in range(1,len(a.array)):
            #    ttxt += '%s ' % a.array[i]
            #self.setText(ttxt)
            #self.setCursorPosition(0)
        #print self.str()    
        QtGui.QLineEdit.focusInEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusIn))
        
    def getV(self):
        return self.idValue
        
    def setV(self,idVal):
        
        if idVal is None:
            self.idValue = None 
            return
        
        idName = self.sql.split()[1][:-1] #Με την προυπόθεση ότι πάντα το πρώτο πεδίο είναι το [table_name].id
        if ',' in idName:
            idName = idName.split(',')[0]
        if idName=='':
            idName = 'id'
        if self.sql1:
            sql = self.sql1 % idVal # Μάλλον ακυρώνεται ... 
        else:            
            if 'WHERE' in self.sql:
                sqlWhere = " AND %s='%s'" % (idName,idVal)
            else:
                #sqlWhere = " WHERE %s=%s" % (idName,idVal)
                sqlWhere = " WHERE %s='%s'" % (idName,idVal)
           
            #sql = self.sql + sqlWhere
            sql = model.reprFlds(self.tbl,idVal)

        v = dbu.getDbOneRow(sql, self.parent.db)
        
        if v:
            txtv = ''
            for i in range(1,len(v)):
                txtv += '%s ' % v[i]
            self.setText(txtv)
            self.idValue = idVal
        else:
            self.setText('')
            self.idValue = None
        self.setCursorPosition(0)
        
    def str_(self):
        
        return '%s %s' % (self.idValue,self.text())

class autoDialog(QtGui.QDialog):
    def __init__(self, id=None, tbl=None,db=None,parent=None,cols=1):
        super(autoDialog, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        self.setWindowTitle(model.getTableLabel(tbl))
        
        self.cols = cols
        self.id  = id #save id for later use (updating record)
        self.tbl = tbl
        self.db  = db
        self.oldVals = None  
        if id:
            oldVals, self.colnames = dbu.getDbRows('select * from %s where id=%s' % (tbl,id),db)
            self.isNew = False
            if oldVals:
                self.oldVals = oldVals[0][1:] #Leave out id
            else:
                id = None
        else:
            oldVals, self.colnames = dbu.getDbRows('select * from %s where id=-1' % tbl,db)
            self.isNew = True
            
        self.fldArray = []
        
        layout = QtGui.QVBoxLayout()       
        glayout = QtGui.QGridLayout()

        self._makeFlds()
        self._glayoutFill(glayout)

        self.button = QtGui.QPushButton(u'Αποθήκευση Νέας Εγγραφής')
        self.button.clicked.connect(self.getV)
        layout.addLayout(glayout)
        layout.addWidget(self.button)
        self.setLayout(layout)
        if id:
            self.setV()
            self.button.setText(u'Αποθήκευση Διόρθωμένης Εγγραφής')
            
    def _makeFlds(self):     
        for el in self.colnames:
            if el == 'id': continue
            typ = el[0]
            if typ in 'cz':
                if dbu.isTableOrView('_%s' % el[1:], self.db) :
                    sql = "select * from _%s" % el[1:]
                else:
                    sql = model.tblFlds(el[1:])#"select * from %s" % el[1:]
                str = u"self.fldArray.append(fld%s(u'%s',sql,parent=self,tbl='%s'))" % (typ,el,el[1:])           
            else:
                str = u"self.fldArray.append(fld%s(u'%s',parent=self))" % (typ,el)
            exec(str)
            
    def _glayoutFill(self,glayout):
        j = 0
        for i in range(len(self.fldArray)):
            glayout.addWidget(QtGui.QLabel(getLabel(self.fldArray[i].lbl)),i /self.cols ,j)
            j += 1
            glayout.addWidget(self.fldArray[i],i/self.cols,j)
            j += 1
            if j > (self.cols*2)-1:
                j = 0
                                
    def getV(self):
        #for el in self.fldArray:
        #    print el.getV()
        self._save()
        self.accept()    
    def setV(self):
        for i in range(len(self.oldVals)):
            self.fldArray[i].setV(self.oldVals[i])

    def _save(self):
        sqlins = "INSERT INTO %s(%s) VALUES (%s)"
        sqlupd = "UPDATE %s SET %s WHERE id=%s"
        cnames = vals = upd = ''
        newVals = []
        for i in range(len(self.colnames)):
            if i == 0: continue
            cnames += '%s,' % self.colnames[i]
            vals   += "'%s'," % self.fldArray[i-1].getV()
            upd    += "%s='%s'," % (self.colnames[i],self.fldArray[i-1].getV())
            newVals.append(self.fldArray[i-1].getV())
        cnames = cnames[:-1]
        vals = vals[:-1]
        upd = upd[:-1]
        sqlin = sqlins % (self.tbl,cnames,vals)
        sqlup = sqlupd % (self.tbl,upd,self.id)
        logMessage = u''
        if self.id:
            sha1old = nte.sha1OfArray(self.oldVals)
            sha1New = nte.sha1OfArray(newVals)
            if sha1old <> sha1New:
                dbu.commitToDb(sqlup, self.db)
                logMessage = u'Updated DB:%s, tbl:%s, id:%s , sql:%s' % (self.db,self.tbl,self.id, sqlup)
            else:
                logMessage = u'No change in record'
        else:
            logMessage = u'New DB:%s, tbl:%s, id:%s, sql:%s' % (self.db,self.tbl,dbu.commitToDb(sqlin, self.db),sqlin)
        print logMessage.encode('utf-8')
def test():
    import sys

    app = QtGui.QApplication([])
    dlg = autoDialog(id=1, tbl='erp',db='tst.sql3')
    dlg.show()
    sys.exit(app.exec_())
    
def test2():
    vals, colnames = dbu.getDbRows('select * from tst_','tst.sql3')
    print vals,colnames 
if __name__ == '__main__':
    test()