"""Utilities"""
import decimal
import datetime


def grup(txtval):
    '''Trasforms a string to uppercase special for Greek comparison'''
    ar1 = u"αάΆΑβγδεέΈζηήΉθιίϊΐΊΪκλμνξοόΌπρσςτυύϋΰΎΫφχψωώΏ"
    ar2 = u"ΑΑΑΑΒΓΔΕΕΕΖΗΗΗΘΙΙΙΙΙΙΚΛΜΝΞΟΟΟΠΡΣΣΤΥΥΥΥΥΥΦΧΨΩΩΩ"
    adi = dict(zip(ar1, ar2))
    return ''.join([adi.get(letter, letter.upper()) for letter in txtval])


def isNum(val):  # is val number or not
    """Check if val is number or not"""
    try:
        float(val)
    except ValueError:
        return False
    except TypeError:
        return False
    else:
        return True


def dec(poso=0, decimals=2):
    """Returns a decimal. If poso is not a number or None returns dec(0)"""
    if poso is None:
        poso = 0
    tmp = decimal.Decimal(poso) if isNum(poso) else decimal.Decimal('0')
    qval = decimal.Decimal(10) ** (-1 * decimals)
    return tmp.quantize(qval, rounding=decimal.ROUND_HALF_UP)


def dec2text_flat(poso, decimals=2):
    return str(dec(poso, decimals)).replace('.', '').replace(',', '')


def iso_number_from_greek(num):
    num = num.strip()
    num = num.replace('.', '')
    num = num.replace(',', '.')
    return num


def dec2gr(poso, zeroAsSpace=False):
    '''
    Returns string with Greek Formatted decimal (12345.67 becomes 12.345,67)
    '''
    tpo = dec(poso)
    if tpo == 0:
        if zeroAsSpace:
            return ''
    return '{:,.2f}'.format(tpo).replace(",", "X").replace(".", ",").\
        replace("X", ".")


def iso_date_from_greek(dat):
    day, month, year = dat.split('/')
    day = day if len(day) == 2 else '0%s' % day
    month = month if len(month) == 2 else '0%s' % month
    return '%s-%s-%s' % (year, month, day)


def remove_simple_quotes(strval):
    retval = strval.strip()
    retval = retval.replace("'", '')
    return retval


def getymd_from_iso(date):
    assert date[4] == '-'
    assert date[7] == '-'
    y, m, d = date.split('-')
    return int(y), int(m), int(d)


def saizon(dat, startmonth=10):
    y, m, d = getymd_from_iso(dat)
    if m >= startmonth:
        return '%s-%s' % (y, y + 1)
    else:
        return '%s-%s' % (y - 1, y)


def week(dat):
    y, m, d = getymd_from_iso(dat)
    wn = '%s' % datetime.date(y, m, d).isocalendar()[1]
    if len(wn) == 1:
        wn = '0' + wn
    return '%s-%s' % (y, wn)


def period(date, diast=2):
    assert diast in (2, 3, 4, 6)
    dval = {2: 'oDi', 3: 'oTr', 4: 'oTe', 6: 'oEj'}
    year, month, date = getymd_from_iso(date)
    imonth = int(month)
    period = imonth // diast
    ypoloipo = imonth % diast
    if ypoloipo > 0:
        period += 1
    return '%s-%s%s' % (year, period, dval[diast])


def group_time_text(adate, per='m'):
    if per == 'd':  # Όλη η ημερομηνία
        dat = adate[:10]
    elif per == 'm':  # Έτος + μήνας ####-##
        dat = adate[:7]
    elif per == 'y':  # Έτος μόνο
        dat = adate[:4]
    elif per == 'm2':
        dat = period(adate, 2)
    elif per == 'm3':
        dat = period(adate, 3)
    elif per == 'm4':
        dat = period(adate, 4)
    elif per == 'm6':
        dat = period(adate, 6)
    elif per == 'w':
        dat = week(adate)
    elif per == 's':
        dat = saizon(adate)
    else:  # Default is Year
        dat = adate[:4]
    return dat


def lmo_hierarchy(lmos, split_char='.'):
    assert len(lmos) > 1
    listlmo = lmos.split(split_char)
    listfinal = ['t']
    if lmos[0] in '267':
        listfinal.append('t267')
    elif lmos[0] in '35':
        listfinal.append('t35')
    listfinal.append(lmos[0])
    tmp = ''
    for el in listlmo:
        if tmp == '':
            tmp = el
        else:
            tmp = split_char.join([tmp, el])
        listfinal.append(tmp)
    return listfinal


def read_csv(acsv):
    import csv
    with open(acsv, encoding='ISO-8859-7') as cs:
        lines = csv.reader(cs, delimiter='|')
        for row in lines:
            pass


def read_txt_to_dict(txtfile):
    tdic = {}
    with open(txtfile) as ofile:
        for line in ofile:
            lst = line.split('|')
            tdic[lst[0]] = lst[1]
    return tdic


class DicDec(dict):
    """
    Dictionary with decimal values except if key starts with 't_'
    """

    def __setitem__(self, key, item):
        # self.__dict__[key] = ul.dec(item)
        if key.startswith('t_'):
            super(DicDec, self).__setitem__(key, item)
        else:
            super(DicDec, self).__setitem__(key, dec(item, 2))


def print_dic(adict):
    for key in adict:
        print('%-40s:%12s' % (key, adict[key]))
    print('=====================================================')


def print_dicl(data, width1='40', width2='>12'):
    fstr = '{:%s}:{:%s}' % (width1, width2)
    le1 = int(width1.replace('<', '').replace('>', '').replace('^', ''))
    le2 = int(width2.replace('<', '').replace('>', '').replace('^', ''))
    print('')
    for key in data[0]:
        print(fstr.format(data[1][key], data[0][key]))
    print('=' * (le1 + le2 + 1))


class RequiredKeyException(Exception):
    pass


def has_keys(keys, adict):
    """
    keys: [key1, key2, ...]
    adict: {key1: val1, key2: val2, ...other1: vother1}
    Returns True if dictionary adict contains all keys from list keys
    If not raises exception with message containing missing keys
    """
    errors = []
    for key in keys:
        if key not in adict:
            errors.append(key)
    if errors:
        erstr = 'required: %s missing from: %s' % (errors, adict)
        raise RequiredKeyException(erstr)
    return True


if __name__ == '__main__':
    print(read_txt_to_dict('log_sxedio.txt'))
    print(dec2text_flat(2350.46, 1))
