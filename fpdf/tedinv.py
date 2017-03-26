# -*- coding: utf-8 -*-

import os
from fpdf import FPDF
from fpdf.ted_helper import Helper
import sys

'''
PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if PATH not in sys.path:
    sys.path.append(PATH)
'''

pdf = FPDF()
hp = Helper(pdf)
pdf.add_font('fn', '', 'times.ttf', uni=True)
pdf.add_font('fb', '', 'timesb.ttf', uni=True)
pdf.add_font('fi', '', 'timesi.ttf', uni=True)
pdf.set_title('A Test Title')
pdf.add_page()


def texts():
    # hp.line(11.0, 12.0, 100.0, 12.0)
    hp.hline(12.0, 11.0, 100.0)
    hp.txtl(11.0, 12.0, 'Για να δούμε ρε φίλε', 30.0)
    # hp.line(105.0, 20.0, 105.0, 60.0)
    hp.vline(105, 20.0, 40.0, .4)
    hp.txtcb(105.0, 20.0, 'A', 22.0)
    hp.txtci(105.0, 30.0, 'AA')
    hp.txtci(105.0, 40.0, 'AAA')
    hp.num(99.0, 105.0, '15,00')
    hp.numb(99.0, 109.0, '150,00')
    hp.numi(99.0, 113.0, '1.500,00')
    hp.num(99.0, 117.0, '15.000,00')


def lines():
    hp.line(10.0, 102.0, 200.0, 102.0)
    hp.line(20.0, 98.0, 20.0, 102.0)
    hp.line(25.0, 98.0, 25.0, 102.0)
    hp.line(30.0, 98.0, 30.0, 102.0)
    hp.txtc(17.0, 99.0, 'α')
    hp.txtc(22.0, 99.0, 'a')
    hp.txtc(27.0, 99.0, 'a')
    hp.line(100.0, 102.0, 100.0, 200.0)
    hp.line(80.0, 102.0, 80.0, 200.0)


hp.donti(x=15, y=180, mikos=60, theseis=14, platos=3)
hp.donti(x=15, y=200, mikos=35, theseis=7, platos=3)
hp.boxes(x=15, y=220, mikos=35, theseis=7, platos=6)

for i, letter in enumerate('abcdefg'):
    hp.txtc(17.0 + (i * 5), 216.5, letter)

hp.rect(10.0, 10.0, 190.0, 280.0)
hp.rect(10.0, 10.0, 100.0, 100.0)
texts()
lines()
hp.boxetit(15, 210, 'test', 'we23')
pdf.add_page()
texts()
lines()
pdf.output('./tedinv.pdf', 'F')


os.system("xdg-open ./tedinv.pdf")
