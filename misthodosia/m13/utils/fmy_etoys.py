# -*- coding: utf-8 -*-
'''
Created on 18 Νοε 2012

@author: tedlaz
'''
def caps(stri):
    st = stri.decode('UTF-8')
    l = u'αβγδεζηθικλμνξοπρστυφχψω άέήίόύώϊ'
    h = u'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ ΑΕΗΙΟΥΩΙ'
    tstr = u''
    for g in st:
        found = False
        for i in range(len(l)):
            if g == l[i]:
                tstr += u'%s' % h[i]
                found = True
                break
        if not found:
            tstr += g.upper()
    return tstr

import textlines_data as td
from qtprint.qt_table_report import gr0

def lfmy():

    l0 = td.egrRow()
    l0.addCol(td.egrCol(u'101.Τύπος Record',1,td.INT,'0')) #Πάντα 0
    l0.addCol(td.egrCol(u'102.Όνομα αρχείου',8,td.TEXT,'JL10')) #Πάντα JL10
    l0.addCol(td.egrCol(u'103.Ημερομηνία δημιουργίας',8,td.DAT)) # Ημερομηνία τρεξίμτος
    l0.addCol(td.egrCol(u'104.Αρ.κύκλου τρεξίματος',4,td.INT)) # Χρήση που αφορά
    l0.addCol(td.egrCol(u'105.FILLER',99,td.TEXT,''))

    l1 = td.egrRow()
    l1.addCol(td.egrCol(u'201.Τύπος Record',1,td.INT,'1'))#Πάντα 1
    l1.addCol(td.egrCol(u'202.Έτος',4,td.INT))
    l1.addCol(td.egrCol(u'203.α.Επώνυμο',18,td.TEXT))
    l1.addCol(td.egrCol(u'203.β.Όνομα',9,td.TEXT))
    l1.addCol(td.egrCol(u'203.γ.Πατρώνυμο',3,td.TEXT))
    l1.addCol(td.egrCol(u'204.Ενδειξη επωνυμίας ή ονοματεπώνυμο',1,td.INT)) # 0= επωνυμία , 1=ονοματεπώνυμο
    l1.addCol(td.egrCol(u'205.Α.Φ.Μ.',9,td.INT))
    l1.addCol(td.egrCol(u'206.Αντικείμενο δραστηριότητας Επιχείρησης',16,td.TEXT))
    l1.addCol(td.egrCol(u'207.Πόλη',10,td.TEXT))
    l1.addCol(td.egrCol(u'208.Οδός',16,td.TEXT))
    l1.addCol(td.egrCol(u'209.Αριθμός',5,td.TEXT))
    l1.addCol(td.egrCol(u'210.Τ.Κ.',5,td.TEXT))
    l1.addCol(td.egrCol(u'211.FILLER',23,td.TEXT,''))

    l2 = td.egrRow(td.ROWSUM)
    l2.addCol(td.egrCol(u'301.Τύπος Record',1,td.INT,'2'))#Πάντα 2
    l2.addCol(td.egrCol(u'302.Ακαθάριστες αποδοχές',15,td.DEC,'',3,9))
    l2.addCol(td.egrCol(u'303.Σύνολο κρατήσεων',15,td.DEC,'',3,10))
    l2.addCol(td.egrCol(u'304.Καθαρές αποδοχές',15,td.DEC,'',3,11))
    l2.addCol(td.egrCol(u'305.Σύνολο φόρου αναλογεί',14,td.DEC,'',3,12))
    l2.addCol(td.egrCol(u'306.Σύνολο παρακρατηθέντος φόρου',14,td.DEC,'',3,13))
    l2.addCol(td.egrCol(u'307.Σύνολο Έκτακτης εισφοράς αλληλεγγύης',13,td.DEC,'',3,14))
    l2.addCol(td.egrCol(u'308.FILLER',32,td.TEXT,''))

    l3 = td.egrRow()
    l3.addCol(td.egrCol(u'401.Τύπος Record',1,td.INT,'3'))#Πάντα 2
    l3.addCol(td.egrCol(u'402.Α.Φ.Μ.',9,td.INT))
    l3.addCol(td.egrCol(u'403.FILLER',1,td.TEXT,''))
    l3.addCol(td.egrCol(u'404.Επώνυμο',18,td.TEXT))
    l3.addCol(td.egrCol(u'405.Όνομα',9,td.TEXT))
    l3.addCol(td.egrCol(u'406.Όνομα συζύγου ή πατέρα',3,td.TEXT))
    #----------------------
    l3.addCol(td.egrCol(u'407.AMKA',11,td.TEXT))
    l3.addCol(td.egrCol(u'408.Αριθμός Τέκνων',2,td.TEXT))
    l3.addCol(td.egrCol(u'409.Είδος αποδοχών',2,td.INT)) # Πινακάκι με είδη αποδοχών
    l3.addCol(td.egrCol(u'410.Ακαθάριστες αποδοχές',10,td.DEC))
    l3.addCol(td.egrCol(u'411.Κρατήσεις εκτός φόρου',9,td.DEC))
    l3.addCol(td.egrCol(u'412.Καθαρές αποδοχές',10,td.DEC))
    l3.addCol(td.egrCol(u'413.Φόρος που αναλογεί',9,td.DEC))
    l3.addCol(td.egrCol(u'414.Φόρος που παρακρατήθηκε',9,td.DEC))
    l3.addCol(td.egrCol(u'415.Έκτακτη εισφορ΄΄α',9,td.DEC))
    l3.addCol(td.egrCol(u'416.FILLER',8,td.TEXT,''))

    return l0,l1,l2,l3

