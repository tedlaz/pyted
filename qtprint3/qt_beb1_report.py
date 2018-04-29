# -*- coding: utf-8 -*-
'''
Created on 5 Μαρ 2013

@author: tedlaz
'''

from PyQt5 import QtGui as Qg
from PyQt5 import QtCore as Qc
from PyQt5 import QtWidgets as Qw
import PyQt5.QtPrintSupport as Qp


class Window(Qw.QWidget):
    def __init__(self, co, vals, html_template, parent=None):
        Qw.QWidget.__init__(self)
        self.setWindowTitle(self.tr('Document Printer'))

        self.editor = Qw.QTextEdit(self)
        self.editor.setFont(Qg.QFont('Courier', 11))
        # self.editor.textChanged.connect(self.handleTextChanged)
        self.buttonOpen = Qw.QPushButton('Open', self)
        self.buttonOpen.clicked.connect(self.handleOpen)
        self.buttonPrint = Qw.QPushButton('Print', self)
        self.buttonPrint.clicked.connect(self.tstPrintPdf)
        self.buttonPreview = Qw.QPushButton('Preview', self)
        self.buttonPreview.clicked.connect(self.handlePreview)
        layout = Qw.QGridLayout(self)
        layout.addWidget(self.editor, 0, 0, 1, 3)
        layout.addWidget(self.buttonOpen, 1, 0)
        layout.addWidget(self.buttonPrint, 1, 1)
        layout.addWidget(self.buttonPreview, 1, 2)
        self.handleTextChanged()
        self.editor.setHtml(html_template)

    def handleOpen(self):
        path = Qw.QFileDialog.getOpenFileName(
            self, self.tr('Open file'), '',
            self.tr('HTML files (*.html);;Text files (*.txt)'))[0]
        if path:
            stream = Qc.QFile(path)
            if stream.open(Qc.QIODevice.ReadOnly):
                info = Qc.QFileInfo(path)
                text = stream.readAll()
                codec = Qc.QTextCodec.codecForHtml(text)
                unistr = codec.toUnicode(text)
                if info.completeSuffix() == 'html':
                    self.editor.setHtml(unistr)
                else:
                    self.editor.setPlainText(unistr)
            stream.close()

    def handlePrint(self):
        dialog = Qw.QPrintDialog()
        if dialog.exec_() == Qw.QDialog.Accepted:
            self.editor.document().print_(dialog.printer())

    def tstPrintPdf(self):
        printer = Qp.QPrinter()
        printer.setResolution(300)
        printer.setPageSize(Qp.QPrinter.A4)
        printer.setOutputFormat(Qp.QPrinter.PdfFormat)
        printer.setOutputFileName('test22.pdf')
        printer.setPageMargins(20, 40, 10, 20, Qp.QPrinter.Millimeter)
        printer.setOrientation(1)
        print('ok')
        self.editor.print_(printer)

    def printAsPdf(self, filename):
        printer = Qp.QPrinter()
        printer.setOutputFormat(Qp.QPrinter.PdfFormat)
        printer.setOrientation(1)
        printer.setOutputFileName(filename)
        self.editor.document().print_(printer)

    def saveAsOdt(self):
        doc = Qw.QTextDocument()
        cursor = Qw.QTextCursor(doc)
        cursor.insertHtml(self.editor.toHtml())
        writer = Qw.QTextDocumentWriter()
        odf_format = writer.supportedDocumentFormats()[1]
        writer.setFormat(odf_format)
        writer.setFileName('hello_world.odt')
        writer.write(doc)

    def handlePreview(self):
        dialog = Qp.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.editor.print_)
        dialog.printer().setPageMargins(20, 30, 10, 20, Qp.QPrinter.Millimeter)
        dialog.printer().setOrientation(0)
        dialog.exec_()

    def handleTextChanged(self):
        enable = True
        self.buttonPrint.setEnabled(enable)
        self.buttonPreview.setEnabled(enable)


def test():
    template_file = '/home/ted/prj/pyted/qtprint3/template.html'
    with open(template_file) as tfile:
        template_html = tfile.read()
    co1 = {
           'eponymia': '',
           'AFM': '',
           'Antikeimeno': '',
           'Adress': '',
           'Tel': ''
    }
    vl1 = {
           'Apo': '1/1/2012',
           'Eos': '31/12/2012',
           'Onomatep': '',
           'Patronymo': '',
           'AdrErg': '',
           'TelErg': '',
           'Eid': '',
           'AFMErg': '',
           'Doy': '',
           'At': '',
           'ApodType': u'Μισθοί',
           'AkApod': '',
           'Kratiseis': '',
           'SynoloKrat': '',
           'Katharo': '',
           'Analogei': '',
           'Parakrat': '',
           'Hmnia': '20/3/2013'
           }
    import sys
    app = Qw.QApplication(sys.argv)
    window = Window(co1, [vl1, vl1], template_html)
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
