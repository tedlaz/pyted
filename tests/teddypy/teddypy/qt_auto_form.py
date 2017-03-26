# -*- coding: utf-8 -*-
'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''

from PyQt4 import QtGui, QtCore, Qt
import dbutils as dbu
import dbmodel as dbm
import utils
import qt_flds as qtf

class autoForm(QtGui.QDialog):
    def __init__(self, id=None, tbl=None,db=None,parent=None,cols=1):
        super(autoForm, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        self.setWindowTitle(dbm.getTableLabel(tbl))
        
        self.cols = cols
        self.id  = id #save id for later use (updating record)
        self.tbl = tbl
        self.db  = db
        self.oldVals = None  
        if id:
            oldVals, self.colnames, status, mssg = dbu.dbRows('select * from %s where id=%s' % (tbl,id),db)
            self.isNew = False
            if oldVals:
                self.oldVals = oldVals[0][1:] #Leave out id
            else:
                id = None
        else:
            oldVals, self.colnames, status, mssg = dbu.dbRows('select * from %s where id=-1' % tbl,db)
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
                sql = 'select * from %s' % el[1:]
                strv = u"self.fldArray.append(qtf.fld%s(u'%s',sql,parent=self,tbl='%s'))" % (typ,el,el[1:])           
            else:
                strv = u"self.fldArray.append(qtf.fld%s(u'%s',parent=self))" % (typ,el)
            exec(strv)
            
    def _glayoutFill(self,glayout):
        j = 0
        for i in range(len(self.fldArray)):
            glayout.addWidget(QtGui.QLabel(dbm.getLabel(self.fldArray[i].lbl)),i /self.cols ,j)
            j += 1
            glayout.addWidget(self.fldArray[i],i/self.cols,j)
            j += 1
            if j > (self.cols*2)-1:
                j = 0
                                
    def getV(self):
        #for el in self.fldArray:
        #    print(el.getV())
        if not self._save():
            pass
        else:
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
            sha1old = utils.sha1OfArray(self.oldVals)
            sha1New = utils.sha1OfArray(newVals)
            if sha1old <> sha1New:
                lastid, msg = dbu.dbCommit(sqlup, self.db)              
                if not lastid:
                    QtGui.QMessageBox.critical(self, u'Πρόβλημα !!!', u'%s' % msg)
                    return False
                logMessage = u'Updated DB:%s, tbl:%s, id:%s , sql:%s' % (self.db,self.tbl,self.id, sqlup)
            else:
                logMessage = u'No change in record'
        else:
            lastid, msg = dbu.dbCommit(sqlin, self.db)
            if not lastid:
                QtGui.QMessageBox.critical(self, u'Πρόβλημα !!!', u'%s' % msg)
                return False
            logMessage = u'New DB:%s, tbl:%s, id:%s, sql:%s' % (self.db,self.tbl,lastid,sqlin)
        return logMessage.encode('utf-8')
    
if __name__ == '__main__':
    pass