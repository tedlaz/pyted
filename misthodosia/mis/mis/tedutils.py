# -*- coding: utf-8 -*-
'''
Created on 19 Νοε 2012

@author: tedlaz
'''
import decimal

def isNum(value): # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters : 
            1.value : the value to check against.
        output: True or False
        """
    try: float(value)
    except ValueError: return False
    else: return True

def dec(poso , dekadika=2 ):
    """ use : Given a number, it returns a decimal with a specific number of decimals
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or int ..)
            2.dekadika : The number of decimals (default 2)
        output: A decimal number     
        """
    PLACES = decimal.Decimal(10) ** (-1 * dekadika)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)
    
if __name__ == '__main__':
    from m12.models import Pro, Xrisi, Period, Mtyp, Mis
    '''
    Για υπολογισμό της μισθοδοσίας
    1. Ελέγχουμε εάν είναι ενημερωμένες οι παρουσίες των ενεργών εργαζομένων
    2. Κάνουμε τους υπολογισμούς
    3. Αποθηκεύουμε σε Βάση Δεδομένων
    '''
    xri = Xrisi.objects.get(xrisi='2012')
    per = Period.objects.get(period='01')
    mis         = Mtyp.objects.get(mtypp=u'2.Μισθός')
    mtypika     = Mtyp.objects.get(mtypp=u'5.ika')
    mtypikaenos = Mtyp.objects.get(mtypp=u'3.ikaenos')
    mtypikaetis = Mtyp.objects.get(mtypp=u'4.ikaetis')
    mtypPlirote = Mtyp.objects.get(mtypp=u'6.pliroteo')
    enoi = Pro.objects.all()
    mt   = Mtyp.objects.get(mtypp=u'1.par')
    '''
    for erg in enoi:
        m1 = Mis.objects.get(xrisi=xri,period=per,pro=erg, mtyp=mt)
        meres = m1.val
        apod  = meres * erg.apod
        m = Mis(xrisi=xri,period=per,pro=erg,mtyp=mis,val= apod)
        m.save()
        ikaenos = dec(apod * erg.eid.kpk.penos / dec(100))
        m = Mis(xrisi=xri,period=per,pro=erg,mtyp=mtypikaenos,val= ikaenos)
        m.save()
        ika     = dec(apod * erg.eid.kpk.ptot / dec(100))
        m = Mis(xrisi=xri,period=per,pro=erg,mtyp=mtypika,val=ika)
        m.save()
        ikaetis =  ika - ikaenos
        m = Mis(xrisi=xri,period=per,pro=erg,mtyp=mtypikaetis,val=ikaetis)
        m.save()
        pliroteo = apod - ikaenos
        m = Mis(xrisi=xri,period=per,pro=erg,mtyp=mtypPlirote,val=pliroteo)
        m.save()
        #print erg.fpr,erg.eid.kpk.penos , erg.apod, erg.eid.kpk.penos *  erg.apod / 100
    '''
    from django.db.models import  Sum
    m = Mis.objects.filter(xrisi=xri,period=per,mtyp=mtypikaetis).aggregate(Sum('val')) 
    print m 