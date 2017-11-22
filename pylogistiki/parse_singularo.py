"""Text file parser για το ημερολόγιο της singular
"""
import utils as ul
import book


def lnv(line, positions, chars):
    """
    Έλεγχος αν σε συγκεκριμένες θέσεις ενός string υπόρχουν συγκεκριμένα chars
    positions : λίστα ακεραίων με τις θέσεις που ψάχνουμε
    chars: string με τους ατίστοιχουσ χαρακτήρες που ψάχνουμε
    """
    assert len(positions) == len(chars)
    for i, position in enumerate(positions):
        if len(line) <= position:
            return False
        if line[position] != chars[i]:
            return False
    return True


def parsefile(elfile, encoding='WINDOWS-1253'):
    dat = par = per = lmo = lmp = xre = pis = ''
    lmoi = {}
    arthra = []
    lineper = 0
    with open(elfile, encoding=encoding) as afile:
        for i, lin in enumerate(afile):
            # Here we have first line for article
            if lnv(lin, [4, 7, 50, 53, 56, 134, 149], '//...,,'):
                dat = ul.iso_date_from_greek(lin[2:12])
                par = ul.remove_simple_quotes(lin[22:48])
                arth = book.Arthro(dat, par, per)
                arthra.append(arth)
                lineper = i + 1
            if lnv(lin, [50, 53, 56, 134, 149, 152], '...,, '):
                lmo = lin[48:60].strip()
                lmp = ul.remove_simple_quotes(lin[77:122])
                xre = ul.dec(ul.iso_number_from_greek(lin[124:137]))
                pis = ul.dec(ul.iso_number_from_greek(lin[139:152]))
                arth.z.append(book.Line(lmo, xre, pis))
                if lmo not in lmoi:
                    lmoi[lmo] = lmp
            elif i == lineper and i > 0:
                if len(lin) < 49 or len(lin) > 130:
                    lineper += 1
                    continue
                if lin[47] != ' ' or lin[22:27] == 'Σχετ.':
                    lineper += 1
                    continue
                arth.per = lin[48:].strip()
                lineper = 0
    return lmoi, arthra


def book_from_file(filename, encoding='WINDOWS-1253'):
    lmoi, data = parsefile(filename, encoding=encoding)
    return book.Book(lmoi, data)
