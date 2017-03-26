# -*- coding: utf-8 -*-
'''
Created on 5 Μαρ 2013

@author: tedlaz
'''

from PyQt4 import QtGui, QtCore
import locale
import dbforms as dbf
locale.setlocale(locale.LC_ALL, '')
sqles = '''
SELECT et.etp,
sum(case when strftime('%m',es.dat) < '{minas}' then esd.val end) aval,
sum(case when strftime('%m',es.dat) < '{minas}' then esd.fpa end) afpa,
sum(case when strftime('%m',es.dat) = '{minas}' then esd.val end) pval,
sum(case when strftime('%m',es.dat) = '{minas}' then esd.fpa end) pfpa,
sum(case when strftime('%m',es.dat) <= '{minas}' then esd.val end) sval,
sum(case when strftime('%m',es.dat) <= '{minas}' then esd.fpa end) sfpa
FROM esd
INNER JOIN et ON et.id=esd.et_id
INNER JOIN es ON es.id=esd.es_id
WHERE strftime('%Y',es.dat)='{etos}'
GROUP BY esd.et_id
ORDER BY et.etp
'''
sqlest = '''
SELECT 
sum(case when strftime('%m',es.dat) < '{minas}' then esd.val end) aval,
sum(case when strftime('%m',es.dat) < '{minas}' then esd.fpa end) afpa,
sum(case when strftime('%m',es.dat) = '{minas}' then esd.val end) pval,
sum(case when strftime('%m',es.dat) = '{minas}' then esd.fpa end) pfpa,
sum(case when strftime('%m',es.dat) <= '{minas}' then esd.val end) sval,
sum(case when strftime('%m',es.dat) <= '{minas}' then esd.fpa end) sfpa
FROM esd
INNER JOIN et ON et.id=esd.et_id
INNER JOIN es ON es.id=esd.es_id
WHERE strftime('%Y',es.dat)='{etos}'
'''
sqlds = '''
SELECT dt.etp,
sum(case when strftime('%m',ds.dat) < '{minas}' then dsd.val end) aval,
sum(case when strftime('%m',ds.dat) < '{minas}' then dsd.fpa end) afpa,
sum(case when strftime('%m',ds.dat) = '{minas}' then dsd.val end) pval,
sum(case when strftime('%m',ds.dat) = '{minas}' then dsd.fpa end) pfpa,
sum(case when strftime('%m',ds.dat) <= '{minas}' then dsd.val end) sval,
sum(case when strftime('%m',ds.dat) <= '{minas}' then dsd.fpa end) sfpa
FROM dsd
INNER JOIN dt ON dt.id=dsd.dt_id
INNER JOIN ds ON ds.id=dsd.ds_id
WHERE strftime('%Y',ds.dat)='{etos}'
GROUP BY dt.id
ORDER BY dt.etp
'''
sqldst = '''
SELECT 
sum(case when strftime('%m',ds.dat) < '{minas}' then dsd.val end) aval,
sum(case when strftime('%m',ds.dat) < '{minas}' then dsd.fpa end) afpa,
sum(case when strftime('%m',ds.dat) = '{minas}' then dsd.val end) pval,
sum(case when strftime('%m',ds.dat) = '{minas}' then dsd.fpa end) pfpa,
sum(case when strftime('%m',ds.dat) <= '{minas}' then dsd.val end) sval,
sum(case when strftime('%m',ds.dat) <= '{minas}' then dsd.fpa end) sfpa
FROM dsd
INNER JOIN dt ON dt.id=dsd.dt_id
INNER JOIN ds ON ds.id=dsd.ds_id
WHERE strftime('%Y',ds.dat)='{etos}'
'''
htmHead =u'''
<!DOCTYPE html>
<html>

<body style=" font-family:'MS Shell Dlg 2';font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;">
<p><center><span style=" font-size:14pt;"><b>Μηνιαία κατάσταση εσόδων - εξόδων</b></span></center><p>
<center><b>{minas} {etos}</b></center><br>

<p style=" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;"><span style=" font-size:16pt; font-weight:600;">Έσοδα</span></p>
<table border="1" align="center" width="100%" cellspacing="0" cellpadding="4">
  <tbody>
    <tr>
      <th rowspan="2"><center>Τύπος</center></th>
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
'''
htmEsLine = u'''
    <tr>
        <td>{katigoria}</td>
        <td align="right">{apo}</td>
        <td align="right">{apofpa}</td>
        <td align="right">{per}</td>
        <td align="right">{perfpa}</td>
        <td align="right">{se}</td>
        <td align="right">{sefpa}</td>
    </tr>
'''
htmEstLine = u'''
    <tr>
        <td><center><b>Σύνολα</b></center></td>
        <td align="right"><b>{apo}</b></td>
        <td align="right"><b>{apofpa}</b></td>
        <td align="right"><b>{per}</b></td>
        <td align="right"><b>{perfpa}</b></td>
        <td align="right"><b>{se}</b></td>
        <td align="right"><b>{sefpa}</b></td>
    </tr>
  </tbody>
</table>    
'''
htmEjHead = u'''
<br>
<br>
<p style=" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;"><span style=" font-size:16pt; font-weight:600;">Έξοδα</span></p>
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
'''
est = u'''
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
'''
final = u'''
</body>
</html>
'''
def nn(val):
    if val:
        if dbf.isNum(val):
            return locale.format("%0.2f", val, grouping=True)
        else:
            return val
    else:
        return ''
    
