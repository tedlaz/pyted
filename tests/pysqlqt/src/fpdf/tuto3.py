# -*- coding: utf-8 -*-
'''
Test invoice to pdf
'''
from fpdf import FPDF

TITLE = u'Δοκιμαστικό κείμενο για τουθ κάλους και καλά κρασιά'


class PDF(FPDF):
    '''
    Final class ...
    '''
    def header(self):
        '''Arial bold 15'''
        self.add_font('alkaios', '', 'Alkaios.ttf', True)
        self.add_font('alkaios', 'I', 'Alkaios-Italic.ttf', True)
        self.add_font('alkaios', 'B', 'Alkaios-Bold.ttf', True)
        self.set_font('alkaios', 'B', 15)
        # Calculate width of title and position
        width = self.get_string_width(TITLE) + 6
        self.set_x((210 - width) / 2)
        # Colors of frame, background and text
        self.set_draw_color(255, 155, 255)
        self.set_fill_color(155, 255, 255)
        self.set_text_color(0, 0, 0)
        # Thickness of frame (1 mm)
        self.set_line_width(0.2)
        # title
        self.hyd(6)
        self.hyd(20)
        self.hyd(30)
        self.text(10, 20, 'Testing this status')
        self.cell(width, 9, TITLE, 1, 0, 'C', 0)

        # Line break
        self.ln(10)

    def hyd(self, rotation):
        '''Rotate'''
        self.rotate(rotation)
        self.text(10, 20, 'Testing this status')
        self.rotate(0)

    def footer(self):
        '''Position at 1.5 cm from bottom'''
        self.set_y(-15)
        # Arial italic 8
        self.set_font('alkaios', '', 8)
        # Text color in gray
        self.set_text_color(0)
        # Page number
        self.cell(0, 10, u'Σελίδα ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        '''Chapter Title'''
        self.set_font('alkaios', 'B', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, u"Κεφάλαιο %d : %s" % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        '''Read text file'''
        txt = file(name).read()
        # Times 12
        self.set_font('alkaios', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')
        self.cell(0, 5, '(end of excerpt)')

    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)


pdf = PDF(orientation='P')
pdf.set_title('just a testing')
pdf.set_subject('General Subject !!')
pdf.set_author('Jules Verne')
pdf.set_keywords('This is a test document')
pdf.print_chapter(1, u'ΤΗΣ ΠΟΥΤΑΝΑΣ ΤΟ ΚΑΓΓΕΛΟ', '20k_c1.txt')
pdf.print_chapter(2, u'ΓΑΜΗΣΕ ΤΑ ΚΑΙ ΑΦΗΣΕ ΤΑ', '20k_c2.txt')
pdf.output('tuto3.pdf')
