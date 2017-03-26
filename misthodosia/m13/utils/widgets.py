# -*- coding: utf-8 -*-
'''
Created on 18 Φεβ 2013

@author: tedlaz
'''

from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtCore import pyqtProperty
from utils import qtutils, dbutils
from collections import OrderedDict
import gui.res_rc 
from utils import factory_sql as fsql
'''
Όλα τα παρακ΄άτω wigets έχουν ένα ενιαίο interface επικοινωνίας
με τις μεθόδους:
setValue : To widget δέχεται τιμή σε sqlite Format
getValue : Μας επιστρέφει τιμή σε sqlite Format
str      : Μας επιστρέφει τιμή σε text format
'''
        
class DbLineEdit(QtGui.QLineEdit):
    def __init__(self, txtVal=None, isRequired=False,parent=None):
        super(DbLineEdit, self).__init__(parent)
        self.isReq = isRequired
        self.setValue(txtVal)
            
    def setValue(self,txtVal):
        if txtVal:
            self.setText(txtVal.strip())
        else:
            self.setText('')
            
    def getValue(self):
        tmpval = '%s' % self.text()
        return tmpval.strip() 
    
    def str_(self):
        return self.getValue()
    
    @pyqtProperty(str)
    def timi(self):
        return self.getValue()
    
    @timi.setter
    def timi(self,timi):
        self.setValue(timi)    
           
class DbDoubleSpinBox(QtGui.QDoubleSpinBox):
    def __init__(self, intVal=0, mini=0, maxi=999999999, parent=None):
        super(DbDoubleSpinBox, self).__init__(parent)
        self.setMinimum(mini)
        self.setMaximum(maxi)
        if intVal:
            self.setValue(intVal)
        else:
            self.setValue(0)
    def getValue(self):
        return self.value()
    
    def str_(self):
        return '%s' % self.value()
     
    @pyqtProperty(float)
    def timi(self):
        return self.getValue()
    @timi.setter
    def timi(self,timi):
        self.setValue(timi)
        
class DbSpinBox(QtGui.QSpinBox):
    def __init__(self, intVal=0 ,mini=0, maxi=999999999, parent=None):
        super(DbSpinBox, self).__init__(parent)
        self.setMinimum(mini)
        self.setMaximum(maxi)
        if intVal:
            self.setValue(intVal)
        else:
            self.setValue(0)
    def getValue(self):
        return self.value()
    
    def str_(self):
        return '%s' % self.value() 

    @pyqtProperty(int)
    def timi(self):
        return self.getValue()
                 
class DbDateEdit(QtGui.QDateEdit):
    def __init__(self, sqliteDate=None, parent=None):
        super(DbDateEdit, self).__init__(parent)
        
        self.setCalendarPopup(True)
        self.setValue(sqliteDate)
            
    def setValue(self,sqliteDate):   
        if sqliteDate:
            yr,mn,dt = sqliteDate.split('-')
            qd = QtCore.QDate()
            qd.setDate(int(yr),int(mn),int(dt))
            self.setDate(qd)
        else:
            self.setDate(QtCore.QDate.currentDate())
            
    def getValue(self):
        return self.date().toString('yyyy-MM-dd')
    
    def str_(self):
        return self.getValue()

    @pyqtProperty(str)
    def timi(self):
        return self.getValue()
        
class DbComboBox(QtGui.QComboBox):
    def __init__(self,cdata = [[]], parent=None):
        super(DbComboBox, self).__init__(parent)
        self.id=[]
        self.setData(cdata)
        
    def setData(self,cdata=[[]]):
        for el in cdata:
            self.id.append(el[0])
            self.addItem(el[1])
                
    def setValue(self,val):
        for i in range(len(self.id)):
            if self.id[i] == val:
                self.setCurrentIndex(i)
    
    def getValue(self):   
        return self.id[self.currentIndex()]
    
    def str_(self):
        return '%s' % self.getValue()
    
    @pyqtProperty(int)
    def timi(self):
        return self.getValue()  
         
