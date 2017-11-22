import utils as ul
from parse_singular import parseel
lm = ul.read_txt_to_dict('log_sxedio.txt')


def print_ledger(lgr, lmoi):
    st1 = '\nArthro: %s Date: %s  Par: %s'
    st2 = '  %6s %13s %-50s %12s %12s'
    for i in lgr:
        print(st1 % (i, lgr[i]['d'], lgr[i]['t']))
        for j in lgr[i]['z']:
            lpe = lmoi[j['l']]
            print(st2 % (j['i'], j['l'], lpe, j['x'], j['p']))


def check_integrity(ledger):
    errors = 0
    for i in ledger:
        delta = 0
        for line in ledger[i]['z']:
            delta += line['x']
            delta -= line['p']
        if delta != 0:
            print('integrity error on %s' % i)
    if not errors:
        print('Data integrity is ok')
        return True
    else:
        return False


def make_totals(lgr, period='d'):
    dva = {}
    pers = set()
    zero = ul.dec(0)
    for i in lgr:
        for j in lgr[i]['z']:
            lmo = j['l']
            per = ul.group_time_text(lgr[i]['d'], period)
            pers.add(per)
            xre = j['x']
            pis = j['p']
            for lmoh in ul.lmo_hierarchy(lmo):
                if lmoh in dva:
                    if per not in dva[lmoh]:
                        dva[lmoh][per] = {'x': zero, 'p': zero, 'y': zero}
                else:
                    dva[lmoh] = {per: {'x': zero, 'p': zero, 'y': zero}}
                txr = dva[lmoh][per]['x'] + xre
                tpi = dva[lmoh][per]['p'] + pis
                typ = txr - tpi
                dva[lmoh][per] = {'x': txr, 'p': tpi, 'y': typ}
    return dva, sorted(list(pers))


def final_list(ledger, lmoi, period='m'):
    # join the dictionaries
    tlmoi = {**lmoi, **lm}
    zero = ul.dec2gr(ul.dec(0))
    data, periods = make_totals(ledger, period)
    fdata = []
    head = ['lmos', 'perigrafi']
    format_string = '%-12s %-50s'
    for per in (periods + ['total']):
        for timi in ('x', 'p', 'y'):
            head.append('%s %s' % (per, timi))
            format_string += ' %12s'
    for lmo in sorted(data):
        tlist = [lmo, tlmoi.get(lmo, lmo)]
        txr = tpi = typ = ul.dec(0)
        for per in periods:
            if per in data[lmo]:
                txr += data[lmo][per]['x']
                tpi += data[lmo][per]['p']
                typ += data[lmo][per]['y']
                tlist.append(ul.dec2gr(data[lmo][per]['x']))
                tlist.append(ul.dec2gr(data[lmo][per]['p']))
                tlist.append(ul.dec2gr(data[lmo][per]['y']))
            else:
                tlist.append(zero)
                tlist.append(zero)
                tlist.append(zero)
        tlist.append(ul.dec2gr(txr))
        tlist.append(ul.dec2gr(tpi))
        tlist.append(ul.dec2gr(typ))
        fdata.append(tuple(tlist))
    return fdata, tuple(head), format_string


def final_list_yp(ledger, lmoi, period='m'):
    # join the dictionaries
    tlmoi = {**lmoi, **lm}
    zero = ul.dec2gr(ul.dec(0))
    data, periods = make_totals(ledger, period)
    fdata = []
    head = ['lmos', 'perigrafi']
    format_string = '%-12s %-50s'
    for per in (periods + ['total']):
        head.append('%s' % per)
        format_string += ' %12s'
    for lmo in sorted(data):
        tlist = [lmo, tlmoi.get(lmo, lmo)]
        typ = ul.dec(0)
        for per in periods:
            if per in data[lmo]:
                typ += data[lmo][per]['y']
                tlist.append(ul.dec2gr(data[lmo][per]['y']))
            else:
                tlist.append(zero)
        tlist.append(ul.dec2gr(typ))
        fdata.append(tuple(tlist))
    return fdata, tuple(head), format_string


def print_is(afile, period='m', only_yp=True):
    lmoi1, ledger1 = parseel(afile)
    if only_yp:
        data, head, fstring = final_list_yp(ledger1, lmoi1, period)
    else:
        data, head, fstring = final_list(ledger1, lmoi1, period)
    print(fstring % head)
    for line in data:
        print(fstring % line)


if __name__ == "__main__":
    # print(ledger1[1])
    # print_ledger(ledger1, lmoi1)
    # check_integrity(ledger1)
    # print(make_totals(ledger1, period='m'))
    print_is('el2017.txt', period='m3', only_yp=True)
