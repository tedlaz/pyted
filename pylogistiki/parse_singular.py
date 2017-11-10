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
