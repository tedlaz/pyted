# -*- coding: utf-8 -*-
'''
Created on 16 Ιαν 2013

@author: tedlaz
'''
from utils import dec as d
def f13(poso):
    poso = d(poso)
    ekp = d(0)
      
    if poso < d(21500):
        ekp = d(2100)
    elif poso < d(22500):
        ekp = d(2000)
    elif poso < d(23500):
        ekp = d(1900)
    elif poso < d(24500):
        ekp = d(1800)
    elif poso < d(25500):
        ekp = d(1700)
    elif poso < d(26500):
        ekp = d(1600)
    elif poso < d(27500):
        ekp = d(1500)
    elif poso < d(28500):
        ekp = d(1400)
    elif poso < d(29500):
        ekp = d(1300)
    elif poso < d(30500):
        ekp = d(1200)
    elif poso < d(31500):
        ekp = d(1100)  
    elif poso < d(32500):
        ekp = d(1000)
    elif poso < d(33500):
        ekp = d(900)
    elif poso < d(34500):
        ekp = d(800)
    elif poso < d(35500):
        ekp = d(700)
    elif poso < d(36500):
        ekp = d(600)
    elif poso < d(37500):
        ekp = d(500)        
    elif poso < d(38500):
        ekp = d(400)
    elif poso < d(39500):
        ekp = d(300)
    elif poso < d(40500):
        ekp = d(200)
    elif poso < d(41500):
        ekp = d(100)
    else:
        ekp = d(0)
    #print 'ekptosi',poso,ekp
    foros = d(0)
    if poso <= d(25000):
        foros = d(poso * d(22) / d(100))
    else:
        foros = d(5500)
        poso = poso - d(25000)
        if poso <= d(17000):
            foros += d(poso * d(32) / d(100))
        else:
            foros += d(5440)
            poso = poso - d(17000)
            foros += d(poso * d(42) / d(100))
    foros = foros - ekp
    if foros < d(0) :
        foros = d(0)
    return foros

def eea(poso):
    poso = d(poso)
    if poso <= d(12000):
        synt = d(0)
    elif poso <= d(20000):
        synt = d(1)
    elif poso <= d(50000):
        synt = d(2)
    elif poso <= d(100000):
        synt = d(3)
    else:
        synt = d(4)
    return d(poso * synt / d(100))

def eeap(poso,bar=1): #bar : 1 εάν ολόκληρη περίοδος 2 εάν μισή (πχ.επίδομα αδείας)
    poso = d(poso)
    tb = d(14) * d(bar)
    eis = poso * tb
    ee = eea(eis)
    return d(ee / tb)

def fp13(poso,bar=1):
    poso = poso
    tb = 14 * bar
    eis = poso * tb
    f = f13(eis)
    #pf = d(f - d(0.015,3) * f)
    return f / tb

def fpXrisis(poso,bar=1,xrisi=2013):
    if xrisi == 2013:
        return  fp13(poso,bar)
    else:
        return 0
    
def eeaXrisis(poso,bar=1,xrisi=2013):
    if xrisi == 2012 or xrisi == 2013:
        return eeap(poso,bar)
    else:
        return d(0) 
       
if __name__ == '__main__':
    p = 2035.72
    print fpXrisis(p,1,2013)
    print eeaXrisis(p,1,2013)