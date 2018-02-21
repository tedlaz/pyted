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


if __name__ == '__main__':
    print(date2period('2017-01-01'))
    print(date2period('2017-03-31'))
    print(date2period('2017-04-01'))
    print(date2period('2017-06-30'))
    print(date2period('2017-07-01'))
    print(date2period('2017-09-30'))
    print(date2period('2017-10-01'))
    print(date2period('2017-12-31'))
