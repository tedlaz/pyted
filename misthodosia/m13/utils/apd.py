# -*- coding: utf-8 -*-
'''
Created on 18 Νοε 2012

@author: tedlaz
'''
            
import textlines_data as td 
import utils.dbutils as adb 
import utils.tedutils as tu          
def lApd():
    l0 = td.egrRow(td.ROWSUM)
    l0.addCol(td.egrCol(u'1.Τύπος εγγραφής',1,td.INT,1))#Πάντα 01
    l0.addCol(td.egrCol(u'2.Πλήθος μέσων που προσκομίζονται',2,td.TEXT,'01')) #Πάντα 01
    l0.addCol(td.egrCol(u'3.ΑΑ μέσου',2,td.TEXT,'01')) #Πάντα 01
    l0.addCol(td.egrCol(u'4.Όνομα Αρχείου',8,td.TEXT,'CSL01'))
    l0.addCol(td.egrCol(u'5.Έκδοση',2,td.TEXT,'01'))
    l0.addCol(td.egrCol(u'6.Τύπος Δ΄΄ηλωσης',2,td.TEXT,'01')) # 01: Κανονική 02:Έκτακτη 03:επανυποβολή 04:Συμπληρωματική
    l0.addCol(td.egrCol(u'7.Υποκατάστημα ΙΚΑ Υποβολής',3,td.INT))
    l0.addCol(td.egrCol(u'8.Ονομασία Υποκαταστήματος ΙΚΑ',50,td.TEXT))
    l0.addCol(td.egrCol(u'9.Επωνυμία / Επώνυμο',80,td.TEXT))
    l0.addCol(td.egrCol(u'10.Όνομα',30,td.TEXT))
    l0.addCol(td.egrCol(u'11.Όνομα Πατρός',30,td.TEXT))
    l0.addCol(td.egrCol(u'12.Α.Μ.Ε.',10,td.INT))
    l0.addCol(td.egrCol(u'13.Α.Φ.Μ.',9, td.INT))
    l0.addCol(td.egrCol(u'14.Οδός',50,td.TEXT))
    l0.addCol(td.egrCol(u'15.Αριθμός',10,td.TEXT))
    l0.addCol(td.egrCol(u'16.Ταχυδρομικός Κωδικός',5,td.INT))
    l0.addCol(td.egrCol(u'17.Πόλη',30,td.TEXT))
    l0.addCol(td.egrCol(u'18.Από μήνα',2,td.TEXT))
    l0.addCol(td.egrCol(u'19.Από έτος',4,td.TEXT))
    l0.addCol(td.egrCol(u'20.Έως μήνα',2,td.TEXT))
    l0.addCol(td.egrCol(u'21.έως έτος',4,td.TEXT))
    l0.addCol(td.egrCol(u'22.Σύνολο Ημερών Ασφάλισης',8,td.INT,'',2,14))
    l0.addCol(td.egrCol(u'23.Σύνολο Αποδοχών',12,td.DEC,'',2,16))
    l0.addCol(td.egrCol(u'24.Σύνολο Καταβλητέων Εισφορών',12,td.DEC,'',2,23))
    l0.addCol(td.egrCol(u'25.Ημερομηνία υποβολής',8,td.TEXT))
    l0.addCol(td.egrCol(u'26.Ημερομηνία παύσης εργασιών',8,td.TEXT))
    l0.addCol(td.egrCol(u'27.Κενά',30,td.TEXT,''))
    

    l1 = td.egrRow()
    l1.addCol(td.egrCol(u'28.Τύπος εγγραφής',1,td.INT,'2'))
    l1.addCol(td.egrCol(u'29.Αριθμός Μητρώου Ασφαλισμένου',9,td.INT))
    l1.addCol(td.egrCol(u'30.Α.Μ.Κ.Α.',11,td.INT))
    l1.addCol(td.egrCol(u'31.Επώνυμο Ασφαλισμένου',50,td.TEXT))
    l1.addCol(td.egrCol(u'32.Όνομα Ασφαλισμένου',30,td.TEXT))
    l1.addCol(td.egrCol(u'33.Όνομα Πατρός Ασφαλισμένου',30,td.TEXT))
    l1.addCol(td.egrCol(u'34.Όνομα Μητρός Ασφαλισμένου',30,td.TEXT))
    l1.addCol(td.egrCol(u'35.Ημερομηνία Γέννησης',8,td.TEXT))
    l1.addCol(td.egrCol(u'36.Α.Φ.Μ.',9,td.INT))

    l2 = td.egrRow()
    l2.addCol(td.egrCol(u'37.Τύπος Εγγραφής',1,td.INT,'3'))
    l2.addCol(td.egrCol(u'38.Αριθμός Παραρτήματος',4,td.INT,'1'))
    l2.addCol(td.egrCol(u'39.Κ.Α.Δ.',4,td.TEXT))
    l2.addCol(td.egrCol(u'40.Πλήρες Ωράριο',1,td.INT,'0'))
    l2.addCol(td.egrCol(u'41.Όλες εργάσιμες',1,td.INT,'0'))
    l2.addCol(td.egrCol(u'42.Κυριακές',1,td.INT))
    l2.addCol(td.egrCol(u'43.Κωδικός Ειδικότητας',6,td.INT))
    l2.addCol(td.egrCol(u'44.Ειδικές περιπτώσεις ασφάλισης',2,td.INT,''))
    l2.addCol(td.egrCol(u'45.Πακέτο Κάλυψης',4,td.INT))
    l2.addCol(td.egrCol(u'46.Μισθολογική περίοδος - μήνας',2,td.INT))
    l2.addCol(td.egrCol(u'47.Μισθολογική περίοδος - έτος',4,td.INT))
    l2.addCol(td.egrCol(u'48.Από Ημερομηνία απασχόλησης',8,td.TEXT,''))
    l2.addCol(td.egrCol(u'49.Έως Ημερομηνία απασχόλησης',8,td.TEXT,''))
    l2.addCol(td.egrCol(u'50.Τύπος αποδοχών',2,td.INT))
    l2.addCol(td.egrCol(u'51.Ημέρες ασφάλισης',3,td.INT))
    l2.addCol(td.egrCol(u'52.Ημερομίσθιο',10,td.DEC))
    l2.addCol(td.egrCol(u'53.Αποδοχές',10,td.DEC))
    l2.addCol(td.egrCol(u'54.Εισφορές ασφαλισμένου',10,td.DEC))
    l2.addCol(td.egrCol(u'55.Εισφορές εργοδότη',10,td.DEC))
    l2.addCol(td.egrCol(u'56.Συνολικές Εισφορές',11,td.DEC))
    l2.addCol(td.egrCol(u'57.Επιδότηση ασφαλισμένου (ποσό)',10,td.DEC,''))
    l2.addCol(td.egrCol(u'58.Επιδότηση εργοδότη (%%)',5,td.DEC,''))
    l2.addCol(td.egrCol(u'59.Επιδότηση εργοδότη (ποσό)',10,td.DEC,''))
    l2.addCol(td.egrCol(u'60.Καταβλητέες εισφορές',11,td.DEC))

    l3 = td.egrRow()
    l3.addCol(td.egrCol(u'61.Τέλος αρχείου',3,td.TEXT,'EOF'))
    
    return l0, l1,l2,l3
