# -*- coding: utf-8 -*-


def date2gr(date, removezero=False):
    '''
    date : iso date yyyy-mm-dd
    returns date: dd/mm/yyyy
    '''
    def remove_zero(stra):
        if len(stra) > 1 and stra[0] == '0':
            return stra[1:]
        else:
            return stra
    if not date:
        return ''

    year, month, day = date.split('-')
    if removezero:
        return '%s/%s/%s' % (remove_zero(day), remove_zero(month), year)
    else:
        return '%s/%s/%s' % (day, month, year)


def grdate2iso(grdate):
    dd, mm, yyyy = grdate.split('/')
    if len(dd) == 1:
        dd = '0%s' % dd
    if len(mm) == 1:
        mm = '0%s' % mm
    return '%s-%s-%s' % (yyyy, mm, dd)


def getymd_from_iso(isodate):
    '''
    Year, month, date From isodate
    '''
    assert isodate[4] == '-'
    assert isodate[7] == '-'
    y, m, d = isodate.split('-')
    return int(y), int(m), int(d)


def saizon(dat, startmonth=10):
    '''
    Επιστρέφει ετήσιο διάστημα από μήνα
    dat : Ημερομηνία
    startmonth : Μήνας που αρχίζει η σαιζόν
    '''
    assert startmonth <= 12
    y, m, d = getymd_from_iso(dat)
    if m >= startmonth:
        return '%s-%s(%s)' % (y, y+1, startmonth)
    else:
        return '%s-%s(%s)' % (y-1, y, startmonth)


def week(dat):
    '''
    returns year-weekNumber
    '''
    y, m, d = getymd_from_iso(dat)
    wn = '%s' % datetime.date(y, m, d).isocalendar()[1]
    if len(wn) == 1:
        wn = '0' + wn
    return '%s-%s' % (y, wn)


def period(date, diast=2):
    '''
    επιστρέφει δίμηνο, τρίμηνο, τετράμηνο, εξάμηνο
    '''
    assert diast in (2, 3, 4, 6)
    dval = {2: u'οΔίμ', 3: u'οΤρίμ', 4: u'οΤετρ', 6: u'οΕξάμ'}
    year, month, date = getymd_from_iso(date)
    imonth = int(month)
    period = imonth // diast
    ypoloipo = imonth % diast
    if ypoloipo > 0:
        period += 1
    return '%s-%s%s' % (year, period, dval[diast])


def group_selector(adate, per='m'):
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


if __name__ == '__main__':
    isod = '2016-05-01'
    grd1 = date2gr(isod)
    grd2 = date2gr(isod, True)
    iso1 = grdate2iso(grd1)
    iso2 = grdate2iso(grd2)
    print(isod, grd1, grd2, iso1, iso2)
