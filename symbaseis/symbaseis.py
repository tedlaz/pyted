# -*- coding: utf-8 -*-
'''
@author: tedlaz
'''
import datetime
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtPrintSupport as Qp
import sys


def get_data(fname, splitter='|', enc='ISO-8859-7'):
    fls = []
    with open(fname, encoding=enc) as fil:
        head = fil.readline().rstrip('\n').split(splitter)
        lines = fil.readlines()
    for line in lines:
        fls.append(dict(zip(head, line.rstrip('\n').split(splitter))))
    return fls


def get_template(templ_file):
    with open(templ_file) as ofile:
        tdata = ofile.read()
    return tdata


def create_html_text(cocsv, ergcsv, cotmpl, ergtmpl):
    cot = get_template(cotmpl)
    ert = get_template(ergtmpl)
    codata = get_data(cocsv)
    cohtml = cot.format(**codata[0])
    vals = get_data(ergcsv)
    lvals = len(vals)
    html_break = "<p style='page-break-after:always;'>"
    fhtml = u''
    for i, v in enumerate(vals):
        erhtml = ert.format(**v)
        erhtml += html_break if i + 1 < lvals else "<p>"
        fhtml += cohtml + erhtml
    return fhtml


class Window(Qw.QWidget):
    def __init__(self, cocsv, ergcsv, cotm, ergtm):
        Qw.QWidget.__init__(self)
        self.setWindowTitle(self.tr('Document Printer'))
        self.editor = Qw.QTextEdit(self)
        self.editor.setFont(Qg.QFont('Arial', 12))
        self.buttonOpen = Qw.QPushButton('Open', self)
        self.buttonOdt = Qw.QPushButton('save as odt', self)
        self.buttonPdf = Qw.QPushButton('save as pdf', self)
        self.buttonPreview = Qw.QPushButton('preview', self)
        layout = Qw.QGridLayout(self)
        layout.addWidget(self.editor, 0, 0, 1, 4)
        layout.addWidget(self.buttonOpen, 1, 0)
        layout.addWidget(self.buttonOdt, 1, 1)
        layout.addWidget(self.buttonPdf, 1, 2)
        layout.addWidget(self.buttonPreview, 1, 3)
        self.editor.setHtml(create_html_text(cocsv, ergcsv, cotm, ergtm))
        self.editor.textChanged.connect(self.handleTextChanged)
        self.buttonOpen.clicked.connect(self.handleOpen)
        self.buttonOdt.clicked.connect(self.saveAsOdt)
        self.buttonPreview.clicked.connect(self.handlePreview)
        self.buttonPdf.clicked.connect(self.tstPrintPdf)
        self.handleTextChanged()

    def handleOpen(self):
        path = Qw.QFileDialog.getOpenFileName(
            self, self.tr('Open file'), '',
            self.tr('HTML files (*.html);;Text files (*.txt)'))
        if path[0] != '':
            stream = Qc.QFile(path[0])
            if stream.open(Qc.QIODevice.ReadOnly):
                info = Qc.QFileInfo(path[0])
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
        printer.setOutputFormat(Qp.QPrinter.PdfFormat)
        now = datetime.date.isoformat(datetime.date.today()).replace('-', '')
        printer.setOutputFileName('%s.symbaseis.pdf' % now)
        self.editor.document().print_(printer)

    def saveAsOdt(self):
        doc = Qg.QTextDocument()
        cursor = Qg.QTextCursor(doc)
        cursor.insertHtml(self.editor.toHtml())
        writer = Qg.QTextDocumentWriter()
        odf_format = writer.supportedDocumentFormats()[1]
        writer.setFormat(odf_format)
        now = datetime.date.isoformat(datetime.date.today()).replace('-', '')
        writer.setFileName('%s.symbaseis.odt' % now)
        writer.write(doc)

    def handlePreview(self):
        dialog = Qp.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.editor.print_)
        dialog.exec_()

    def handleTextChanged(self):
        enable = not self.editor.document().isEmpty()
        self.buttonOdt.setEnabled(enable)
        self.buttonPreview.setEnabled(enable)


if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    window = Window('company.csv',
                    'prosopiko.csv',
                    'template_company_data.html',
                    'template_erg_data.html')
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
