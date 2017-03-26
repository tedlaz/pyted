# -*- coding: utf-8 -*-
'''
Created on 5 Μαρ 2013

@author: tedlaz
'''

from PyQt4 import QtGui, QtCore

txtTempl =u'''
<!DOCTYPE html>
<html>

<body style=" font-family:'MS Shell Dlg 2';font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;">
<p><center><span style=" font-size:14pt;"><b>Μηνιαία κατάσταση εσόδων - εξόδων</b></span></center><p>
<center>Περίοδος : {5}   έως : {6}</center><br>

<p style=" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;"><span style=" font-size:16pt; font-weight:600;">Έσοδα</span></p>
<table border="1" align="center" width="100%" cellspacing="0" cellpadding="4">
  <tbody>
    <tr>
      <th rowspan="2">Τύπος</th>
      <th colspan="2">Από μεταφορά</th>
      <th colspan="2">Περίοδος</th>
      <th colspan="2">Σε μεταφορά</th>
    </tr>
    <tr>
      <th>Ποσό</th>
      <th>ΦΠΑ</th>
      <th>Ποσό</th>
      <th>ΦΠΑ</th>
      <th>Ποσό</th>
      <th>ΦΠΑ</th>
    </tr>
        <tr>
        <td>Για να δούμε τι θα γίνει με αυτό</td>
        <td align="right">1.200,35</td>
        <td align="right">285,42</td>
        <td align="right">2.000,00</td>
        <td align="right">365,00</td>
        <td align="right">3.200,35</td>
        <td align="right">580,44</td>
    </tr>
        <tr>
        <td>Για να δούμε τι θα γίνει με αυτό</td>
        <td class='alnr'>1.200,35</td>
        <td class='alnr'>285,42</td>
        <td class='alnr'>2.000,00</td>
        <td class='alnr'>365,00</td>
        <td class='alnr'>3.200,35</td>
        <td class='alnr'>580,44</td>
    </tr>
  </tbody>
</table>
<br>
<br>
<br>
<p class="breakhere"></p>
<b>Έξοδα</b>
<table width="100%" border="1" cellpadding="1" cellspacing="1">
  <tbody>
    <tr>
      <th rowspan="2">Τύπος</th>
      <th colspan="2">Από μεταφορά</th>
      <th colspan="2">Περίοδος</th>
      <th colspan="2">Σε μεταφορά</th>
    </tr>
    <tr>
      <th>Ποσό</th>
      <th>ΦΠΑ</th>
      <th>Ποσό</th>
      <th>ΦΠΑ</th>
      <th>Ποσό</th>
      <th>ΦΠΑ</th>
    </tr>
    <tr>
        <td>Για να δούμε τι θα γίνει με αυτό</td>
        <td class='alnr'>1.200,35</td>
        <td class='alnr'>285,42</td>
        <td class='alnr'>2.000,00</td>
        <td class='alnr'>365,00</td>
        <td class='alnr'>3.200,35</td>
        <td class='alnr'>580,44</td>
    </tr>
  </tbody>
</table>
</body>
</html>
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
        #self.editor.textChanged.connect(self.handleTextChanged)
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

        self.editor.setHtml(txtTempl)#fillText(txtTempl,co,vals))

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
        printer.setResolution(300)
        printer.setPageSize(QtGui.QPrinter.A4)
        printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
        printer.setOutputFileName('test22.pdf')
        printer.setPageMargins(20,40,10,20,QtGui.QPrinter.Millimeter)
        printer.setOrientation(1)
           
        print 'ok'
        #self.editor.document.setPageSize(QtGui.QPrinter.QSizeF(printer.pageRect().size()))
        self.editor.print_(printer)

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
        dialog.printer().setPageMargins(20,30,10,20,QtGui.QPrinter.Millimeter)
        dialog.setOrientation(1)
        dialog.exec_()
        
        

    def handleTextChanged(self):
        enable = True #not self.editor.document().isEmpty()
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