def makeFMYFile(fname,etos,db,imniaEkdosis='2012-12-31'):
    
    doy, co, vols = fmyEtoys(etos,imniaEkdosis,db)
    f = open(fname,'w')
    f.write(doy.encode('CP1253') )
    f.close()
    
    return co, vols

sqlergData = '''
SELECT  m12_mis.xrisi_id, m12_fpr.afm, m12_fpr.epon, m12_fpr.onom,m12_fpr.patr,m12_fpr.pol,odo,m12_fpr.num,m12_fpr.tk,10 as apot ,
        sum(m12_misdf.apod),  0 as xar, 0 as ogxar, sum(m12_misdf.ikaer),  sum(m12_misdf.forol), sum(m12_misdf.fmy), sum(m12_misdf.fmy) as fpa, '' as ypm, sum(m12_misdf.meres)
FROM m12_misdf
INNER JOIN m12_pro on m12_pro.id = m12_misdf.pro_id
INNER JOIN m12_fpr on m12_fpr.id = m12_pro.fpr_id
INNER JOIN m12_mis on m12_mis.id = m12_misdf.mis_id
WHERE m12_mis.xrisi_id='%s'
GROUP BY  m12_mis.xrisi_id, m12_fpr.afm
ORDER BY  m12_mis.xrisi_id, m12_fpr.afm
'''

sqlergData1 = '''
SELECT  m12_mis.xrisi_id, m12_fpr.afm, m12_fpr.epon, m12_fpr.onom,m12_fpr.patr,m12_fpr.amka,0 as paidia,10 as apot ,
        sum( case when mtyp_id=200 then val end) as apod,  
        sum( case when mtyp_id=500 then val end) as ikaEno,
        sum( case when mtyp_id=599 then val end) as forol, 
        sum( case when mtyp_id=600 then val end) as fmy, 
        sum( case when mtyp_id=600 then val end) as fpa, 
    sum( case when mtyp_id=610 then val end) as eea, 
        m12_eid.eidp
FROM m12_misd
INNER JOIN m12_pro on m12_pro.id = m12_misd.pro_id
INNER JOIN m12_fpr on m12_fpr.id = m12_pro.fpr_id
INNER JOIN m12_mis on m12_mis.id = m12_misd.mis_id
INNER JOIN m12_eid on m12_eid.id = m12_pro.eid_id
WHERE m12_mis.xrisi_id='%s'
GROUP BY  m12_mis.xrisi_id, m12_fpr.afm
ORDER BY  m12_mis.xrisi_id, m12_fpr.afm
'''