class PtextForm(QtGui.QDialog):
    def __init__(self,parent=None, etos=None, minas=None):
        super(PtextForm, self).__init__(parent)
        layout = QtGui.QVBoxLayout()
        
        self.parent = parent
        self.fname = None #Όνομα αρχείου pdf για αποθήκευση της περιοδικής ΦΠΑ
        
        headLay = QtGui.QHBoxLayout()
        headLay.addWidget(dbf.makeTitle(u'Μηνιαία κατάσταση Εσόδων - εξόδων'))
        self.letos = QtGui.QLabel(u'Έτος')
        self.letos.setMaximumSize(60, 60)
        self.etos = QtGui.QLineEdit()
        headLay.addWidget(self.letos)
        headLay.addWidget(self.etos)
        self.ltr = QtGui.QLabel(u'Μήνας')
        self.tr = QtGui.QLineEdit()
        headLay.addWidget(self.ltr)
        headLay.addWidget(self.tr)
        self.go = QtGui.QPushButton(u'Πάμε')
        self.go.clicked.connect(self.fillData)
        headLay.addWidget(self.go)
        layout.addLayout(headLay)
        self.ptext = QtGui.QTextEdit(self)
        #self.ptext.setFont(QtGui.QFont('Courier',20))
        #self.ptext.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.ptext.setReadOnly(True) 
        layout.addWidget(self.ptext)
        self.buttonPreview = QtGui.QPushButton(u'Προεπισκόπιση', self)
        self.buttonPreview.clicked.connect(self.handlePreview)
        self.buttonPdf = QtGui.QPushButton(u'pdf', self)
        self.buttonPdf.clicked.connect(self.printAsPdf)
        hlay = QtGui.QHBoxLayout()
        hlay.addWidget(self.buttonPreview)
        hlay.addWidget(self.buttonPdf)
        layout.addLayout(hlay)
        self.setLayout(layout)        
        #self.fillData()
        if minas and etos:
            self.etos.setText(etos)
            self.tr.setText(minas)
            self.fillData(etos, minas)
    def printAsPdf(self):
        if self.fname:   
            fname = '%s' %QtGui.QFileDialog.getSaveFileName(self,
                    u"Αποθήκευση σε pdf",
                    self.fname,#os.path.dirname(self.db),
                    "pdf (*.pdf)")
        else:
            fname = None
        if fname:
            printer = QtGui.QPrinter()
            printer.setResolution(300)
            printer.setPageSize(QtGui.QPrinter.A4)
            printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOutputFileName(fname)
            printer.setPageMargins(10,20,10,20,QtGui.QPrinter.Millimeter)
            printer.setOrientation(0)
            self.ptext.print_(printer) 
               
    def handlePreview(self):
        dialog = QtGui.QPrintPreviewDialog()
        dialog.printer().setResolution(300)
        dialog.printer().setPageSize(QtGui.QPrinter.A4)
        dialog.printer().setPageMargins(10,10,10,20,QtGui.QPrinter.Millimeter)
        dialog.paintRequested.connect(self.ptext.print_)
        dialog.exec_()
                
    def canAdd(self):
        return False
    
    def fillData(self, et=None, mina=None):
        if et:
            etos = et
        else:
            etos = self.etos.text()
        if mina:    
            minas = mina
        else:
            minas = self.tr.text()
             
        if self.parent:
            db = self.parent.db
        else:
            self.ptext.setHtml(u"f2 Line 499 : Δεν υπάρχει σύνδεση με βάση")
            return

        sqlco = "SELECT cop, ono, pat,afm FROM co WHERE id=1"
        cod ,b = dbf.getDbRows(sqlco, db)
        sqlMina = "SELECT mip FROM mi WHERE id='%s'" % minas
        mipe ,b= dbf.getDbRows(sqlMina, db)
        
        mi = '%s' % mipe[0]
        
        self.fname = u'esex-%s-%s-%s' % (cod[0][0],etos,minas)
        f = {'etos':etos,'minas':minas}
        f1 = {'etos':etos,'minas':mi}
        fsqles = sqles.format(**f)
        vals,d = dbf.getDbRows(fsqles, db)
        fhtmHead = htmHead.format(**f1)
        strHtmes = ""
        for li in vals:
            if li[5] == None:
                continue
            fes = {'katigoria':nn(li[0]),'apo':nn(li[1]),'apofpa':nn(li[2]),'per':nn(li[3]),'perfpa':nn(li[4]),'se':nn(li[5]),'sefpa':nn(li[6])}
            strHtmes += htmEsLine.format(**fes)
            
        fsqlest = sqlest.format(**f)
        vals,d = dbf.getDbRows(fsqlest, db)
        strHtmest = ""
        for li in vals:
            fes = {'apo':nn(li[0]),'apofpa':nn(li[1]),'per':nn(li[2]),'perfpa':nn(li[3]),'se':nn(li[4]),'sefpa':nn(li[5])}
            strHtmest += htmEstLine.format(**fes)
        
        fsqlds = sqlds.format(**f)
        vals,d = dbf.getDbRows(fsqlds, db)
        strHtmds = ""
        for li in vals:
            if li[5] == None:
                continue
            fes = {'katigoria':nn(li[0]),'apo':nn(li[1]),'apofpa':nn(li[2]),'per':nn(li[3]),'perfpa':nn(li[4]),'se':nn(li[5]),'sefpa':nn(li[6])}
            strHtmds += htmEsLine.format(**fes)
        
        fsqldst = sqldst.format(**f)
        vals,d = dbf.getDbRows(fsqldst, db)
        strHtmdst = ""
        for li in vals:
            fes = {'apo':nn(li[0]),'apofpa':nn(li[1]),'per':nn(li[2]),'perfpa':nn(li[3]),'se':nn(li[4]),'sefpa':nn(li[5])}
            strHtmdst += htmEstLine.format(**fes)    
        self.ptext.setHtml(fhtmHead + strHtmes + strHtmest + htmEjHead + strHtmds + strHtmdst +final)        

if __name__ == '__main__':
    pass
    #createHtml('2011','02')
