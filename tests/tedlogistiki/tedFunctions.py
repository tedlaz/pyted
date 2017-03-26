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
    PLACES = decimal.Decimal(10) ** (-1 * dekadika)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)

def checkGreekAFM(afm):
    """ use : It checks a number if its valid Greek Vat number
        input Parameters:
            1.afm : The number (in any format) to be checked against.
        output: True or False
        """
    ar = [256,128,64,32,16,8,4,2]
    iSum = 0
    btRem = 0
    l = len(afm)
    if not isNum(afm):
        return False

    if l <> 9:
        return False
    for i in range(l-1):
        iSum += int(afm[i]) * ar[i]
    if iSum == 0 :
        return False
    else:
        btRem = iSum % 11
        if (int(afm[8]) == btRem) or ((btRem == 10) and (int(afm[8]) == 0)):
            return True
        else:
            return False

def calcIka(posa, vpika, vpikaEnos, vorio, vmeres=25): # Ypologizei to IKA
    """ use : Ypologismos IKA me oria.
        input parameters:
            1.posa      : array me ajies gia ika (p.x. [1230.45,34.5]])
            2.vpika     : Pososto IKA synolika
            3.vpikaEnos : Pososto IKA ergazomenoy
            4.vorio     : Orio IKA (me basi tis 25 imeres)
            5.vmeres    : Hmeres gia IKA
        output:
            Array me times [[poso1,ikaergazomenoy1,ikaergodoti1,ikaTotal1],[k.l.p]]
        """
    orio = dec(dec(vorio) / dec(25) * dec(vmeres))
    pika = dec(vpika)
    pikaEnos = dec(vpikaEnos)
    sumGiaIKA = dec(0)
    ika = []
    for poso in posa:
        dposo = dec(poso)
        sumGiaIKA += dposo
        if orio - sumGiaIKA >= 0:
            tmpIKA = dec(dposo * pika /dec(100))
            tmpIKAenos = dec(dposo * pikaEnos /dec(100))
            tmpIKAetis = tmpIKA - tmpIKAenos
            ika.append([dposo, tmpIKAenos, tmpIKAetis, tmpIKA])
        else:
            if orio - sumGiaIKA + dposo >= 0:
                d = orio - sumGiaIKA + dposo
                tmpIKA = dec(d * pika / dec(100))
                tmpIKAenos = dec(d * pikaEnos / dec(100))
                tmpIKAetis = tmpIKA - tmpIKAenos
                ika.append([dposo, tmpIKAenos, tmpIKAetis, tmpIKA ])
            else:
                ika.append([dposo, dec(0),dec(0),dec(0)])
    totalIKA = dec(0)
    
    if debugging :
        for val in ika:
            totalIKA += val[3]
        print totalIKA
    return ika

def calcIkaw(etos,kpk,meres,posa): # Ypoligizei to IKA me default times ..
    orioEtoys = {   '2003':1960.25,
                    '2004':2058.25,
                    '2005':2140.5,
                    '2006':2226}
    orio = orioEtoys[etos]
    
    vkpk = {'106':[50.66,19.45],'102':[45.06, 16.00]}
    
    vika = vkpk[kpk][0]
    vikaenos = vkpk[kpk][1]
    arr =  calcIka(posa, vika, vikaenos, orio, meres)
    for element in arr:
        for col in element:
            print '%12.2f' % col,
        print
    return arr
    
def arrayTotal(arr):
    """
        use: It creates a numeric array with accoumulated sum members
    """
    if not isNumArray(arr):
        return []
    counter = 0
    tarr = []
    for el in arr:
        tarr.append(el+counter)
        counter  += el
    return tarr

def arrayAjia(arr): # Ypologizei to athrisma ton oron enos aritmitikoy array
    """
        use: Returns the sum of the members of an numeric array. 
    """
    if not isNumArray(arr):
        return 0
    tmpVal = 0
    for el in arr:
        tmpVal += el
    return tmpVal
    
def arrayDelta(arr):
    """
        use: Returns an array with delta values of arr.
    """
    if not isNumArray(arr):
        return []
    tarr = []
    for i in range(len(arr)):
        if i == 0:
            tarr.append(arr[i])
        else:
            tarr.append(arr[i]-arr[i-1])
    return tarr
    
def looksLikeArrayTotal(arr): # Elegxei ean to array tha mporei na einai totalArray
    """
        use : Checks if arr is possibly a totalArray
    """
    if not isNumArray(arr):
        return []
    delta = arrayDelta(arr)
    for element in delta:
        if element < 0:
            return False
    return True
    
def splitPoso(poso, splitArray): # Spaei to poso me basi to splitArray
    """ use : Splits poso according splitArray
        input parameters:
            1.poso       : Value for split
            2.splitArray : Array to split according to.
        output: Array with splitted Value.
    """
    tmpPoso = dec(poso)
    returnArray = []
    for el in splitArray:
        if tmpPoso <= el:
            returnArray.append(tmpPoso)
            return returnArray
        else:
            returnArray.append(el)
            tmpPoso = tmpPoso - el
    returnArray.append(tmpPoso)
    return returnArray

def katanomiPoso(poso,arrKatanomis): 
    """
       use: Katanemei to poso analogika me to arrKatanomis
       kai opoia diafora tin bazei ston proto megalytero oro 
    """
    tAjiaKatanomis = dec(arrayAjia(arrKatanomis))
    tmpKatanemimeno = []
    tmpMax = dec(0)
    for el in arrKatanomis:
        valKatanomis = dec(dec(poso)/tAjiaKatanomis * dec(el))
        tmpKatanemimeno.append(valKatanomis)
        if tmpMax < valKatanomis:
            tmpMax = valKatanomis
    tDiafora = dec(poso) - arrayAjia(tmpKatanemimeno)
    if tDiafora <> dec(0):
        for i in range(len(tmpKatanemimeno)):
            if tmpKatanemimeno[i] == tmpMax:
                tmpKatanemimeno[i] += tDiafora
                return tmpKatanemimeno
    return tmpKatanemimeno
    
