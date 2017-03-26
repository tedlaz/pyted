# -*- coding: utf-8 -*-
'''
Created on 2014-01-24

@author: tedlaz
'''

from PyQt4 import QtGui, Qt

class rptDlg(QtGui.QDialog):
    def __init__(self,html=u'Δοκιμή',title='Document1',parent=None):
        super(rptDlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        self.odtName = '%s.odt' % title
        self.pdfName = '%s.pdf' % title
        self.setWindowTitle(title)   

        self.editor = QtGui.QTextEdit(self)
        self.editor.setFont(QtGui.QFont('Arial',12))

        self.buttonPdf = QtGui.QPushButton(u'Εξαγωγή σε pdf', self)
        self.buttonPdf.clicked.connect(self.saveAsPdf)
                
        self.buttonOdt = QtGui.QPushButton(u'Εξαγωγή σε odt', self)
        self.buttonOdt.clicked.connect(self.saveAsOdt)
        
        self.buttonPreview = QtGui.QPushButton(u'Προεπισκόπιση', self)
        self.buttonPreview.clicked.connect(self.handlePreview)
        
        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.editor, 0, 0, 1, 3)
        layout.addWidget(self.buttonPdf, 1, 0)
        layout.addWidget(self.buttonOdt, 1, 1)
        layout.addWidget(self.buttonPreview, 1, 2)
        
        self.editor.setHtml(html)

    def handlePrint(self):
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.editor.document().print_(dialog.printer())
            
    def saveAsPdf(self):
        fname = '%s' % QtGui.QFileDialog.getSaveFileName(self,
                u"Αποθήκευση σε μορφή pdf",
                self.pdfName,
                "pdf (*.pdf)")
        if fname:
            printer = QtGui.QPrinter()
            printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOutputFileName(fname)
            self.editor.document().print_(printer)
        
    def saveAsOdt(self):
        fname = '%s' % QtGui.QFileDialog.getSaveFileName(self,
                u"Αποθήκευση σε μορφή Libre Office (odt)",
                self.odtName,
                "Libre Office  (*.odt)")
        if fname:
            doc = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(doc)
            cursor.insertHtml(self.editor.toHtml())
            writer = QtGui.QTextDocumentWriter()
            odf_format = writer.supportedDocumentFormats()[1]
            writer.setFormat(odf_format)
            writer.setFileName(fname)
            writer.write(doc)
        
    def handlePreview(self):
        dialog = QtGui.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.editor.print_)
        dialog.exec_()


if __name__ == "__main__":
    import sys
    
    import test_printHtml
    
    app = QtGui.QApplication(sys.argv)
    window = rptDlg(test_printHtml.toHtml(),test_printHtml.reportTitle)
    
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())