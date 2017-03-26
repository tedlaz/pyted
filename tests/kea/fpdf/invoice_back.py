# -*- coding: utf-8 -*-
# Invoice creation

import os
from fpdf import FPDF
import sys
import dec

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
        self.pdf.add_font('fnt', '', 'times.ttf', True)
        self.pdf.add_font('fnt', 'I', 'timesi.ttf', True)
        self.pdf.add_font('fnt', 'B', 'timesbd.ttf', True)
        self.data = datad
        self.lines_per_page = 40
        self.total_lines = len(self.data['lines'])
        self.tpos = 0
        self.tajia = 0
        self.dvat = {}
        # Calculate total invoice pages
        self.total_pages = int(self.total_lines / float(self.lines_per_page))
        remain = self.total_lines % self.lines_per_page
        if remain > 0:
            self.total_pages += 1

    def make_sums(self, vat, pos, ajia):
        self.tpos += pos
        self.tajia += ajia
        self.dvat[vat] = self.dvat.get(vat, 0) + ajia

    def make(self):
        self.pdf.add_page()
        self.print_header()

        current_page = 1

        for i, el in enumerate(self.data['lines']):
            j = i % self.lines_per_page
            line = 104.0 + 3 * j

            self.pdf.set_font('fnt', '', 9.0)
            self.pdf.set_txt(line, 10.1, el['per'], 90.0, 'L', 0)
            self.pdf.set_txt(line, 100.5, el['mon'], 9.0, 'C', 0)
            self.pdf.set_txt(line, 111.0,
                             dec.strGrDec(el['pos']), 17.0, 'R', 0)
            self.pdf.set_txt(line, 130.0,
                             dec.strGrDec(el['timi']), 17.0, 'R', 0)
            self.pdf.set_txt(line, 148.3, el['synt'], 13.0, 'C', 0)
            ajia = round(el['pos'] * el['timi'], 2)
            self.make_sums(int(el['synt']), el['pos'], ajia)
            self.pdf.set_txt(line, 178.0, dec.strGrDec(ajia), 20.0, 'R', 0)
            if j == self.lines_per_page - 1 and i + 1 < self.total_lines:
                self.print_page_lines()
                self.print_page_footer(current_page)
                self.pdf.add_page()
                self.print_header()
                current_page += 1
        self.print_page_footer(current_page)
        self.print_invoice_footer()
        self.print_page_lines()
        self.pdf.output('./invoice.pdf')

    def print_header(self):
        self.pdf.set_line_width(1.0)
        self.pdf.image('logo.png', 11.0, 11.0, link='', type='', w=20.0, h=20)

        self.pdf.set_font('fnt', 'B', 11.0)
        self.pdf.set_txt(45.0, 101, self.data['ityp'], 96.0, 'C', 0)

        l0 = 101.0
        l1 = 130.0
        self.pdf.set_font('fnt', '', 10.0)
        self.pdf.set_txt(55.0, l0, u'Αριθμός', 20.0, 'L', 0)
        self.pdf.set_txt(55.0, l1, ': %s' % self.data['inum'], 20.0, 'L', 0)
        self.pdf.set_txt(60.0, l0, u'Ημερομηνία - ώρα', 25.0, 'L', 0)
        self.pdf.set_txt(60.0, l1, ': %s' % self.data['idat'], 23.0, 'L', 0)
        self.pdf.set_txt(65.0, l0, u'Τρόπος πληρωμής', 20.0, 'L', 0)
        self.pdf.set_txt(65.0, l1, ': %s' % self.data['ipli'], 40.0, 'L', 0)
        self.pdf.set_txt(70.0, l0, u'Σκοπός διακίνησης', 20.0, 'L', 0)
        self.pdf.set_txt(70.0, l1, ': %s' % self.data['isko'], 40.0, 'L', 0)
        self.pdf.set_txt(75.0, l0, u'Τόπος αποστολής', 20.0, 'L', 0)
        self.pdf.set_txt(75.0, l1, ': %s' % self.data['iapo'], 40.0, 'L', 0)
        self.pdf.set_txt(80.0, l0, u'Τόπος προορισμού', 20.0, 'L', 0)
        self.pdf.set_txt(80.0, l1, ': %s' % self.data['ipro'], 40.0, 'L', 0)

        self.pdf.set_font('fnt', 'B', 14.0)
        self.pdf.set_txt(12, 35.0, self.data['cepo'], 155.0, 'C', 0)
        self.pdf.set_font('fnt', 'B', 10.0)
        self.pdf.set_txt(17, 35.0, self.data['cepa'], 155.0, 'C', 0)
        self.pdf.set_txt(22, 35.0, u'Α.Φ.Μ.: %s - Δ.Ο.Υ.: %s' % (
            self.data['cafm'], self.data['cdoy']), 155.0, 'C', 0)
        self.pdf.set_txt(26, 35.0, self.data['cadr'], 155.0, 'C', 0)
        self.pdf.set_txt(30, 35.0, self.data['cloi'], 155.0, 'C', 0)

        self.pdf.set_font('fnt', 'B', 10.0)
        self.pdf.set_txt(44.0, 10.0, u'Στοιχεία Πελάτη', 13.0, 'L', border=0)

        l0 = 10.0
        l1 = 28.0
        self.pdf.set_font('fnt', '', 10.0)
        self.pdf.set_txt(50.0, l0, u'Επωνυμία', 20.0, 'L', border=0)
        self.pdf.set_txt(50.0, l1, ': %s' % self.data['pepo'],
                         60.0, 'L', border=0)
        self.pdf.set_txt(54.0, l0, u'Α.Φ.Μ.', 20.0, 'L', border=0)
        self.pdf.set_txt(54.0, l1, ': %s' % self.data['pafm'],
                         20.0, 'L', border=0)
        self.pdf.set_txt(58.0, l0, u'Δ.Ο.Υ.', 20.0, 'L', border=0)
        self.pdf.set_txt(58.0, l1, ': %s' % self.data['pdoy'],
                         20.0, 'L', border=0)
        self.pdf.set_txt(62.0, l0, u'Επάγγελμα', 20.0, 'L', border=0)
        self.pdf.set_txt(62.0, l1, ': %s' % self.data['pepa'],
                         60.0, 'L', border=0)
        self.pdf.set_txt(66.0, l0, u'Διεύθυνση', 18.0, 'L', border=0)
        self.pdf.set_txt(66.0, l1, ': %s' % self.data['pado'],
                         70.0, 'L', border=0)
        self.pdf.set_txt(70.0, l0, u'Πόλη - Τ.Κ.', 18.0, 'L', border=0)
        self.pdf.set_txt(70.0, l1, ': %s' % self.data['padp'],
                         22.0, 'L', border=0)
        self.pdf.set_txt(74.0, l0, u'Τηλέφωνο', 18.0, 'L', border=0)
        self.pdf.set_txt(74.0, l1, ': %s' % self.data['ptel'],
                         30.0, 'L', border=0)

        self.pdf.set_font('fnt', 'B', 9.0)
        self.pdf.set_txt(96.0, 10.1, 'Περιγραφή', 90.0, 'C', 0)
        self.pdf.set_txt(94.5, 100.5, 'Μον.', 9.0, 'C', 0)
        self.pdf.set_txt(97.5, 100.5, 'Μετρ.', 9.0, 'C', 0)
        self.pdf.set_txt(96.0, 111.0, 'Ποσότητα', 17.0, 'C', 0)
        self.pdf.set_txt(94.5, 130.0, 'Τιμή', 17.0, 'C', 0)
        self.pdf.set_txt(97.5, 130.0, 'Μονάδας', 17.0, 'C', 0)
        self.pdf.set_txt(94.5, 148.3, 'Συντ.', 13.0, 'C', 0)
        self.pdf.set_txt(97.5, 148.3, 'Φ.Π.Α.', 13.0, 'C', 0)
        self.pdf.set_txt(94.5, 178.0, 'Καθαρή', 20.0, 'C', 0)
        self.pdf.set_txt(97.5, 178.0, 'Αξία', 20.0, 'C', 0)

        self.pdf.set_font('fnt', 'B', 9.0)
        self.pdf.set_txt(240.3, 101, '%', 13.0, 'C', 0)
        self.pdf.set_txt(243, 101, 'Φ.Π.Α.', 13.0, 'C', 0)
        self.pdf.set_txt(240.3, 122, 'Αξία υποκείμενη', 13.0, 'C', 0)
        self.pdf.set_txt(243, 122, 'σε Φ.Π.Α.', 13.0, 'C', 0)
        self.pdf.set_txt(242, 151, 'Φ.Π.Α.', 13.0, 'C', 0)
        self.pdf.set_txt(242, 180, 'Σύνολο', 13.0, 'C', 0)

    def print_page_footer(self, cpage):
        row = 230
        self.pdf.set_font('fnt', 'B', 9.0)
        self.pdf.set_txt(row, 111, '%s' % dec.strGrDec(self.tpos), 17, 'R', 0)
        self.pdf.set_txt(row, 178, '%s' % dec.strGrDec(self.tajia), 20, 'R', 0)
        if self.total_pages == 1:
            return

        self.pdf.set_txt(
            row,
            50,
            u'Σελίδα %s από %s σε μεταφορά' % (cpage, self.total_pages),
            20.0, 'R', 0)

    def print_page_lines(self):
        self.pdf.line_horizontal(95.0, 10.0, 200.0, 0.0)
        self.pdf.line_horizontal(102.0, 10.0, 200.0, 0.0)
        self.pdf.line_horizontal(230.0, 10.0, 200.0, 0.0)
        self.pdf.line_horizontal(248.0, 100.0, 200.0, 0.3)
        self.pdf.line_horizontal(263.0, 114.0, 200.0, 0.3)

        self.pdf.line_vertical(100.0, 95.0, 230.0, 0.0)
        self.pdf.line_vertical(110.0, 95.0, 230.0, 0.0)
        self.pdf.line_vertical(130.0, 95.0, 230.0, 0.0)
        self.pdf.line_vertical(148.0, 95.0, 230.0, 0.0)
        self.pdf.line_vertical(161.0, 95.0, 230.0, 0.0)
        self.pdf.line_vertical(178.0, 95.0, 230.0, 0.0)
        self.pdf.line_vertical(114.0, 240.0, 270.0, 0.3)
        self.pdf.line_vertical(145.0, 240.0, 270.0, 0.3)
        self.pdf.line_vertical(170.0, 240.0, 270.0, 0.3)

        # self.pdf.rectw(10, 10, 190, 31, '', 0.3)
        self.pdf.rectw(10, 44, 87, 47, '', 0.3)
        self.pdf.rectw(100, 44, 100, 8, '', 0.3)
        self.pdf.rectw(100, 53, 100, 38, '', 0.3)
        self.pdf.rectw(10, 95, 190, 135, '', 0.3)
        self.pdf.rectw(100, 240, 100, 30, '', 0.3)

        # Barcode here
        code = self.data['code']
        self.pdf.interleaved2of5(code, 10.0, 273.0, w=1.2)
        self.pdf.set_font('courier', '', 10.0)
        self.pdf.set_txt(269.0, 11.0, code, 40.0, 'L', 0)

    def print_invoice_footer(self):
        self.pdf.set_fill_color(255, 246, 94)
        self.pdf.set_xy(172.0, 264.0)
        self.pdf.cell(0, 5, u"", 0, 1, 'R', 1)
        self.pdf.set_font('fnt', '', 9.0)
        i = 248
        step = 3
        tposo = tfpa = ttot = 0

        for key in self.dvat:
            poso = self.dvat[key]
            tposo += poso
            fpa = round(poso * key / 100.0, 2)
            tfpa += fpa
            tot = poso + fpa
            ttot += tot
            self.pdf.set_txt(i, 101, dec.strGrDec(key), 13.0, 'C', 0)
            self.pdf.set_txt(i, 116, dec.strGrDec(poso), 26.0, 'R', 0)
            self.pdf.set_txt(i, 142, dec.strGrDec(fpa), 26.0, 'R', 0)
            self.pdf.set_txt(i, 172, dec.strGrDec(tot), 26.0, 'R', 0)
            i += step
        self.pdf.set_font('fnt', 'B', 10.0)
        self.pdf.set_txt(264, 116, dec.strGrDec(tposo), 26.0, 'R', 0)
        self.pdf.set_txt(264, 142, dec.strGrDec(tfpa), 26.0, 'R', 0)
        self.pdf.set_txt(264, 172, dec.strGrDec(ttot), 26.0, 'R', 0)