sql0= '''
SELECT  ikac,ikap,cop,ono,pat,ame,afm,odo,num,tk,pol,perapo,xrisi,pereos
FROM m12_co,m12_xrisi,m12_trimino
WHERE m12_xrisi.id=%s AND m12_trimino.id=%s
'''
sql0Minas ='''
SELECT  ikac,ikap,cop,ono,pat,ame,afm,odo,num,tk,pol,perapo,xrisi,pereos
FROM m12_co,m12_xrisi,m12_apdp
WHERE m12_xrisi.id=%s AND m12_apdp.id=%s
'''
sql1 = '''
SELECT m12_mis.id, m12_period.trimino_id, m12_misd.pro_id,
m12_fpr.aika, m12_fpr.amka, m12_fpr.epon, m12_fpr.onom,m12_fpr.patr,m12_fpr.mitr,m12_fpr.igen,m12_fpr.afm,
m12_coy.kad,m12_eid.kad,
sum( case when mtyp_id=110 then val end) as imeres,
sum( case when mtyp_id=100 then val end) as imeromisthio,
sum( case when mtyp_id=200 then val end) as apodoxes,
sum( case when mtyp_id=500 then val end) as ikaEnos,
sum( case when mtyp_id=501 then val end) as ikaEtis,
sum( case when mtyp_id=502 then val end) as ika,
sum( case when mtyp_id=503 then val end) as aptyp,
sum( case when mtyp_id=504 then val end) as kpk,
m12_period.period, m12_xrisi.xrisi
FROM m12_misd
INNER JOIN  m12_mis on m12_mis.id = m12_misd.mis_id
INNER JOIN m12_period on m12_period.id=m12_mis.period_id
INNER JOIN m12_pro on m12_pro.id=m12_misd.pro_id
INNER JOIN m12_fpr on m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_coy on m12_coy.id=m12_pro.coy_id
INNER JOIN m12_eid on m12_eid.id=m12_pro.eid_id
INNER JOIN m12_xrisi on m12_xrisi.id=m12_mis.xrisi_id
WHERE m12_mis.xrisi_id=%s AND m12_period.trimino_id=%s
group by mis_id,pro_id
order by pro_id
'''

