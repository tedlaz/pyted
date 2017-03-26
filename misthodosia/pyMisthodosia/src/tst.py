#!/usr/bin/env python
#coding=utf-8

'''
Created on 06 Ιουν 2011

@author: tedlaz
'''
import functions as f
import decimal as decim
from datetime import datetime, date, time

class d():
    def __init__(self,val=0, txt='',desc='',decimals=4):
        self.decimals = decimals
        self.val = f.dec(val,self.decimals)
        self.txt = txt
        self.desc= desc
        
    def d(self,txt):
        self.txt=txt
    def __add__(self,x):
        if isinstance(x,int):
            return d(self.val+x,'','%s<%s> + %s' % (self.txt,self.val,x ))
        elif isinstance(x,decim.Decimal):
            return d(self.val+x,'','%s<%s> + %s' % (self.txt,self.val,x ))
        elif isinstance(x,d):
            return d(self.val+x.val,'','%s<%s> + %s<%s>' %(self.txt,self.val,x.txt,x.val))
        else:
            return d(0,'Error')
    def __sub__(self,x):
        if isinstance(x,int):
            return d(self.val-x,'','%s<%s> - %s' % (self.txt,self.val,x ))
        elif isinstance(x,decim.Decimal):
            return d(self.val-x,'','%s<%s> - %s' % (self.txt,self.val,x ))
        elif isinstance(x,d):
            return d(self.val-x.val,'','%s<%s> - %s<%s>' %(self.txt,self.val,x.txt,x.val))
        else:
            return d(0,'Error')
    def __mul__(self,x):
        if isinstance(x,int):
            return d(f.dec(self.val*f.dec(x),4),'','%s<%s> X %s' % (self.txt,self.val,x ))
        elif isinstance(x,decim.Decimal):
            return d(f.dec(self.val*f.dec(x),4),'','%s<%s> X %s' % (self.txt,self.val,x ))
        elif isinstance(x,d):
            return d(f.dec(self.val*x.val,4),'','%s<%s> X %s<%s>' %(self.txt,self.val,x.txt,x.val))
        else:
            return d(0,'Error')
    def __div__(self,x):
        if isinstance(x,int):
            return d(f.dec(self.val/f.dec(x),4),'','%s<%s> / %s' % (self.txt,self.val,x ))
        elif isinstance(x,decim.Decimal):
            return d(f.dec(self.val/f.dec(x),4),'','%s<%s> / %s' % (self.txt,self.val,x ))
        elif isinstance(x,d):
            return d(f.dec(self.val/x.val,4),'','%s<%s> / %s<%s>' %(self.txt,self.val,x.txt,x.val))
        else:
            return d(0,'Error')
    def __str__(self):
        if len(self.desc.strip()) == 0:
            return '%s = %s '% (self.txt,self.val)
        else:
            return '%s = %s (%s)'% (self.txt,self.val,self.desc)

