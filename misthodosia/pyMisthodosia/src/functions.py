#!/usr/bin/env python
#coding=utf-8

'''
Created on 20 Μαϊ 2011

@author: tedlaz
'''
import decimal
import sqlite3

def isNum(value): # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters : 
            1.value : the value to check against.
        output: True or False
    """
    if not value:
        return False
    try: float(value)
    except ValueError: return False
    else: return True
    
def dec(poso , dekadika=2 ):
    """ 
    use : Given a number, it returns a decimal with a specific number of decimal digits
    input Parameters:
          1.poso     : The number for conversion in any format (e.g. string or int ..)
          2.dekadika : The number of decimals (default 2)
    output: A decimal number     
    """
    PLACES = decimal.Decimal(10) ** (-1 * dekadika)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)

def runSQL(sqlArr,db):
    con = sqlite3.connect(db) 
    cur = con.cursor()
    for sql in sqlArr:
        cur.execute(sql)
    con.commit()
    cur.close()
    con.close()
    
def createDB(db='tst.db'):
    sqAr = []
    sqAr.append("create table if not exists mis_xrisi(id INTEGER PRIMARY KEY NOT NULL, xrisi_p TEXT,closed INTEGER NOT NULL)")
    sqAr.append("create table if not exists mis_wper(id INTEGER PRIMARY KEY NOT NULL, wper_p TEXT)")
    sqAr.append("create table if not exists mis_wperm(id INTEGER PRIMARY KEY NOT NULL, wperm_p TEXT)")
    sqAr.append("create table if not exists mis_kpk(id INTEGER PRIMARY KEY NOT NULL,\
                 kpk_p TEXT, perg DECIMAL NOT NULL, petis DECIMAL NOT NULL, ptotal DECIMAL NOT NULL)")
    sqAr.append("create table if not exists mis_werg(id INTEGER PRIMARY KEY NOT NULL, werg_p TEXT)")
    sqAr.append("create table if not exists mis_eid(id INTEGER PRIMARY KEY NOT NULL,\
                 eid_p TEXT, kpk_id INTEGER NOT NULL,werg_id INTEGER NOT NULL)")  
    sqAr.append("create table if not exists mis_erg(id INTEGER PRIMARY KEY NOT NULL,\
                 epo TEXT, ono TEXT, pat TEXT, mit TEXT, eid_id INTEGER NOT NULL)")
    sqAr.append("create table if not exists mis_erg_ika(id INTEGER PRIMARY KEY NOT NULL,\
                 am_ika TEXT, amka TEXT, gennisi TEXT)")
    sqAr.append("create table if not exists mis_erg_doy(id INTEGER PRIMARY KEY NOT NULL,\
                 afm TEXT, eggamos TEXT, paidia TEXT, ar_taftotitas TEXT)")        
    sqAr.append("create table if not exists mis_wpar(id INTEGER PRIMARY KEY NOT NULL, wpar_p TEXT)")
    sqAr.append("create table if not exists mis_par1(id INTEGER PRIMARY KEY NOT NULL,\
                xrisi_id INTEGER NOT NULL, wper_id INTEGER NOT NULL, sxolia TEXT, closed INTEGER NOT NULL)")
    sqAr.append("create table if not exists mis_par2(id INTEGER PRIMARY KEY NOT NULL,\
                par1_id INTEGER NOT NULL, erg_id INTEGER NOT NULL, sxolia TEXT, closed INTEGER NOT NULL)")    
    sqAr.append("create table if not exists mis_par3(id INTEGER PRIMARY KEY NOT NULL,\
                 par2_id INTEGER NOT NULL,\
                 wpar_id INTEGER NOT NULL, val DECIMAL NOT NULL)")
    sqAr.append("create table if not exists mis_wm(id INTEGER PRIMARY KEY NOT NULL, wm_p TEXT)")
    sqAr.append("create table if not exists mis_m1(id INTEGER PRIMARY KEY NOT NULL,\
                xrisi_id INTEGER NOT NULL, wperm_id INTEGER NOT NULL, sxolia TEXT, closed INTEGER NOT NULL)")
    sqAr.append("create table if not exists mis_m2(id INTEGER PRIMARY KEY NOT NULL,\
                m1_id INTEGER NOT NULL, erg_id INTEGER NOT NULL, sxolia TEXT, closed INTEGER NOT NULL)")    
    sqAr.append("create table if not exists mis_m3(id INTEGER PRIMARY KEY NOT NULL,\
                 m2_id INTEGER NOT NULL,\
                 wm_id INTEGER NOT NULL, val DECIMAL NOT NULL)")
    
    sqAr.append("CREATE UNIQUE INDEX i_eid_p on mis_eid (eid_p ASC)")
    sqAr.append("CREATE UNIQUE INDEX i_kpk_p on mis_kpk (kpk_p ASC)")
    sqAr.append("CREATE UNIQUE INDEX i_xr_per on mis_par1 (xrisi_id ASC, wper_id ASC)")
    sqAr.append("CREATE UNIQUE INDEX i_par1_erg on mis_par2 (par1_id ASC, erg_id ASC)")
    sqAr.append("CREATE UNIQUE INDEX i_par2_wpar on mis_par3 (par2_id ASC, wpar_id ASC)")
    sqAr.append("CREATE UNIQUE INDEX i_werg_p on mis_werg (werg_p ASC)")
    sqAr.append("CREATE UNIQUE INDEX i_wm_p on mis_wm (wm_p ASC)")
    sqAr.append("CREATE UNIQUE INDEX i_wpar_p on mis_wpar (wpar_p ASC)")
    sqAr.append("CREATE UNIQUE INDEX i_wper_p on mis_wper (wper_p ASC)")
    sqAr.append("CREATE UNIQUE INDEX i_wperm_p on mis_wperm (wperm_p ASC)")
    
    runSQL(sqAr,db)
    sqdata = []
    sqdata.append("INSERT INTO mis_xrisi VALUES(2010,'Χρήση 2010',0)")
    sqdata.append("INSERT INTO mis_wper VALUES(1,'Παρουσίες Ιανουαρίου')")
    sqdata.append("INSERT INTO mis_wper VALUES(2,'Παρουσίες Φεβρουαρίου')")
    sqdata.append("INSERT INTO mis_wper VALUES(3,'Παρουσίες Μαρτίου')")
    sqdata.append("INSERT INTO mis_wper VALUES(4,'Παρουσίες Απριλίου')")
    sqdata.append("INSERT INTO mis_wper VALUES(5,'Παρουσίες Μαϊου')")
    sqdata.append("INSERT INTO mis_wper VALUES(6,'Παρουσίες Ιουνίου')")
    sqdata.append("INSERT INTO mis_wper VALUES(7,'Παρουσίες Ιουλίου')")
    sqdata.append("INSERT INTO mis_wper VALUES(8,'Παρουσίες Αυγούστου')")
    sqdata.append("INSERT INTO mis_wper VALUES(9,'Παρουσίες Σεπτεμβρίου')")
    sqdata.append("INSERT INTO mis_wper VALUES(10,'Παρουσίες Οκτωβρίου')")
    sqdata.append("INSERT INTO mis_wper VALUES(11,'Παρουσίες Νοεμβρίου')")
    sqdata.append("INSERT INTO mis_wper VALUES(12,'Παρουσίες Δεκεμβρίου')")

    sqdata.append("INSERT INTO mis_wperm VALUES(1,'Μισθοδοσία Ιανουαρίου')")
    sqdata.append("INSERT INTO mis_wperm VALUES(2,'Μισθοδοσία Φεβρουαρίου')")
    sqdata.append("INSERT INTO mis_wperm VALUES(3,'Μισθοδοσία Μαρτίου')")
    sqdata.append("INSERT INTO mis_wperm VALUES(4,'Μισθοδοσία Απριλίου')")
    sqdata.append("INSERT INTO mis_wperm VALUES(5,'Μισθοδοσία Μαϊου')")
    sqdata.append("INSERT INTO mis_wperm VALUES(6,'Μισθοδοσία Ιουνίου')")
    sqdata.append("INSERT INTO mis_wperm VALUES(7,'Μισθοδοσία Ιουλίου')")
    sqdata.append("INSERT INTO mis_wperm VALUES(8,'Μισθοδοσία Αυγούστου')")
    sqdata.append("INSERT INTO mis_wperm VALUES(9,'Μισθοδοσία Σεπτεμβρίου')")
    sqdata.append("INSERT INTO mis_wperm VALUES(10,'Μισθοδοσία Οκτωβρίου')")
    sqdata.append("INSERT INTO mis_wperm VALUES(11,'Μισθοδοσία Νοεμβρίου')")
    sqdata.append("INSERT INTO mis_wperm VALUES(12,'Μισθοδοσία Δεκεμβρίου')")
    sqdata.append("INSERT INTO mis_wperm VALUES(13,'Μισθοδοσία Δώρου Πάσχα')")
    sqdata.append("INSERT INTO mis_wperm VALUES(14,'Μισθοδοσία Επιδόματος Αδείας')")
    sqdata.append("INSERT INTO mis_wperm VALUES(15,'Μισθοδοσία Δώρου Χριστουγέννων')")
    sqdata.append("INSERT INTO mis_wperm VALUES(16,'Μισθοδοσία Επιδόματος Ισολογισμού')")
    sqdata.append("INSERT INTO mis_wperm VALUES(17,'Μισθοδοσία Αποζημίωσης Απόλυσης')") 
       
    sqdata.append("INSERT INTO mis_kpk VALUES(101,'ΙΚΑ-ΤΕΑΜ Μικτά',16,28.06,44.06)")
    sqdata.append("INSERT INTO mis_kpk VALUES(105,'ΙΚΑ-ΤΕΑΜ Βαρέα',19.45,30.21,49.66)")
    
    sqdata.append("INSERT INTO mis_werg VALUES(1,'Μισθωτός')")
    sqdata.append("INSERT INTO mis_werg VALUES(2,'Ημερομίσθιος')")
    sqdata.append("INSERT INTO mis_werg VALUES(3,'Ωρομίσθιος')")
    
    sqdata.append("INSERT INTO mis_wpar VALUES(10,'Εργάσιμες μέρες')")
    sqdata.append("INSERT INTO mis_wpar VALUES(11,'Κανονική Άδεια μέρες')")
    sqdata.append("INSERT INTO mis_wpar VALUES(12,'Υπερωρίες ώρες')")
    
    sqdata.append("INSERT INTO mis_wm VALUES(1000,'Μισθός')")
    sqdata.append("INSERT INTO mis_wm VALUES(1010,'Ημερομίσθιο')")
    sqdata.append("INSERT INTO mis_wm VALUES(1020,'Ωρομίσθιο')")
    sqdata.append("INSERT INTO mis_wm VALUES(1030,'Ημέρες εργασίας')")
    sqdata.append("INSERT INTO mis_wm VALUES(1040,'Μικτές αποδοχές περιόδου')")
    sqdata.append("INSERT INTO mis_wm VALUES(1050,'ποσοστό ΙΚΑ')")
    sqdata.append("INSERT INTO mis_wm VALUES(1060,'ποσοστό ΙΚΑ εργαζομένου')")
    sqdata.append("INSERT INTO mis_wm VALUES(1070,'ποσοστό ΙΚΑ εργοδότη')")
    sqdata.append("INSERT INTO mis_wm VALUES(1080,'ΙΚΑ')")
    sqdata.append("INSERT INTO mis_wm VALUES(1090,'ΙΚΑ εργαζομένου')")
    sqdata.append("INSERT INTO mis_wm VALUES(1100,'ΙΚΑ εργοδότη')")
    sqdata.append("INSERT INTO mis_wm VALUES(1110,'Αποδοχές για φόρο')")
    sqdata.append("INSERT INTO mis_wm VALUES(1120,'Περίοδοι για υπολογισμό φόρου')")
    sqdata.append("INSERT INTO mis_wm VALUES(1130,'Φόρος που αναλογεί')")
    sqdata.append("INSERT INTO mis_wm VALUES(1140,'Φόρος που παρακρατήθηκε')")
    sqdata.append("INSERT INTO mis_wm VALUES(1150,'Φόρος περιόδου που αναλογεί')")
    sqdata.append("INSERT INTO mis_wm VALUES(1160,'Φόρος περιόδου που παρακρατήθηκε')")
    sqdata.append("INSERT INTO mis_wm VALUES(1170,'Πληρωτέες αποδοχές')")
    sqdata.append("INSERT INTO mis_wm VALUES(1180,'Συνολικό κόστος')")
    
    runSQL(sqdata,db)
    sqtest = []
    sqtest.append("INSERT INTO MIS_eid(eid_p,kpk_id,werg_id) VALUES('Λογιστής',101,1)")
    sqtest.append("INSERT INTO MIS_eid(eid_p,kpk_id,werg_id) VALUES('Καθαριότητα',105,2)")
    
    sqtest.append("INSERT INTO mis_erg(epo,ono,pat,mit,eid_id)VALUES('Λάζαρος','Θεόδωρος','Κων/νος','Σταυρούλα',1)")
    sqtest.append("INSERT INTO mis_erg(epo,ono,pat,mit,eid_id)VALUES('Δαζέα','Πόπη','Νικόλαος','Μαρία',2)")
    
    sqtest.append("INSERT INTO mis_par1 VALUES(1,2010,1,'Δοκιμαστική',0)")
    sqtest.append("INSERT INTO mis_par2 VALUES(1,1,1,'Λάζαρος',0)")
    sqtest.append("INSERT INTO mis_par2 VALUES(2,1,2,'πόπη',0)")
    sqtest.append("INSERT INTO mis_par3 VALUES(1,1,10,20)")
    sqtest.append("INSERT INTO mis_par3 VALUES(2,1,11,5)")
    sqtest.append("INSERT INTO mis_par3 VALUES(3,2,10,25)")
    runSQL(sqtest,db)
    print 'DataBase Created or Updated'
    
def calcMinesApozimiosis(etif):
    eti = int(etif)
    if   eti < 1:
        if etif < 2.0 /12 :
            return 0
        else :
            return 1
    elif eti == 1: return 2
    elif eti == 2: return 2
    elif eti == 3: return 2
    elif eti == 4: return 3
    elif eti == 5: return 3
    elif eti == 6: return 4
    elif eti == 7: return 4
    elif eti == 8: return 5
    elif eti == 9: return 5
    elif eti ==10: return 6
    elif eti ==11: return 7
    elif eti ==12: return 8
    elif eti ==13: return 9
    elif eti ==14: return 10
    elif eti ==15: return 11
    elif eti ==16: return 12
    elif eti ==17: return 13
    elif eti ==18: return 14
    elif eti ==19: return 15
    elif eti ==20: return 16
    elif eti ==21: return 17
    elif eti ==22: return 18
    elif eti ==23: return 19
    elif eti ==24: return 20
    elif eti ==25: return 21
    elif eti ==26: return 22
    elif eti ==27: return 23
    elif eti > 28: return 24
    else         : return 0
def calcFMY2011(poso,paidia=0):
    klimakas = [12000,4000,6000,4000,6000,8000,20000,40000]
    pforoy  = [0,18,24,26,32,36,38,40,45]
    ekptosiPaidion = dec(0)
    
    #Calculate children discount
    if   paidia == 0 : ekptosiPaidion = dec(0)
    elif paidia == 1 : ekptosiPaidion = dec(1500)
    elif paidia == 2 : ekptosiPaidion = dec(3000)
    elif paidia == 3 : ekptosiPaidion = dec(11500)
    elif paidia  > 3 :
        ekptosiPaidion = dec(11500) + dec((paidia-3)* dec(2000))
    else:
        ekptosiPaidion = dec(0)
    klimaka = []
    klimaka.append(klimakas[0]+ekptosiPaidion)
    
    for i in range(len(klimakas)-1):
        if ekptosiPaidion <= klimakas[i+1]:
            klimaka.append(klimakas[i+1]-ekptosiPaidion)
            ekptosiPaidia = dec(0)
        else:
            klimaka.append(0)
            ekptosiPaidia = ekptosiPaidia - klimakas[i+1]
    tmpApodoxes = dec(poso)
    tmpForosPoyAnalogei = dec(0)
    for i in range(len(klimaka)):
        if tmpApodoxes == dec(0):
            pass
        elif tmpApodoxes <= dec(klimaka[i]):
            tmpForosPoyAnalogei += dec(tmpApodoxes * pforoy[i] / dec(100))
            tmpApodoxes = dec(0)
        else:
            tmpForosPoyAnalogei += dec(klimaka[i] * pforoy[i] / dec(100))
            tmpApodoxes = tmpApodoxes - klimaka[i]
    if tmpApodoxes <> dec(0):
        tmpForosPoyAnalogei += dec(tmpApodoxes * pforoy[i+1] / dec(100))
    forosPoyParakratithike = tmpForosPoyAnalogei - dec(dec(1.5) * tmpForosPoyAnalogei/ dec(100))
    return tmpForosPoyAnalogei, forosPoyParakratithike

class parakratisiForou():
    def __init__(self,apodoxesPeriodoy, paidia=0, periodoi=1, extraApodoxes = 0, etos=2011):
        self.apodoxes = dec(apodoxesPeriodoy * periodoi + extraApodoxes)
        self.apodoxesPeriodoy = dec(apodoxesPeriodoy)
        self.forologiteoPeriodoy = self.apodoxesPeriodoy+dec(extraApodoxes)
        self.paidia   = paidia
        self.periodoi = periodoi
        if etos == 2011:
            a1, p1 = calcFMY2011(self.apodoxes,self.paidia)
            a2, p2 = calcFMY2011(self.apodoxesPeriodoy*periodoi,self.paidia)
        else:
            a1=p1=a2=p2=dec(0)
        da = a1 - a2
        dp = p1 - p2
        self.forosPoyAnalogei, self.forosPoyParakratithike  = a1 , p1
        self.forosPeriodoy = dec(self.forosPoyAnalogei / periodoi) + da
        self.forosPeriodoyParakratitheis = dec(self.forosPoyParakratithike/periodoi) + dp

    def __str__(self):
        tstr  = ''
        #tstr += 'Φορολογητέο περιόδου        : %s\n' % self.forologiteoPeriodoy
        tstr += 'Περιόδοι          : %s\n' % self.periodoi
        tstr += 'Φορολογητέο χρήσης: %s \n' % self.apodoxes
        tstr += 'Φόρος που αναλογεί: %s\n' % self.forosPoyAnalogei
        tstr += 'Φόρος που παρ/θηκε: %s\n' % self.forosPoyParakratithike
        tstr += 'Φόρος περιόδου που αναλογεί : %s\n' % self.forosPeriodoy
        tstr += 'Φόρος περιόδου που παρ/θηκε : %s\n' % self.forosPeriodoyParakratitheis
        return  tstr
def calForosApozimiosisApolysis(apozimiosi, syntelestisForou = 0.2):
    if   apozimiosi <= 20000 : return dec(0)
    elif apozimiosi > 20000  : return dec((apozimiosi-20000)*dec(syntelestisForou))
    else                     : return dec(0) 
                    
class calcApozimiosiApolysis():
    def __init__(self,misthos,eti):
        self.misthos            = dec(misthos)
        self.eti                = eti
        self.miniaiaApozimiosi  = dec(misthos * 14.0 / 12.0)
        self.mines              = dec(calcMinesApozimiosis(eti))
        self.apozimiosi         = dec(self.miniaiaApozimiosi * self.mines)
        self.foros              = calForosApozimiosisApolysis(self.apozimiosi)
        self.pliroteaApozimiosi = self.apozimiosi - self.foros
        
    def __str__(self):
        tstr  = 'Υπολογισμός αποζημίωσης απόλυσης \n'
        tstr += '-------------------------------- \n'
        tstr += 'Μικτές αποδοχές %s  Χ 14 / 12 = %s Μηνιαία αποζημίωση\n' % (self.misthos, self.miniaiaApozimiosi)
        tstr += 'Μηνιαία αποζημίωση %s Χ %s μήνες = %s Αποζημίωση απόλυσης\n' % (self.miniaiaApozimiosi,self.mines,self.apozimiosi)
        tstr += 'Φόρος που αναλογεί : %s\n' % self.foros
        tstr += 'Αποζημίωση %s - φόρος %s = %s Πληρωτέο\n' % (self.apozimiosi,self.foros,self.pliroteaApozimiosi)
        return tstr
    
class erg():
    '''select mis_erg.id, epo, ono, eid_p , kpk_p, perg, petis,ptotal
    from mis_erg
    inner join mis_eid on mis_erg.eid_id=mis_eid.id
    inner join mis_kpk on mis_eid.kpk_id = mis_kpk.id'''
    def __init__(self,code,poson=0,meres=0, misthotos=0, ika=100):
        poika = {101:[dec(44.06),dec(16)],
                 105:[dec(49.66),dec(19.45)],
                 100:[dec(0),dec(0)]}
        self.code = code
        self.imeres = meres
        self.isMisthotos = misthotos
        if misthotos == 0:
            self.misthos = dec(0) 
            self.imeromisthio = dec(poson)
            self.oromisthio = dec(self.imeromisthio * 6 / 40)
        elif misthotos == 1:
            self.misthos = dec(poson)
            self.imeromisthio = dec(self.misthos / 25)
            self.oromisthio = dec(self.misthos/25 * 6 / 40)
        else:
            self.misthos = dec(0)
            self.imeromisthio = dec(0)
            self.oromisthio = dec(0)
        self.imeresDef = 25
        self.pika, self.pikaenos = poika[ika]
        self.paidia = 0
        
class calcMisthodosiaMina():
    def __init__(self,ergData):
        self.forDb = []
        self.erg       = ergData
        self.misthos   = ergData.misthos
        self.imeresDef = ergData.imeresDef
        self.imeres    = ergData.imeres
        if ergData.isMisthotos == 0:
            self.apodoxes  = dec(ergData.imeromisthio * self.imeres)
        elif ergData.isMisthotos == 1:
            self.apodoxes = dec(ergData.misthos * self.imeres / 25)
        else:
            self.apodoxes = dec(0)
        self.ika       = dec(ergData.pika * self.apodoxes / dec(100))
        self.ikaenos   = dec(ergData.pikaenos * self.apodoxes / dec(100))
        self.ikaetis   = self.ika - self.ikaenos
        self.giaforo   = self.apodoxes - self.ikaenos 
        self.parForou  = parakratisiForou(self.giaforo,ergData.paidia,14,0)
        self.katharo   = self.giaforo - self.parForou.forosPeriodoyParakratitheis
        self.kostos1   = self.apodoxes + self.ikaetis
        self.kostos2   = self.katharo + self.parForou.forosPeriodoyParakratitheis + self.ika  
    def toDB(self):
        sql2 = "INSERT INTO mis_m2(m1_id,erg_id,closed) VALUES(%s,%s,%s)" % (1,1,1)
        sql3 = "INSERT INTO mis_m3(m2_id,wm_id,val) VALUES(%s,%s,%s)"
        sql  = []
        sql.append(sql3 % (1,1000,self.misthos))
        sql.append(sql3 % (1,1010,self.erg.imeromisthio))
        sql.append(sql3 % (1,1020,self.erg.oromisthio))
        sql.append(sql3 % (1,1030,self.imeres))
        sql.append(sql3 % (1,1040,self.apodoxes))
        sql.append(sql3 % (1,1090,self.ikaenos))
        sql.append(sql3 % (1,1100,self.ikaetis))
        sql.append(sql3 % (1,1080,self.ika))
        sql.append(sql3 % (1,1110,self.giaforo))
        sql.append(sql3 % (1,1160,self.parForou.forosPeriodoyParakratitheis))
        sql.append(sql3 % (1,1170,self.katharo))
        sql.append(sql3 % (1,1180,self.kostos1))
        runSQL(sql,'tst.db')     
    def __str__(self):
        str  = '==========================================================\n'
        str += '   Μισθοδοσία εργαζομένου : %s\n'% self.erg.code
        str += 'Μισθός            : %s       \n' % self.misthos
        str += 'Ημερομίσθιο       : %s       \n' % self.erg.imeromisthio
        str += 'Ωρομίσθιο         : %s       \n' % self.erg.oromisthio
        str += 'Ημέρες            : %s       \n' % self.imeres
        str += 'Αποδοχές περιόδου : %s       \n' % self.apodoxes
        str += 'Ικα εργαζομένου   : %s       \n' % self.ikaenos
        str += 'Ικα εργοδότη      : %s       \n' % self.ikaetis
        str += 'Ικα Συνολικά      : %s       \n' % self.ika
        str += 'Φορολογητέο       : %s       \n' % self.giaforo
        str += self.parForou.__str__()
        str += 'Πληρωτέο          : %s       \n' % self.katharo
        str += 'Κόστος 1          : %s       \n' % self.kostos1
        str += 'Κόστος 2          : %s       \n' % self.kostos2
        return str
'''
select  xrisi_id, wper_p,epo,ono,eid_p,werg_p,wpar_p, kpk_p,perg,petis,ptotal,val
from mis_par3
inner join mis_wpar on wpar_id = mis_wpar.id 
inner join  mis_par2 on par2_id = mis_par2.id
inner join mis_par1 on  mis_par2.par1_id = mis_par1.id
inner join mis_wper on mis_par1.wper_id = mis_wper.id
inner join mis_erg on mis_par2.erg_id = mis_erg.id
inner join mis_eid on mis_erg.eid_id = mis_eid.id
inner join mis_werg on mis_eid.werg_id =mis_werg.id
inner join mis_kpk on mis_eid.kpk_id=mis_kpk.id
'''    
'''
select  m2_id , wm_p,val
from mis_m3
inner join mis_wm on wm_id=mis_wm.id
'''    
if __name__ == '__main__':
    #ap = calcApozimiosiApolysis(2700,0.17)
    #print ap
    #pf = parakratisiForou(1850,0,14,0)
    #print pf
    #createDB()
    enoi = [erg('nona',90,6,0,105),erg('gki',54.6,6,0,101),erg('ted',1350.47,25,1,101)]
    for er in enoi:
        calcMisthodosiaMina(er).toDB()
    