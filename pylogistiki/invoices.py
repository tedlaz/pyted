"""Invoice class"""
import utils as ul


class Lmos():
    trpr = '%s %s'

    def __init__(self, code, per, pfpa):
        self.code = code
        self.per = per
        self.pfpa = ul.dec(pfpa)

    @property
    def fpa_percent(self):
        return ul.dec(self.pfpa / ul.dec(100))

    def __repr__(self):
        return self.trpr % (self.code, self.per)


class InvoiceLine():
    trpr = '%s %s %s %s'

    def __init__(self, lmos, poso):
        self.lmos = lmos
        self.poso = ul.dec(poso)
        self.fpa = self.calc_fpa()

    @property
    def total(self):
        return self.poso + self.fpa

    def calc_fpa(self):
        return ul.dec(self.poso * self.lmos.fpa_percent)

    def correct_fpa(self, value, threshold=0.1):
        value = ul.dec(value)
        if abs(self.calc_fpa() - value) < threshold:
            self.fpa = value
        else:
            raise ValueError('fpa is out of threshold')

    def __repr__(self):
        return self.trpr % (self.lmos, self.poso, self.fpa, self.total)


class Invoice():
    def __init__(self, date, par, afm, normal=True):
        self.date = date
        self.par = par
        self.afm = afm
        self.note = 'normal' if normal else 'credit'
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

    @property
    def amount(self):
        val = ul.dec(0)
        for line in self.lines:
            val += line.poso
        return val

    @property
    def tax(self):
        tax = ul.dec(0)
        for line in self.lines:
            tax += line.fpa
        return tax

    @property
    def total(self):
        total = ul.dec(0)
        for line in self.lines:
            total += line.total
        return total

    def __repr__(self):
        tm1 = 'Date : %s Number: %s AFM: %s Type: %s\n'
        val = tm1 % (self.date, self.par, self.afm, self.note)
        for line in self.lines:
            val += '%s\n' % line
        val += 'Σύνολα %s %s %s' % (self.amount, self.tax, self.total)
        return val


def agemp(date, par, afm, poso13=0, poso24=0):
    inv = Invoice(date, par, afm)
    if poso13 != 0:
        lmo13 = Lmos('20.13', 'Αγορές εμπορευμάτων ΦΠΑ 13%', 13)
        inv.add_line(InvoiceLine(lmo13, poso13))
    if poso24 != 0:
        lmo24 = Lmos('20.24', 'Αγορές εμπορευμάτων ΦΠΑ 24%', 24)
        inv.add_line(InvoiceLine(lmo24, poso24))
    return inv
