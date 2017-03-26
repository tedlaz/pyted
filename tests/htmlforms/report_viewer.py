# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import sys


class Report_viewer(QtGui.QWidget):

    def __init__(self, html, pdf_name):
        QtGui.QWidget.__init__(self)

        self.pdf_name = pdf_name
        self.setWindowTitle(u'Αναφορά για εκτύπωση')

        self.editor = QtGui.QTextEdit(self)
        self.editor.setFont(QtGui.QFont('Times New Roman', 12))
        self.editor.textChanged.connect(self.handleTextChanged)

        self.buttonOpen = QtGui.QPushButton('Open', self)
        self.buttonOpen.clicked.connect(self.handleOpen)

        self.buttonPrint = QtGui.QPushButton('Print', self)
        self.buttonPrint.clicked.connect(self.tstPrintPdf)

        self.buttonPreview = QtGui.QPushButton('Preview', self)
        self.buttonPreview.clicked.connect(self.handlePreview)

        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.editor, 0, 0, 1, 3)
        layout.addWidget(self.buttonOpen, 1, 0)
        layout.addWidget(self.buttonPrint, 1, 1)
        layout.addWidget(self.buttonPreview, 1, 2)

        self.handleTextChanged()
        self.editor.setHtml(html)

    def handleOpen(self):
        path = QtGui.QFileDialog.getOpenFileName(
            self, self.tr('Open file'), '',
            self.tr('HTML files (*.html);;Text files (*.txt)'))
        if not path.isEmpty():
            stream = QtCore.QFile(path)
            if stream.open(QtCore.QIODevice.ReadOnly):
                info = QtCore.QFileInfo(path)
                text = stream.readAll()
                codec = QtCore.QTextCodec.codecForHtml(text)
                unistr = codec.toUnicode(text)
                if info.completeSuffix() == 'html':
                    self.editor.setHtml(unistr)
                else:
                    self.editor.setPlainText(unistr)
            stream.close()

    def handlePrint(self):
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.editor.document().print_(dialog.printer())

    def tstPrintPdf(self):
        fname = '%s' % QtGui.QFileDialog.getSaveFileName(self,
          u"Αποθήκευση ως", self.pdf_name, u"Αρχείο (*.pdf)")
        printer = QtGui.QPrinter()
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName(fname)
        self.editor.document().print_(printer)

    def saveAsOdt(self):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.insertHtml(self.editor.toHtml())
        writer = QtGui.QTextDocumentWriter()
        odf_format = writer.supportedDocumentFormats()[1]
        writer.setFormat(odf_format)
        writer.setFileName('symbaseis.odt')
        writer.write(doc)

    def handlePreview(self):
        dialog = QtGui.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.editor.print_)
        dialog.exec_()

    def handleTextChanged(self):
        enable = not self.editor.document().isEmpty()
        self.buttonPrint.setEnabled(enable)
        self.buttonPreview.setEnabled(enable)


def view_html_report(html, pdf_name='tst.pdf'):
    app = QtGui.QApplication(sys.argv)
    window = Report_viewer(html, pdf_name)
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    html_h = u'<p><center>'
    html_h += u'<span style="font-size:14pt; text-decoration:underline;">'
    html_h += u'<b>ΚΟΙΝΟΧΡΗΣΤΑ ΑΝΑ ΔΙΑΜΕΡΙΣΜΑ</b></span>'
    html_h += u'</center><p>'
    html_h += u'Περίοδος : 3ο Τετράμηνο 2015<br>'
    html_h += u'Ημ/νία έκδοσης : 13/12/2015<br>'
    view_html_report(html_h)
