# -*- coding: utf-8 -*-
'''
Created on 3 Mar 2015

@author: ted lazaros

version 1.0
'''

from PyQt4 import QtGui, QtCore
import decimal

ALEFT, ACENTER, ARIGHT = range(3)
TSTR, TDATE, TINT, TDEC = range(4)


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
    """
    use : Given a number, it returns a decimal with a specific number of
          decimal digits
    input Parameters:
          1.poso     : The number for conversion in any format
                        (e.g. string or int ..)
          2.dekadika : The number of decimals (default 2)
    output: A decimal number
    """
    PLACES = decimal.Decimal(10) ** (-1 * dekadika)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


def gr(number):
    'Returns Greek Decimal(2) number or empty space'
    number = dec(number)
    if abs(number) <= 0.004:
        return ''
    s = '%.2f' % number
    a, d = s.split('.')
    groups = []
    while a and a[-1].isdigit():
        groups.append(a[-3:])
        a = a[:-3]
    return a + '.'.join(reversed(groups)) + ',' + d


def gr0(number):
    'Returns Greek Decimal(2) number or 0,00'
    number = dec(number)
    if abs(number) <= 0.004:
        return '0,00'
    s = '%.2f' % number
    a, d = s.split('.')
    groups = []
    while a and a[-1].isdigit():
        groups.append(a[-3:])
        a = a[:-3]
    return a + '.'.join(reversed(groups)) + ',' + d


def grint(number):
    'Returns Greek Decimal(1) number'
    number = dec(number)
    if abs(number) <= 0.004:
        return ''
    s = '%.1f' % number
    a, d = s.split('.')
    groups = []
    while a and a[-1].isdigit():
        groups.append(a[-3:])
        a = a[:-3]
    return a + '.'.join(reversed(groups)) + ',' + d


def is_iso_date(val):
    val = u'%s' % val
    len_val = len(val)
    if len_val == 10 and val[4] == '-' and val[7] == '-':
        return True
    else:
        return False


def grd(imnia):
    'Returns Greek Date'
    y, m, d = imnia.split('-')
    return '%s/%s/%s' % (d, m, y)


def align(opt=ALEFT):
    if opt == ALEFT:
        option = QtGui.QTextOption(QtCore.Qt.AlignLeft |
                                   QtCore.Qt.AlignVCenter)
    elif opt == ACENTER:
        option = QtGui.QTextOption(QtCore.Qt.AlignCenter |
                                   QtCore.Qt.AlignVCenter)
    else:
        option = QtGui.QTextOption(QtCore.Qt.AlignRight |
                                   QtCore.Qt.AlignVCenter)
    option.setWrapMode(QtGui.QTextOption.WordWrap)
    return option


def frmt(val, typos):
    if typos == TSTR:  # String
        frmtVal = '%s' % val
    elif typos == TINT:  # Integer
        frmtVal = '%s' % val
    elif typos == TDEC:  # Decimal
        frmtVal = gr(val)
    elif typos == TDATE:  # Date
        frmtVal = grd(val)
    else:
        frmtVal = '%s' % val
    return frmtVal


def len_type_align(arrays):
    maxs = []
    types = []
    aligns = []
    sums = []
    for i in range(len(arrays[0])):
        maxs.append(0)
        types.append(0)
        aligns.append(0)
        sums.append(0)
    for line in arrays:
        for i, column in enumerate(line):
            siz = 0
            typ = type(column)
            if typ is str or typ is unicode:
                if is_iso_date(column):
                    # print column, typ, 'date'
                    types[i] = max(types[i], TDATE)
                    aligns[i] = max(aligns[i], ACENTER)
                    siz = 10
                else:
                    # print column, typ, 'unicode or str'
                    types[i] = max(types[i], TSTR)
                    aligns[i] = max(aligns[i], ALEFT)
                    siz = len(u'%s' % column) + 2
            elif typ is int:
                # print column, typ, 'Integer'
                types[i] = max(types[i], TINT)
                aligns[i] = max(aligns[i], ARIGHT)
                siz = len(u'%s' % column) + 3
            elif typ is float:
                # print column, typ, 'Float'
                types[i] = max(types[i], TDEC)
                aligns[i] = max(aligns[i], ARIGHT)
                siz = len(u'%s' % column)
                sums[i] += column
            else:
                # print column, typ, 'agnosto'
                types[i] = max(types[i], TSTR)
                aligns[i] = max(aligns[i], ALEFT)
                siz = len(u'%s' % column) + 2
            maxs[i] = max(maxs[i], siz)
    for i, el in enumerate(sums):
        if el:
            maxs[i] = max(maxs[i], len(gr(el)))
    return maxs, types, aligns


