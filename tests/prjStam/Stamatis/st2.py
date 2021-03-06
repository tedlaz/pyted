# coding: utf-8

'''Module : tedFunctions.py
    Utility functions for reuse

    Function functionName(input parameters):
        use: Description
        input parameters :
            1.ParameterName     : Parameter description 
            2.....
        output: Output parameter description and type
    '''

import decimal

debugging = False

def isNum(value): # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters : 
            1.value : the value to check against.
        output: True or False
        """
    try: float(value)
    except ValueError: return False
    else: return True

def isNumArray(valArray): # Elegxei ean oloi oi oroi toy array, einai aritmoi
    """
        use: Checks if all members of valArray are numeric.
        input parameters : valArray =  the array for check
        output: True or False
    """
    for element in valArray:
        timi = False
        try: float(element)
        except ValueError: return False
        else: timi = True
    return timi

def dec(poso , dekadika=2 ):
    """ use : Given a number, it returns a decimal with a specific number of decimals
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or int ..)
            2.dekadika : The number of decimals (default 2)
        output: A decimal number     
        """
    strq = '0.' + '0' * (dekadika -1) + '1'
    PLACES = decimal.Decimal(10) ** (-1 * dekadika)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)

def addArr(ar1,ar2):
    tmp_arr = []
    if len(ar1) == len(ar2):
        for i in range(len(ar1)):
            tmp_arr.append(ar1[i]+ar2[i])
    return tmp_arr

def createHarmony(basis,elements=1000,dekadika=10):
    arr = []
    for el in range(elements):
        arr.append(dec(basis,dekadika)* (el+1))
    return arr

def getNharmony(basis,n=100,dekadika=10):
    return dec(dec(basis,dekadika) * n,dekadika)

def findSt(balanceBasis,firstCountBasis,aditiveBasis,fores=150,dekadika=10):
    bBasis = dec(balanceBasis,dekadika)
    fBasis = dec(firstCountBasis,dekadika)
    aBasis = dec(aditiveBasis,dekadika)
    bBasis_arr = createHarmony(bBasis,fores * 2, dekadika)
    fBasis_arr = createHarmony(fBasis,fores,dekadika)
    aBasis_arr = createHarmony(aBasis,fores, dekadika)
    tBasis_arr = addArr(fBasis_arr,aBasis_arr)
    print bBasis
    x_arr = []
    y1_arr = []
    y2_arr = []
    for el in tBasis_arr:
        a = findLowerUpperHarmonic(bBasis,el,dekadika)
        x, y1,y2 = a[1],a[7],a[4]
        x_arr.append(x)
        y1_arr.append(y1)
        y2_arr.append(y2)
        print a[1],a[7],a[4]
    return x_arr, y1_arr,y2_arr, bBasis

def findLowerUpperHarmonic(basis,num,dekadika=10):
    nbasis = dec(basis,dekadika)
    nnum   = dec(num,dekadika)
    if nnum < nbasis :
        return nbasis,nnum,0,0,0,0,0,0
    div   = int( nnum / nbasis )
    div2  = div
    l = getNharmony(basis,div)
    dl = nnum - l
    if dl == 0:
        h = l
        dh = dl = dec('0',0)
    else:
        div2 = div+1
        h = getNharmony(basis,div2)
        dh = h - nnum
    if dl > nbasis or dh > nbasis:
        print "Error !!!"
    return nbasis, nnum, div, l, dl, div2, h, dh,

def strLowerUpper(basis,num):
    ar = findLowerUpperHarmonic(basis,num)
    s  = "----------------------------------------------\n"
    s += "|     Results from Harmonic function         |\n"
    s += "----------------------------------------------\n"
    s += "| Basis            : %23s |\n" % ar[0]
    s += "| Num              : %23s |\n" % ar[1]
    s += "| Armoniki Low No  : %23s |\n" % ar[2]
    s += "| Low Armoniki     : %23s |\n" % ar[3]
    s += "| Low Delta        : %23s |\n" % ar[4]
    s += "| Armoniki High No : %23s |\n" % ar[5]
    s += "| Hi Armoniki      : %23s |\n" % ar[6]
    s += "| Hi Delta         : %23s |\n" % ar[7]
    s += "----------------------------------------------"
    s += "\n\n"
    return s    

def parseFile(arxeio = 'tstForParsing.txt', resultf='results.txt'):
    f = open(arxeio,'r')
    r = open(resultf,'w')
    base = '0'
    num  = '0'
    lineNo = 1
    for line in f:
        ltype = line[0]
        if   ltype == '1':
            base = line[2:30]
        elif ltype == '2':
            num = line[2:30]
            if isNum(base) and isNum(num):
                r.write(strLowerUpper(base,num))
            else:
                r.write( 'Error in file %s, line %s\n\n' % (arxeio,lineNo))
        else:
            pass
        lineNo += 1
    f.close()
    r.close()
if __name__ == "__main__":
    #parseFile()
    x, y1 , y2, basis = findSt('1.6749','1.67262158','1.66053886',100)
    import numpy as np
    import matplotlib.pyplot as plt
    plt.plot(x,y1,x,y2)
    plt.grid()

    plt.title(u'Σταμάτης Πανταζόπουλος')
    xlabel = u'Βασική αρμονική = %s' % basis
    plt.xlabel(xlabel)
    plt.text(50,1,'Text inside')
    plt.show()

