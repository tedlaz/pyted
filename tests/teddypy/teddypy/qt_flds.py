# -*- coding: utf-8 -*-
'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''

from PyQt4 import QtGui, QtCore, Qt

import params
import dbutils as dbu
import dbmodel as dbm
import qt_form_find as ff

import res_rc

class fldb(QtGui.QCheckBox):
    """
    True or False field
    Gets / Sets two values : 0 for unchecked , 2 for checked
    """

    def __init__(self, lbl, chkVal=False, isRequired=False, parent=None):
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
    def __init__(self, lbl, txtVal=None, isRequired=False, parent=None):
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

class fldj(flds):
    '''
    Text field with numeric chars only.
    '''
    def __init__(self, lbl,txtVal=None, isRequired=False, parent=None):
        super(fldj, self).__init__(lbl,txtVal, isRequired,parent)
        rval = QtCore.QRegExp('(\d*)([1-9])(\d*)')
        self.setValidator(QtGui.QRegExpValidator(rval))
            
class fldt(QtGui.QTextEdit):
    """
    Text field
    """
    def __init__(self, lbl, txtVal=None, isRequired=False, parent=None):
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
  
class fldd(QtGui.QDateEdit):
    '''
    Date values
    '''
    def __init__(self, lbl, sqliteDate=None, parent=None):
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
        return self.date().toString(params.SQLITE_DATE_FORMAT)
  
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
        self.setToolTip(params.MSG_RESET_DATE)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.RightButton:
            self.setText('')
        else:
            QtGui.QToolButton.mousePressEvent(self, event)
            
    def menuCalendar(self):
        self.setText(self.cal.selectedDate().toString(params.GREEK_DATE_FORMAT))
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
    def __init__(self,lbl,vals=[1,1,1,1,1,0,0],parent=None,dayNames=params.WEEK_DAYS):
        super(fldw, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding))
       
        self.lbl = lbl
        self.parent = parent
        
        self.setV(vals) # ���������� �� self.grid
        self.selected = [0, 0]
        self.dayNames = dayNames.split()
        self.setMinimumSize(QtCore.QSize(170, 20))
        self.setMaximumSize(QtCore.QSize(170, 20))
        self.setToolTip(params.MSG_SELECT_DAYS)
        
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
    
            #print(event.x(), event.y())
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
        #print(self.getValues())
        
    def getV(self,strVal=True): 
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
        vals, flds, status, mssg = dbu.dbRows(dbm.reprFlds(self.tbl), self.parent.db)
        
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
    ����������
    sql     = �� sql ��� ��� ����� �� �������� ��� ��������� ��������
    titles  = ������������ ��� �� table ��� ��������� �������� (string �� ������������ �� |)
    db      = � �������� ��� ������� �����������
    sizes   = �� ����� ��� ������ ��� ��������� ��������
    idVal   = �� �������� ������ ��� ��� ����� ������ ���� ��� ��������� ������������ ������� 
    '''
    
    def __init__(self, lbl,sql=None,idVal=None, sql1=None, parent=None,tbl=None):
        super(fldz, self).__init__(parent)
        
        self.lbl = lbl
        self.parent = parent
        
        self.tbl    = lbl
        self.sql    = sql
        self.sql1   = sql1 # SQL ������ ��� �� setValue ...
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
        a = ff.fFind(self.sql, self.parent.db, self.tbl, parent=self.parent)
        
        if a.exec_() == QtGui.QDialog.Accepted:
            self.idValue = a.array[0]
            self.setV(self.idValue) 
        QtGui.QLineEdit.focusInEvent(self, QtGui.QFocusEvent(QtCore.QEvent.FocusIn))
        
    def getV(self):
        return self.idValue
        
    def setV(self,idVal):
        
        if idVal is None:
            self.idValue = None 
            return
        
        idName = self.sql.split()[1][:-1]
        if ',' in idName:
            idName = idName.split(',')[0]
        if idName=='':
            idName = 'id'
        if self.sql1:
            sql = self.sql1 % idVal # ������ ���������� ... 
        else:            
            if 'WHERE' in self.sql:
                sqlWhere = " AND %s='%s'" % (idName,idVal)
            else:
                #sqlWhere = " WHERE %s=%s" % (idName,idVal)
                sqlWhere = " WHERE %s='%s'" % (idName,idVal)
           
            #sql = self.sql + sqlWhere
            sql = dbm.reprFlds(self.tbl,idVal)
        v , fnames, status, mssg = dbu.dbRows(sql, self.parent.db, 1)
        
        if status == dbu.ONE_VAL:
            v = v[0]
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
    
def test():
    import os
    import sys
    import qt_auto_form as af
    import test_create_demo_db as tcd

    sqls = "SELECT * FROM erp"
    print(tcd.create_demo_db())
    app = QtGui.QApplication([])
    dlg = af.autoForm(None, 'erp',tcd.db)
    dlg.show() 
    s = app.exec_()
    print(dbu.dbRows(sqls, tcd.db))
    os.remove(tcd.db)
    sys.exit(s)
    
if __name__ == '__main__':
    test()