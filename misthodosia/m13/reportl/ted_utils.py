# -*- coding: utf-8 -*-
'''
Created on Nov 22, 2011

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

def makeDecimalFromString(strNumber):
    g = "".join(strNumber.split())
    return dec(g.replace(",","."))

def runSQL(sqlArr,db):
    con = sqlite3.connect(db) 
    cur = con.cursor()
    for sql in sqlArr:
        cur.execute(sql)
    con.commit()
    cur.close()
    con.close()
    
def parFor2011(poson,paidia=0,per=14,ekptosi=1.5):
    poso =dec(poson * per)
    def ekptosiPaidia(paidia=0):
        if   paidia == 0 : return dec(0)
        elif paidia == 1 : return dec(2000)
        elif paidia == 2 : return dec(4000)
        elif paidia == 3 : return dec(12500)
        elif paidia > 3  : return dec(12500 + ((paidia-3)*2500))
        else             : return dec(0)
    oria = [8000,4000,4000,6000,4000,6000,8000,20000,40000]
    synt = [0,10,18,24,26,32,36,38,40,45]
    ekpPaidia = ekptosiPaidia(paidia)
    for i in range(len(oria)):
        if i == 0:
            oria[0] += ekpPaidia
        else:    
            if ekpPaidia - dec(oria[i]) > 0:
                ekpPaidia = ekpPaidia - dec(oria[i])
                oria[i] = dec(0)
            else:
                oria[i] = dec(oria[i])-ekpPaidia
                ekpPaidia = dec(0)
    foros = dec(0)
    for i in range(len(oria)):
        if dec(poso) - oria[i] > 0 :
            foros = foros + dec(oria[i] * dec(synt[i]) / dec(100)) 
            poso = dec(poso) - oria[i]
        else:
            foros = foros + dec(dec(poso) * dec(synt[i]) / dec(100))
            poso = dec(0)
    if poso > 0:
        foros = foros + dec(dec(poso) * dec(synt[len(oria)]) / dec(100))
        poso = dec(0)
    par = dec(foros * dec(ekptosi) / dec(100))
    forosPar = dec(foros - par)
    forosPeriodoy = dec(foros / dec(per))
    forosPeriodoyPar = dec(forosPar / dec(per))
    return forosPeriodoy,forosPeriodoyPar

class ika_kpk():
    def __init__(self,kpkp,pTotal,pErgazomenos):
        self.kpk_p        = kpkp
        self.p            = dec(pTotal)
        self.pergazomenos = dec(pErgazomenos)
        self.pergodotis   = self.p - self.pergazomenos
        
def ika_kpkFactory(kode):
    if   kode == '101': return ika_kpk('101.ΙΚΑ ΜΙΚΤΑ ΤΕΑΜ',45.06,16.5)
    elif kode == '105': return ika_kpk('105.ΙΚΑ ΜΙΚΤΑ ΒΑΡΕΑ',50.66,19.95)
    else              : return ika_kpk('Xωρίς ΙΚΑ',0,0)         
def mis_test_Data():
    par = {'xrisi':'2004','per':'01','erg':'Lazaros','ergasimes':15,'kanAdeia':10,'YperoriesOres':5}
    return par
       
def calcMisImeromisthio(meres,imeromisthio,ika_kpk='101',onomatep ='',paidia=0):
    e = {}  #Ta dedomena
    p = {}  #H perigrafi tis diadikasias
    
    ika = ika_kpkFactory(ika_kpk)

    e['ono']       = '%s' % onomatep
    p['ono']       = 'Ονοματεπώνυμο : %s' % e['ono']
    
    e['imsthio']   = dec(imeromisthio)
    p['imsthio']   = 'Ημερομίσθιο = %s' % e['imsthio']
    
    e['meres']     = dec(meres,0)
    p['meres']     = 'Ημέρες εργασίας = %s' % e['meres']
    
    e['kpk']       = ika.kpk_p
    p['kpk']       = 'Κωδικός πακέτου κάλυψης ΙΚΑ : %s' % e['kpk']
    
    e['pikaEnos']  = ika.pergazomenos
    p['pikaEnos']  = 'Ποσοστό ΙΚΑ εργαζομένου = %s' % e['pikaEnos']
    
    e['pikaTotal'] = ika.p
    p['pikaTotal'] = 'Συνολικό ποσοστό ΙΚΑ = %s' % e['pikaTotal']
    
    e['apodoxes']  = dec(e['imsthio'] * e['meres'])
    p['apodoxes']  = 'Αποδοχές περιόδου : Ημερομίσθιο (%s) Χ Ημέρες (%s) = %s' % (e['imsthio'],e['meres'],e['apodoxes'])
    
    e['ikaEnos']   = dec(e['apodoxes'] * e['pikaEnos']/dec(100))
    p['ikaEnos']   = 'Κρατήσεις IΚΑ εργαζομένου : Αποδοχές περιόδου (%s) Χ ποσοστό ΙΚΑ εργαζομένου (%s%%) = %s' % (e['apodoxes'],e['pikaEnos'],e['ikaEnos']) 
    
    e['ikaTotal']  = dec(e['apodoxes'] * e['pikaTotal']/dec(100))
    p['ikaTotal']  = 'Κρατήσεις ΙΚΑ : Αποδοχές περιόδου (%s) Χ ποσοστό ΙΚΑ (%s%%) = %s' % (e['apodoxes'],e['pikaTotal'],e['ikaTotal'])
    
    e['ikaEtis']   = e['ikaTotal'] - e['ikaEnos']
    p['ikaEtis']   = 'Κρατήσεις ΙΚΑ εργοδότη : ΙΚΑ συνολικά (%s) - ΙΚΑ εργαζομένου (%s) = %s' % (e['ikaTotal'],e['ikaEnos'],e['ikaEtis']) 
    
    e['giaforo']   = e['apodoxes']- e['ikaEnos']
    p['giaforo']   = 'Φορολογητέο περιόδου : Αποδοχές περιόδου (%s) - ΙΚΑ εργαζομένου (%s) = %s' % (e['apodoxes'],e['ikaEnos'],e['giaforo'])
    
    e['forosAn'],e['foros'] = parFor2011(e['giaforo'])
    p['forosAn'] = 'Φόρος που αναλογεί : Φορολογητέο (%s) σε κλίμακα = %s' % (e['giaforo'],e['forosAn'])
    p['foros']   = 'Φόρος που παρακρατήθηκε : Φόρος που αναλογεί (%s) - έκπτωση 1,5%% = %s' % (e['forosAn'],e['foros'])
        
    e['krEnos'] = e['ikaEnos'] + e['foros']
    p['krEnos'] = 'Κρατήσεις εργαζομένου : ΙΚΑ εργαζομένου (%s) + φόρος (%s) = %s' % (e['ikaEnos'],e['foros'],e['krEnos'])
    
    e['pliroteo'] = e['apodoxes'] - e['krEnos']
    p['pliroteo'] = 'Πληρωτέο : Μικτές αποδοχές (%s) - κρατήσεις εργαζομένου (%s) = %s' % (e['apodoxes'],e['krEnos'],e['pliroteo'])
        
    e['krEti'] = e['ikaEtis']
    p['krEti'] = 'Κρατήσεις εργοδότη : ΙΚΑ εργοδότη (%s) + = %s' %(e['ikaEtis'],e['krEti'])
    
    e['krTotal'] = e['krEnos'] + e['krEti']
    p['krTotal'] = 'Κρατήσεις Συνολικά : Κρατήσεις εργαζόμενου(%s) + κρατήσεις εργοδότη (%s) = %s' %(e['krEnos'],e['krEti'],e['krTotal'])

    e['kostos'] = e['apodoxes'] + e['krEti']
    p['kostos'] = 'Συνολικό κόστος μισθοδοσίας : Αποδοχές περιόδου (%s) + κρατήσεις εργοδότη (%s) = %s' % (e['apodoxes'],e['krEti'],e['kostos'])
    
    e['pm']    = dec(e['pliroteo']/e['kostos'] * dec(100),0)
    p['pm']    = 'Ποσοστό Πληρωτέου / Συνολικό κόστος' 
    
    e['pkr']    = dec(e['krTotal']/e['kostos'] * dec(100),0)
    p['pkr']    = 'Ποσοστό Κρατήσεων / Συνολικό κόστος'
    
    return e,p

def test(meres,imeromisthio,kpk,onoma):
    ar = ['ono','imsthio','meres','apodoxes','kpk','pikaEnos','pikaTotal','ikaEnos','ikaEtis','ikaTotal','giaforo','forosAn','foros','krEnos','krEti','kostos','pliroteo']
    a = calcMisImeromisthio(meres,imeromisthio,kpk,onoma)
    for k in ar:
        print a[1][k]
    print '-' * 80
    
def test2(meres,imeromisthio,kpk,onoma):
    sqlCreate = "CREATE TABLE IF NOT EXISTS mis (id INTEGER PRIMARY KEY NOT NULL,xrisi text, per text,erg text, type text, val text, per text);"
    sqlInsert = "INSERT INTO mis(xrisi,period,erg,type,val,per) VALUES ('%s','%s','%s','%s','%s','%s');\n"
    ar = ['ono','imsthio','meres','apodoxes','ikaEnos','ikaEtis','ikaTotal','pliroteo','krEnos','krEti','krTotal','kostos','pm','pkr']
    a = calcMisImeromisthio(meres,imeromisthio,kpk,onoma)
    sql = []
    for k in ar:
        sql.append(sqlInsert % ('2011','01',a[0]['ono'],k,a[0][k],a[1][k]))
    runSQL(sql,'tst.sql3')
    for k in ar:
        s = '%10s' % a[0][k]
        print s.replace('.',',') ,
    print ''
if __name__ == '__main__':
    test2(4,40,  '101','Δουζίνας Δημήτρης   ')
    test2(4,50,  '105','Καβατζικλής Γεώργιος')
    test2(4,40,  '105','Γκάτζιας Άγγελος    ')
    test2(4,105, '105','Βουδούρη Παγώνα     ')
    test2(4,105, '105','Παρδαλάκης Νίκος    ')
    test2(4,54.6,'105','Μαλισιώβας Κων/νος  ')
    test2(4,54.6,'105','Πλουμπής Μελέτιος   ')
    test2(1,54.6,'105','Κλιματζάς Κων/νος   ')
    test2(4,40,  '101','Καλογήρου Ευγενία   ')
    test2(4,40,  '101','Καρπέτας Βασίλειος  ')