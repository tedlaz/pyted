# -*- coding: utf-8 -*-
# Invoice creation

import os
from fpdf import FPDF
from fpdf import dec
from fpdf.ted_helper import Helper
import sys


PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if PATH not in sys.path:
    sys.path.append(PATH)

left_margin = 10.0
top_margin = 10.0
p_width = 190
p_height = 260.0


class Invoice():

    def __init__(self, datad):
        self.pdf = FPDF()
        self.hp = Helper(self.pdf)
        self.pdf.add_font('fn', '', 'times.ttf', True)
        self.pdf.add_font('fi', '', 'timesi.ttf', True)
        self.pdf.add_font('fb', '', 'timesb.ttf', True)
        self.data = datad
        self.lines_per_page = 35
        self.total_lines = len(self.data['lines'])
        self.tpos = 0
        self.tajia = 0
        self.dvat = {}
        # Calculate total invoice pages
        self.total_pages = int(self.total_lines / float(self.lines_per_page))
        self.current_page = 1
        self.col_posotita = 129.0
        self.col_ajia = 200.0
        remain = self.total_lines % self.lines_per_page
        if remain > 0:
            self.total_pages += 1

    def make_sums(self, vat, pos, ajia):
        self.tpos += pos
        self.tajia += ajia
        self.dvat[vat] = self.dvat.get(vat, 0) + ajia

    def make(self, filename='invoice.pdf'):
        self.pdf.add_page()
        self.print_header()
        for i, el in enumerate(self.data['lines']):
            j = i % self.lines_per_page
            line = 104.5 + 3.6 * j
            fs = 9  # Μέγεθος γραμματοσειράς αναλυτικών γραμμών
            self.hp.txtl(10.1, line,  el['per'], fs)
            self.hp.txtc(105.0, line, el['mon'], fs)
            self.hp.num(self.col_posotita, line, dec.strGrDec(el['pos']), fs)
            self.hp.num(148.0, line, dec.strGrDec(el['timi']), fs)
            self.hp.txtc(155.0, line, '%s %%' % el['synt'], fs)
            ajia = round(el['pos'] * el['timi'], 2)
            self.make_sums(int(el['synt']), el['pos'], ajia)
            self.hp.num(self.col_ajia, line, dec.strGrDec(ajia), fs)
            if j == self.lines_per_page - 1 and i + 1 < self.total_lines:
                self.print_page_lines()
                self.print_page_footer(self.current_page)
                self.pdf.add_page()
                self.current_page += 1
                self.print_header()
        self.print_page_footer(self.current_page)
        self.print_invoice_footer()
        self.print_page_lines()
        self.pdf.output(filename)

    def print_header(self):
        self.pdf.set_line_width(1.0)
        logo = os.path.join(PATH, "fpdf/logo.png")
        self.pdf.image(logo, 11.0, 11.0, link='', type='', w=20.0, h=20)
        # Τύπος παραστατικού
        self.hp.txtcb(150.0, 47.5, self.data['ityp'], 12)
        # Γραμμή από μεταφορά
        if self.current_page > 1:
            rowa = 92.5
            smtxt = u'Από μεταφορά'
            self.hp.txtcb(50, rowa, smtxt)
            self.hp.numb(self.col_posotita, rowa, dec.strGrDec(self.tpos), 8)
            self.hp.numb(self.col_ajia, rowa, dec.strGrDec(self.tajia), 8)
        # Στοιχεία εκδότη
        afmdoyt = u'Α.Φ.Μ.: %s - Δ.Ο.Υ.: %s'
        afmdoy = afmdoyt % (self.data['cafm'], self.data['cdoy'])
        self.hp.txtcb(120, 12, self.data['cepo'], 18)
        self.hp.txtcb(120, 17, self.data['cepa'])
        self.hp.txtcb(120, 22, afmdoy)
        self.hp.txtcb(120, 26, self.data['cadr'])
        self.hp.txtcb(120, 30, self.data['cloi'])
        # Στοιχεία Πελάτη
        self.hp.txtlb(10.0, 46.0, u'Στοιχεία Πελάτη')
        l0 = 10.0
        l1 = 28.0
        self.hp.txtl(l0, 54, u'Επωνυμία')
        self.hp.txtl(l1, 54, ': %s' % self.data['pepo'])
        self.hp.txtl(l0, 58, u'Α.Φ.Μ.')
        self.hp.txtl(l1, 58, ': %s' % self.data['pafm'])
        self.hp.txtl(l0, 62, u'Δ.Ο.Υ.')
        self.hp.txtl(l1, 62, ': %s' % self.data['pdoy'])
        self.hp.txtl(l0, 66, u'Επάγγελμα')
        self.hp.txtl(l1, 66, ': %s' % self.data['pepa'])
        self.hp.txtl(l0, 70, u'Διεύθυνση')
        self.hp.txtl(l1, 70, ': %s' % self.data['pado'])
        self.hp.txtl(l0, 74, u'Πόλη - Τ.Κ.')
        self.hp.txtl(l1, 74, ': %s' % self.data['padp'])
        self.hp.txtl(l0, 78, u'Τηλέφωνο')
        self.hp.txtl(l1, 78, ': %s' % self.data['ptel'])
        # Στοιχεία παραστατικού
        l0 = 101.0
        l1 = 130.0
        self.hp.txtl(l0, 55.0, u'Αριθμός')
        self.hp.txtl(l1, 55.0, ': %s' % self.data['inum'])
        self.hp.txtl(l0, 60.0, u'Ημερομηνία - ώρα')
        self.hp.txtl(l1, 60.0, ': %s' % self.data['idat'])
        self.hp.txtl(l0, 65.0, u'Τρόπος πληρωμής')
        self.hp.txtl(l1, 65.0, ': %s' % self.data['ipli'])
        self.hp.txtl(l0, 70.0, u'Σκοπός διακίνησης')
        self.hp.txtl(l1, 70.0, ': %s' % self.data['isko'])
        self.hp.txtl(l0, 75.0, u'Τόπος αποστολής')
        self.hp.txtl(l1, 75.0, ': %s' % self.data['iapo'])
        self.hp.txtl(l0, 80.0, u'Τόπος προορισμού')
        self.hp.txtl(l1, 80.0, ': %s' % self.data['ipro'])
        # Τίτλοι αναλυτικών γραμμών παραστατικού
        trow = 98.0
        self.hp.txtcb(50, trow, u'Περιγραφή', 13)
        self.hp.txtcb(105, trow - 1.5, u'Μον.')
        self.hp.txtcb(105, trow + 1.5, u'Μετρ.')
        self.hp.txtcb(120.0, trow, u'ποσότητα', 12)
        self.hp.txtcb(139.0, trow - 1.5, u'Τιμή')
        self.hp.txtcb(139.0, trow + 1.5, u'Μονάδας')
        self.hp.txtcb(155.0, trow - 1.5, u'Συντ.')
        self.hp.txtcb(155.0, trow + 1.5, u'Φ.Π.Α.')
        self.hp.txtcb(169.0, trow, u'Έκπτωση')
        self.hp.txtcb(190.0, trow - 1.5, u'Καθαρή')
        self.hp.txtcb(190.0, trow + 1.5, u'Αξία')
        # Τίτλοι για πίνακα ανάλυσης ανά συντελεστή ΦΠΑ
        self.hp.txtcb(107, 242, 'Συντ.')
        self.hp.txtcb(107, 245.5, 'Φ.Π.Α.')
        self.hp.txtcb(129, 242, 'Αξία υποκείμενη')
        self.hp.txtcb(129, 245.5, 'σε Φ.Π.Α.')
        self.hp.txtcb(157.0, 244, 'Φ.Π.Α.', 13.0)
        self.hp.txtcb(185.0, 244, 'Σύνολο', 13.0)
        # ---------------------------------------------------------------
        # Εδώ κάνουμε τις γκρίζες γραμμές
        self.pdf.set_fill_color(230, 230, 230)
        bstart = 106.8
        bima = 7.22
        for i in range(17):  # 35 / 2 στρογγυλοποίηση προς τα κάτω
            self.pdf.set_xy(10.0, bstart + (i * bima))
            self.pdf.cell(0, 3.7, u"", 0, 1, 'R', 1)
        self.pdf.set_fill_color(256, 256, 256)
        # ---------------------------------------------------------------

    def print_page_footer(self, cpage):
        row = 233
        smtxt = u'Σελίδα %s από %s σε μεταφορά:' % (cpage, self.total_pages)
        if self.total_pages == self.current_page:
            smtxt = u'Σελίδα %s από %s σύνολα:' % (cpage, self.total_pages)

        self.hp.txtcb(50, row, smtxt)
        self.hp.numb(self.col_posotita, row, dec.strGrDec(self.tpos))
        self.hp.numb(self.col_ajia, row, dec.strGrDec(self.tajia))

    def print_page_lines(self):
        # Οριζόντιες γραμμές παραστατικού
        self.hp.hline(95.0, 10.0, 200.0, 0.0)
        self.hp.hline(102.0, 10.0, 200.0, 0.0)
        self.hp.hline(230.0, 10.0, 200.0, 0.0)
        self.hp.hline(248.0, 100.0, 200.0, 0.3)
        self.hp.hline(263.0, 114.0, 200.0, 0.3)
        # Κάθετες γραμμές παραστατικού
        self.hp.vline(100.0, 95.0, 230.0, 0.0)
        self.hp.vline(110.0, 95.0, 230.0, 0.0)
        self.hp.vline(130.0, 95.0, 230.0, 0.0)
        self.hp.vline(148.0, 95.0, 230.0, 0.0)
        self.hp.vline(161.0, 95.0, 230.0, 0.0)
        self.hp.vline(178.0, 95.0, 230.0, 0.0)
        self.hp.vline(114.0, 240.0, 270.0, 0.3)
        self.hp.vline(145.0, 240.0, 270.0, 0.3)
        self.hp.vline(170.0, 240.0, 270.0, 0.3)
        # Πλαίσιο στοιχείων πελατών
        self.hp.rect(10, 44, 87, 47, 0.3)
        # Πλαίσιο τύπου παραστατικού (ΤΙΜΟΛΟΓΙΟ-ΔΕΛΤΙΟ ΑΠΟΣΤΟΛΗΣ ΚΛΠ)
        self.hp.rect(100, 44, 100, 8, 0.3)
        # Πλαίσιο στοιχείων παραστατικού
        self.hp.rect(100, 53, 100, 38, 0.3)
        # Πλαίσιο αναλυτικών εγγραφών παραστατικού
        self.hp.rect(10, 95, 190, 135, 0.3)
        # Πλαίσιο πίνακα ανάλυσης ανά συντελεστή ΦΠΑ
        self.hp.rect(100, 240, 100, 30, 0.3)
        # Barcode here
        code = self.data['code']
        self.pdf.interleaved2of5(code, 10.0, 273.0, w=1.2)
        self.hp.txtl(10.0, 269.0, code)

    def print_invoice_footer(self):
        # Χρωματίζουμε κίτρινο το πεδίο με τη συνολική αξία του παραστατικού
        self.pdf.set_fill_color(255, 246, 94)
        self.pdf.set_xy(172.0, 264.0)
        self.pdf.cell(0, 5, u"", 0, 1, 'R', 1)
        i = 252.0
        step = 4
        tposo = tfpa = ttot = 0
        for key in self.dvat:
            poso = self.dvat[key]
            tposo += poso
            fpa = round(poso * key / 100.0, 2)
            tfpa += fpa
            tot = poso + fpa
            ttot += tot
            self.hp.txtc(107.0, i, '%s %%' % key)
            self.hp.num(145.0, i, dec.strGrDec(poso))
            self.hp.num(170.0, i, dec.strGrDec(fpa))
            self.hp.num(200.0, i, dec.strGrDec(tot))
            i += step
        self.hp.numb(145.0, 266.0, dec.strGrDec(tposo))
        self.hp.numb(170.0, 266.0, dec.strGrDec(tfpa))
        self.hp.numb(200.0, 266.0, dec.strGrDec(ttot))


