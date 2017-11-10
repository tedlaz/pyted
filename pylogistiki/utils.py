"""Utilities"""
import decimal
import datetime


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
    return tmp.quantize(decimal.Decimal(10) ** (-1 * decimals))


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


if __name__ == '__main__':
    print(read_txt_to_dict('log_sxedio.txt'))
