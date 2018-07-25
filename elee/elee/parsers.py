"""
Παρσάρισμα ημερολογίου singular
"""
from . import utils as ul
from . import arthro


def check_line(line, stxt):
    """
    Ελέγχει μια γραμμή κειμένου για συγκεκριμένους χαρακτήρες σε επιλεγμένα
    σημεία. Άν δεν υπάρχουν οι αναμενόμενοι χαρακτήρες στις θέσεις τους
    επιστρέφει False, διαφορετικά επιστρέφει True
    stxt: '0:t|2:r|5:s'
    """
    # Μετατρέπουμε το stxt σε dictionary
    dpos = {int(s[0]): s[1] for s in [k.split(':') for k in stxt.split('|')]}
    lline = len(line)
    for position in dpos:
        if lline <= position:  # Το μήκος της γραμμής μεγαλύτερο από τη θέση
            return False
        if line[position] != dpos[position]:
            return False
    return True


def parse_el(elfile, encoding='WINDOWS-1253'):
    dat = par = per = lmo = lmp = xre = pis = ''
    lmoi = {}
    arthra = []
    lineper = 0
    arthro_number = line_number = 1
    with open(elfile, encoding=encoding) as afile:
        for i, lin in enumerate(afile):
            # Here we have first line for article
            if check_line(lin, '4:/|7:/|50:.|53:.|56:.|134:,|149:,'):
                dat = ul.iso_date_from_greek(lin[2:12])
                par = ul.remove_simple_quotes(lin[22:48])
                arth = arthro.Arthro(dat, par, per, arthro_number)
                arthro_number += 1
                arthra.append(arth)
                lineper = i + 1
            if check_line(lin, '50:.|53:.|56:.|134:,|149:,|152: '):
                lmo = lin[48:60].strip()
                lmp = ul.remove_simple_quotes(lin[77:122])
                xre = ul.dec(ul.iso_number_from_greek(lin[124:137]))
                pis = ul.dec(ul.iso_number_from_greek(lin[139:152]))
                arth.add_line(lmo, xre, pis, line_number)
                line_number += 1
                if lmo not in lmoi:
                    lmoi[lmo] = lmp
            elif i == lineper and i > 0:
                if len(lin) < 49 or len(lin) > 130:
                    lineper += 1
                    continue
                if lin[47] != ' ' or lin[22:27] == 'Σχετ.':
                    lineper += 1
                    continue
                arth.pe2 = lin[23:48].strip()
                arth.per = lin[48:].strip()
                lineper = 0
    return lmoi, arthra


def parse_el_pandas(elfile, encoding='WINDOWS-1253'):
    dat = par = per = lmo = lmp = xre = pis = ''
    lmoi = {}
    arthra = []
    lineper = 0
    lins = []
    arthro_number = line_number = 1
    with open(elfile, encoding=encoding) as afile:
        for i, lin in enumerate(afile):
            # Here we have first line for article
            if check_line(lin, '4:/|7:/|50:.|53:.|56:.|134:,|149:,'):
                dat = ul.iso_date_from_greek(lin[2:12])
                par = ul.remove_simple_quotes(lin[22:48])
                arth = arthro.Arthro(dat, par, per, arthro_number)
                arthro_number += 1
                arthra.append(arth)
                lineper = i + 1
            if check_line(lin, '50:.|53:.|56:.|134:,|149:,|152: '):
                lmo = lin[48:60].strip()
                lmp = ul.remove_simple_quotes(lin[77:122])
                xre = ul.dec(ul.iso_number_from_greek(lin[124:137]))
                pis = ul.dec(ul.iso_number_from_greek(lin[139:152]))
                arth.add_line(lmo, xre, pis, line_number)
                lins.append([arthro_number, line_number, dat,
                             par, lmo, xre, pis])
                line_number += 1
                if lmo not in lmoi:
                    lmoi[lmo] = lmp
            elif i == lineper and i > 0:
                if len(lin) < 49 or len(lin) > 130:
                    lineper += 1
                    continue
                if lin[47] != ' ' or lin[22:27] == 'Σχετ.':
                    lineper += 1
                    continue
                arth.pe2 = lin[23:48].strip()
                arth.per = lin[48:].strip()
                lineper = 0
    return lmoi, arthra, lins


def parse_ee_old(eefile, encoding='WINDOWS-1253'):
    name_afm = {}  # {'tedlaz': 04678}
    dublicates = {}
    with open(eefile, encoding=encoding) as afile:
        for i, lin in enumerate(afile):
            if len(lin) < 100:
                continue
            vals = lin[67:91].split()
            if len(vals) == 0:
                continue
            if ul.is_afm(vals[0]):
                afm = vals[0]
                name = lin[77:91].split('-')[0].strip()
                if name in name_afm.keys():
                    if afm == name_afm[name]:
                        continue
                    else:  # Ιδιο όνομα με διαφορετικό ΑΦΜ
                        print("Ίδιο όνομα με άλλο ΑΦΜ (γραμμή %s)" % (i + 1))
                        name = '%s -> %s' % (name, i + 1)
                        dublicates[name] = afm
                else:
                    name_afm[name] = afm
    return name_afm, dublicates


def parse_ee(eefile, encoding='WINDOWS-1253'):
    """
    """
    adi = {}
    dat = ''
    with open(eefile, encoding=encoding) as afile:
        for i, lin in enumerate(afile):
            if lin[2:14] == 'Κινήσεις της':
                dat = lin[32:42]
                # print(dat)
            if len(lin) < 100:
                continue
            vals = lin[67:91].split()
            if len(vals) == 0:
                continue
            if ul.is_afm(vals[0]):
                afm = vals[0]
                name = lin[77:91].split('-')[0].strip()
                adi[dat] = adi.get(dat, {})
                adi[dat][name] = afm
    return adi


def parse_ee_flat(eefile, encoding='WINDOWS-1253'):
    """
    Επιστρέφει list of tuples [(dat1, name1, afm1), (dat2, name2, afm2), ..]
    """
    date_name_afm = []
    dat = ''
    with open(eefile, encoding=encoding) as afile:
        for lin in afile:
            if lin[2:14] == 'Κινήσεις της':
                dat = ul.iso_date_from_greek(lin[32:42])
                # print(dat)
            if len(lin) < 100:
                continue
            vals = lin[67:91].split()
            if len(vals) == 0:
                continue
            if ul.is_afm(vals[0]):
                afm = vals[0]
                name = lin[77:91].split('-')[0].strip()
                date_name_afm.append((dat, name, afm))
    return date_name_afm
