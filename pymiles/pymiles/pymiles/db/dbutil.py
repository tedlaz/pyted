import os
import decimal
import datetime
PATH = os.path.dirname(os.path.realpath(__file__))


def dec(poso=0, decimals=2):
    """ use : Given a number, it returns a decimal with a specific number
        of decimal digits
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or
                int ..)
            2.decimals : The number of decimals (default 2)
        output: A decimal number
        """
    def isNum(value):  # Einai to value arithmos, i den einai ?
        try:
            float(value)
        except ValueError:
            return False
        else:
            return True

    PLACES = decimal.Decimal(10) ** (-1 * decimals)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


def dec2gr(poso, decimals=2, zeroAsSpace=False):
    '''
    Returns string with Greek Formatted decimal (12345.67 becomes 12.345,67)
    '''
    if dec(poso) == dec(0):
        if zeroAsSpace:
            return ''
        else:
            decs = '0' * decimals
            if decimals > 0:
                return '0,' + decs
            else:
                return '0'

    def triades(txt, separator='.'):
        '''
        Help function to split digits to thousants ( 123456 becomes 123.456 )
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

    prosimo = ''
    strposo = str(poso)
    if len(strposo) > 0:
        if strposo[0] in '-':
            prosimo = '-'
            strposo = strposo[1:]
    timi = '%s' % dec(strposo, decimals)
    intpart, decpart = timi.split('.')
    final = triades(intpart) + ',' + decpart
    if final[0] == '.':
        final = final[1:]
    return prosimo + final


def date2gr(isodate):
    '''
    date : iso date yyyy-mm-dd
    '''
    def remove_zero(stra):
        if len(stra) > 1 and stra[0] == '0':
            return stra[1:]
        else:
            return stra
    year, month, day = isodate.split('-')
    dt = datetime.date(int(year), int(month), int(day))
    assert dt > datetime.date(1200, 1, 1)
    return '%s/%s/%s' % (remove_zero(day), remove_zero(month), year)


def date2str(isodate, order='ymd'):
    year, month, day = isodate.split('-')
    dt = datetime.date(int(year), int(month), int(day))
    assert dt > datetime.date(1200, 1, 1)
    if order == 'ymd':
        return '%s%s%s' % (year, month, day)
    elif order == 'ydm':
        return '%s%s%s' % (year, day, month)
    elif order == 'dym':
        return '%s%s%s' % (day, year, month)
    elif order == 'dmy':
        return '%s%s%s' % (day, month, year)
    elif order == 'myd':
        return '%s%s%s' % (month, year, day)
    elif order == 'mdy':
        return '%s%s%s' % (month, day, year)
    else:
        return '%s%s%s' % (year, month, day)


def nul2zero(val):
    '''
    Instead of null returns 0. For sqlite use.
    '''
    if val:
        return val
    else:
        return 0


def grupper(txtVal):
    '''
    Trasforms a string to uppercase special for Greek comparison
    '''
    ar1 = u"αάΆΑβγδεέΈζηήΉθιίϊΊκλμνξοόΌπρσςτυύΎφχψωώΏ"
    ar2 = u"ΑΑΑΑΒΓΔΕΕΕΖΗΗΗΘΙΙΙΙΚΛΜΝΞΟΟΟΠΡΣΣΤΥΥΥΦΧΨΩΩΩ"
    ftxt = u''
    for letter in txtVal:
        if letter in ar1:
            ftxt += ar2[ar1.index(letter)]
        else:
            ftxt += letter.upper()
    return ftxt

