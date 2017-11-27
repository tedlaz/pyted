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


def create_html_text(cocsv, ergcsv, cotmpl, ergtmpl, fdate=None):
    cot = get_template(cotmpl)
    ert = get_template(ergtmpl)
    codata = get_data(cocsv)
    cohtml = cot.format(**codata[0])
    val = get_data(ergcsv)
    vals = []
    if fdate:
        for elm in val:
            if elm['ddilosi'] == fdate:
                vals.append(elm)
    else:
        vals = val
    lvals = len(vals)
    html_break = "<p style='page-break-after:always;'>"
    fhtml = u''
    for i, v in enumerate(vals):
        if len(v['symliksidate']) > 3:
            v['symtype'] = 'Ορισμένου χρόνου'
        else:
            v['symtype'] = 'Αορίστου χρόνου'
        if v['symdate'] != v['proslipsidate']:
            v['symtype'] += ' (Tροποποιητική)'
        erhtml = ert.format(**v)
        erhtml += html_break if i + 1 < lvals else "<p>"
        fhtml += cohtml + erhtml
    return fhtml


class Window(Qw.QWidget):
    def __init__(self, cocsv, ergcsv, cotm, ergtm):
        Qw.QWidget.__init__(self)
        self.cocsv = cocsv
        self.ergcsv = ergcsv
        self.cotm = cotm
        self.ergtm = ergtm
        self.setWindowTitle(self.tr('Συμβάσεις εργαζομένων'))
        self.editor = Qw.QTextEdit(self)
        self.editor.setFont(Qg.QFont('Arial', 12))
        self.buttonOpen = Qw.QPushButton('Open', self)
        self.buttonOdt = Qw.QPushButton('save as odt', self)
        self.buttonPdf = Qw.QPushButton('save as pdf', self)
        self.buttonPreview = Qw.QPushButton('preview', self)
        layout = Qw.QGridLayout(self)
        self.datef = Qw.QDateEdit()
        self.datef.setCalendarPopup(True)
        self.datef.setDisplayFormat('dd/MM/yyyy')
        self.datef.setDate(Qc.QDate.currentDate())
        self.bgo = Qw.QPushButton('Όλες οι Συμβάσεις', self)
        layout.addWidget(self.datef, 0, 0)
        layout.addWidget(self.bgo, 0, 1)
        layout.addWidget(self.editor, 1, 0, 1, 4)
        layout.addWidget(self.buttonOpen, 2, 0)
        layout.addWidget(self.buttonOdt, 2, 1)
        layout.addWidget(self.buttonPdf, 2, 2)
        layout.addWidget(self.buttonPreview, 2, 3)
        self.bgo.clicked.connect(self.fillAll)
        self.editor.textChanged.connect(self.handleTextChanged)
        self.buttonOpen.clicked.connect(self.handleOpen)
        self.buttonOdt.clicked.connect(self.saveAsOdt)
        self.buttonPreview.clicked.connect(self.handlePreview)
        self.buttonPdf.clicked.connect(self.tstPrintPdf)
        self.datef.dateChanged.connect(self.fillHtml)
        self.handleTextChanged()

    def fillHtml(self):
        # dtgr: Ημερομηνία ετοιμασίας συμβάσεων
        dtgr = self.datef.date().toString('dd/MM/yyyy')
        self.editor.setHtml(create_html_text(self.cocsv,
                                             self.ergcsv,
                                             self.cotm,
                                             self.ergtm,
                                             dtgr))

    def fillAll(self):
        # dtgr: Ημερομηνία ετοιμασίας συμβάσεων
        self.editor.setHtml(create_html_text(self.cocsv,
                                             self.ergcsv,
                                             self.cotm,
                                             self.ergtm))

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
        now = datetime.date.isoformat(datetime.date.today()).replace('-', '')
        fname = '%s.symbaseis.pdf' % now
        options = Qw.QFileDialog.Options()
        fdl, _ = Qw.QFileDialog.getSaveFileName(self, "Αποθήκευση", fname,
                    "Pdf Files (*.pdf)", options=options)
        if fdl:
            printer = Qp.QPrinter()
            printer.setOutputFormat(Qp.QPrinter.PdfFormat)
            printer.setOutputFileName(fdl)
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
        self.buttonPdf.setEnabled(enable)


if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    window = Window('company.csv',
                    'prosopiko.csv',
                    'template_company_data.html',
                    'template_erg_data.html')
    window.resize(640, 800)
    window.show()
    sys.exit(app.exec_())