if __name__ == '__main__':
    dati = [{'per': 'Δοκιμή', 'mon': 'Τεμ', 'pos': 2, 'timi': 1236.45,
             'synt': '13'},
            {'per': 'Δοκιμή2', 'mon': 'Τεμ', 'pos': 1, 'timi': 10,
             'synt': '10'},
            {'per': 'Λογιστικές υπηρεσίες', 'mon': 'Τεμ', 'pos': 1,
             'timi': 100, 'synt': '23'}]
    dat = {'name': 'test',
           'cepo': u'ΔΟΚΙΜΟΣ ΔΟΚΙΜΙΔΗΣ - ΔΟΚΙΜΗΣ ΔΟΚΙΜΑΣ ΟΕ - σκατά',
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
           'ityp': u'ΤΙΜΟΛΟΓΙΟ ΠΑΡΟΧΗΣ ΥΠΗΡΕΣΙΩΝ',
           'inum': u'10334',
           'idat': u'15/02/2015 12:45',
           'ipli': u'Πίστωση 20 μέρες',
           'isko': u'Πώληση',
           'iapo': u'Έδρα μας',
           'ipro': u'Έδρα τους',
           'code': '1506081420144369',
           'lines': dati * 200}
    inv = Invoice(dat)
    inv.make()
    # make_pdf(data*20)
