# -*- coding: utf-8 -*-

import os
from fpdf import FPDF
import sys
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

    def make(self):
        self.pdf.add_page()
        self.print_header()
        total_lines = len(self.data['lines'])
        lines_per_page = 25
        for i, el in enumerate(self.data['lines']):
            j = i % lines_per_page
            line = 103.0 + 5 * j
            if j % 2 == 1:
                #self.pdf.set_fill_color(220, 235, 255)
                #self.pdf.set_xy(10.1, line)
                #self.pdf.cell(0, 5, u"", 0, 1, 'L', 1)
                pass
            else:
                self.pdf.set_fill_color(255, 255, 255)
            self.pdf.set_font('fnt', '', 9.0)
            self.pdf.set_txt(line, 10.1, el['per'], 90.0, 'L', 0)
            self.pdf.set_txt(line, 100.5, el['mon'], 9.0, 'C', 0)
            self.pdf.set_txt(line, 111.0, el['pos'], 17.0, 'R', 0)
            self.pdf.set_txt(line, 130.0, el['timi'], 17.0, 'R', 0)
            self.pdf.set_txt(line, 148.3, el['synt'], 13.0, 'C', 0)
            self.pdf.set_txt(line, 178.0, el['ajia'], 20.0, 'R', 0)
            if j == lines_per_page - 1 and i+1 < total_lines:
                self.print_page_lines()
                self.print_page_footer()
                self.pdf.add_page()
                self.print_header()
        self.print_invoice_footer()
        self.print_page_lines()
        self.pdf.output('./invoice.pdf')

    def print_header(self):
        self.pdf.set_line_width(1.0)
        self.pdf.image('logo.png', 11.0, 11.0, link='', type='', w=20.0, h=4.2)

        self.pdf.set_font('fnt', 'B', 11.0)
        self.pdf.set_txt(45.0, 101, u'ΤΙΜΟΛΟΓΙΟ ΠΩΛΗΣΗΣ - ΔΕΛΤΙΟ ΑΠΟΣΤΟΛΗΣ', 96.0, 'C', 0)

        self.pdf.set_font('fnt', '', 10.0)
        self.pdf.set_txt(55.0, 101.0, u'Αριθμός', 20.0, 'L', 0)
        self.pdf.set_txt(55.0, 130.0, u': 00000001', 20.0, 'L', 0)
        self.pdf.set_txt(60.0, 101.0, u'Ημερομηνία - ώρα', 25.0, 'L', 0)
        self.pdf.set_txt(60.0, 130.0, ': 19/02/2009 14:30', 23.0, 'L', 0)
        self.pdf.set_txt(65.0, 101.0, u'Τρόπος πληρωμής', 20.0, 'L', 0)
        self.pdf.set_txt(65.0, 130.0, u': Πίστωση 30 ημερών', 40.0, 'L', 0)
        self.pdf.set_txt(70.0, 101.0, u'Σκοπός διακίνησης', 20.0, 'L', 0)
        self.pdf.set_txt(70.0, 130.0, u': Πώληση', 40.0, 'L', 0)
        self.pdf.set_txt(75.0, 101.0, u'Τόπος αποστολής', 20.0, 'L', 0)
        self.pdf.set_txt(75.0, 130.0, u': Έδρα μας', 40.0, 'L', 0)
        self.pdf.set_txt(80.0, 101.0, u'Τόπος προορισμού', 20.0, 'L', 0)
        self.pdf.set_txt(80.0, 130.0, u': Έδρα τους', 40.0, 'L', 0)

        self.pdf.set_font('fnt', 'B', 24.0)
        self.pdf.set_txt(10, 10.0, u'ΑΦΟΙ ΜΑΛΑΚΟΓΙΑΝΝΗ ΕΠΕ', 190.0, 'C', 0)
        self.pdf.set_font('fnt', '', 10.0)
        self.pdf.set_txt(15, 10.0, u'Α.Φ.Μ.: 012345678, κλπ, κλπ, κλπ', 190.0, 'C', 0)

        self.pdf.set_font('fnt', '', 10.0)
        self.pdf.set_txt(59.0, 17.0, u'Λήπτης:', 13.0, 'L', border=0)
        self.pdf.set_txt(59.0, 35.0, u'Λαμόγιας Άγγελος', 140.0, 'L', border=0)
        self.pdf.set_txt(64.0, 17.0, u'Διεύθυνση:', 18.0, 'L', border=0)
        self.pdf.set_txt(64.0, 35.0, u'Σισμανογλείου 44', 125.0, 'L', border=0)
        self.pdf.set_txt(69.0, 17.0, u'Τηλέφωνο:', 18.0, 'L', border=0)
        self.pdf.set_txt(69.0, 35.0, '210 40 35 455', 30.0, 'L', border=0)
        self.pdf.set_txt(74.0, 17.0, u'Πόλη:', 18.0, 'L', border=0)
        self.pdf.set_txt(74.0, 35.0, u'Αθήνα', 22.0, 'L', border=0)

        self.pdf.set_txt(80.0, 17.0, u'ΑΦΜ :', 15.0, 'L', border=0)
        self.pdf.set_txt(80.0, 28.0, '123456789', 25.0, 'L', border=0)

        self.pdf.set_font('fnt', 'B', 9.0)
        self.pdf.set_txt(96.0, 10.1, 'Περιγραφή', 90.0, 'C', 0)
        self.pdf.set_txt(94.5, 100.5, 'Μον.', 9.0, 'C', 0)
        self.pdf.set_txt(97.5, 100.5, 'Μετρ.', 9.0, 'C', 0)
        self.pdf.set_txt(96.0, 111.0, 'Ποσότητα', 17.0, 'C', 0)
        self.pdf.set_txt(94.5, 130.0, 'Τιμή', 17.0, 'C', 0)
        self.pdf.set_txt(97.5, 130.0, 'Μονάδας', 17.0, 'C', 0)
        self.pdf.set_txt(94.5, 148.3, 'Συντ.', 13.0, 'C', 0)
        self.pdf.set_txt(97.5, 148.3, 'Φ.Π.Α.', 13.0, 'C', 0)
        self.pdf.set_txt(94.5, 161.0, 'Καθαρή', 20.0, 'C', 0)
        self.pdf.set_txt(97.5, 161.0, 'Αξία', 20.0, 'C', 0)

        self.pdf.set_font('fnt', 'B', 9.0)
        self.pdf.set_txt(240.3, 101, '%', 13.0, 'C', 0)
        self.pdf.set_txt(243, 101, 'Φ.Π.Α.', 13.0, 'C', 0)
        self.pdf.set_txt(240.3, 122, 'Αξία υποκείμενη', 13.0, 'C', 0)
        self.pdf.set_txt(243, 122, 'σε Φ.Π.Α.', 13.0, 'C', 0)
        self.pdf.set_txt(242, 151, 'Φ.Π.Α.', 13.0, 'C', 0)
        self.pdf.set_txt(242, 180, 'Σύνολο', 13.0, 'C', 0)

    def print_page_footer(self):
        pass

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
        self.pdf.line_vertical(114.0, 240.0, 270.0, 0.3)
        self.pdf.line_vertical(145.0, 240.0, 270.0, 0.3)
        self.pdf.line_vertical(170.0, 240.0, 270.0, 0.3)

        self.pdf.rectw(100, 44, 100, 47, '', 0.3)
        self.pdf.rectw(10, 95, 190, 135, '', 0.3)
        self.pdf.rectw(100, 240, 100, 30, '', 0.3)

        code = '1506081420144360'
        self.pdf.interleaved2of5(code, 10.0, 273.0, w=1.2)
        self.pdf.set_font('courier', '', 10.0)
        self.pdf.set_txt(269.0, 11.0, code, 40.0, 'L', 0)

    def print_invoice_footer(self):
        self.pdf.set_fill_color(255, 246, 94)
        self.pdf.set_xy(172.0, 264.0)
        self.pdf.cell(0, 5, u"", 0, 1, 'R', 1)
        self.pdf.set_font('fnt', '', 9.0)
        self.pdf.set_txt(248, 101, '13', 13.0, 'C', 0)
        self.pdf.set_txt(248, 116, '2.435,82', 26.0, 'R', 0)
        self.pdf.set_txt(248, 142, '582,45', 26.0, 'R', 0)
        self.pdf.set_txt(248, 172, '3.156,48', 26.0, 'R', 0)
        self.pdf.set_txt(252, 101, '26', 13.0, 'C', 0)
        self.pdf.set_txt(252, 116, '2.435,82', 26.0, 'R', 0)
        self.pdf.set_txt(252, 142, '582,45', 26.0, 'R', 0)
        self.pdf.set_txt(252, 172, '3.156,48', 26.0, 'R', 0)
        self.pdf.set_txt(256, 101, '6.5', 13.0, 'C', 0)
        self.pdf.set_txt(256, 116, '2.435,82', 26.0, 'R', 0)
        self.pdf.set_txt(256, 142, '582,45', 26.0, 'R', 0)
        self.pdf.set_txt(256, 172, '3.156,48', 26.0, 'R', 0)
        self.pdf.set_font('fnt', 'B', 10.0)
        self.pdf.set_txt(264, 116, '2.435,82', 26.0, 'R', 0)
        self.pdf.set_txt(264, 142, '582,45', 26.0, 'R', 0)
        self.pdf.set_txt(264, 172, '3.156,48', 26.0, 'R', 0)


if __name__ == '__main__':
    dati = [{'per': 'Δοκιμή', 'mon': 'Τεμ', 'pos': '1', 'timi': '10,00', 'synt': '13', 'ajia': '10,00'},
            {'per': 'Δοκιμή2', 'mon': 'Τεμ', 'pos': '10', 'timi': '12,31', 'synt': '13', 'ajia': '123,10'},
            {'per': 'Εκτυπωτής Brother', 'mon': 'Λίτρο', 'pos': '1', 'timi': '1.252,45', 'synt': '23', 'ajia': '1.252,45'}]
    dat = {'name': 'test', 'lines': dati}
    inv = Invoice(dat)
    inv.make()
    #make_pdf(data*20)
