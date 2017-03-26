# -*- coding: utf-8 -*-
'''
Created on 5 Μαρ 2013

@author: tedlaz
'''

from PyQt4 import QtGui, QtCore

txtTempl =u'''
<p><center><span style=" font-size:14pt; text-decoration: underline;"><b>ΒΕΒΑΙΩΣΗ ΚΑΤΑΒΟΛΗΣ ΕΤΗΣΙΩΝ ΑΠΟΔΟΧΩΝ</b></span></center><p>
<center>Που καταβλήθηκαν από : {5}   έως : {6}</center><br>
<b>ΣΤΟΙΧΕΙΑ ΕΡΓΟΔΟΤΗ - ΦΟΡΕΑ</b><br>
Επωνυμία : {0} <br>
ΑΦΜ : {1} <br>
Αντικείμενο : {2} <br>
Διεύθυνση : {3} {4}<br>
<br>
<b>Ι.ΣΤΟΙΧΕΙΑ ΕΡΓΑΖΟΜΕΝΟΥ</b>
<table width="100%" border="0" cellpadding="2" cellspacing="2">
    <tbody>
        <tr>
            <td>Ονοματεπώνυμο : {7}</td>
            <td>Όνομα Πατρός : {8}</td>  
            <td>Α.Φ.Μ. : {12}</td>  
            <td></td>
        </tr>
        <tr>
            <td>Διεύθυνση : {9}</td>
            <td></td>
            <td>Τηλέφ : {10}</td>
            <td></td>
        </tr>   
        <tr>
            <td>Ειδικότητα : {11}</td>
            <td></td>
            <td>Οικον.Εφορία : {13} </td>
            <td>Αρ.Δελτ.Ταυτ : {14}</td> 
        </tr>
    </tbody>
</table>
<br><br>
<b>ΙΙ.ΑΜΟΙΒΕΣ ΠΟΥ ΦΟΡΟΛΟΓΟΥΝΤΑΙ</b>
<table width="100%" border="1" cellpadding="2" cellspacing="2">
  <tbody>
    <tr>
      <td><center>Είδος Αποδοχών</center></td>
      <td><center>Ακαθάριστες Αποδοχές</center></td>
      <td><center>Κρατήσεις Ταμείων</center></td>
      <td><center>Σύνολο κρατήσεων</center></td>
      <td><center>Καθαρό ποσόν</center></td>
      <td><center>Φόρος που αναλογεί</center></td>
      <td><center>Φόρος που παρακρατήθηκε</center></td>
      <td><center>Ειδ.Εισφ.Αλληλ. Ν.3986/2011 αρ.29</center></td>
    </tr>
    <tr>
      <td><center>{15}</center></td>
      <td align="right">{16}</td>
      <td align="right">{17}</td>
      <td align="right">{18}</td>
      <td align="right">{19}</td>
      <td align="right">{20}</td>
      <td align="right">{21}</td>
    </tr>
  </tbody>
</table>
<br>
<br>
<br>
<table width="100%" border="0" cellpadding="2" cellspacing="2">
  <tbody>
    <tr>
      <td><center></center></td>
      <td><center>Ημερομηνία : {22}</center></td>
    </tr>
        <tr>
      <td><center></center></td>
      <td><center><br><br>Ο βεβαιών</center></td>
    </tr>
  </tbody>
</table>
'''

def fillText(template,co,vals):
    ftxt = u''
    i=1
    for vl in vals:
        ftxt +=  template.format(co['eponymia'],
                            co['AFM'],
                            co['Antikeimeno'],
                            co['Adress'],
                            co['Tel'],
                            vl['Apo'],
                            vl['Eos'],
                            vl['Onomatep'],
                            vl['Patronymo'],
                            vl['AdrErg'],
                            vl['TelErg'],
                            vl['Eid'],
                            vl['AFMErg'],
                            vl['Doy'],
                            vl['At'],
                            vl['ApodType'],
                            vl['AkApod'],
                            vl['Kratiseis'],
                            vl['SynoloKrat'],
                            vl['Katharo'],
                            vl['Analogei'],
                            vl['Parakrat'],
                            vl['Hmnia']
                            )
        ftxt += (u"<p style='page-break-after:always;'>" if i < len(vals) else u"<p>")
        i += 1
    return ftxt
    
class Window(QtGui.QWidget):
    def __init__(self,co,vals,parent=None):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle(self.tr('Document Printer'))
        
        self.editor = QtGui.QTextEdit(self)
        self.editor.setFont(QtGui.QFont('Courier',11))
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

        self.editor.setHtml(fillText(txtTempl,co,vals))

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
        printer = QtGui.QPrinter()
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOrientation(1)
        printer.setOutputFileName('test22.pdf')
        self.editor.document().print_(printer)

    def printAsPdf(self,filename):
        printer = QtGui.QPrinter()
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOrientation(1)
        printer.setOutputFileName(filename)
        self.editor.document().print_(printer)
                
    def saveAsOdt(self):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.insertHtml(self.editor.toHtml())
        writer = QtGui.QTextDocumentWriter()
        odf_format = writer.supportedDocumentFormats()[1]
        writer.setFormat(odf_format)
        writer.setFileName('hello_world.odt')
        writer.write(doc)
        
    def handlePreview(self):
        dialog = QtGui.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.editor.print_)
        dialog.exec_()
        dialog.setOrientation(1)

    def handleTextChanged(self):
        enable = not self.editor.document().isEmpty()
        self.buttonPrint.setEnabled(enable)
        self.buttonPreview.setEnabled(enable)
        
def test():
    co1 = {
           'eponymia':'',
           'AFM':'',
           'Antikeimeno':'',
           'Adress':'',
           'Tel':''
    }
    vl1 = {
           'Apo':'1/1/2012',
           'Eos':'31/12/2012',
           'Onomatep':'',
           'Patronymo':'',
           'AdrErg':'',
           'TelErg':'',
           'Eid':'',
           'AFMErg':'',
           'Doy':'',
           'At':'',
           'ApodType':u'Μισθοί',
           'AkApod':'',
           'Kratiseis':'',
           'SynoloKrat':'',
           'Katharo':'',
           'Analogei':'',
           'Parakrat':'',
           'Hmnia':'20/3/2013'
           }
    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window(co1,[vl1,vl1])
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
        
if __name__ == '__main__':
    test()
