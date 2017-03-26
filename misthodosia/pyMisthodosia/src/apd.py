#!/usr/bin/env python
#coding=utf-8

'''
Created on 06 Ιουν 2011

@author: tedlaz
'''
NUM = 9
DEC = 99
TXT = 0
DAT = 1
class field():
    def __init__(self, name,size,type):
        self.name = name
        self.size = size
        self.type = type
    def toString(self,val):
        txtval = '%s' % val
        lenval = len(txtval)
        if lenval > self.size:
            return ''
        dlen = self.size - lenval
        txt = ''
        if self.type == NUM: #Numeric with trailing zeros
            txt = ('0' * dlen) + txtval
        elif self.type == TXT: #Text with following spaces
            txt = txtval + (' ' * dlen)
        elif self.type == DEC: #Numeric with two decimals
            txt = ('0' * dlen) + txtval
            
        elif self.type == DAT: #Date Field DDMMYYYY
            txt = txtval + (' ' * dlen)
        else:
            txt = txtval + (' ' * dlen)
        return txt
    def __str__(self):
        return '%s -- %s' % (self.name, self.size)
  
class line():
    def __init__(self):
        self.fields = []
    def add(self,field):
        self.fields.append(field)
    def size(self):
        sz = 0
        for fld in self.fields:
            sz += fld.size
        return sz
    def newLine(self,fieldData):
        str = ''
        if len(fieldData) <> len(self.fields):
            return ''
        for i in range(len(fieldData)):
            str += '%s' % self.fields[i].toString(fieldData[i])
        str += '\n'
        return str
    def __str__(self):
        no=0
        st = ''
        for fld in self.fields:
            no += 1
            st += '%s --- %s\n' % (no,fld)
        return st
    
class apd():
    def __init__(self):
        self.line1=line()
        self.line1.add(field('Τύπος Εγγραφής',1,NUM))
        self.line1.add(field('Πλήθος μέσων που προσκομίζονται',2,NUM))
        self.line1.add(field('Α/Α μέσου',2,NUM))
        self.line1.add(field('Όνομα Αρχείου',8,TXT))
        self.line1.add(field('Έκδοση',2,NUM))
        self.line1.add(field('Τύπος Δήλωσης',2,NUM))
        self.line1.add(field('Υποκατάστημα ΙΚΑ Υποβολής',3,NUM))
        self.line1.add(field('Ονομασία Υποκαταστήματος ΙΚΑ',50,TXT))
        self.line1.add(field('Επωνυμία / Επώνυμο',80,TXT))
        self.line1.add(field('Όνομα',30,TXT))
        self.line1.add(field('Όνομα Πατρός',30,TXT))
        self.line1.add(field('Α.Μ.Ε.',10,NUM))
        self.line1.add(field('Α.Φ.Μ.',9,NUM))
        self.line1.add(field('Οδός',50,TXT))
        self.line1.add(field('Αριθμός',10,TXT))
        self.line1.add(field('Ταχυδρομικός Κωδικός',5,NUM))
        self.line1.add(field('Πόλη',30,TXT))
        self.line1.add(field('Από μήνα',2,NUM))
        self.line1.add(field('Από έτος',4,NUM))
        self.line1.add(field('Έως μήνα',2,NUM))
        self.line1.add(field('Έως έτος',4,NUM))
        self.line1.add(field('Σύνολο Ημερών Ασφάλισης',8,NUM))
        self.line1.add(field('Σύνολο Αποδοχών',12,DEC))
        self.line1.add(field('Σύνολο Καταβλητέων Εισφορών',12,DEC))
        self.line1.add(field('Ημερομηνία υποβολής',8,DAT))
        self.line1.add(field('Ημερομηνία παύσης εργασιών',8,DAT))
        self.line1.add(field('Κενά',30,TXT))
        self.line2=line()
        self.line2.add(field('Τύπος Εγγραφής',1,NUM))
        self.line2.add(field('Αριθμός Μητρώου Ασφαλισμένου',9,NUM))
        self.line2.add(field('Α.Μ.Κ.Α.',11,NUM))
        self.line2.add(field('Επώνυμο Ασφαλισμένου',50,TXT))
        self.line2.add(field('Όνομα Ασφαλισμένου',30,TXT))
        self.line2.add(field('Όνομα Πατρός Ασφαλισμένου',30,TXT))
        self.line2.add(field('Όνομα Μητρός Ασφαλισμένου',30,TXT))
        self.line2.add(field('Ημερομηνία Γέννησης',8,DAT))
        self.line2.add(field('Α.Φ.Μ.',9,NUM))
        self.line3=line()
        self.line3.add(field('Τύπος Εγγραφής',1,NUM))
        self.line3.add(field('Αριθμός Παραρτήματος',4,NUM))
        self.line3.add(field('Κ.Α.Δ.',4,NUM))
        self.line3.add(field('Πλήρες ωράριο',1,NUM))
        self.line3.add(field('Όλες εργάσιμες',1,NUM))
        self.line3.add(field('Κυριακές',1,NUM))
        self.line3.add(field('Κωδικός Ειδικότητας',6,NUM))
        self.line3.add(field('Ειδικές περιπτώσεις ασφάλισης',2,NUM))
        self.line3.add(field('Πακέτο Κάλυψης',4,NUM))
        self.line3.add(field('Μισθολογική περίοδος - μήνας',2,NUM))
        self.line3.add(field('Μισθολογική περίοδος - έτος',4,NUM))
        self.line3.add(field('Από Ημερομηνία απασχόλησης',8,DAT))
        self.line3.add(field('Έως Ημερομηνία απασχόλησης',8,DAT))
        self.line3.add(field('Τύπος αποδοχών',2,NUM))
        self.line3.add(field('Ημέρες Ασφάλισης',3,NUM))
        self.line3.add(field('Ημερομίσθιο',10,DEC))
        self.line3.add(field('Αποδοχές',10,DEC))
        self.line3.add(field('Εισφορές Ασφαλισμένου',10,DEC))
        self.line3.add(field('Εισφορές Εργοδότη',10,DEC))
        self.line3.add(field('Συνολικές Εισφορές',11,DEC))
        self.line3.add(field('Επιδότηση ασφαλισμένου (ποσό)',10,DEC))
        self.line3.add(field('Επιδότηση εργοδότη (%)',5,DEC))
        self.line3.add(field('Επιδότηση εργοδότη (ποσό)',10,DEC))
        self.line3.add(field('Καταβλητέες εισφορές',11,DEC))
        self.line4=line()
        self.line4.add(field('Τέλος Αρχείου',3,TXT))
        
    def saveToFile(self,filename):
        print 'File saved !!'
    def getFromFile(self,filename):
        pass

if __name__ == '__main__':
    ap = apd()
    str = ''
    str += ap.line1.newLine(['1','1','1','CSL01','1','1','098','Μοσχάτου','Nicopolis AE',
                                '','','0123456789','999999999','Κεδρηνού','66','11634',
                                'Αθήνα','01','2010','03','2010','25','150032','345','10062011','',''])
    str += ap.line2.newLine(['2','123123','111111111','Λάζαρος','Θεόδωρος',
                                      'Κων/νος','Σταυρούλα','10021963','999999999'])
    str += ap.line3.newLine(['3','1','22','1','0','333','','101','01','2010','','',
                             '01','25','','150032','100','200','300','','','','','300'])
    str += ap.line4.newLine(['eof'])
    print str