def calcFMY(forologiteo, paidia=0, ekptosi=True, etos='2006', methorios=False): # Ypologizei to Foro MIsthoton Ypiresion
    """ use : Ypologismos Foroy eisodimatos misthoton 
        input parameters:
            1.forologiteo : To poso gia forologisi
            2.padia       : arithmos paidion
            3.ekptosi     : ekptosi foroy 1,5%
            4.etos        : forologiko etos
            5.methorios   : An katoikei o ypoxreos sti methorio
        output: Decimal me ton foro
    """
    paidia = int(paidia)
    if etos == '2007':
        eisa = [dec(12000),dec(18000),dec(45000)]
        syntelestis = [dec(0),dec(29),dec(39),dec(40)]
    elif etos == '2006':
        eisa = [dec(11000),dec(2000),dec(10000)]
        syntelestis = [dec(0),dec(15),dec(30),dec(40)]
    else:
        print 'Den ginetai ypologismos'
        return 0
    ekptosipaidion = 0
    if paidia == 0 :
        ekptosipaidion = 0
    elif paidia == 1:
        ekptosipaidion = 1000
    elif paidia == 2:
        ekptosipaidion = 2000
    elif paidia == 3:
        ekptosipaidion = 10000
    elif paidia > 3: 
        ekptosipaidion = 10000 + ((paidia - 3 ) * 1000)
    else:
        ekptosipaidion = 0
    eis = []
    eis.append(dec(ekptosipaidion)+eisa[0])
    if eis[0] > eisa[0] + eisa[1]:
        eis.append(dec(0))
    else:
        eis.append(eisa[0]+eisa[1]-eis[0])
    if eis[0]+ eis[1] > eisa[0] + eisa[1] + eisa[2]:
        eis.append(dec(0))
    else:
        eis.append(eisa[0]+eisa[1]+eisa[2]-eis[0]-eis[1])
    forologiteoSplitted = splitPoso(forologiteo,eis)
    foros = dec(0)
    for i in range(len(forologiteoSplitted)):
        foros += dec(forologiteoSplitted[i] * syntelestis[i]/dec(100))
    if ekptosi:
        foros  = dec(foros - (foros * dec(15)/dec(1000)))
    return foros

def foroPeriodoy(forologiteoPer, paidia=0, periodoi=14, ekptosi=True, etos='2006', methorios=False):
    """ 
        use : Ypologismos analogias foroy gia misthologiki periodo
        input parameters :
            1.forologiteoPer : To poso tis periodoy gia forologisi
            2.padia          : arithmos paidion
            3.periodoi       : to Synolo ton periodon se ena forologiko etos
            4.ekptosi        : ekptosi foroy 1,5%
            5.etos           : forologiko etos
            6.methorios      : An katoikei o ypoxreos sti methorio
        output : foros poy analogei stin periodo
    """
    forolp = dec(forologiteoPer)
    forologiteo = dec(forolp * periodoi)
    return dec(calcFMY(forologiteo,paidia,ekptosi,etos,methorios) / dec(periodoi))

def miscalc(dederg): 
    """
        dederg : Dedomena periodoy ergazomenoy 
    """
    basikesImeresIKA = dec(25)
    misthos = dec(dederg['misthos'])
    ergasimesImeres = dec(dederg['meres'])
    seKanonikiAdeia = dec(dederg['kad'])
    ImeresGiaMisthodosia = ergasimesImeres + seKanonikiAdeia
    ApodoxesPeriodoy = misthos /dec(25) * ImeresGiaMisthodosia
    orioIKA = dec(2226.0)/basikesImeresIKA * ImeresGiaMisthodosia

    if ApodoxesPeriodoy <= orioIKA:
        ApodoxesGiaIKA = ApodoxesPeriodoy
    else:
        ApodoxesGiaIKA = orioIKA

    pIKA = dec(45.06)
    pIKAergazomenoy = dec(16)
    IKA = dec(ApodoxesGiaIKA * pIKA/100)
    IKAergazomenoy = dec(ApodoxesGiaIKA * pIKAergazomenoy/100)
    IKAergodoti = IKA - IKAergazomenoy
    pliroteo = ApodoxesPeriodoy - IKAergazomenoy
    return misthos, IKA, IKAergazomenoy, pliroteo, orioIKA

def misthodosiaCalc(xrisi, periodos, misthodosiaType):
    dedomenaErgazomenon = getErgazomenoiPeriodou(xrisi, periodos, misthodosiaType)
    for dedomenaErgazomenou in dedomenaErgazomenon:
        tactApodoxes = calcTaktikesApodoxesPeriodou(dedomenaErgazomenou)
        apodoxes     = calcApodoxesPeriodou(tactApodoxes)
        kratiseis    = calcKratiseisPeriodou()
        calcForoPeriodou()
        
def getDataFromFile(f='./osyk/dn_kpk.txt',splitChar='|'):
    """
        use: Returns an array with data readed from file f with split character splitChar.
        input parameters:
            1. f          : file name
            2. splitChar  : Split Character
        output: Array with data from file.
    """
    fl = open(f,'r')
    tmpArr = []
    for line in fl.readlines():
        tlin = line
        tlin = tlin[:-1]
        tmpArr.append(tlin.split(splitChar))
    return tmpArr
    
def printarrData(arr):
    for lin in arr:
        for col in lin:
            print col,
        print ''

