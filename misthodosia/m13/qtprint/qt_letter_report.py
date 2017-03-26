# -*- coding: utf-8 -*-
'''
Created on 5 Μαρ 2013

@author: tedlaz
'''

from PyQt4 import QtGui, QtCore

txt =u'''
<p><center><span style=" font-size:14pt; text-decoration: underline;"><b>ΟΡΟΙ ΑΤΟΜΙΚΗΣ ΣΥΜΒΑΣΗΣ ΕΡΓΑΣΙΑΣ ΜΕΡΙΚΗΣ Η ΚΑΙ ΕΚ ΠΕΡΙΤΡΟΠΗΣ ΑΠΑΣΧΟΛΗΣΗΣ</b></span></center><p>
<br>
<p><center><span style=" font-size:12pt;"><b>Ο ΕΡΓΟΔΟΤΗΣ</b></span></center><p>
ΕΠΩΝΥΜΙΑ : {0}
<br>
ΔΡΑΣΤΗΡΙΟΤΗΤΑ : {1}
<br>
ΔΙΕΥΘΥΝΣΗ : {2}
<br>
ΟΝ/ΜΟ ΕΚΠΡΟΣΩΠΟΥ : {3}
<br>
<p><center><span style=" font-size:12pt;"><b>Ο ΕΡΓΑΖΟΜΕΝΟΣ</b></span></center><p>
ΟΝ/ΜΟ : {4}  ΟΝΟΜΑ ΠΑΤΡΟΣ :  {5}
<br>
ΔΙΕΥΘΥΝΣΗ ΚΑΤΟΙΚΙΑΣ : {6}
<br>
ΣΤΟΙΧΕΙΑ ΤΑΥΤΟΤΗΤΑΣ : {7}
<br>
<p><center><span style=" font-size:12pt;"><b>ΟΥΣΙΩΔΕΙΣ ΟΡΟΙ</b></span></center><p>
Α. ΕΙΔΟΣ ΣΥΜΒΑΣΗΣ : {8}
<ol>
  <li>ΗΜΕΡΟΜΗΝΙΑ ΕΝΑΡΞΗΣ ΣΥΜΒΑΣΗΣ : {9}</li>
  <li>ΗΜΕΡΟΜΗΝΙΑ ΛΗΞΗΣ ΣΥΜΒΑΣΗΣ : {10}</li>
</ol>
Β. ΧΡΟΝΟΣ ΑΠΑΣΧΟΛΗΣΗΣ : 
<ol>
  <li>ΗΜΕΡΕΣ ΕΒΔΟΜΑΔΙΑΙΩΣ : {11}</li>
  <li>ΩΡΕΣ ΕΒΔΟΜΑΔΙΑΙΩΣ : {12}</li>
  <li>3. ΩΡΑΡΙΟ ΗΜΕΡΗΣΙΑΣ ΑΠΑΣΧΟΛΗΣΗΣ : {13}</li>
</ol>
Γ. ΤΟΠΟΣ ΠΑΡΟΧΗΣ ΕΡΓΑΣΙΑΣ : {14}
<br>
Δ. ΕΙΔΙΚΟΤΗΤΑ ΕΡΓΑΖΟΜΕΝΟΥ : {15}
<br>
Ε. ΑΠΟΔΟΧΕΣ  : {16}
<br>
<center>ΟΙ ΣΥΜΒΑΛΛΟΜΕΝΟΙ</center>
<table width="100%" border="0" cellpadding="2" cellspacing="2">
  <tbody>
    <tr>
      <td><center>Ο ΕΡΓΟΔΟΤΗΣ</center></td>
      <td><center>Ο ΕΡΓΑΖΟΜΕΝΟΣ</center></td>
    </tr>
  </tbody>
</table>
<br>
<br>
<br>
<br>
<table width="100%" border="0" cellpadding="2" cellspacing="2">
  <tbody>
    <tr>
      <td><center>ΣΦΡΑΓΙΔΑ-ΥΠΟΓΡΑΦΗ</center></td>
      <td><center>ΥΠΟΓΡΑΦΗ    </center></td>
    </tr>
  </tbody>
</table>
'''
class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle(self.tr('Document Printer'))
        self.editor = QtGui.QTextEdit(self)
        self.editor.setFont(QtGui.QFont('Helvetica',12))
        self.editor.textChanged.connect(self.handleTextChanged)
        self.buttonOpen = QtGui.QPushButton('Open', self)
        self.buttonOpen.clicked.connect(self.handleOpen)
        self.buttonPrint = QtGui.QPushButton('Print', self)
        self.buttonPrint.clicked.connect(self.saveAsOdt)
        self.buttonPreview = QtGui.QPushButton('Preview', self)
        self.buttonPreview.clicked.connect(self.handlePreview)
        
        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.editor, 0, 0, 1, 3)
        layout.addWidget(self.buttonOpen, 1, 0)
        layout.addWidget(self.buttonPrint, 1, 1)
        layout.addWidget(self.buttonPreview, 1, 2)
        self.handleTextChanged()
        vals = [[u'ΑΚΤΗ ΦΑΡΑΓΓΑ ΠΑΡΟΥ ΕΠΕ ΑΦΜ: 999249820',u'ΕΣΤΙΑΤΟΡΙΟ-ΜΠΑΡ',u'ΑΓΑΘΗΜΕΡΟΥ 3, ΑΘΗΝΑ',u'ΜΙΧΑΗΛ ΑΘΕΡΙΝΗΣ-ΣΠΑΡΤΙΩΤΗΣ',
                 u'ΘΕΟΔΩΡΟΣ ΛΑΖΑΡΟΣ',u'ΚΩΝΣΤΑΝΤΙΝΟΣ',u'ΑΘΗΝΑΣ 4',u'Α.Τ. Ζ3474',u'Αορίστου Χρόνου',u'15/1/2013',
                 u'',u'2',u'13',u'ΠΑΡΑΣΚΕΥΗ - ΣΑΒΒΑΤΟ 8:00 - 15:00',u'ΑΓΑΘΗΜΕΡΟΥ 3',u'ΣΕΡΒΙΤΟΡΟΣ',u'54,60'],
                [u'ΝΙΚΟΠΟΛΙΣ ΑΕ',u'ΕΣΤΙΑΤΟΡΙΟ-ΜΠΑΡ',u'ΑΓΑΘΗΜΕΡΟΥ 8 ΑΘΗΝΑ 15235',u'ΣΠΑΡΤΙΩΤΗΣ ΜΙΧΑΛΗΣ',
                 u'ΘΕΟΔΩΡΟΣ ΛΑΖΑΡΟΣ',u'ΚΩΝΣΤΑΝΤΙΝΟΥ',u'ΑΘΗΝΑΣ 4',u'Α.Τ. Ζ3474',u'Αορίστου Χρόνου',u'15/1/2013',
                 u'',u'2',u'13',u'ΠΑΡΑΣΚΕΥΗ - ΣΑΒΒΑΤΟ 8:00 - 15:00',u'ΑΓΑΘΗΜΕΡΟΥ 3',u'ΣΕΡΒΙΤΟΡΟΣ',u'54,60']]
        ftxt = u''
        i=1
        for v in vals:
            ftxt +=  txt.format(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9],v[10],v[11],v[12],v[13],v[14],v[15],v[16])
            ftxt += ("<p style='page-break-after:always;'>" if i < len(vals) else "<p>")
            i += 1
        self.editor.setHtml(ftxt)

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
        printer.setOutputFileName('test22.pdf')
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

    def handleTextChanged(self):
        enable = not self.editor.document().isEmpty()
        self.buttonPrint.setEnabled(enable)
        self.buttonPreview.setEnabled(enable)
        

if __name__ == '__main__':
    
    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
    
    #print num2descr(4949901945689)