class ButtonLineEdit(QtGui.QLineEdit):
    '''
    QlineEdit with button and sql based values
    Παράμετροι
    sql     = Το sql που μας δίνει τα δεδομένα του παράθυρου επιλογής
    titles  = Επικεφαλίδες για το table του παράθυρου επιλογής (string με διαχωριστικό το |)
    db      = Η διαδρομή του αρχείου μισθοδοσίας
    sizes   = Τα πλάτη των στηλών του παράθυρου επιλογής
    idVal   = Το πρωτεύον κλειδί που άμα πάρει αρχική τιμή μας εμφανίζει συγκεκριμένη εγγραφή 
    '''
    
    def __init__(self, sql=None, titles=None,db=None,idVal=None, sql1=None,sizes=[30,300], parent=None):
        super(ButtonLineEdit, self).__init__(parent)
        
        self.sql    = sql
        self.sql1   = sql1 # SQL ειδικά για το setValue ...
        self.titles = titles.split('|')
        self.db     = db
        self.sizes  = sizes
        
        self.setValue(idVal)

        self.setReadOnly(True)
        self.button = QtGui.QToolButton(self)
        
        iconFind = QtGui.QIcon()
        iconFind.addPixmap(QtGui.QPixmap(":/pr/find"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button.setIcon(QtGui.QIcon(iconFind))
        
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        
        self.button.clicked.connect(self.clicked)

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

        a = qtutils.fFind(self.sql, self.titles, self.sizes, self.db ,parent=self)
        
        if a.exec_() == QtGui.QDialog.Accepted:
            self.idValue = a.array[0]
            self.setText(a.array[1])
            
        #print self.str()    
        QtGui.QLineEdit.focusInEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusIn))
        
    def getValue(self):
        return self.idValue
        
    def setValue(self,idVal):
        
        if idVal is None:
            self.idValue = None 
            return

        idName = self.sql.split()[1][:-1]
        if self.sql1:
            sql = self.sql1 % idVal # Μάλλον ακυρώνεται ... 
        else:            
            if 'WHERE' in self.sql:
                sqlWhere = " AND %s=%s" % (idName,idVal)
            else:
                sqlWhere = " WHERE %s=%s" % (idName,idVal)
           
            sql = self.sql + sqlWhere
        
        v = dbutils.getDbOneRow(sql, self.db)
        
        if v:
            self.setText(v[1])
            self.idValue = idVal
        else:
            self.setText('')
            self.idValue = None
    def str_(self):
        
        return '%s %s' % (self.idValue,self.text())
    @pyqtProperty(int)
    def timi(self):
        return self.getValue()
    
BLANK, GREEN = range(2)

class WeekDays(QtGui.QWidget):

    def __init__(self,vals=[1,1,1,1,1,0,0],parent=None,dayNames=u'ΔΕ ΤΡ ΤΕ ΠΕ ΠΑ ΣΑ ΚΥ'):
        super(WeekDays, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding))
       
        self.setValue(vals) # Δημιουργεί το self.grid
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
        
    def getValue(self,strVal=False): # strval : Εάν η επιστρεφόμενη τιμή είναι string ή array
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
        
    def str_(self):
        return self.getValue(True)
        
    def setValue(self,darr=[0,0,0,0,0,0,0]):
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
        self.setValue([0,0,0,0,0,0,0])
        
    def set5days(self):
        'Set Standard five days week'
        self.setValue([1,1,1,1,1,0,0])
        
    @pyqtProperty(str)
    def timi(self):
        return self.getValue(True) 
      
def fieldFactory(typ, params=[],isRequired=False):
    paramLen = len(params)
    if typ == 'txt':
        if paramLen == 0:
            return DbLineEdit()
        else:
            return DbLineEdit(params[0],isRequired)
    elif typ == 'int':
        if paramLen == 0:
            return DbSpinBox()
        else:
            return DbSpinBox(params[0])
    elif typ == 'dec':
        if paramLen == 0:
            return DbDoubleSpinBox()
        else:
            return DbDoubleSpinBox(params[0])
    elif typ == 'dat':
        if paramLen == 0:
            return DbDateEdit()
        else:
            return DbDateEdit(params[0])
    elif typ == 'key':
        if paramLen == 4:
            return ButtonLineEdit(params[0],params[1],params[2],params[3])
        else:
            return ButtonLineEdit(params[0],params[1],params[2])
    elif typ == 'box':
        return DbComboBox(params[0])
    elif typ == 'wdy':
        if params:
            return WeekDays(params[0])
        else:
            return WeekDays()
    else:
        return None,None
    
            