def calcMisNormal(misth,misths,mer,brad=0,kyrMer=0,kyrOr=0,yp=0,ypBrad=0,ypKy=0):
    code = d(901,'Τακτικές αποδοχές')
    misthos =d(misth,'Μισθός') ; print misthos
    misthoss = d(misths,'Συμβατικός μισθός') ; print misthoss
    imergasias = d(mer,'Ημέρες εργασίας') ; print imergasias
    brady = d(brad,'Ώρες για Βραδυνή προσαύξηση') ; print brady
    kyriakiMeres = d(kyrMer,'Μέρες Κυριακές-Αργίες για προσαύξηση') ; print kyriakiMeres
    kyriakiOres = d(kyrOr,'ώρες για προσαύξηση Κυριακών-Αργιών') ; print kyriakiOres
    yperories = d(yp,'Υπερωρίες') ; print yperories
    ypBrady = d(ypBrad,'Υπερωρίες για βραδυνή προσαύξηση') ; print ypBrady
    ypKyr = d(ypKy,'Υπερωρίες για προσαύξηση Κυριακών-Αργιών') ; print ypKyr  
    meresSymbasisMina =d(25,'Ημέρες εργασίας ανά μήνα') ; print meresSymbasisMina
    meresIKABdomada =d(6,'Ημέρες εργασίας (ΙΚΑ) ανά βδομάδα') ; print meresIKABdomada
    meresSymbasiBdomada =d(5,'Ημέρες εργασίας πραγματικές ανά βδομάδα') ; print meresSymbasiBdomada
    oresSymbasiBdomada = d(40,'Ώρες εργασίας ανά βδομάδα') ; print oresSymbasiBdomada
    posostoNyxta = d(.25,'Ποσοστό νυχτερινής προσαύξησης') ; print posostoNyxta
    posostoKyriaki = d(.75,'Ποσοστό προσαύξησης Κυριακών-Αργιών') ; print posostoKyriaki
    posostoYperoria= d(.5,'Ποσοστό προσαύξησης υπερωριών') ;print posostoYperoria
    imeromisthio = misthos / meresSymbasisMina ; imeromisthio.d('Ημερομίσθιο')                    ; print imeromisthio
    imeromisthios= misthoss/ meresSymbasisMina ; imeromisthios.d('Συμβατικό Ημερομίσθιο')         ; print imeromisthios 
    bdomadiatiko = imeromisthio * meresIKABdomada      ; bdomadiatiko.d('Βδομαδιάτικο')           ; print bdomadiatiko
    bdomadiatikos = imeromisthios * meresIKABdomada    ; bdomadiatikos.d('Συμβατικό Βδομαδιάτικο'); print bdomadiatikos
    oromisthio   = bdomadiatiko / oresSymbasiBdomada   ; oromisthio.d('Ωρομίσθιο')                ; print oromisthio 
    oromisthios   = bdomadiatikos / oresSymbasiBdomada ; oromisthios.d('Συμβατικό Ωρομίσθιο')     ; print oromisthios

    apodoxes = imeromisthio * imergasias ; apodoxes.d('Τακτικές αποδοχές περιόδου'); print apodoxes
    nyxta1 = oromisthios * brady ; nyxta1.d('Νυχτερινές αποδοχές για προσαύξηση') ; print nyxta1
    nyxta2 =  nyxta1 * posostoNyxta ; nyxta2.d('Προσαύξηση νυχτερινής απασχόλησης') ; print nyxta2
    kyrm1 = imeromisthio * posostoKyriaki ; kyrm1.d('Ημερομίσθιο προσαύξησης Κυριακής');print kyrm1
    kyrm2 = kyriakiMeres * kyrm1 ; kyrm2.d('Προσαύξηση Κυριακών'); print kyrm2
    kyr1 = oromisthios * kyriakiOres ; kyr1.d('Αποδοχές Κυριακών-Αργιών για προσαύξηση') ; print kyr1
    kyr2 = kyr1 * posostoKyriaki ; kyr2.d('Προσαύξηση Κυριακών-Αργιών') ; print kyr2
    yp1 = oromisthio * yperories ; yp1.d('Κανονική αμοιβή υπερωριών') ; print yp1
    ypkyr1 = oromisthios * ypKyr ; ypkyr1.d('Αποδοχές υπερωρίας Κυριακών-Αργιών για προσαύξηση') ; print ypkyr1
    ypkyr2 = ypkyr1 * posostoKyriaki ; ypkyr2.d('Προσαύξηση υπερωριών Κυριακών-Αργιών') ; print ypkyr2
    ypnyxta1 = oromisthios * ypBrady ; ypnyxta1.d('Νυχτερινές αποδοχές υπερωριών για προσαύξηση') ; print ypnyxta1
    ypnyxta2 =  ypnyxta1 * posostoNyxta ; ypnyxta2.d('Προσαύξηση υπερωριών νυχτερινής απασχόλησης') ; print ypnyxta2
    yp2 = yp1+ypkyr2+ypnyxta2 ; yp2.d('Συνολική αξία υπερωριών για προσαύξηση') ; print yp2
    yp3 = yp2 * posostoYperoria ; yp3.d('Προσαύξηση Υπερωριών') ; print yp3
    yp4 = yp1+yp3 ; yp4.d('Συνολικό κόστος υπερωριών'); print yp4
    totalApodoxes = apodoxes +nyxta2+kyr2+yp4; totalApodoxes.d('Συνολικές μικτές αποδοχές περιόδου') ; print totalApodoxes
    pika     = d(.4406,'Ποσοστό ΙΚΑ') ; print pika
    pikaenos = d(.16,'Ποσοστό ΙΚΑ εργαζομένου') ; print pikaenos
    pikaetis = pika - pikaenos ; pikaetis.d('Ποσοστό ΙΚΑ εργοδότη');print pikaetis
    ika      = totalApodoxes * pika ; ika.d('ΙΚΑ'); print ika
    ikaenos  = totalApodoxes * pikaenos ; ikaenos.d('ΙΚΑ εργαζομένου'); print ikaenos
    ikaetis  = ika - ikaenos ; ikaetis.d('ΙΚΑ εργοδότη'); print ikaetis
    forologiteo = totalApodoxes - ikaenos ; forologiteo.d('Φορολογητέο') ; print forologiteo
