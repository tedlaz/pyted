from dec import dec
debug = False


def _pr(string):
    if debug:
        print(string)


def z2s(num):
    if num == 0:
        return ' '
    else:
        return num


def omosimoi(val1, val2):
    return (val1 > 0 and val2 > 0) or (val1 < 0 and val2 < 0)


def almost_equal(val1, val2, threshold=0.2):
    # print(round(abs(val1 - val2), 2))
    return round(abs(val1 - val2), 2) <= threshold


def print_fdata(fdata):
    tmpl = '%-13s%1s%-12s %4s %14s %14s %5s %12s %10s\n'
    st1 = tmpl % ('lmos', ' ', '   lfpa', 'fn', 'poso', 'fpa', '', 'cfpa', 'd')
    for lm in sorted(fdata):
        lmd = fdata[lm]
        llmd = len(lmd)
        if llmd > 1:
            llmp = '*'
        else:
            llmp = ''
        for vt in lmd:
            fn = lmd[vt]['fn']
            val = lmd[vt]['val']
            fpa = lmd[vt]['fpa']
            pfpa = lmd[vt]['pfpa']
            cfpa = dec(val * dec(pfpa) / dec(100))
            dlt = z2s(fpa - cfpa)
            st1 += tmpl % (lm, llmp, vt, fn, val,
                           z2s(fpa), z2s(pfpa), z2s(cfpa), dlt)
    print(st1)


def closest(vat, val, vatp=[23.0, 24.0, 13.0, 17.0, 16.0]):
    '''
    finds closest match of vat percentage
    Returns minimum cost , vat percentage
    '''
    cost = [dec(abs(val * pc / 100.0 - vat)) for pc in vatp]
    min_cost = min(cost)
    bestvatp = vatp[cost.index(min_cost)]
    # delta = dec(val * bestvatp / 100.0 - vat)
    return min_cost, bestvatp


def match(vals, fpas, pfpas=[23.0, 24.0, 13.0, 17.0, 16.0]):
    if len(fpas) > len(vals):
        print('Error')
        return []
    for f, fpa in enumerate(fpas):
        for v, val in enumerate(vals):
            cfpa = [dec(abs(val * pfpa / 100.0 - fpa)) for pfpa in pfpas]
            print(fpa, val, min(cfpa), pfpas[cfpa.index(min(cfpa))])