StyleSheet = """
QLineEdit { background-color: rgb(255, 255, 192); }
QDateEdit { background-color: rgb(255, 255, 192); }
"""                                  
class autoDialog(QtGui.QDialog):
    def __init__(self,tname='m12_mis',db=None,idv=None, parent=None):
        QtGui.QDialog.__init__(self)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        if not db:
            self.accept()
              
        self.setStyleSheet(StyleSheet)
        self.table = tname
        self.setWindowTitle(fsql.t[self.table][0])
        self.db = db
        self.id = idv
        self.lb = []
        self.od = OrderedDict()
        
        self.layout = QtGui.QGridLayout()
        
       
        bsave = QtGui.QPushButton(u'Αποθήκευση')
        bquit = QtGui.QPushButton(u'Ακύρωση')
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(bquit)
        buttonLayout.addItem(QtGui.QSpacerItem(100,60,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding))
        buttonLayout.addWidget(bsave)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(self.layout)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
        
        bsave.clicked.connect(self.updateOrInsert)
        bquit.clicked.connect(self.reject)
        
        self.__makeControls()
        self.__populate()
        #self.sqls()
    def __makeControls(self):
        
        fields =  dbutils.parseDDL(self.table,self.db)
        fields.pop(0) # αφαίρεση της στήλης του id
        for line in fields:
            typ = line['ctype']
            name = line['cname']
            req  = line['requi'] 
            if name == 'orar' and self.table == 'm12_orar':
                typ = 'wdy'
            self.lb.append(fsql.l[name+'-'+self.table]) 
            if typ == 'key':
                self.od[name] = fieldFactory(typ,[fsql.f[name][0],fsql.f[name][1],self.db])
            else:
                self.od[name] = fieldFactory(typ,isRequired=req)
        i = 0
        for key in self.od:
            try:
                self.layout.addWidget(QtGui.QLabel(self.lb[i]),i,0)
            except:
                pass
            self.layout.addWidget(self.od[key],i,1)
            i += 1
            
    def __populate(self):
        if not self.id: # Εάν δεν έχει τιμή το id επιστρέφουμε ...
            return None
        #Πρώτα απ'όλα βρίσκουμε την εγγραφή         
        rowVal = dbutils.getDbOneRow(self.selectSQL(), self.db)
        i=0
        if rowVal:
            for key in self.od:
                self.od[key].setValue(rowVal[i])
                i += 1
                
    def __areDataValid(self):
        errorLog = '' 
        i=0
        for key in self.od:
            if self.od[key].getValue() is None:
                errorLog += u'Το πεδίο %s δεν έχει σωστή τιμή\n' % self.lb[i]
            i += 1
        if errorLog:
            QtGui.QMessageBox.warning(self,u'Προσοχή υπάρχουν λάθη',errorLog)
            return False 
        return True 
    
    def updateOrInsert(self):
        if not self.__areDataValid():
            return # Τα μυνήματα θα μας τα δώσει η συνάρτηση self.validation
        
        if self.id:
            sql = self.updateSQL()
            #make update Here
        else:
            sql = self.insertSQL()
            #Make insert Here
        insNo = dbutils.commitToDb(sql, self.db)
        if insNo:
            QtGui.QMessageBox.warning(self,u'Όλα Καλά',u'Η εγγραφή αποθηκευτηκε με αριθμό : %s' % insNo)
        else:
            QtGui.QMessageBox.warning(self,u'Όλα Καλά',u'Η εγγραφή με αριθμό : %s Ενημερώθηκε' % self.id)
        self.accept()
                    
    def insertSQL(self):
        str1 = "INSERT INTO %s (" % self.table
        str2 = "("
        for  key in self.od:
            str1 += "%s," % key
            str2 += "'%s'," % self.od[key].getValue()
        str1 = str1[:-1] + ") VALUES "
        str2 = str2[:-1] + ')'
        sqlInsert = str1 + str2
        return sqlInsert
    
    def updateSQL(self):
        sqlUpdate  = "UPDATE %s SET " % self.table
        for  key in self.od:
            sqlUpdate += "%s='%s'," % (key,self.od[key].getValue())
        sqlUpdate = sqlUpdate[:-1] + ' '
        sqlUpdate += "WHERE id=%s" % self.id
        return sqlUpdate
    
    def selectSQL(self):
        sqlSelect = "SELECT "
        for key in self.od:
            sqlSelect += "%s," % key
        sqlSelect = sqlSelect[:-1] + ' '
        sqlSelect += "FROM %s " % self.table
        sqlSelect += "WHERE id=%s" % self.id
        return sqlSelect
    
    def sqls(self):
        print self.selectSQL()
        print self.insertSQL()
        print self.updateSQL()

def tst():
    s = "SELECT m12_pro.id, m12_pro.prod || ' ' || m12_fpr.epon "
    a = s.split()
    print a[1][:-1]
            
if __name__ == '__main__':
    
    import sys
    app = QtGui.QApplication([])
    adds = autoDialog('m12_orar','c:/ted/dropbox/mis.sql3',3)
    #adds = ButtonLineEdit()
    adds.show()
    #adds.od['sex_id'].setValue('0')
    sys.exit(app.exec_()) 
    tst()