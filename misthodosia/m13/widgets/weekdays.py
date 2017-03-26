# -*- coding: utf-8 -*-
'''
Created on 19 Φεβ 2013

@author: tedlaz
'''

# -*- coding: utf-8 -*-
from __future__ import division
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, Qt
BLANK, GREEN = range(2)

class WeekDaysWidget(QtGui.QWidget):

    def __init__(self, parent=None,vals=[1,1,1,1,1,0,0]):
        super(WeekDaysWidget, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding))
       
        self.setValues(vals) # Δημιουργεί το self.grid
        self.selected = [0, 0]
        
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
        days = [u'ΔΕ',u'ΤΡ',u'ΤΕ',u'ΠΕ',u'ΠΑ',u'ΣΑ',u'ΚΥ']
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
            painter.drawText(rect.adjusted(6, 3, -3, -3),days[x])
            painter.drawRect(rect)
        #print self.getValues()
        
    def getValues(self,strVal=False): # strval : Εάν η επιστρεφόμενη τιμή είναι string ή array
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
        
    def setValues(self,darr=[0,0,0,0,0,0,0]):
        'Set values to days vector. But first checks for proper array length and type'
        tmparr = []
        
        if isinstance(darr,str):
            tmparr = eval(darr)
        else:
            tmparr = darr
            
        if len(tmparr) == 7:
            self.grid = tmparr
        else:
            self.grid = [0,0,0,0,0,0,0]
        self.update() 
              
    def reset(self):
        'Set everything to Null'
        self.setValues([0,0,0,0,0,0,0])
        
    def set5days(self):
        'Set Standard five days week'
        self.setValues([1,1,1,1,1,0,0])              
        
def calcDays(year,month,d=[4,5],num=0):
    import calendar
    stra = ''
    first,days = calendar.monthrange(year,month)
    f={0:0,1:0,2:0,3:0,4:0,5:0,6:0}
    k={0:'Δε',1:'Τρ',2:'Τε',3:'Πε',4:'Πα',5:'Σα',6:'Κυ'}
    months = [u'Ιανουάριος',u'Φεβρουάριος',u'Μάρτιος',u'Απρίλιος',
                u'Μάϊος',u'Ιούνιος',u'Ιούλιος',u'Αύγουστος',
                u'Σεπτέμβριος',u'Οκτώβριος',u'Νοέμβριος',u'Δεκέμβριος'
             ]
    wdays = [u'Δευτέρες',u'Τρίτες',u'Τετάρτες',u'Πέμπτες',u'Παρασκευές',u'Σάββατα',u'Κυριακές']
    
    for i in range(days):
        a = (first + i) % 7
        f[a] += 1
        
    tot = 0
    meres = ''
    
    for el in d:
        tot += f[el]
        meres += '%s + ' % wdays[el]
     
    stra += 'Περίοδος : %s %s \n' %  (months[month-1],year)
    stra += '\n'
    
    for key in f:
        stra+= '%s:%s ' % (k[key],f[key])
        
    meres = meres[:-2]
    stra += '\n'
    stra += '\n%s =  %s ημέρες' % (meres,tot)
    if num :
        return tot
    else:
        return stra 
    
def calcDaysFromControl(year,month,c=[0,0,0,0,0,0,0],num=0):
    ar = []
    for i in range(len(c)):
        if c[i]:
            ar.append(i)
    return calcDays(year,month,ar,num)

class test(QtGui.QDialog):
    def __init__(self,parent=None,wdays=[1,1,1,1,1,0,0]):
        QtGui.QDialog.__init__(self)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        groupBox = QtGui.QGroupBox()
        groupBox.setTitle(u'Ημέρες εργασίας / βδομάδα')
        groupBox.setGeometry(QtCore.QRect(30, 30, 190, 51))
        groupBox.setMinimumSize(QtCore.QSize(190, 51))
        groupBox.setMaximumSize(QtCore.QSize(190, 51))
        
        self.cw = WeekDaysWidget(groupBox,wdays)
        self.cw.setGeometry(QtCore.QRect(10, 20, 75, 23))
        
        etosl = QtGui.QLabel(u'Έτος')
        self.etos = QtGui.QSpinBox()
        self.etos.setMinimum(1900)
        self.etos.setMaximum(2099)
        
        minasl = QtGui.QLabel(u'μήνας')
        self.minas  = QtGui.QSpinBox()
        self.minas.setMinimum(1)
        self.minas.setMaximum(12)
        
        gridl = QtGui.QGridLayout()
        gridl.addWidget(etosl,0,0)
        gridl.addWidget(self.etos,0,1)
        gridl.addWidget(minasl,1,0)
        gridl.addWidget(self.minas,1,1)
        
        
        button = QtGui.QPushButton(u'test')
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(groupBox)
        layout.addLayout(gridl)
        layout.addWidget(button)
        self.setLayout(layout)
        button.clicked.connect(self.buttonPress)
        
    def buttonPress(self):
        reply = QtGui.QMessageBox.information(self, u"Δοκιμαστικό", calcDaysFromControl(self.etos.value(),self.minas.value(),self.cw.getValues()))
        return reply
    
class weekDaysData():
    def __init__(self, vals = '[0,0,0,0,0,0,0]'):
        self.setData(vals)
        self.weekDaysNames = [u'Δευτέρες',u'Τρίτες',u'Τετάρτες',u'Πέμπτες',u'Παρασκευές',u'Σάββατα',u'Κυριακές']
        
    def setData(self,vals):
        if isinstance(vals,str):
            self.vals = eval(vals)
        else:
            if len(vals) == 7:
                self.vals = vals
            else:
                self.vals = [0,0,0,0,0,0,0]
                
    def getDataToStr(self):
        st = '['
        for i in range(7):
            if i == 6:
                st += '%s]' % self.vals[i]
            else:
                st += '%s,' % self.vals[i]
        return st
    
    def getDataArray(self):
        return self.vals
    
class testw():
    def __init__(self,val):
        a = 3 / val  
        
if __name__ == "__main__":
    import sys
    #calcDays(2013,5)
    try:
        d = testw(0)
        print d.a
    except:
        d = 4
        print 'lathos'
    wd = weekDaysData('[0,0,0,1,1,0,0]')
    print wd.getDataToStr()
    app = QtGui.QApplication(sys.argv)
    form = test()
    form.setWindowTitle(u"weekdays Δοκιμή")
    form.show()
    app.exec_()