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

def caps(stri):
    st = stri #stri.decode('UTF-8')
    l = u'αβγδεζηθικλμνξοπρστυφχψωάέήίόύώϊΆ'
    h = u'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΑΕΗΙΟΥΩΙΑ'
    tstr = u''
    for g in st:
        found = False
        for i in range(len(l)):
            if g == l[i]:
                tstr += u'%s' % h[i]
                found = True
                break
        if not found:
            tstr += g.upper()
    return tstr 
 
def dateTostr(sqlite3Date):
    y,m,d = sqlite3Date.split('-')
    return '%s%s%s' % (d,m,y)  

def nowToSqliteDate():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")

def nowToStr():
    a = nowToSqliteDate()
    return dateTostr(a)

def num2descr(num,fromIteration=0):
    'Μετατροπή ακεραίου αριθμού σε Ελληνική περιγραφή'
    a1 = u'Ένα Δύο Τρία Τέσσερα Πέντε Έξι Επτά Οκτώ Εννέα Δέκα Έντεκα Δώδεκα'.split()
    a1.insert(0,'')
    a2 = u'Δέκα Είκοσι Τριάντα Σαράντα Πενήντα Εξήντα Εβδομήντα Ογδόντα Ενενήντα Εκατό'.split()
    a2.insert(0,'')
    a3 = u'Εκατόν Διακόσια Τριακόσια Τετρακόσια Πεντακόσια Εξακόσια Επτακόσια Οκτακόσια Εννιακόσια Χίλια'.split() 
    a3.insert(0,'')
    intNum = int(num)
    strNum = '%s' % intNum
    lenNum = len(strNum)
    if intNum == 0 and not fromIteration:
        desc = u'Μηδέν'
    elif intNum < 13:
        desc = a1[intNum]
    elif intNum < 100:
        desc = '%s %s' % (a2[int(strNum[0])], a1[int(strNum[1])])
    elif intNum == 100:
        desc = u'Εκατό'
    elif intNum < 1000:
        desc = '%s %s' % (a3[int(strNum[0])],num2descr(int(strNum[1:]),1))
    elif intNum == 1000:
        desc = u'Χίλια'
    elif intNum < 2000:
        desc = u'Χίλια %s' % num2descr(int(strNum[1:]))
    elif intNum < 1000000:
        desc = u'%s Χιλιάδες %s' %  (num2descr(int(strNum[:-3]),1).replace(u'σια',u'σιες'), num2descr(int(strNum[-3:]),1))
    elif intNum < 1000000000:
        if int(strNum[-7]) == 1:
            desc = u'%s Εκατομμύριo %s' %  (num2descr(int(strNum[:-6]),1), num2descr(int(strNum[-6:]),1))
        else:
            desc = u'%s Εκατομμύρια %s' %  (num2descr(int(strNum[:-6]),1), num2descr(int(strNum[-6:]),1))
    elif intNum < 1000000000000:
        desc = u'%s Δισεκατομμύρια %s' %  (num2descr(int(strNum[:-9]),1), num2descr(int(strNum[-9:]),1))
    elif intNum < 1000000000000000:
        desc = u'%s Τρισεκατομμύρια %s' %  (num2descr(int(strNum[:-12]),1), num2descr(int(strNum[-12:]),1))
    else:
        desc = u'Δεν μπορώ να μετρήσω παραπάνω...'    
    return desc

if __name__ == '__main__':
    print(num2descr(12))