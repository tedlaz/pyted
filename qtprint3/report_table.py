# -*- coding: utf-8 -*-
'''
Created on 3 Mar 2013

@author: tedlaz

version 1.0
'''
import decimal
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtPrintSupport as Qp

PAGE_NUMBER_TEXT = 'Σελίδα'


def isNum(value):  # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters :
            1.value : the value to check against.
        output: True or False
    """
    if not value:
        return False
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


def dec(poso, dekadika=2):
    """Return a decimal"""
    PLACES = decimal.Decimal(10) ** (-1 * dekadika)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


# Utility Functions
def gr(number):
    'Returns Greek Decimal(2) number or empty space'
    number = dec(number)
    if abs(number) <= 0.004:
        return ''
    s = '%.2f' % number
    int_part, decimal_part = s.split('.')
    groups = []
    while int_part and int_part[-1].isdigit():
        groups.append(int_part[-3:])
        int_part = int_part[:-3]
    return int_part + '.'.join(reversed(groups)) + ',' + decimal_part


def gr0(number):
    'Returns Greek Decimal(2) number or 0,00'
    number = dec(number)
    if abs(number) <= 0.004:
        return '0,00'
    s = '%.2f' % number
    int_part, decimal_part = s.split('.')
    groups = []
    while int_part and int_part[-1].isdigit():
        groups.append(int_part[-3:])
        int_part = int_part[:-3]
    return int_part + '.'.join(reversed(groups)) + ',' + decimal_part


def grint(number):
    'Returns Greek Decimal(1) number'
    number = dec(number)
    if abs(number) <= 0.004:
        return ''
    s = '%.1f' % number
    int_part, decimal_part = s.split('.')
    groups = []
    while int_part and int_part[-1].isdigit():
        groups.append(int_part[-3:])
        int_part = int_part[:-3]
    return int_part + '.'.join(reversed(groups)) + ',' + decimal_part


def grd(imnia):
    'Returns Greek Date'
    year, month, date = imnia.split('-')
    return '%s/%s/%s' % (date, month, year)


def align(opt=0):
    if opt == 0:
        option = Qg.QTextOption(Qc.Qt.AlignLeft | Qc.Qt.AlignVCenter)
    elif opt == 1:
        option = Qg.QTextOption(Qc.Qt.AlignCenter | Qc.Qt.AlignVCenter)
    else:
        option = Qg.QTextOption(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
    option.setWrapMode(Qg.QTextOption.WordWrap)
    return option


LEFT, CENTER, RIGHT = align(0), align(1), align(2)


def frmt(val, typos):
    if typos == 0:  # String
        frmtVal = '%s' % val
    elif typos == 1:  # Integer
        frmtVal = '%s' % val
    elif typos == 2:  # Decimal
        frmtVal = gr(val)
    elif typos == 3:  # Date
        frmtVal = grd(val)
    elif typos == 4:  # Decimal with one decimal digit
        frmtVal = grint(val)
    else:
        frmtVal = '%s' % val
    return frmtVal


def mfont(family, size, bold=False, italic=False):
    new_font = Qg.QFont(family, size)
    if bold:
        new_font.setBold(True)
    if italic:
        new_font.setItalic(True)
    return new_font


class TableReport():
    def __init__(self, f, dfi):
        self.f = f
        self.f['data'] = dfi
        self.printer = Qp.QPrinter()
        # Set portrait or landscape
        if self.f['orientation'] in (0, 'portrait'):
            self.printer.setOrientation(Qp.QPrinter.Portrait)
        else:
            self.printer.setOrientation(Qp.QPrinter.Landscape)
        self.pageRect = self.printer.pageRect()
        self.max_width = self.pageRect.width()
        self.max_height = self.pageRect.height()
        self.x_left, self.y_top = 52, 52
        # Συνολικό ωφέλιμο μήκος σελίδας
        self.net_width = self.pageRect.width() - 2 * self.x_left + 13
        self.net_height = self.pageRect.height() - 2 * self.y_top + 13
        self.net_height_table = self.pageRect.height() - 95
        self.max_x = self.x_left + self.net_width
        fontSize = f.get('fontsize', 9)
        self.x_off = self.y_off = f.get('offset', 3)
        # Set Fonts
        family = self.f.get('fontFamily', 'Helvetica')
        self.font_h1 = mfont(family, 20, bold=True)
        self.font_h2 = mfont(family, 12, bold=True, italic=True)
        self.font_h3 = mfont(family, 10, italic=True)
        self.font_th = mfont(family, fontSize, bold=True)  # table header
        self.font_tl = mfont(family, fontSize)  # table line
        self.font_pf = mfont(family, fontSize)  # page footer
        self.tableMetrics = Qg.QFontMetrics(self.font_tl)
        self.tableHeaderHeight = int(self.tableMetrics.height() * 3)
        self.tableColumnHeight = int(self.tableMetrics.height() * 1.7)
        # Το πλάτος των στηλών
        self.colWidths = [self.tableMetrics.width('w' * i) +
                          self.x_off for i in self.f['columnSizes']]
        self.totalColWidths = sum(self.colWidths)
        # Ο αριθμός των στηλών
        self.column_number = len(self.colWidths)
        self.y_footer = self.pageRect.height() - 54

    def report(self):
        '''Here we assemble the pieces to make the final report'''
        # Για κάποιο άγνωστο λόγο δεν μπορεί να οριστεί στο __init__
        self.pnt = Qg.QPainter(self.printer)
        self.x = self.x_left
        self.y = self.y_top
        self.page_number = 1
        # self.fix_painter_bug()
        self.report_header()
        # self.page_header()
        self.page_footer()
        self.table_header()
        self.table_lines()
        # self.box()
        self.table_footer()
        self.pnt.end()  # Πρέπει οπωσδήποτε να υπάρχει αυτό στο τέλος

    def report_header(self, hspaceAfter=20):
        self.text_centered(
            self.f['ReportHeader1'], self.font_h1, spaceAfter=25)
        self.text_centered(
            self.f['ReportHeader2'], self.font_h2, spaceAfter=20)
        self.text_centered(
            self.f['ReportHeader3'], self.font_h3, spaceAfter=20)
        self.y += hspaceAfter

    def fix_painter_bug(self):
        'This is a workaround for painter to paint lines properly'
        self.pnt.setPen(Qc.Qt.NoPen)
        self.pnt.setPen(Qc.Qt.black)

    def page_header(self, painter):
        pass

    def hline(self, xvl, yvl, x_end, width=None, dots=False):
        """Draw horizontal lines"""
        self.pnt.save()
        pen = Qg.QPen()
        pen.setColor(Qc.Qt.black)
        if dots:
            pen.setStyle(Qc.Qt.DotLine)
        if width:
            pen.setWidth(width)
        self.pnt.setPen(pen)
        self.pnt.drawLine(xvl, yvl, x_end, yvl)
        self.pnt.restore()

    def txt(self, wid, hei, val, align, font, off=3):
        """Draw text to canvas"""
        self.pnt.save()
        self.pnt.setFont(font)
        xvl = self.x + off
        yvl = self.y + off
        flags = Qc.Qt.TextDontClip | Qc.Qt.TextWordWrap
        drec = Qc.QRectF(xvl, yvl, wid, hei)
        brec = self.pnt.fontMetrics().boundingRect(drec.toRect(), flags, val)
        # print(wid, brec.width(), hei, brec.height(), self.tableColumnHeight)
        if brec.height() > hei:
            hei = brec.height()
        # if yvl + hei > self.net_height_table:
        #     print('ektos selidas')
        self.pnt.drawText(Qc.QRectF(xvl, yvl, wid, hei), val, align)
        self.pnt.restore()
        return hei + 5

    def calc_width(self, wid, hei, val, align, font, off=3):
        """Draw text to canvas"""
        self.pnt.save()
        self.pnt.setFont(font)
        xvl = self.x + off
        yvl = self.y + off
        flags = Qc.Qt.TextDontClip | Qc.Qt.TextWordWrap
        drec = Qc.QRectF(xvl, yvl, wid, hei)
        brec = self.pnt.fontMetrics().boundingRect(drec.toRect(), flags, val)
        if brec.height() > hei:
            hei = brec.height()
        self.pnt.restore()
        return hei + 5

    def text_centered(self, text, font, spaceAfter=25):
        if text == '':
            return
        self.pnt.save()
        self.pnt.setFont(font)
        self.pnt.setPen(Qc.Qt.black)
        self.pnt.drawText(
            Qc.QRectF(self.x, self.y, self.net_width, 31),
            text, align(1))
        self.y += spaceAfter
        self.pnt.restore()

    def table_header(self):
        self.x = self.x_left
        y_line = self.y + self.tableHeaderHeight
        self.hline(self.x, y_line, self.max_x, width=2)
        for i, lbl in enumerate(self.f['headerLabels']):
            wid = self.colWidths[i] - 2 * self.x_off
            hei = self.tableHeaderHeight - 2 * self.x_off
            self.txt(wid, hei, lbl, CENTER, self.font_th)
            self.x += self.colWidths[i]
        self.y += self.tableHeaderHeight
        self.x = self.x_left

    def count_size_or_print(self, line, count):
        max_height = self.tableColumnHeight
        for i in range(self.column_number):
            wid = self.colWidths[i] - 6
            hei = self.tableColumnHeight - 6
            val = frmt(line[i], self.f['columnTypes'][i])
            ali = align(self.f['columnAlign'][i])
            if count:
                hei = self.calc_width(wid, hei, val, ali, self.font_tl)
            else:
                hei = self.txt(wid, hei, val, ali, self.font_tl)
            if hei > max_height:
                max_height = hei
            if not count:
                self.x += self.colWidths[i]
        return max_height

    def table_lines(self):
        self.x = self.x_left
        dlen = len(self.f['data'])
        for j, el in enumerate(self.f['data']):
            # Εδώ γίνεται ο έλεγχος για νέα σελίδα
            el_max_width = self.count_size_or_print(el, count=True)
            if self.y + el_max_width > self.net_height_table:
                self.new_page()
            height = self.tableColumnHeight
            for i in range(self.column_number):
                wid = self.colWidths[i] - 6
                hei = self.tableColumnHeight - 6
                val = frmt(el[i], self.f['columnTypes'][i])
                ali = align(self.f['columnAlign'][i])
                hei = self.txt(wid, hei, val, ali, self.font_tl)
                if hei > height:
                    height = hei
                self.x += self.colWidths[i]
            # self.count_size_or_print(el, count=False)
            self.x = self.x_left
            self.y += height
            y_line = self.y
            if dlen == j + 1:
                self.hline(self.x, y_line, self.max_x, width=2)
            else:
                self.hline(self.x, y_line, self.max_x, dots=True)

    def table_footer(self):
        if not self.f['columnToSum']:
            return False
        sumArr = []
        for el in self.f['columnToSum']:
            if el == 0:
                sumArr.append('')
            else:
                sumArr.append(0)
        for el in self.f['data']:
            for i in range(self.column_number):
                if self.f['columnToSum'][i] != 0:
                    sumArr[i] += el[i]
        self.y += 10
        self.x = self.x_left
        for i in range(self.column_number):
            if self.f['columnToSum'][i]:
                wid = self.colWidths[i] - 6
                hei = self.tableColumnHeight - 6
                val = frmt(sumArr[i], self.f['columnTypes'][i])
                ali = align(self.f['columnAlign'][i])
                self.txt(wid, hei, val, ali, self.font_th)
            self.x += self.colWidths[i]
        self.y += self.tableColumnHeight
        self.x = self.x_left

    def page_footer(self):
        self.x, old_y, self.y = self.x_left, self.y, self.y_footer
        if self.f['footerLine']:
            self.hline(self.x, self.y, self.max_x)
        self.y += 2
        footer_text = self.f['footerText']
        has_page_numbers = self.f.get('footerPageNumbers', True)
        if has_page_numbers:
            num_text = '%s %s' % (PAGE_NUMBER_TEXT, self.page_number)
        else:
            num_text = ''
        self.txt(self.net_width, 31, footer_text, CENTER, self.font_pf, off=0)
        self.txt(self.net_width, 31, num_text, RIGHT, self.font_pf, off=0)
        self.x, self.y = self.x_left, old_y

    def new_page(self):
        self.pnt.save()
        self.printer.newPage()
        self.page_number += 1
        self.x, self.y = self.x_left, self.y_top
        self.page_footer()
        self.table_header()
        self.pnt.restore()

    def box(self):
        self.pnt.drawRect(
            self.x_left, self.y_top, self.net_width, self.net_height)

    def printPreview(self):
        if self.f['pdfName']:
            self.printer.setOutputFormat(Qp.QPrinter.PdfFormat)
            self.printer.setOutputFileName(self.f['pdfName'])
        self.printer.setPaperSize(Qp.QPrinter.A4)
        self.printer.setFullPage(True)
        pp = Qp.QPrintPreviewDialog(self.printer)
        pp.paintRequested.connect(self.report)
        pp.exec_()

    def printPdf(self):
        if self.f['pdfName']:
            self.printer.setOutputFormat(Qg.QPrinter.PdfFormat)
            self.printer.setOutputFileName(self.f['pdfName'])
            self.printer.setPaperSize(Qg.QPrinter.A4)
            self.printer.setFullPage(True)
            self.report()
