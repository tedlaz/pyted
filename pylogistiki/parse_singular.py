"""Text file parser για το ημερολόγιο της singular
"""
import utils as ul


def parseel(elfile, encoding='WINDOWS-1253'):
    """Parsing Ημερολόγιο Γενικής Λογιστικής
       Επιστρέφει δύο dictionaries:
       d_lmo: {'38.00.00': 'Ταμείο κεντρικού', ...}
       d_tr: {1:{'d': '2017-10-13, 't': 'ΤΔΑ344', 's': 'Περιγραφή',
              'z': [{'i': 1, 'l': '20.00', 'x': 10.00, 'p': 0},
                    {'i': 2, 'l': '54.00', 'x':  2.30, 'p': 0},
                    {'i': 3, 'l': '50.00', 'x':     0, 'p': 12.30},
                    ]}}
        i : id
        d : date
        t : Parastatiko No
        s : Sxolia
        l : Logariasmos
        x : Xreosi
        p : Pistosi
    """
    id0 = 0  # id value for table tr
    id1 = 0  # id value for table trd
    dat = ''  # date for table tr
    par = ''  # par for table tr
    trp = ''  # per for table tr
    lmo = ''  # lmo for table lmo
    lmop = ''  # per for table lmo
    xr = ''  # xreosi for table trd
    pi = ''  # pistosi for table trd
    d_lmo = {}
    d_tr = {}
    with open(elfile, encoding=encoding) as afile:
        for line in afile:
            # first check if linesize > 152
            if len(line) > 152:
                # Check if we have line with accoount code
                if line[50] == '.' and line[53] == '.':
                    pass
                else:
                    continue
                # Check for date witch means we have first transaction line
                if line[4] == '/' and line[7] == '/':
                    id0 += 1
                    dat = ul.iso_date_from_greek(line[2:12])
                    par = ul.remove_simple_quotes(line[22:48])
                    d_tr[id0] = {'d': dat, 't': par, 's': trp, 'z': []}
                id1 += 1
                lmo = line[48:60].strip()
                lmop = ul.remove_simple_quotes(line[77:122])
                if lmo not in d_lmo:
                    d_lmo[lmo] = lmop
                xr = ul.dec(ul.iso_number_from_greek(line[124:137]))
                pi = ul.dec(ul.iso_number_from_greek(line[139:152]))
                d_tr[id0]['z'].append({'i': id1, 'l': lmo, 'x': xr, 'p': pi})
    if not d_lmo:
        print(u'Το αρχείο με το ημερολόγιο λογιστικής είναι κενό ή λανθασμένο')
        return None
    return d_lmo, d_tr


es = [u'ΤΠΛ', u'ΑΠΛ', u'ΤΠΥ', u'ΑΠΥ', u'ΠΙΣ', u'ΤΠΕ', u'ΕΠΛ']
ej = [u'ΛΟΙΠΑ', u'ΤΑΓ', u'ΠΑΓ', u'ΠΤΕ']


def typosee(typ):
    fval = 'ER'
    if typ in es:
        fval = 'ΕΣ'
    elif typ in ej:
        fval = 'ΕΞ'
    if typ == 'ΠΑΓ':
        fval = 'ΠΑ'
    return fval


def parseee(eefile, encoding='WINDOWS-1253'):
    tid = 0
    dat = ''
    teg = ''
    typ = 0
    par = ''
    afm = ''
    lmo = ''
    aji = 0
    fpa = 0
    eee = 1
    a_eet = []
    with open(eefile, encoding=encoding) as afile:
        for line in afile:
            # first check if linesize > 152
            if 'Κινήσεις της' == line[2:14]:
                dat = ul.iso_date_from_greek(line[32:42])
            tid = ul.remove_simple_quotes(line[1:8])
            if ul.isNum(tid):
                teg = ul.remove_simple_quotes(line[9:34])
                typ = typosee(teg)
                par = ul.remove_simple_quotes(line[35:66])
                afm = line[67:76]
                if ul.isNum(afm):
                    lmo = ul.remove_simple_quotes(line[77:91])
                else:
                    afm = ''
                    lmo = ul.remove_simple_quotes(line[67:91])
                aji = ul.dec(ul.iso_number_from_greek(line[92:112]))
                fpa = ul.dec(ul.iso_number_from_greek(line[113:133]))
                tot = aji + fpa
                # if float(aji) < 0:
                #     maji = float(aji) * -1
                #     mfpa = float(fpa) * -1
                #     note = 'credit'
                # else:
                #     maji = aji
                #     mfpa = fpa
                #     note = 'normal'
                a_eet.append((tid, dat, typ, par, lmo, aji, fpa, tot))
    return a_eet


def printee(afile):
    data = parseee(afile)
    tst = '%-5s %10s %2s %-20s %-30s %12s %12s %12s'
    for el in data:
        print(tst % el)


if __name__ == '__main__':
    file = '/home/tedlaz/pelates/2017/c/ee2017c.txt'
    printee(file)