def fmyEtoys(etos,rundate,db):
    from utils import dbutils as dbu
    from utils.tedutils import dec as d
    xrisiId = dbu.getDbSingleVal("SELECT id from m12_xrisi WHERE xrisi='%s'" % etos, db)
    cd = dbu.getDbOneRow("SELECT cop,ono,pat,cotyp,afm,dra,pol,odo,num,tk FROM m12_co INNER JOIN m12_cotyp ON m12_cotyp.id=m12_co.cotyp_id",db) #Company Data
    co = {
           'eponymia':u'%s %s' % (cd[0],cd[1]),
           'AFM':u'%s' % cd[4],
           'Antikeimeno':u'%s' % cd[5],
           'Adress':u'%s %s %s %s' % (cd[6],cd[7],cd[8],cd[9]),
           'Tel':u''
        }
    ed = dbu.getDbRows(sqlergData1 % xrisiId, db) # Ergazomenoi Data
    l0, l1, l2 , l3 = lfmy()
    doc = td.egrDoc([l0,l1,l2,l3])
    doc.addLine(0, ['','',etos+'1231',etos,''])
    doc.addLine(1, ['',etos,cd[0],cd[1],cd[2],cd[3],cd[4],cd[5],cd[6],cd[7],cd[8],cd[9],''])
    doc.addLine(2,[u'',u'',u'',u'',u'',u'',u'',u''])
    vls = []
    for l in ed:
        fpa = d(l[11]/0.985)
        doc.addLine(3,['',l[1],'',l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10],fpa,l[11],l[13],''])
        vl = {
               'Apo':u'1/1/%s' % etos,
               'Eos':u'31/12/%s' % etos,
               'Onomatep':u'%s %s' % (l[3],l[2]),
               'Patronymo':u'%s' % l[4],
               'AdrErg':u'%s, %s %s, %s' % (l[5],l[6],l[7],l[8]),
               'TelErg':u'',
               'Eid':u'%s'% l[14],
               'AFMErg':u'%s' % l[1],
               'Doy':u'',
               'At':u'',
               'ApodType':u'Μισθοί',
               'AkApod':u'%s'% gr0(l[8]),
               'Kratiseis':u'%s'% gr0(l[9]),
               'SynoloKrat':u'%s'% gr0(l[9]),
               'Katharo':u'%s' % gr0(l[10]),
               'Analogei':u'%s' % gr0(fpa),
               'Parakrat':u'%s' % gr0(l[11]),
               'Hmnia':u'%s' % rundate,
               'eea' :u'%s' % gr0(l[13]) 
               }
        vls.append(vl)
    return doc.__str__(),co,vls

def tst():
    l0, l1, l2 , l3 = lfmy()
    doc = td.egrDoc([l0,l1,l2,l3])
    doc.addLine(0,['','','20120101','2011',''])
    doc.addLine(1,[u'',u'2011',u'Λάζαρος',u'Θεόδωρος',u'Κων',u'0',u'046949583',
                    u'Εισαγωγές',u'Αθήνα',u'Κεδρηνού',u'66',u'13343',u''])
    doc.addLine(2,[u'',u'',u'',u'',u'',u'',u'',u'',u'',u'',u''])
    doc.addLine(3,[u'',u'046949583',u'',u'Μαυράκης',u'Νικόλαος',u'Κων',u'Αθήνα',
                    u'Ανάφης',u'4',u'14287',u'10',u'830.15',u'',u'',u'100',u'730.15',u'',u'',u'',u'',u'',u'',u''])
    doc.addLine(3,[u'',u'079774863',u'',u'Μαραβέλιας',u'ΣΠύρος',u'Κων',u'Αθήνα',
                    u'Ανάφης',u'4',u'14287',u'10',u'1526.44',u'',u'',u'334.28',u'1192.16',u'',u'',u'',u'',u'',u'',u''])
    return doc.__str__()

if __name__ == '__main__':
    print fmyEtoys('2012','2012-01-01','mis.sql3')