def create_pairs(l1, l2):
    ll1 = len(l1)
    ll2 = len(l2)
    assert ll2 >= ll1
    aa = []
    if ll1 == 1:
        for el in l2:
            aa.append([[l1[0], el], ])
    elif ll1 == 2:
        lst = make_list(ll2)
        for ll in lst:
            aa.append([[l1[0], l2[ll[0]]], [l1[1], l2[ll[1]]]])
    elif ll1 == 3:
        if ll2 == 3:
            aa.append([[l1[0], l2[0]], [l1[1], l2[1]], [l1[2], l2[2]]])
            aa.append([[l1[0], l2[0]], [l1[1], l2[2]], [l1[2], l2[1]]])
            aa.append([[l1[0], l2[1]], [l1[1], l2[0]], [l1[2], l2[2]]])
            aa.append([[l1[0], l2[1]], [l1[1], l2[2]], [l1[2], l2[0]]])
            aa.append([[l1[0], l2[2]], [l1[1], l2[0]], [l1[2], l2[1]]])
            aa.append([[l1[0], l2[2]], [l1[1], l2[1]], [l1[2], l2[0]]])
        elif ll2 == 4:
            aa.append([[l1[0], l2[0]], [l1[1], l2[1]], [l1[2], l2[2]]])
            aa.append([[l1[0], l2[0]], [l1[1], l2[2]], [l1[2], l2[1]]])
            aa.append([[l1[0], l2[1]], [l1[1], l2[0]], [l1[2], l2[2]]])
            aa.append([[l1[0], l2[1]], [l1[1], l2[2]], [l1[2], l2[0]]])
            aa.append([[l1[0], l2[2]], [l1[1], l2[0]], [l1[2], l2[1]]])
            aa.append([[l1[0], l2[2]], [l1[1], l2[1]], [l1[2], l2[0]]])
            #
            aa.append([[l1[0], l2[0]], [l1[1], l2[1]], [l1[2], l2[3]]])
            aa.append([[l1[0], l2[0]], [l1[1], l2[3]], [l1[2], l2[1]]])
            aa.append([[l1[0], l2[1]], [l1[1], l2[0]], [l1[2], l2[3]]])
            aa.append([[l1[0], l2[1]], [l1[1], l2[3]], [l1[2], l2[0]]])
            aa.append([[l1[0], l2[3]], [l1[1], l2[0]], [l1[2], l2[1]]])
            aa.append([[l1[0], l2[3]], [l1[1], l2[1]], [l1[2], l2[0]]])
            #
            aa.append([[l1[0], l2[0]], [l1[1], l2[3]], [l1[2], l2[2]]])
            aa.append([[l1[0], l2[0]], [l1[1], l2[2]], [l1[2], l2[3]]])
            aa.append([[l1[0], l2[3]], [l1[1], l2[0]], [l1[2], l2[2]]])
            aa.append([[l1[0], l2[3]], [l1[1], l2[2]], [l1[2], l2[0]]])
            aa.append([[l1[0], l2[2]], [l1[1], l2[0]], [l1[2], l2[3]]])
            aa.append([[l1[0], l2[2]], [l1[1], l2[3]], [l1[2], l2[0]]])
            #
            aa.append([[l1[0], l2[3]], [l1[1], l2[1]], [l1[2], l2[2]]])
            aa.append([[l1[0], l2[3]], [l1[1], l2[2]], [l1[2], l2[1]]])
            aa.append([[l1[0], l2[1]], [l1[1], l2[3]], [l1[2], l2[2]]])
            aa.append([[l1[0], l2[1]], [l1[1], l2[2]], [l1[2], l2[3]]])
            aa.append([[l1[0], l2[2]], [l1[1], l2[3]], [l1[2], l2[1]]])
            aa.append([[l1[0], l2[2]], [l1[1], l2[1]], [l1[2], l2[3]]])
    else:
        return []
    lcost = []
    for el in aa:
        # print(el)
        minv = dec(0)
        for pair in el:
            cost, vatp = closest(pair[0], pair[1])
            pair.append(vatp)
            pair.append(float(cost))
            minv += cost
        lcost.append(minv)
        # print('cost %s' % minv)
    gmin = aa[lcost.index(min(lcost))]
    return gmin


def make_list(siz):
    assert(siz > 1)
    v1 = range(siz)
    flist = []
    for i, val in enumerate(v1):
        for j in v1[i+1:]:
            flist.append([i, j])
            flist.append([j, i])
    return flist


def make_list2(siz, order=2):
    assert(siz >= order)
    v1 = range(siz)
    flist = []
    for i, val in enumerate(v1):
        for j in v1[i+1:]:
            flist.append([i, j])
            flist.append([j, i])
    return flist


def vat_to_lmoi(vatl, lmol, vatv, lmov, eggno):
    '''
    vatl : List of vat accounts (e.g. ['54.00.213', '54.00.224'])
    lmol : List of lmo accounts (e.g. ['20.01.013', '20.01.024', '20.00.000])
    vatv : List of vat values   (e.g. [13.0, 24.0])
    lmov : List of lmo values   (e.g. [100.0, 100.0, 132.42])
    '''
    if len(lmol) == 0:
        return []
    # Some assertions
    assert len(vatl) == len(vatv)
    assert len(lmol) == len(lmov)
    assert len(vatl) <= len(lmol)
    # For the moment just check that we have unique value fields
    assert len(vatv) == len(set(vatv))
    assert len(lmov) == len(set(lmov))
    pairs = create_pairs(vatv, lmov)
    plmov = []
    lfin = []
    for pr in pairs:
        anvl = vatl[vatv.index(pr[0])]
        anll = lmol[lmov.index(pr[1])]
        lfin.append([eggno, anll, anvl, pr[2], pr[1], pr[0], pr[3]])
        plmov.append(pr[1])
    for almo in lmov:
        if almo not in plmov:
            lfin.append([eggno, lmol[lmov.index(almo)], '', '', almo, 0, 0])
    return lfin