if __name__ == '__main__':
    dati = [{'per': 'Δοκιμή', 'mon': 'Τεμ', 'pos': 1, 'timi': 1236.45,
             'synt': '0'},
            {'per': 'Δοκιμή2', 'mon': 'Κιλό', 'pos': 1.27, 'timi': 10,
             'synt': '24'},
            {'per': 'Λογιστικές υπηρεσίες', 'mon': 'Τεμ', 'pos': 2,
             'timi': 100, 'synt': '24'}]
    dat = {'name': 'test',
           'cepo': u'ΔΟΚΙΜΟΣ ΔΟΚΙΜΙΔΗΣ - ΔΟΚΙΜΗΣ ΔΟΚΙΜΑΣ ΟΕ',
           'cepa': u'Υπηρεσίες Τεχνικών Έργων - Αποχετεύσεις κλπ',
           'cafm': u'123456789',
           'cdoy': u"Α' Θεσσαλονίκης",
           'cadr': u'Ανδρέα Κάλβου 435, Αθήνα - Τ.Κ.: 132 53',
           'cloi': u'Α.Ρ.Γ.Ε.ΜΗ: 123456789123 - ΑΡ.ΜΗΤΡ.ΠΡΟΜ. 1447/2000',
           'ctel': u'210 86 54 713',
           'pepo': u'Παλλικαρίδης Δοκιμές ΕΠΕ',
           'pafm': u'012345678',
           'pdoy': u'Τρίπολης',
           'pepa': u'Εμπόριο χάρτου',
           'pado': u'Καλάμου 14',
           'padp': u'Τρίπολη 123 48',
           'ptel': u'2247 46 578',
           'ityp': u'ΤΙΜΟΛΟΓΙΟ - ΔΕΛΤΙΟ ΑΠΟΣΤΟΛΗΣ',
           'inum': u'10334',
           'idat': u'15/02/2015 12:45',
           'ipli': u'Πίστωση 20 μέρες',
           'isko': u'Πώληση',
           'iapo': u'Έδρα μας',
           'ipro': u'Έδρα τους',
           'code': '1506081420144369',
           'lines': dati * 60}
    inv = Invoice(dat)
    inv.make('ted.pdf')
    # make_pdf(data*20)