def meresImerologiakes(apo,eos):
    yapo ,yeos = int(apo[:4]) , int(eos[:4])
    mapo ,meos = int(apo[4:6]), int(eos[4:6])
    dapo ,deos = int(apo[6:]) , int(eos[6:])
    dat_apo = date(yapo,mapo,dapo)
    dat_eos = date(yeos,meos,deos)
    delta = dat_eos - dat_apo
    meres = delta.days+1
    return meres

def ores(apo,eos): # yyyymmddhhmm
    yapo ,yeos = int(apo[:4]) , int(eos[:4]    )
    mapo ,meos = int(apo[4:6]), int(eos[4:6]   )
    dapo ,deos = int(apo[6:8]) , int(eos[6:8]  )
    hapo, heos = int(apo[8:10]), int(eos[8:10] )
    lapo, leos = int(apo[10:]),  int(eos[10:]  )
    brEnarksi = 22
    brLiksi   = 6 
    dat_apo = datetime(yapo,mapo,dapo,hapo,lapo)
    dat_eos = datetime(yeos,meos,deos,heos,leos)
    delta = dat_eos - dat_apo
    ores = (delta.seconds / 3600.0)+ (delta.days*24)
    nyxterines = 0
    loipes     = 0
    v1 = lapo / 60.0
    v2 = leos / 60.0
    #if v2 == 0 : v2 =1
    for i in range(hapo,int(ores+hapo)):
        modi = i % 24
        if modi < 6 or modi >=22:
            nyxterines += 1
        else:
            loipes += 1
    if hapo < 6 or hapo >=22:
        nyxterines = nyxterines - v1
    else:
        loipes = loipes - v1
    if heos < 6 or heos >= 22:
        nyxterines = nyxterines + v2
    else:
        loipes = loipes + v2
    yperories = ores - 8
    if yperories < 0: yperories = 0    
    return ores, loipes, nyxterines,yperories
        
def calcMisDoroXrist(apo,eos,_meres,_poso):
    code = d(903,'Δώρο Χριστουγέννων')
    total_meres = d(meresImerologiakes('20110501','20111231'),'Συνολικές μέρες για Δώρο')
    meres = d(_meres,'Ημέρες εργασίας')
    poso = d(_poso,'Αποδοχές περιόδου')
    pmeres = d(meresImerologiakes(apo,eos),'Ημέρες από %s έως %s' % (apo,eos))
    kyriakes = meres / 6 ; kyriakes.d('Κυριακές που αναλογούν')
    meresMeKyriakes = kyriakes + meres ; meresMeKyriakes.d('Ημέρες εργασίας σύν Κυριακές')
    d1 = pmeres - meresMeKyriakes ; d1.d('Υπόλοιπες μέρες για μισό')
    meresmises = d1 / 2 ; meresmises.d('Μισές ημέρες')
    meresGiaDoro = meresMeKyriakes + meresmises ; meresGiaDoro.d('Μέρες για υπολογισμό δώρου')
    imeromisthiaGiaMiaMeraDoro = d(8,'Ημερομίσθια που απαιτούνται για 1 ημέρα δώρου')
    mesoImeromisthio = poso / meresGiaDoro ;  mesoImeromisthio.d('Μέσο ημερομίσθιο')
    meresDoroy = meresGiaDoro / imeromisthiaGiaMiaMeraDoro ; meresDoroy.d('Ημέρες δώρου')
    doro = mesoImeromisthio * meresDoroy ; doro.d('Δώρο Χριστουγέννων')
    print total_meres
    print pmeres
    print kyriakes
    print meresMeKyriakes
    print d1
    print meresmises
    print meresDoroy
    print mesoImeromisthio
    print doro
    print poso / 8
    
def calcMisDoroPasxa(meres):
    code = d(904,'Δώρο Πάσχα')
    tmeres = d(120,'Συνολικές ημερολογιακές ημέρες')
    anal = d(.5,'Αναλογία Δώρου Πάσχα')
    meres = d(meres,'Ημερολογιακές Ημέρες')
    for i in range(120):
        p = f.dec((i+1) / 120.0 * .5, 5)
        #print i+1 , p  
def calcMisEpAdeias():
    code = d(905,'Επίδομα Άδειας')
def calcMisEpIsolog():
    code = d(906,'Επίδομα Ισολογισμού')
def calcMisAsthenia():
    code = d(908,'Αποδοχές Ασθενείας')
def calcMisYperories():
    code = d(911,'Υπερωρίες')
    
if __name__ == '__main__':
    #calcMisNormal(750,750,27,0,2,0,30,0,0)
    #calcMisDoroPasxa(1)
    calcMisDoroXrist('20080820','20081231',100,5390)
    print ores('201101012100','201101020600')