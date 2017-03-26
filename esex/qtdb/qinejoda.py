# -*- coding: utf-8 -*-
'''
Created on 18 Φεβ 2011

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore

import dbforms as dbf

class ValidatedItemDelegate(QtGui.QStyledItemDelegate):
    def createEditor(self, widget, option, index):
        if not index.isValid():
            return 0
        if index.column() > 0: #only on the cells in the first column
            editor = QtGui.QLineEdit(widget)
            validator = QtGui.QDoubleValidator(-99.0,9999999999.0,2,editor)
            editor.setValidator(validator)
            return editor
        return super(ValidatedItemDelegate, self).createEditor(widget, option, index)

class fInsertEggrafi(QtGui.QDialog):
    def __init__(self, dbt, parent=None):
        super(fInsertEggrafi, self).__init__(parent)

        self.db = dbt

        self.setWindowTitle(u'Εισαγωγή Νέας Εγγραφής')

        glayout = QtGui.QGridLayout()

        lbDate  = QtGui.QLabel(u'Ημερομηνία')
        glayout.addWidget(lbDate,0,0)
        self.dat = dbf.DbDateEdit()
        self.dat.setMaximumWidth(110)
        glayout.addWidget(self.dat,0,1)

        lbPar = QtGui.QLabel(u'Παράρτημα')
        glayout.addWidget(lbPar,0,2)
        self.yp = dbf.DbButtonLineEdit('SELECT * FROM yp',db=self.db,idVal=1,tbl='yp_id')
        self.yp.setMaximumWidth(150)
        glayout.addWidget(self.yp,0,3)


        lbSyn = QtGui.QLabel(u'Αναζήτηση με ΑΦΜ')
        glayout.addWidget(lbSyn,1,0,1,1)
        self.pelafm = QtGui.QLineEdit()
        self.pelafm.setMaximumWidth(100)
        glayout.addWidget(self.pelafm,1,1,1,1)

        lbSyn = QtGui.QLabel(u'Προμηθευτής')
        glayout.addWidget(lbSyn,1,2,1,1)
        self.pel = dbf.DbButtonLineEdit('SELECT id,afm,epon FROM pro',db=self.db,tbl='pro_id')
        glayout.addWidget(self.pel,1,3,1,1)

        lbPar = QtGui.QLabel(u'Παραστατικό')
        glayout.addWidget(lbPar,2,0,1,1)
        self.par = dbf.DbLineEdit()
        self.par.setMaximumWidth(100)
        glayout.addWidget(self.par,2,1,1,1)


        vlayout = QtGui.QVBoxLayout(self)
        vlayout.addWidget(dbf.makeTitle(u'Εγγραφές αγορών, εξόδων'))
        vlayout.addLayout(glayout)

        self.tbl = QtGui.QTableWidget(self) # QtGui.QTableWidget(self)
        self.tbl.setStyleSheet("alternate-background-color: rgba(248,206,200);" )
        self.tbl.setItemDelegate(ValidatedItemDelegate())
        self.tbl.verticalHeader().setDefaultSectionSize(25)
        self.tbl.setAlternatingRowColors(True)
        self.tbl.setColumnCount(4)
        self.tbl.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem(u'Λογαριασμός'))
        self.tbl.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem(u'Αξία'))
        self.tbl.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem(u'ΦΠΑ'))
        self.tbl.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem(u'Σύνολο'))
        self.tbl.setColumnWidth(0,300)
        vlayout.addWidget(self.tbl)

        foot = QtGui.QGridLayout()
        lbltval = QtGui.QLabel(u'Καθαρή Αξία')
        lbltfpa = QtGui.QLabel(u'ΦΠΑ')
        lblttot = QtGui.QLabel(u'Σύνολο')
        self.tval = dbf.DbLineEdit()
        self.tfpa = dbf.DbLineEdit()
        self.ttot = dbf.DbLineEdit()
        self.tval.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tfpa.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ttot.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tval.setReadOnly(True)
        self.tfpa.setReadOnly(True)
        self.ttot.setReadOnly(True)
        foot.addWidget(lbltval,0,0,1,1)
        foot.addWidget(lbltfpa,0,1,1,1)
        foot.addWidget(lblttot,0,2,1,1)
        foot.addWidget(self.tval,1,0,1,1)
        foot.addWidget(self.tfpa,1,1,1,1)
        foot.addWidget(self.ttot,1,2,1,1)
        spfoot = QtGui.QSpacerItem(110, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        foot.addItem(spfoot,1, 3, 1, 1)
        self.bSave = QtGui.QPushButton(u'Αποθήκευση')
        self.bSave.setMinimumSize(QtCore.QSize(0, 40))
        foot.addWidget(self.bSave,0,4,2,1)

        vlayout.addLayout(foot)


        self.logt = QtGui.QTextEdit()
        self.logt.setReadOnly(True)
        self.logt.setMaximumHeight(50)
        vlayout.addWidget(self.logt)

        self.setLayout(vlayout)
        self.resize(800, 600)

        self.makeConnections()

        self.aa ='' #Για το άνοιγμα τουffind
        self.arData = []
        self.setNewLmoLines()

    def makeConnections(self):
        self.connect(self.tbl,QtCore.SIGNAL("cellChanged(int, int)"),self.onCellChange)
        self.bSave.clicked.connect(self.dbSave)

    def dbSave(self):
        sqlm = "INSERT INTO ds (yp_id,dat,par,pro_id,tval,tfpa,ttot) VALUES (?,?,?,?,?,?,?)"
        sqld = "INSERT INTO dsd (ds_id,dt_id,val,fpa) VALUES (?,?,?,?)"
        imnia = '%s' % self.dat.date().toString('yyyy-MM-dd')
        ypok  = '%s' % self.yp.timi
        pro   = '%s' % self.pel.timi
        parko = '%s' % self.par.text()
        sumv = self.sums()
        tval = '%s' % sumv[1]
        tfpa = '%s' % sumv[2]
        ttot = '%s' % sumv[3]
        validated = u''
        if not dbf.allowInsertDate(imnia, self.db) : validated += u'Η ημερομηνία ανήκει σε κλειστή περίοδο\n'
        if tval == '0': validated += u'Τουλάχιστον μία γραμμή με αξία\n'
        if pro == 'None': validated += u'Στοιχεία προμηθευτή\n'
        if parko == '': validated += u'Αριθμός παραστατικού\n'
        for lin in self.arData:
            if lin[1] == 0: continue
            etid = '%s' % lin[0]
            if etid == '0': validated += u'Λογαριασμός\n'
        if len(validated) >0:
            QtGui.QMessageBox.critical(self, u"Συμπληρώστε τα παρακάτω",validated)
            return

        dsid = dbf.commitToDb(sqlm,[ypok,imnia,parko,pro,tval,tfpa,ttot],self.db)
        for lin in self.arData:
            if lin[1] == 0:
                continue
            dtid = '%s' % lin[0]
            val  = '%s' % lin[1]
            fpa  = '%s' % lin[2]
            k = dbf.commitToDb(sqld,[dsid,dtid,val,fpa],self.db)
        if dsid:
            logData = u"Κατεχωρήθη στα έξοδα το Νο.%s(%s) αξίας %s ευρώ με AA : %s\n" % (parko,imnia,ttot,dsid)
        else:
            logData = u"Το παραστατικό No.%s είναι ήδη καταχωρημένο\n" % (parko,)
            QtGui.QMessageBox.critical(self, u"Λάθος εισαγωγής",logData)
            return
        self.addLog(logData,True)
        self.resetData()

    def resetData(self):
        self.par.setText('')
        for lin in self.arData:
            lin[1]=lin[2]=lin[3]=0
        for i in range(self.tbl.rowCount()):
            self.tbl.setItem(i,1,self.decItem(0))
            self.tbl.setItem(i,2,self.decItem(0))
            self.tbl.setItem(i,3,self.decItem(0))

    def addLog(self,logText,saveToDB=False):
        datetime = dbf.strDateTime()
        self.logt.setText(datetime +' -> '+ logText + self.logt.toPlainText())
        if saveToDB:
            dbf.addLogToDb(logText, self.db)
            #dbf.commitToDb("INSERT INTO lg(ldt,logp) VALUES (?,?)",[datetime,logText],self.db)

    def setNewLmoLines(self):
        dat1,heads = dbf.getDbRows('SELECT * FROM dt',self.db)
        for frm in dat1:
            self.newLine()
            row = self.tbl.rowCount()-1
            f0 = dbf.dec(frm[0],0)
            self.arData[row][0] = f0
            self.arData[row][4] = dbf.dec(frm[2])
            self.aa = frm[1]
            self.tbl.setItem(row,0,self.strItem(self.aa))


    def onCellChange(self,row,col):
        #if self.tbl.item(row,col).text() == '0':
        #    return
        pfpa = dbf.dec(self.arData[row][4]/dbf.dec(100),4)
        unfpa = 1+ pfpa

        if col == 0:
            bb =  self.tbl.item(row,col).text()
            #print 'Line 107-->bb: %s, aa: %s' % (bb,self.aa)
            if bb <> self.aa:
                frm = dbf.fFind('SELECT * FROM dt',self.db,'dt',1,parent=self)
                if frm.exec_() == QtGui.QDialog.Accepted:
                    f0 = dbf.dec(frm.array[0],0)
                    self.arData[row][0] = f0
                    self.arData[row][4] = dbf.dec(frm.array[2])
                    self.aa = frm.array[1]
                    self.tbl.setItem(row,0,self.strItem(self.aa))
                    if self.arData[row][1] <> 0:
                        pfpa = dbf.dec(self.arData[row][4]/dbf.dec(100),4)
                        fpa = dbf.dec(self.arData[row][1] * pfpa)
                        tot  = self.arData[row][1] + fpa
                        self.arData[row][2] = fpa
                        self.arData[row][3] = tot
                        self.tbl.setItem(row,2,self.decItem(fpa))
                        self.tbl.setItem(row,3,self.decItem(tot))
        elif col == 1:
            val = dbf.dec(self.tbl.item(row,col).text().replace(',','.'))

            if val <> self.arData[row][col]:
                fpa = dbf.dec(val * pfpa)
                tot  = val + fpa
                self.arData[row][1] = val
                self.arData[row][2] = fpa
                self.arData[row][3] = tot
                self.tbl.setItem(row,1,self.decItem(val))
                self.tbl.setItem(row,2,self.decItem(fpa))
                self.tbl.setItem(row,3,self.decItem(tot))

        elif col == 2:
            fpa = dbf.dec(self.tbl.item(row,col).text().replace(',','.'))
            if fpa <> self.arData[row][col]:
                if pfpa == 0:
                    fpa = dbf.dec(0)
                    val = dbf.dec(0)
                else:
                    val = dbf.dec(fpa/pfpa)
                tot = val + fpa
                self.arData[row][1] = val
                self.arData[row][2] = fpa
                self.arData[row][3] = tot
                self.tbl.setItem(row,1,self.decItem(val))
                self.tbl.setItem(row,2,self.decItem(fpa))
                self.tbl.setItem(row,3,self.decItem(tot))

        elif col == 3:
            tot = dbf.dec(self.tbl.item(row,col).text().replace(',','.'))
            if tot <> self.arData[row][col]:
                val = dbf.dec(tot/unfpa)
                fpa = tot - val
                self.arData[row][1] = val
                self.arData[row][2] = fpa
                self.arData[row][3] = tot
                self.tbl.setItem(row,1,self.decItem(val))
                self.tbl.setItem(row,2,self.decItem(fpa))
                self.tbl.setItem(row,3,self.decItem(tot))
                print ''
        self.updateTotals()

    def keyPressEvent(self,ev):
        crow = self.tbl.currentRow()
        ccol = self.tbl.currentColumn()
        if (ev.key()==QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            if self.tbl.hasFocus():
                if ccol < self.tbl.columnCount()-1:
                    self.tbl.setCurrentCell(crow, ccol+1)
                else:
                    if (self.tbl.rowCount()-1) == crow:
                        if self.arData[crow][3] == 0:
                            crow = crow -1
                        else:
                            self.newLine()
                    self.tbl.setCurrentCell(crow+1, 0)
            if self.pelafm.hasFocus():
                self.findCustomerByAFM(self.pelafm.text())

    def findCustomerByAFM(self,txt):
        txtb = txt+'%'
        sql = "SELECT id, afm,epon FROM pro WHERE afm LIKE '%s'" % txtb
        pel = dbf.getDbOneRow(sql,self.db)
        if pel:
            self.pel.setValue(pel[0])
        else:
            if len(txt) == 9:
                pel = dbf.checkVat(txt)
                if pel['valid']:
                    ccod = '%s' % pel['countryCode']
                    afm  = '%s' % pel['vatNumber']
                    rdat = '%s' % pel['requestDate']
                    epon = '%s' % pel['name']
                    addr = '%s' % pel['address']
                    sqin = "INSERT INTO pro (ccod,afm,rdat,epon,addr) VALUES (?,?,?,?,?)"
                    msgtxt = u'Βρέθηκε προμηθευτής με στοιχεία:\n ΑΦΜ : %s\nΕπωνυμία : %s\nΔιεύθυνση : %s\n\nΝα καταχωρηθεί ??' % (afm,epon,addr)
                    reply = QtGui.QMessageBox.question(self, u'Επιτυχής αναζήτηση',msgtxt , QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                    if reply == QtGui.QMessageBox.Yes:
                        synid = dbf.commitToDb(sqin,[ccod,afm,rdat,epon,addr], self.db)
                        self.pel.setValue(synid)
                        self.addLog(u'Έγινε καταχώρηση Προμηθευτή: %s' % self.pel.text(),True)
                else:
                    if 'conError' in pel:
                        QtGui.QMessageBox.critical(self, u"Αποτυχία σύνδεσης",u"Δεν γίνεται σύνδεση με τη Βάση Δεδομένων του VIES")
                    else:
                        QtGui.QMessageBox.critical(self, u"Αποτυχία αναζήτησης",u"Δεν βρέθηκε ενεργό ΑΦΜ : %s στη Βάση Δεδομένων του VIES" % txt)
            else:
                self.addLog(u'Δώσε ολόκληρο το ΑΦΜ για να γίνει αναζήτηση στη βάση δεδομένων')
        #QtGui.QDialog.keyPressEvent(self,ev) #Final method

    def newLine(self):
        '''
        arData : θέση[0]: et_id (Τύπος Εγγραφής)
                 Θέση[1]: val
                 θέση[2]: fpa
                 θέση[3]: tot (Σύνολο)
                 θέση[4]: ποσοστό φπα για τον υπολογισμό
        '''
        self.arData.append([0,0,0,0,0])
        rc = self.tbl.rowCount()
        self.tbl.setRowCount(rc+1)

        for i in range(1,4):
            self.tbl.setItem(rc,i,self.decItem(0))

    def sums(self):
        return [sum(x) for x in zip(*self.arData)]

    def updateTotals(self):
        totals = self.sums()
        self.tval.setText('%s' % totals[1])
        self.tfpa.setText('%s' % totals[2])
        self.ttot.setText('%s' % totals[3])

    def decItem(self,val):
        item = QtGui.QTableWidgetItem('%s' % val)
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        return item

    def strItem(self,val):
        item = QtGui.QTableWidgetItem('%s' % val)
        return item

    def canAdd(self):
        return False
if __name__ == '__main__':
    print 'just for check eksoda'
