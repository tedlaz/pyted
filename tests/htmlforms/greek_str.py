import decimal


def isNum(value):  # Einai to value arithmos, i den einai ?
    """
    use: Returns False if value is not a number , True otherwise
    input parameters:
        1.value : the value to check against.
    output: True or False
    """
    if not value:
        return False
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


def dec(poso, dekadika=2):
    """
    use : Given a number, it returns a decimal with a specific number
          of decimal digits
    input Parameters:
        1.poso : The number for conversion in any format (e.g. string or int)
        2.dekadika : The number of decimals (default 2)
    output: A decimal number
    """
    PLACES = decimal.Decimal(10) ** (-1 * dekadika)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


# Utility Functions
def greek_num_str(number, zero2null=False, decimals=2):
    '''
    Returns Greek Decimal(2) number or
    if zero2null is True '' (empty string)
    else 0,00
    '''
    number = dec(number, decimals)
    if abs(number) <= 0.004:
        if zero2null:
            return ''
        else:
            return '0,00'
    s = '%.2f' % number
    a, d = s.split('.')
    groups = []
    while a and a[-1].isdigit():
        groups.append(a[-3:])
        a = a[:-3]
    return a + '.'.join(reversed(groups)) + ',' + d


def greek_int_str(number):
    'Returns Greek Decimal(1) number'
    strn = greek_num_str(number, False, 0)
    left, right = strn.split(',')
    return left


def greek_date_str(imnia):
    '''
    imnia must be iso date YYYY-MM-DD
    returns dd/mm/yyyy
    '''
    y, m, d = imnia.split('-')
    return '%s/%s/%s' % (d, m, y)


if __name__ == '__main__':
    num = -1002536.64589
    dat = '2015-10-30'
    print(greek_int_str(num))
    print(greek_num_str(num))
    print(greek_num_str(num, True))
    print(greek_date_str(dat))
    matr = [[1, 1, 1, 1], [2, 2, 2, 6]]
    a = list(zip(*matr))
    print([sum(b) for b in a])
