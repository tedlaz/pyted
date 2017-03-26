# -*- coding: utf-8 -*-
'''
Created on 4 Απρ 2013

@author: tedlaz
'''
from collections import OrderedDict
from utils import dec as d
from fmy import fpXrisis, eeaXrisis
calcarr = [['apod','meres * imsthio'],
           ['ika','apod * 12.2 / 100'],
           ['forologiteo','apod - ika'],
           ['foro','foros(forologiteo)'],
           ['ypol','10']
           ]

def foros(poso):
    return poso * .1 
        
def calcmis(xrisi,period,mistype,ergData,calcArray=calcarr):
    meres   = ergData.setdefault('meres',0)
    merasles3 = ergData.setdefault('merasles3',0)
    merasmor3 = ergData.setdefault('merasmor3',0)
    yperor    = ergData.setdefault('yperor',0)
    kyrpros   = ergData.setdefault('kyrpros',0)
    nyxtpros  = ergData.setdefault('nyxtpros',0)
    
    imsthio = ergData.setdefault('imsthio',0)
    pika = ergData.setdefault('pika',0)
    pikaenos = ergData.setdefault('pikaenos',0)
    xrisin = int(xrisi)
    f = OrderedDict()
    for el in calcArray:
        calcstr = '%s = %s' % (el[0],el[1])
        exec calcstr
        f[el[0]] = d(eval(el[0]))
    return f

def flatCalcMis(xrisi,period,mistype,ergData):
    vtypos = ergData.setdefault('typos',2) # 1=Μισθός , 2=Ημερομίσθιο, 3=Ωρομίσθιο
    vtapod = ergData.setdefault('tapod',0) # Εάν vtypos=1 μισθός κλπ
    vmeres   = ergData.setdefault('meres',0)
    vdefmeres = ergData.setdefault('vdefmeres',25) #Ημέρες εργασίας ανά μήνα
    vdefmeresw = ergData.setdefault('vdefmeresw',6) #Ημέρες εργασίας ανά βδομάδα
    vdefores = ergData.setdefault('vdefores',40) #Ώρες εργασίας ανά βδομάδα
    vmeresKanAdeias = ergData.setdefault('meresKanAdeias',0)
    vmerasles3 = ergData.setdefault('merasles3',0) # Μέρες ασθένειας < 3
    vmerasmor3 = ergData.setdefault('merasmor3',0) # Μέρες ασθένειας > 3
    vyperor    = ergData.setdefault('yperor',0) #΄Ώρες υπερωριών
    vsyntyper  = ergData.setdefault('syntyper',1.75)
    vkyrpros   = ergData.setdefault('kyrpros',0) #μέρες κυριακών - αργιών για προσαύξηση 75%
    vsyntkyr   = ergData.setdefault('syntkyr',.75) # Συντελεστής προσαύξησης κυριακών - αργιών (75%)
    vnyxtpros  = ergData.setdefault('nyxtpros',0) #ώρες για νυχτερινή προσαύξηση 25%
    vsynnyxt  = ergData.setdefault('synnyxt',.25)
    
    imeromisthio = 100
    misthos = 101
    oromisthio = 102 
    meresYpologismoy=109
    meresIka=110
    kapod = 150
    proskyr = 151
    nyxtpros = 152
    yper = 154
    
    apod=200
    ikaenos=500
    ikaetis=501
    ika=502
    typosapodoxon=503
    kpk=504
    pikaenos=505
    pika=506
    forologiteo=599
    fmyanalogei=601
    fmyparaktr=600
    eea=610
    totalkratiseis=700
    priroteo=900
    
    r = OrderedDict()
        
    #1.Τακτικές αποδοχές - Αργίες - Κυριακές - Νυχτερινά
    r[meresYpologismoy] = vmeres + vmeresKanAdeias
    
    if vtypos == 1:
        r[apod] = d(d(r[meresYpologismoy]) / d(vdefmeres) * d(vtapod))
        r[imeromisthio] = d(vtapod / vdefmeres)
        r[oromisthio] = d(r[imeromisthio] * vdefmeresw / vdefores)
    elif vtypos == 2:
        r[apod] = d(r[meresYpologismoy] * vtapod)
        r[imeromisthio] = d(vtapod)
        r[oromisthio] = d(r[imeromisthio] * vdefmeresw / vdefores)        
    elif vtypos ==3:
        r[apod] = d(r[meresYpologismoy] / vdefmeresw * vdefores * vtapod)
        r[imeromisthio] = d(vdefores / vdefmeresw * vtapod)
        r[oromisthio] = vtapod
    else:
        r[apod] = d(0)
        
    if vkyrpros > 0: # Κυριακές - Γιορτές με προσαύξηση 75%
        r[proskyr] = d(d(vkyrpros) * d(r[imeromisthio]) * d(vsyntkyr))
        r[apod] += r[proskyr]
    
    if vnyxtpros > 0:
        r[nyxtpros] =  d(d(vnyxtpros) *  r[oromisthio] * d(vsynnyxt))
        r[apod] += r[nyxtpros]
        print u'Νυχτερινή προσαύξηση %s' % r[nyxtpros]
    #2.Υπερωρίες
    if vyperor > 0:
        r[yper] = d( d(vyperor) * r[oromisthio] * d(vsyntyper))  
    #4.Ασθένεια
    return r
if __name__ == '__main__':
    from utils_db import getDbRowsByFldName
    db = 'c:/ted/testing.m13'
    sql = "select varnam, formula FROM z_calcd  WHERE calc_id=1  ORDER BY id"
    ergDataAr=[{'xrisi':2013,'meres':4,'tapod':40,'pikaenos':16.5,'pika':43.96,'kyrpros':2},
               {'xrisi':2013,'typos':1,'meres':25,'tapod':2400,'pikaenos':14.5,'pika':40.96,'nyxtpros':8}]
    calcArr = getDbRowsByFldName(sql,db)
    for ergData in ergDataAr:
        print flatCalcMis('2013',1,1,ergData)#.setdefault('forologiteo',0)