sql1Minas = '''
SELECT m12_mis.id, m12_period.id, m12_misd.pro_id,
m12_fpr.aika, m12_fpr.amka, m12_fpr.epon, m12_fpr.onom,m12_fpr.patr,m12_fpr.mitr,m12_fpr.igen,m12_fpr.afm,
m12_coy.kad,m12_eid.keid,
sum( case when mtyp_id=110 then val end) as imeres,
sum( case when mtyp_id=100 then val end) as imeromisthio,
sum( case when mtyp_id=200 then val end) as apodoxes,
sum( case when mtyp_id=500 then val end) as ikaEnos,
sum( case when mtyp_id=501 then val end) as ikaEtis,
sum( case when mtyp_id=502 then val end) as ika,
sum( case when mtyp_id=503 then val end) as aptyp,
sum( case when mtyp_id=504 then val end) as kpk,
m12_period.period, m12_xrisi.xrisi,
sum( case when mtyp_id=111 then val end) as kyriakes
FROM m12_misd
INNER JOIN  m12_mis on m12_mis.id = m12_misd.mis_id
INNER JOIN m12_period on m12_period.id=m12_mis.period_id
INNER JOIN m12_pro on m12_pro.id=m12_misd.pro_id
INNER JOIN m12_fpr on m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_coy on m12_coy.id=m12_pro.coy_id
INNER JOIN m12_eid on m12_eid.id=m12_pro.eid_id
INNER JOIN m12_xrisi on m12_xrisi.id=m12_mis.xrisi_id
WHERE m12_mis.xrisi_id=%s AND m12_period.id=%s
group by mis_id,pro_id
order by pro_id
'''
def makeApd(xrisi,trimino,db):
    '''
    1. Συγκέντρωση στοιχείων εταιρείας
    2. Συγκέντρωση στοιχείων εργαζομένων
    3. Συγκέντρωση στοιχείων μισθοδοσιών
    '''
    xrid = adb.getDbSingleVal("SELECT id FROM m12_xrisi WHERE xrisi='%s'" % xrisi, db)
    h = adb.getDbOneRow(sql0Minas % (xrid,trimino), db)
    arr = adb.getDbRows(sql1Minas % (xrid,trimino), db)
    if not h:
        return 'Error'
    if not arr:
        return 'Error'
    l0, l1, l2, l3 = lApd()
    doc = td.egrDoc([l0, l1,l2,l3])
    doc.addLine(0, [u'',u'',u'',u'',u'',u'',h[0],tu.caps(h[1]),tu.caps(h[2]),tu.caps(h[3]),tu.caps(h[4]),h[5],h[6],tu.caps(h[7]),tu.caps(h[8]),h[9],tu.caps(h[10]),h[11],h[12],h[13],h[12],u'',u'',u'',tu.nowToStr(),u'',u''])
    ergno=0
    for lin in arr:
        if ergno == int(lin[2]):
            pass 
        else:
            ergno = int(lin[2])
            if lin[23] == None : 
                l23 = 0
            else:
                l23 = lin[23]
            doc.addLine(1, [u'',lin[3],lin[4],tu.caps(lin[5]),tu.caps(lin[6]),tu.caps(lin[7]),tu.caps(lin[8]),tu.dateTostr(lin[9]),lin[10]])
        doc.addLine(2,[u'',u'',lin[11],u'',u'',l23,lin[12],u'',lin[20],lin[21],lin[22],u'',u'',lin[19],lin[13],lin[14],lin[15],lin[16],lin[17],lin[18],u'',u'',u'',lin[18]])
    doc.addLine(3,[u'',])
    return doc.__str__()
    
def readAPD(fname='CSL01.txt'):
    f = open(fname)
    for line in f:
        if line[:1] == '1':
            print 'main'
        elif line[:1] == '2':
            print 'erg'
        elif line[:1] == '3':
            print 'mis'
        else:
            print 'final'
            
def makeAPDfile(fname,xrisi,trimino,db):
    f = open(fname,'w')
    f.write(makeApd(xrisi,trimino,db).encode('CP1253'))
    f.close() 
         
if __name__ == '__main__':
    #print caps('κωνσταντίνος και καλά κρασιά για όλα τα καλά παιδιά ali baba and fourty thieves')
    #f = open('CSL01.txt','w')
    #f.write(makeAPD().encode('ISO8859-7'))
    #f.close()
    #readAPD()

    d = makeApd('2013',12,'e:/tmp/mistst.m13')#.encode('ISO8859-7')
    print d
    #print d.makeSums(0)
    #makeAPDfile("csl12")