# -*- coding: utf-8 -*-
'''
Created on 9 Ιαν 2014

@author: tedlaz
'''
import decimal
import datetime
from collections import OrderedDict
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

def numOrEmptytext(val):
    '''
    Returns number if exists else ''
    '''
    if isNum(val):
        return val
    else:
        return ''
    
def addArrays(first,second):
    return [x + y for x, y in zip(first, second)]

def createSubtotalsFromOrderedVals(vals,depth):
    '''
    Having an ordered from left to right vals array [[a1,a2,...,an],[b1,b2,..bn],...[N1,N2,...,Nn]]
    uses columns from 0 to Depth to create subtotals on Numeric Values
    '''
    tots = OrderedDict()
    ar = []
    for val in vals:      
        stra = ''
        preval = '0'
        for col in range(depth):
            if stra == '': par = '0'
            else: par = stra
            stra += '%s' % val[col]
            ar.append(stra)
            if stra in tots:
                tots[stra] = [par,addArrays(tots[stra][1],val[depth:]),'%s'% val[col],preval]
            else:
                tots[stra] = [par,[numOrEmptytext(tim) for tim in val[depth:]],'%s'% val[col],preval]
            preval = '%s'% val[col]    
    farr = []
    for key in tots:
        farr.append([tots[key][2],tots[key][3],tots[key][1]])
    return farr
    
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

def strGrDec(poso , dekadika=2):
    '''
    Returns string with Greek Formatted decimal (12345.67 becomes 12.345,67)
    '''
    timi = '%s' % dec(poso,dekadika)
    intpart, decpart = timi.split('.')
    final = triades(intpart)+','+ decpart
    if final[0] =='.':
        final = final[1:]
    return final
def decFromGrDec(txtposo):
    '''
    create decimal value from Greek decimal value (1.234,78 becomes 1234.78)
    '''
    tposo = txtposo.replace('.','')
    return dec(tposo.replace(',','.'))  
  
def strDateTimeNow():
    '''
    returns datetime string (2010-01-31 20:30:15)
    '''
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def strDateNow():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")
    
def greekDateFromIso(isoDate):
    '''
    iso date on the form : YYYY-MM-DD (eg 2010-12-31)
    '''
    year, month, date = isoDate.split('-')
    return '%s/%s/%s' % (date,month,year)

def sha1OfFile(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()
    
def sha1OfArray(array):
    tmp = u''
    for el in array:
        tmp += u'%s' % el
    return hashlib.sha1(tmp.encode('utf-8')).hexdigest()
   
if __name__ == '__main__':
    print greekDateFromIso('2013-01-31')
    print strDateTimeNow()
    print greekDateFromIso(strDateNow())
    print strGrDec('1453334455.34')
    print decFromGrDec('1.234,56')
    print addArrays([1,1,1],[4,5,6,7])
    print createSubtotalsFromOrderedVals([['a','aa',10,11],['a','aa',20,10]],3)
    print sha1OfArray(['ted',1,30])