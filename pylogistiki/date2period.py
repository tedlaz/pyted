"""
Date functions
"""


def date2period(isodate):
    year, month, _ = isodate.split('-')
    imonth = int(month)
    if imonth <= 3:
        return '%s-%s-%s' % (year, '03', '31')
    elif imonth <= 6:
        return '%s-%s-%s' % (year, '06', '30')
    elif imonth <= 9:
        return '%s-%s-%s' % (year, '09', '30')
    elif imonth <= 12:
        return '%s-%s-%s' % (year, '12', '31')
    else:
        return '%s-%s-%s' % (year, '12', '31')


def date2per(isodate, rate=2):
    """Returns Year-Period Type-Period Number """
    assert rate in (1, 2, 3, 4, 6)
    year, month, _ = isodate.split('-')
    imonth = int(month)
    per = imonth // rate
    rem = imonth % rate
    if rem > 0:
        per += 1
    return "%s%s%s" % (year, rate, per)



def date2trimino(isodate):
    year, month, _ = isodate.split('-')
    imonth = int(month)
    if imonth <= 3:
        return '%s-%s' % (year, '1')
    elif imonth <= 6:
        return '%s-%s' % (year, '2')
    elif imonth <= 9:
        return '%s-%s' % (year, '3')
    elif imonth <= 12:
        return '%s-%s' % (year, '4')
    else:
        return '%s-%s' % (year, '4')


if __name__ == '__main__':
    # print(date2period('2017-01-01'))
    # print(date2period('2017-03-31'))
    # print(date2period('2017-04-01'))
    # print(date2period('2017-06-30'))
    # print(date2period('2017-07-01'))
    # print(date2period('2017-09-30'))
    # print(date2period('2017-10-01'))
    # print(date2period('2017-12-31'))
    # print(date2trimino('2017-12-31'))
    # print(date2trimino('2017-05-15'))
    # print(date2trimino('2017-08-01'))
    dt1 = '2018-08-12'
    print(date2per(dt1, 1))
    print(date2per(dt1, 2))
    print(date2per(dt1, 3))
    print(date2per(dt1, 4))
    print(date2per(dt1, 6))
