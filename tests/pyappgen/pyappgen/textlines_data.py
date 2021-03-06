# -*- coding: utf-8 -*-
'''
Created on 18 Δεκ 2012
1.Δημιουργία γραμμών κειμένου σταθερού μεγέθους για τη δημιουργία αρχείων για
  ΙΚΑ , ΔΟΥ , κλπ
2.Ανάγνωση από αρχεία σταθερού μεγέθους και επιστροφή array με τα δεδομένα
@author: tedlaz
'''
import num_txt_etc as nm
TEXT, INT,DEC, DAT = range(4)
class egrCol():
    '''
    Σταθερού μεγέθους στήλη δεδομένων. 
    '''
    def __init__(self,name,size,typ=TEXT, fixedValue=None,ln=None,col=None):
        self.name = name
        self.size = size
        self.typ = typ
        self.fixedValue = fixedValue
        self.ln = ln
        self.col = col
        
    def makeColVal(self,val):
        #sval = ''
        #print 'Typos-->',self.typ
        if self.fixedValue:
            tstr =  u'%s' % self.fixedValue
        else:
            tstr = u'%s' % val
            
            
        if self.typ == INT:
            difInt = self.size - len(tstr)
            if difInt < 0:
                return '0' * self.size 
            sval = ('0' * difInt) + tstr

        elif self.typ == TEXT:
            difText = self.size - len(tstr)
            if difText < 0:
                return tstr[:self.size]
            sval = tstr + (' ' * difText)
            
        elif self.typ == DAT:
            difDat = self.size - len(tstr)
            if difDat < 0:
                return tstr[:self.size]
            sval = tstr + (' ' * difDat)
            
        elif self.typ == DEC:
            
            if '.' in tstr:
                akereo, dekadiko = tstr.split(".")
            elif ',' in tstr:
                akereo, dekadiko = tstr.split(",")
            else:
                akereo, dekadiko = tstr , '00'
                
            ldek = len(dekadiko)
            
            if ldek == 0:
                dekadiko = '00'
            elif ldek == 1:
                dekadiko = dekadiko + '0'
            else:
                dekadiko = dekadiko[:2]
                
            tv = akereo + dekadiko
            #print akereo, dekadiko
            dif2= self.size - len(tv)
            
            if dif2 < 0:
                return tv[:self.size]
            
            sval = ('0' * dif2) + tv
        return sval

ROWSTD, ROWSUM = range(2)
class egrRow():
    '''
    Σταθερού μήκους γραμμή δεδομένων που αποτελείται από στήλες δεδομένων (βλέπε παραπάνω).
    Οι στήλες είναι οργανωμένες με βάση τη σειρά εισαγωγής τους.
    '''
    def __init__(self,typ=ROWSTD):
        self.name = 'No name'
        self.typ = typ
        self.egrCols = []
        self.lineSize = 0 # Το μήκος της γραμμής
        self.arrSize  = 0 # Ο αριθμός των στηλών

    def addCol(self,eggrcol):
        self.egrCols.append(eggrcol)
        self.lineSize += eggrcol.size
        self.arrSize += 1

    def toStr(self,data=[]):
        tval = ''
        for i in range(self.arrSize):
            tval += self.egrCols[i].makeColVal(data[i])
        return tval
                    
class egrDoc():
    
    def __init__(self,ltypes):
        self.lineTypes = ltypes # Οι τύποι γραμμών
        self.lines = ''         # Οι συνολικές γραμμές του σε μορφή text.
        self.vals  = []
        
    def addLine(self,lno=None,val=[]):
        self.lines += self.lineTypes[lno].toStr(val) + '\n'
        self.vals.append([lno,val])
        
    def makeSums(self,lno):
        a = {}
        for lin in self.vals:
            if lin[0] == lno:
                for i in range(self.lineTypes[lno].arrSize):
                    #print 'Typos: %s' % self.lineTypes[lno].egrCols[i].typ
                    if self.lineTypes[lno].egrCols[i].typ == DEC:
                        tf = nm.dec(lin[1][i])
                        try:
                            a[i] += tf
                        except:
                            a[i] = tf
                    elif self.lineTypes[lno].egrCols[i].typ == INT:
                        tf = lin[1][i]
                        if tf:
                            tf = int(tf)
                        else:
                            tf = 0
                        try:
                            a[i] += tf
                        except:
                            a[i] = tf
        return a 
               
    def __str__(self):
        txt = ''
        for l in self.vals:
            if self.lineTypes[l[0]].typ == ROWSUM:
                #print 'This is Rowsum , l[0] = %s' % l[0]
                for i in range(self.lineTypes[l[0]].arrSize):
                    egrc = self.lineTypes[l[0]].egrCols[i]
                    if egrc.ln and egrc.col:
                        l[1][i] = self.makeSums(egrc.ln)[egrc.col]
                        
            txt += self.lineTypes[l[0]].toStr(l[1]) + '\n'
        return txt[:-1]
                    
if __name__ == '__main__':
    r1 = egrRow(ROWSUM)
    r1.addCol(egrCol(u'Type',1,INT,'1'))
    r1.addCol(egrCol(u'Ονομα',15,TEXT))
    r1.addCol(egrCol(u'Επώνυμο',15,TEXT))
    r1.addCol(egrCol(u'Ποσό',14,DEC))
    r1.addCol(egrCol(u'Σύνολο Ποσό',15,DEC,'',2,2))
    r1.addCol(egrCol(u'Σύνολο μέρες',10,INT,'',2,4))
        
    r2 = egrRow()
    r2.addCol(egrCol(u'Type',1,INT,'2'))
    r2.addCol(egrCol(u'Σύνολο Ποσό',15,DEC,'',2,2))
    r2.addCol(egrCol(u'Σύνολο μέρες',10,INT,'',2,4))
    
    r3 = egrRow()
    r3.addCol(egrCol(u'Type',1,INT,'3'))
    r3.addCol(egrCol(u'ΑΦΜ',9,TEXT))
    r3.addCol(egrCol(u'Ποσό',15,DEC))
    r3.addCol(egrCol(u'Κρατήσεις',15,DEC))
    r3.addCol(egrCol(u'Μέρες',10,INT))
    
    doc = egrDoc([r1,r2,r3])
    doc.addLine(0,['','ted','Lazaros','12000.45','',''])
    doc.addLine(1,['','','',''])
    doc.addLine(2,['','046949584','1230','110','2','4'])
    doc.addLine(2,['','046949584','32','50','5'])
    doc.addLine(2,['','046949584','1','1','3'])
    print doc
    print doc.makeSums(2)