def chkvat(dbd, synvats=[13.0, 24.0, 23.0], vacc='54.00', omades='1267'):
    '''
    dbd : list of tuples [(id, lmo, val)]
    '''
    data = {}
    for lin in dbd:
        _id = lin[0]
        lmo = lin[1]
        val = lin[2]
        data[_id] = data.get(_id, {'vatl': [], 'vatv': [], 'vatf': [],
                                   'omal': [], 'omav': [], 'omaf': [],
                                   'othl': [], 'othv': []})
        if lmo.startswith(vacc):
            data[_id]['vatl'].append(lmo)
            data[_id]['vatv'].append(val)
            data[_id]['vatf'].append(False)
        elif lmo[0] in omades:
            data[_id]['omal'].append(lmo)
            data[_id]['omav'].append(val)
            data[_id]['omaf'].append(False)
        else:
            data[_id]['othl'].append(lmo)
            data[_id]['othv'].append(val)
    # print(data)
    joined = {}
    dist = {}
    errors = '\nΕνδεχόμενα λάθη:\n'
    ss = []
    for num in data:
        arthro = data[num]
        tot = sum(arthro['vatv']) + sum(arthro['omav']) + sum(arthro['othv'])
        try:
            assert round(tot, 2) == 0
        except:
            print('Transaction %s is not balanced' % arthro)
        ar1 = vat_to_lmoi(arthro['vatl'], arthro['omal'], arthro['vatv'], arthro['omav'], num)
        if ar1:
            ss += ar1
    # Create Totals Here
    tt = {}
    tfpa = dec(0)
    for el in ss:
        lmo = el[1]
        vmo = el[2]
        vatp = el[3]
        val = el[4]
        vat = el[5]
        delta = el[6]
        if lmo not in tt:
            tt[lmo] = {}
        if vmo not in tt[lmo]:
            tt[lmo][vmo] = {}
        if vatp not in tt[lmo][vmo]:
            tt[lmo][vmo][vatp] = {'val': dec(0), 'vat': dec(0), 'delta': 0}
        tt[lmo][vmo][vatp]['val'] += dec(val)
        tt[lmo][vmo][vatp]['vat'] += dec(vat)
        delta = dec(dec(val) * dec(vatp) / dec(100.0) - dec(vat))
        tt[lmo][vmo][vatp]['delta'] += delta
        tfpa += dec(vat)
    tml = "%-14s %-14s %4s %14s %14s %5s"
    for lm in sorted(tt):
        for vl in tt[lm]:
            for vt in tt[lm][vl]:
                val = tt[lm][vl][vt]['val']
                vat = tt[lm][vl][vt]['vat']
                # dlt = z2s(tt[lm][vl][vt]['delta'])
                dlt = dec(val * dec(vt) / dec(100.0) - vat)
                print(tml % (lm, vl, vt, val, z2s(vat), z2s(dlt)))
    print('FPA %s' % tfpa)
    # return tt
    # '''
    for el in sorted(ss, key=lambda x: x[1]):
        tml = "%-5s %-14s %-14s %4s %14s %14s %5s"
        print(tml % (el[0], el[1], el[2], el[3], el[4], z2s(el[5]), z2s(el[6])))
    # '''

if __name__ == '__main__':
    import db
    # print(omosimoi(0, 13))
    # print(almost_equal(1.84, 1.875))
    dbd = [[1, '64.00.013', 100.0],
           [1, '64.00.000', 30.0],
           [1, '64.00.013', 10.0],
           [1, '54.00.000', 10],
           [1, '54.00.613', 1.3],
           [1, '54.00.613', 13.0],
           [1, '64.00.024', 20.0],
           [1, '54.00.624', 4.8],
           [1, '50.00.001', -189.1],
           [2, '70.00.013', -10.0],
           [2, '54.00.713', -1.3],
           [2, '30.00.001', 11.3],
           [3, '70.00.000', -100.0],
           [3, '30.00.000', 100.0],
           [4, '64.08.024', 100.0],
           [4, '54.00.100', 12],
           [4, '54.00.624', 23.0],
           [4, '50.00.000', -135.0]]
    sql = ("SELECT tr.id, lmo.lmo, trd.xr - trd.pi AS val "
           "FROM tr "
           "INNER JOIN trd ON tr.id=trd.id_tr "
           "INNER JOIN lmo ON lmo.id=trd.id_lmo "
           "WHERE tr.dat BETWEEN '2017-01-01' AND '2017-12-31';")
    dbpath = '/home/tedlaz/tedfiles/prj/2017/2017a.sql3'
    data = db.dataFromDB(dbpath, sql)
    # print(data)
    # The order of vat percentage is important
    # Most frequently used must appear first
    # fdata = chk_vat(data, [24.0, 13.0, 17.0, 23.0, 16.0], 0.08)
    chkvat(data, [24.0, 13.0, 17.0])  # , 23.0, 16.0])