def distribute(val, distArray):
    """
    input parameters:
    val       : value for distribution
    distArray : Distribution Array
    """
    tmpArr = []
    try:
        tar = sum(distArray)
    except:
        return 0
    for el in distArray:
        tmpArr.append(val * el / tar)
    nval = sum(tmpArr)

    dif = val - nval  # Get the possible difference to fix round problem
    if dif == 0:
        pass
    else:
        # Max number Element gets the difference
        tmpArr[tmpArr.index(max(tmpArr))] += dif
    return tmpArr


class qtTableReport():
    def __init__(self, f={}):
        self.f = f
        self.printer = QtGui.QPrinter()
        # Set portrait or landscape
        if self.f['orientation'] == 0:
            self.printer.setOrientation(QtGui.QPrinter.Portrait)
        else:
            self.printer.setOrientation(QtGui.QPrinter.Landscape)
        self.page_width = self.printer.pageRect().width()
        self.__colNo = len(self.f['headerLabels'])
        self.oftop = 3  # Top offset
        self.oflow = 6  # Down offset
        self.ofpage = 100  # Down page offset
        self.top_margin = 60
        self.bottom_margin = 70
        self.min_left_margin = 60
        self.__set_fonts()
        self.tableMetrics = QtGui.QFontMetrics(self.__TableLineFont)
        self.tableHeaderHeight = int(self.tableMetrics.height() * 3)
        self.tableColumnHeight = int(self.tableMetrics.height() * 2.3)
        # column width
        dist_val = self.page_width-self.min_left_margin-10
        self.lens, self.types, self.aligns = len_type_align(f['data'])
        self.colWidths = distribute(dist_val, self.lens)

        self.line_width = sum(self.colWidths)

        if self.page_width >= self.line_width + (2 * self.min_left_margin):
            self.left_margin = (self.page_width - self.line_width) / 2
        else:
            # Must print an error message
            self.left_margin = self.min_left_margin

    def __set_fonts(self):
        fontSize = 9

        self.__RHead1Font = QtGui.QFont(self.f['fontFamily'], 20)
        self.__RHead1Font.setBold(True)

        self.__RHead2Font = QtGui.QFont(self.f['fontFamily'], 12)
        self.__RHead2Font.setBold(True)
        self.__RHead2Font.setItalic(True)

        self.__RHead3Font = QtGui.QFont(self.f['fontFamily'], 10)
        self.__RHead3Font.setItalic(True)

        self.__TableHeadFont = QtGui.QFont(self.f['fontFamily'], fontSize)
        self.__TableHeadFont.setBold(True)

        self.__TableLineFont = QtGui.QFont(self.f['fontFamily'], fontSize)

        self.__FooterFont = QtGui.QFont(self.f['fontFamily'], fontSize)
        # self.__FooterFont.setItalic(True)

    def __drawCol(self):
        pass

    def __drawCenteredText(self, text, painter, font, height=30):
        if text == '':
            return
        painter.setFont(font)
        rect = QtCore.QRectF(self.x,
                             self.y,
                             self.pageRect.width() - 2 * self.xLeftMargin,
                             height)
        painter.drawText(rect, text, align(1))
        self.y += height + 1

    def __drawReportHeader(self, painter, vheight=20):
        self.__drawCenteredText(self.f['ReportHeader1'],
                                painter,
                                self.__RHead1Font,
                                height=vheight + 5)
        self.__drawCenteredText(self.f['ReportHeader2'],
                                painter,
                                self.__RHead2Font,
                                height=vheight)
        self.__drawCenteredText(self.f['ReportHeader3'],
                                painter,
                                self.__RHead3Font,
                                height=vheight)

    def __fixPainterBug(self, painter):
        'This is a workaround for painter to paint lines properly'
        painter.setPen(QtCore.Qt.NoPen)
        painter.setPen(QtCore.Qt.black)

    def __drawPageHeader(self, painter):
        pass

    def __drawRectWithText(self, x, y, width, height, value, option):
        pass

    def __drawTableHeader(self, painter):
        painter.save()
        painter.setFont(self.__TableHeadFont)
        self.x = self.xLeftMargin
        self.__draw_table_fat_line(painter)
        for i in range(len(self.f['headerLabels'])):
            rect = QtCore.QRectF(self.x + self.oftop,
                                 self.y + self.oftop,
                                 self.colWidths[i] - self.oflow,
                                 self.tableHeaderHeight - self.oflow)
            painter.drawText(rect, self.f['headerLabels'][i], align(1))
            self.x += self.colWidths[i]
        self.y += self.tableHeaderHeight
        self.x = self.xLeftMargin
        painter.restore()

    def __draw_table_fat_line(self, painter):
        painter.save()
        pen = QtGui.QPen()
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(self.xLeftMargin,
                         self.y + self.tableHeaderHeight,
                         self.xLeftMargin + self.line_width,
                         self.y + self.tableHeaderHeight)
        painter.restore()

    def __draw_table_dash_line(self, painter):
        painter.save()
        painter.setPen(QtCore.Qt.black | QtCore.Qt.DashLine)
        painter.drawLine(self.xLeftMargin,
                         self.y + self.tableColumnHeight,
                         self.xLeftMargin + self.line_width,
                         self.y + self.tableColumnHeight)
        painter.restore()

    def __drawTableLines(self, painter):
        painter.save()
        self.x = self.xLeftMargin
        dlen = len(self.f['data'])
        for j, el in enumerate(self.f['data']):
            if self.y > self.pageRect.height() - self.ofpage:
                painter.save()
                self.__drawNewPage(painter)
                painter.restore()
            painter.setFont(self.__TableLineFont)
            painter.setPen(QtCore.Qt.black | QtCore.Qt.DashLine)
            for i in range(self.__colNo):
                txt_rec = QtCore.QRectF(self.x + self.oftop,
                                        self.y + self.oftop,
                                        self.colWidths[i] - self.oflow,
                                        self.tableColumnHeight - self.oflow)
                painter.drawText(txt_rec,
                                 frmt(el[i], self.types[i]),
                                 align(self.aligns[i]))
                self.x += self.colWidths[i]
            if j + 1 == dlen:
                self.__draw_table_fat_line(painter)
            else:
                self.__draw_table_dash_line(painter)
            self.x = self.xLeftMargin
            self.y += self.tableColumnHeight
        painter.restore()

    def __drawTableFooter(self, painter):
        painter.save()

        sumArr = []
        for el in self.types:
            if el < TDEC:
                sumArr.append('')
            else:
                sumArr.append(0)

        for el in self.f['data']:
            for i in range(self.__colNo):
                if self.types[i] == TDEC:
                    sumArr[i] += el[i]
        self.y += 10
        painter.setFont(self.__TableHeadFont)
        self.x = self.xLeftMargin

        for i in range(self.__colNo):
            if self.types[i] == TDEC:
                txt_rec = QtCore.QRectF(self.x + 3,
                                        self.y + 3,
                                        self.colWidths[i] - 6,
                                        self.tableColumnHeight - 6)
                painter.drawText(txt_rec,
                                 frmt(sumArr[i], self.types[i]),
                                 align(self.aligns[i]))
            self.x += self.colWidths[i]
        self.y += self.tableColumnHeight
        self.x = self.xLeftMargin
        painter.restore()

    def __drawPageFooter(self, painter):
        painter.save()
        pen = QtGui.QPen()
        pen.setColor(QtCore.Qt.black)
        painter.setPen(pen)
        self.x = self.xLeftMargin
        old_y = self.y
        self.y = self.yFooter
        if self.f['footerLine']:
            painter.drawLine(self.xLeftMargin,
                             self.y,
                             self.xLeftMargin + self.line_width,
                             self.y)
        self.y += 2
        painter.setFont(self.__FooterFont)
        if self.f['footerPageNumberText'] == '':
            finalText = self.f['footerText']
        else:
            finalText = '%s' % self.f['footerText']
            selText = '%s %s' % (self.f['footerPageNumberText'], self.pageNo)
        txt_rec = QtCore.QRectF(self.x,
                                self.y,
                                self.pageRect.width() - 2 * self.xLeftMargin,
                                31)
        painter.drawText(txt_rec, finalText, align(1))
        painter.drawText(txt_rec, selText, align(2))
        self.y = old_y
        self.x = self.xLeftMargin
        painter.restore()

    def __drawNewPage(self, painter):
        painter.save()
        self.printer.newPage()
        self.pageNo += 1
        self.x = self.xLeftMargin
        self.y = self.yTopMargin
        self.__drawPageFooter(painter)
        self.__drawTableHeader(painter)
        painter.restore()

    def __tstPoly(self, painter, siz=15, num=10):
        x, y = self.xLeftMargin, self.y + 90

        def poly(pts):
            return QtGui.QPolygonF(map(lambda p: QtCore.QPointF(*p), pts))
        xsiz = siz
        ysiz = int(siz / 2)
        for i in range(num):
            pts = [[x, y], [x, y + ysiz], [x + xsiz, y + ysiz], [x + xsiz, y]]
            pts = pts[:]
            painter.drawPolyline(poly(pts))
            x += xsiz
        x = self.xLeftMargin
        painter.drawLine(QtCore.QPoint(x, y - 3),
                         QtCore.QPoint(x + (num * xsiz), y - 3))
        print 'height : {0}, width : {1}'.format(self.pageRect.height(),
                                                 self.pageRect.width())
        painter.drawRect(self.xLeftMargin,
                         self.yTopMargin,
                         self.pageRect.width() - self.xLeftMargin - 36,
                         self.pageRect.height() - 2 * self.yTopMargin)

    def __drawReport(self):
        '''Here we assemble the pieces to make the final report'''
        painter = QtGui.QPainter(self.printer)
        painter.save()
        self.pageRect = self.printer.pageRect()
        # initialize print Cursor
        self.xLeftMargin = self.x = self.left_margin
        self.yTopMargin = self.y = self.top_margin
        self.yFooter = self.pageRect.height() - self.bottom_margin
        self.pageNo = 1
        self.__drawReportHeader(painter)
        # self.__drawPageHeader()
        self.__fixPainterBug(painter)
        self.__drawPageFooter(painter)
        self.__drawTableHeader(painter)
        self.__drawTableLines(painter)
        # self.__tstPoly(painter)
        self.__drawTableFooter(painter)
        painter.restore()

    def printPreview(self):
        if self.f['pdfName']:
            self.printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            self.printer.setOutputFileName(self.f['pdfName'])
        self.printer.setPaperSize(QtGui.QPrinter.A4)
        self.printer.setFullPage(True)
        pp = QtGui.QPrintPreviewDialog(self.printer)
        pp.paintRequested.connect(self.__drawReport)
        pp.exec_()

    def printPdf(self):
        if self.f['pdfName']:
            self.printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            self.printer.setOutputFileName(self.f['pdfName'])
            self.printer.setPaperSize(QtGui.QPrinter.A4)
            self.printer.setFullPage(True)
            self.__drawReport()
