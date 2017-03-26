# -*- coding: utf-8 -*-
'''
Programmer : Ted Lazaros (tedlaz@gmail.com)
'''

import decimal
import hashlib

def isNum(value): # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters : 
            1.value : the value to check against.
        output: True or False
        """
    try: float(value)
    except ValueError: return False
    else: return True

def dec(poso , decimals=2 ):
    """ use : Given a number, it returns a decimal with a specific number of decimals
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or int ..)
            2.decimals : The number of decimals (default 2)
        output: A decimal number     
        """
    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)

def triades(txt,separator='.'):
    '''
    Help function to create triads
    '''
    ltxt = len(txt)
    rem = ltxt % 3
    precSpace = 3 - rem
    stxt = ' ' * precSpace + txt
    a = []
    while len(stxt) > 0:
        a.append(stxt[:3])
        stxt = stxt[3:]
    a[0] = a[0].strip()
    fval = ''
    for el in a:
        fval += el + separator
    return fval[:-1]

def strGrDec(poso , decimals=2):
    '''
    Returns string with Greek Formatted decimal (12345.67 becomes 12.345,67)
    '''
    timi = '%s' % dec(poso,decimals)
    intpart, decpart = timi.split('.')
    final = triades(intpart) +',' + decpart
    if final[0] =='.':
        final = final[1:]
    return final

def sha1OfFile(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()
    
def sha1OfArray(array):
    tmp = u''
    for el in array:
        tmp += u'%s' % el
    return hashlib.sha1(tmp.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    pass