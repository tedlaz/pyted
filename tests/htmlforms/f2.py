# -*- coding: utf-8 -*-
'''
Created on 28 Νοε 2013

@author: tedlaz
'''
from collections import OrderedDict
import dbforms as dbf
from PyQt4 import QtCore, QtGui
import locale
import dbforms as dbf
import sys
import os
locale.setlocale(locale.LC_ALL, '')

sqla = u"""
SELECT strftime('%Y',es.dat) as etos,tr.id as trid,et.f2_id as etp,sum(esd.val) as tesv,sum(esd.fpa) as tesfpa
from es
INNER JOIN sr ON sr.id=es.sr_id
INNER JOIN pel ON pel.id=es.pel_id
INNER JOIN esd ON es.id = esd.es_id
INNER JOIN et ON et.id = esd.et_id
INNER JOIN tr on tr.id = (cast(strftime('%m', es.dat) as integer) + 2) / 3 
WHERE etos = '{0}' and tr.id={1}
group by etos,tr.id,et.f2_id
UNION
SELECT strftime('%Y',ds.dat) as etos,tr.id,dt.f2_id,sum(dsd.val),sum(dsd.fpa)
from ds
INNER JOIN pro ON pro.id=ds.pro_id
INNER JOIN dsd ON ds.id = dsd.ds_id
INNER JOIN dt ON dt.id = dsd.dt_id
INNER JOIN tr on tr.id = (cast(strftime('%m', ds.dat) as integer) + 2) / 3 
WHERE etos = '{0}' and tr.id={1}
group by etos,tr.id,dt.f2_id
"""   
txth =u'''
<html>
<body style=" font-size:8pt; font-weight:400; font-style:normal; text-decoration:none;">
<h2><center>ΠΕΡΙΟΔΙΚΗ ΔΗΛΩΣΗ ΦΠΑ</center></h2>
<br>
<p>Έτος : <b>{etos}</b> Τρίμηνο :  <b>{tr}</b></p> 
<br>
<table border="1" align="center" width="100%" cellspacing="0" cellpadding="4">
  <tbody>
    <tr>
      <td colspan=12>Α. ΠΙΝΑΚΑΣ ΜΕ ΤΑ ΣΤΟΙΧΕΙΑ ΤΟΥ ΥΠΟΚΕΙΜΕΝΟΥ ΣΤΟ ΦΟΡΟ Ή ΛΗΠΤΗ</td>  
    </tr>
    <tr> 
      <td colspan=12>101.ΕΠΩΝΥΜΟ Ή ΕΠΩΝΥΜΙΑ <b> {epon} </b></td>   
    </tr>
    <tr> 
      <td colspan=4>102.ΟΝΟΜΑ <br> <b>{onom}</b></td>
      <td><center>103<center></td>
      <td colspan=4>ΟΝΟΜΑ ΠΑΤΕΡΑ <br><b>{patr}</b></td>
      <td><center>104<center></td>
      <td colspan=2>ΑΦΜ <br><b>{afm}</b></td> 
    </tr>
'''
txta = u'''
    <tr>
      <td colspan=12>Β. ΠΙΝΑΚΑΣ ΕΚΡΟΩΝ - ΕΙΣΡΟΩΝ μετά την αφαίρεση (κατά συντελεστή) των επιστροφών - εκπτώσεων.</td>  
    </tr>    
    <tr>
      <td rowspan=3><center>Ι. ΕΚΡΟΕΣ, ΕΝΔΟΚ. ΑΠΟΚΤΗΣΕΙΣ & ΠΡΑΞΕΙΣ ΛΗΠΤΗ σε λοιπή Ελλάδα</center></td>  
      <td width="3%"><center>301</center></td>
      <td align="right" width="9%">{i301}</td>
      <td width="3%"><center>13</center></td>
      <td width="3%"><center>331</center></td>
      <td align="right" width="7%">{i331}</td>
      <td rowspan=3><center>Ι. ΕΙΣΡΟΕΣ, ΕΝΔΟΚ. ΑΠΟΚΤ. ΚΛΠ στη λοιπή Ελλάδα</center></td>  
      <td width="3%"><center>351</center></td>
      <td align="right" width="9%">{i351}</td>
      <td width="3%"><center>13</center></td>
      <td width="3%"><center>371</center></td>
      <td align="right" width="7%">{i371}</td>      
    </tr>
    <tr> 
      <td><center>302</center></td>
      <td align="right">{i302}</td>
      <td><center>6,5</center></td>
      <td><center>332</center></td>
      <td align="right">{i332}</td>
      <td><center>352</center></td>
      <td align="right">{i352}</td>
      <td><center>6,5</center></td>
      <td><center>372</center></td>
      <td align="right">{i372}</td> 
    </tr>
    <tr> 
      <td><center>303</center></td>
      <td align="right">{i303}</td>
      <td><center>23</center></td>
      <td><center>333</center></td>
      <td align="right">{i333}</td> 
      <td><center>353</center></td>
      <td align="right">{i353}</td>
      <td><center>23</center></td>
      <td><center>373</center></td>
      <td align="right">{i373}</td> 
    </tr>
    <tr>
      <td rowspan=3><center>ΙΙ. ΕΚΡΟΕΣ, ΕΝΔΟΚ. ΑΠΟΚΤΗΣΕΙΣ & ΠΡΑΞΕΙΣ ΛΗΠΤΗ στα νησιά Αιγαίου</center></td>  
      <td><center>304</center></td>
      <td align="right">{i304}</td>
      <td><center>9</center></td>
      <td><center>334</center></td>
      <td align="right">{i334}</td>
      <td rowspan=3><center>ΙΙ. ΕΙΣΡΟΕΣ, ΕΝΔΟΚ. ΑΠΟΚΤ. ΚΛΠ στα νησιά Αιγαίου</center></td>  
      <td><center>354</center></td>
      <td align="right">{i354}</td>
      <td><center>9</center></td>
      <td><center>374</center></td>
      <td align="right">{i374}</td>      
    </tr>
    <tr> 
      <td><center>305</center></td>
      <td align="right">{i305}</td>
      <td><center>5</center></td>
      <td><center>335</center></td>
      <td align="right">{i335}</td>
      <td><center>355</center></td>
      <td align="right">{i355}</td>
      <td><center>5</center></td>
      <td><center>375</center></td>
      <td align="right">{i375}</td> 
    </tr>
    <tr> 
      <td><center>306</center></td>
      <td align="right">{i306}</td>
      <td><center>16</center></td>
      <td><center>336</center></td>
      <td align="right">{i336}</td> 
      <td><center>356</center></td>
      <td align="right">{i356}</td>
      <td><center>16</center></td>
      <td><center>376</center></td>
      <td align="right">{i376}</td> 
    </tr>
    <tr>
      <td><center><b>ΣΥΝΟΛΟ ΦΟΡ. ΕΚΡΟΩΝ</b></center></td>  
      <td><center><b>307</b></center></td>
      <td align="right"><b>{i307}</b></td>
      <td><center>ΣΥΝ</center></td>
      <td><center>337</center></td>
      <td align="right"><b>{i337}</b></td>
      <td><center>Δαπάνες γεν.εξ. φορολογητέα</center></td>  
      <td><center>357</center></td>
      <td align="right">{i357}</td>
      <td><center>ΦΠΑ</center></td>
      <td><center>377</center></td>
      <td align="right">{i377}</td>      
    </tr>
    <tr>
      <td><center>Εκροές φορολ.εκτός Ελ Με δικ εκπτ.</center></td>  
      <td><center>308</center></td>
      <td align="right">{i308}</td>
      <td colspan=3 rowspan=4><center></center></td>
      <td><center><b>ΣΥΝΟΛΟ ΦΟΡΟΛ. ΕΙΣΡΟΩΝ</b></center></td>  
      <td><center>358</center></td>
      <td align="right"><b>{i358}</b></td>
      <td><center>ΣΥΝ</center></td>
      <td><center>378</center></td>
      <td align="right"><b>{i378}</b></td>      
    </tr>
    <tr>
      <td><center>Ενδοκ. παραδ. & λοιπά με δικ εκπτ.</center></td>  
      <td><center>309</center></td>
      <td align="right">{i309}</td>
      <td colspan=3><center>δ. ΠΡΟΣΤΙΘΕΜΕΝΑ ΠΟΣΑ ΣΤΟ ΣΥΝΟΛΟ ΦΟΡΟΥ ΕΙΣΡΟΩΝ</center></td> 
      <td colspan=3 rowspan=4><center></center></td> 
    </tr>
    <tr>
      <td><center>Ενδοκ. παραδ. & Λοιπά χωρίς δικ εκπτ.</center></td>  
      <td><center>310</center></td>
      <td align="right">{i310}</td>
      <td><center>Επιστροφή φόρου</center></td>
      <td><center>400</center></td>
      <td align="right">{i400}</td> 
    </tr>
    <tr>
      <td><center><b>ΣΥΝΟΛΟ ΕΚΡΟΩΝ</b></center></td>  
      <td><center>311</center></td>
      <td align="right"><b>{i311}</b></td>
      <td><center>Πιστ. υπολ.</center></td>
      <td><center>401</center></td>
      <td align="right">{i401}</td> 
    </tr> 
    <tr>
      <td colspan=6><center>γ. ΕΙΔΙΚΟΙ Λ/ΜΟΙ</center></td>  
      <td><center>Λοιπά Προστ.</center></td>
      <td><center>402</center></td>
      <td align="right">{i402}</td> 
    </tr>
    <tr>
      <td colspan=3><center>Συνολικές ενδοκοινοτικές αποκτήσεις</center></td>  
      <td><center>341</center></td>
      <td align="right" colspan=2>{i341}</td>
      <td><center>Χρ. Αρχικής</center></td> 
      <td><center>403</center></td>
      <td align="right">{i403}</td> 
      <td colspan=2><center>404</center></td>
      <td align="right">{i404}</td>
    </tr>
    <tr>
      <td colspan=3><center>Συνολικές ενδοκοινοτικές παραδόσεις</center></td>  
      <td><center>342</center></td>
      <td align="right" colspan=2>{i342}</td>
      <td colspan=3 ><center>ε.ΑΦΑΙΡΟΥΜΕΝΑ ΠΟΣΑ</center></td> 
      <td colspan=3 rowspan=2><center></center></td>   
    </tr>            
  </tbody>
    <tr>
      <td colspan=3><center>Πράξεις λήπτη αγαθών & υπηρ.</center></td>  
      <td><center>343</center></td>
      <td align="right" colspan=2>{i343}</td>
      <td><center>ΦΠΑ Prorata</center></td>
      <td><center>411</center></td>
      <td align="right">{i411}</td>   
   
    </tr>
    <tr>
      <td colspan=3><center>Ενδοκ. Λήψεις υπηρ.</center></td>  
      <td><center>344</center></td>
      <td align="right" colspan=2>{i344}</td>
      <td><center>Λοιπά Αφαιρούμενα</center></td>
      <td><center>412</center></td>
      <td align="right">{i412}</td>
      <td colspan=2><center>413</center></td>   
      <td align="right">{i413}</td>  
    </tr>
    <tr>
      <td colspan=3><center>Ενδοκ. παροχές υπηρ.</center></td>  
      <td><center>345</center></td>
      <td align="right" colspan=2>{i345}</td>
      <td colspan=3><center><b>ΥΠΟΛΟΙΠΟ ΦΟΡΟΥ ΕΙΣΡΟΩΝ</b></center></td>
      <td colspan=2><center>420</center></td>   
      <td align="right"><b>{i420}</b></td>  
    </tr>
    <tr>
      <td colspan=12>Γ. ΠΙΝΑΚΑΣ ΕΚΚΑΘΑΡΙΣΗΣ ΤΟΥ ΦΟΡΟΥ για καταβολή, έκπτωση ή επιστροφή</td>  
    </tr>
    <tr>
      <td><center><b>ΠΙΣΤΩΤΙΚΟ ΥΠΟΛΟΙΠΟ</b></center></td>  
      <td><center><b>501</b></center></td>
      <td align="right"><b>{i501}</b></td>
      <td colspan=3></center></td>
      <td colspan=3><center><b>ΧΡΕΩΣΤΙΚΟ ΥΠΟΛΟΙΠΟ</b></center></td>
      <td><center><b>511</b></center></td>
      <td align="right" colspan=2><b>{i511}</b></td>
    </tr>       
   <tbody>      
</table>
<br>
<br>
<br>
<br>

</body>
</html>
'''
def numOrEmptytext(val):
    if dbf.isNum(val):
        return val
    else:
        return ''
vals = [
        ['a1','b1','c1',1,1,1,1],
        ['a1','b1','c2',1,1,1,1],
        ['a1','b1','c3',1,1,1,1],
        ['a1','b2','c2',1,1,1,1],
        ['a1','b2','c5',1,1,1,1],
        ['a1','b3','c1',1,1,1,1],
        ['a2','b1','c2',1,1,1,1],
        ['a2','b3','c1',1,1,1,1],
        ]
def addArrs(ar1,ar2):
    '''
    having ar1: [a1,a2,...,an] and ar2: [b1,b2,...,bn]
    addArrs(ar1,ar2) returns [a1+b1,a2+b2,...,an+bn]
    '''
    len1 = len(ar1)
    len2 = len(ar2)
    if len1 <> len2:
        print 'error , arrays have not the same length'
        return []
    far = []
    for i in range(len1):
        'If Numeric adds else appends empty string'
        if dbf.isNum(ar1[i]) and dbf.isNum(ar2[i]):
            far.append(ar1[i]+ar2[i])
        else:
            far.append('')
    return far

def createSubtotalsFromOrderedVals(vals,depth):
    '''
    Having an ordered from left to right vals array [[a1,a2,...,an],[b1,b2,..bn],...[N1,N2,...,Nn]]
    uses columns from 0 to Depth to create subtotals on Numeric Values
    '''
    tots = OrderedDict()
    ar = []
    for val in vals:      
        stra = ''
        preval = '0'
        for col in range(depth):
            if stra == '': par = '0'
            else: par = stra
            #par = stra
            stra += '%s' % val[col]
            ar.append(stra)
            if stra in tots:
                tots[stra] = [par,addArrs(tots[stra][1],val[depth:]),'%s'% val[col],preval]
            else:
                tots[stra] = [par,[numOrEmptytext(tim) for tim in val[depth:]],'%s'% val[col],preval]
            preval = '%s'% val[col]  
    print tots
tstArr = [
          [0,452,0],
          [1,180,23],
          [301,188000,24440],
          [303,20481500,4710745],
          [357,969,171.27]]
def fpaCheck(arr):
    va = ['i301','i302','i303','i304','i305','i306','i307','i308','i309','i310','i311','i331','i332','i333','i334','i335','i336','i337',
          'i341','i342','i343','i344','i345','i346',
          'i351','i352','i353','i354','i355','i356','i357','i358','i371','i372','i373','i374','i375','i376','i377','i378',
          'i400','i401','i402','i403','i404','i411','i412','i413','i420',
          'i501','i502','i503','i511','i512','i513','i514','i521','i522']
    f = OrderedDict()
    des = dex = dbf.dec(0)
    for el in va:
        f[el] = dbf.dec(0)
    for lin in arr:
        linv = 'i%s' % lin[0]
        l1 = dbf.dec(lin[1])
        l2 = dbf.dec(lin[2])
        if linv == 'i301' : 
            f['i301'] += l1
            f['i331'] += dbf.dec((l1 * dbf.dec(.13,3)))
            des += l2 - f['i331']
        elif linv == 'i302' : 
            f['i302'] += l1
            f['i332'] += dbf.dec((l1 * dbf.dec(.065,3)))
            des += l2 - f['i332']
        elif linv == 'i303' : 
            f['i303'] += l1
            f['i333'] += dbf.dec((l1 * dbf.dec(.23,3)))
            des += l2 - f['i333']
        elif linv == 'i304' : 
            f['i304'] += l1
            f['i334'] += dbf.dec((l1 * dbf.dec(.09,3)))
            des += l2 - f['i334']
        elif linv == 'i305' : 
            f['i305'] += l1
            f['i335'] += dbf.dec((l1 * dbf.dec(.05,3)))
            des += l2 - f['i335']
        elif linv == 'i306' : 
            f['i306'] += l1
            f['i336'] += dbf.dec((l1 * dbf.dec(.16,3)))
            des += l2 - f['i336']
        elif linv == 'i308' : f['i308'] += l1 
        elif linv == 'i309' : f['i309'] += l1 
        elif linv == 'i310' : f['i310'] += l1         
        elif linv == 'i351' : 
            f['i351'] += l1
            f['i371'] += dbf.dec((l1 * dbf.dec(.13,3)))
            dex += l2 - f['i371']
        elif linv == 'i352' : 
            f['i352'] += l1
            f['i372'] += dbf.dec((l1 * dbf.dec(.065,3)))
            dex += l2 - f['i372']
        elif linv == 'i353' : 
            f['i353'] += l1
            f['i373'] += dbf.dec((l1 * dbf.dec(.23,3)))
            dex += l2 - f['i373']
        elif linv == 'i354' : 
            f['i354'] += l1
            f['i374'] += dbf.dec((l1 * dbf.dec(.09,3)))
            dex += l2 - f['i374']
        elif linv == 'i355' : 
            f['i355'] += l1
            f['i375'] += dbf.dec((l1 * dbf.dec(.05,3)))
            dex += l2 - f['i375']
        elif linv == 'i356' : 
            f['i356'] += l1
            f['i376'] += dbf.dec((l1 * dbf.dec(.16,3)))
            dex += l2 - f['i376']                                                                                                          
        elif linv == 'i357' : 
            f['i357'] += l1
            f['i377'] += l2
        
    if des > 0: f['i412'] += des
    else:       f['i402'] += dbf.dec(des * dbf.dec(-1))
    
    if dex > 0: f['i402'] += dex
    else:       f['i412'] += dbf.dec(dex * dbf.dec(-1))
    f['i307'] = f['i301']+f['i302']+f['i303']+f['i304']+f['i305']+f['i306']
    f['i337'] = f['i331']+f['i332']+f['i333']+f['i334']+f['i335']+f['i336']
    f['i358'] = f['i351']+f['i352']+f['i353']+f['i354']+f['i355']+f['i356']+f['i357']
    f['i378'] = f['i371']+f['i372']+f['i373']+f['i374']+f['i375']+f['i376']+f['i377']
    f['i311'] = f['i307']+f['i308']+f['i309']+f['i310']
    f['i404'] = f['i400']+f['i401']+f['i402']+f['i403']
    f['i413'] = f['i411']+f['i412']
    f['i420'] = f['i378']+f['i404']-f['i413']
    if f['i337'] > f['i420']:
        f['i511'] = f['i337']-f['i420']
    else:
        f['i501'] = f['i420']-f['i337']
    return f

def strFpa(f):
    for key in f:
        f[key] = locale.format("%0.2f", f[key], grouping=True)
    str  = ''
    str += '301 : %13s  331 : %12s   351 : %13s  371 : %12s\n' % (f[301],f[331],f[351],f[371])
    str += '302 : %13s  332 : %12s   352 : %13s  372 : %12s\n' % (f[302],f[332],f[352],f[372])
    str += '303 : %13s  333 : %12s   353 : %13s  373 : %12s\n' % (f[303],f[333],f[353],f[373])
    str += '304 : %13s  334 : %12s   354 : %13s  374 : %12s\n' % (f[304],f[334],f[354],f[374])
    str += '305 : %13s  335 : %12s   355 : %13s  375 : %12s\n' % (f[305],f[335],f[355],f[375])
    str += '306 : %13s  336 : %12s   356 : %13s  376 : %12s\n' % (f[306],f[336],f[356],f[376])
    str += '307 : %13s  337 : %12s   357 : %13s  377 : %12s\n' % (f[307],f[337],f[357],f[377])
    str += '308 : %13s        %12s   358 : %13s  378 : %12s\n' % (f[308],''    ,f[358],f[378])
    str += '309 : %13s  \n' % (f[309],)
    str += '310 : %13s        %12s   400 : %13s \n' % (f[310],''    ,f[400])
    str += '311 : %13s        %12s   401 : %13s \n' % (f[311],''    ,f[401])
    str += '      %13s        %12s   402 : %13s \n' % (''    ,''    ,f[402])
    str += '341 : %13s  344 : %12s   403 : %13s  404 : %12s\n' % (f[341],f[344],f[403],f[404])
    str += '342 : %13s  345 : %12s   411 : %13s \n' % (f[342] ,f[345],f[411])
    str += '343 : %13s  346 : %12s   412 : %13s  413 : %12s\n\n' % (f[343],f[346],f[412],f[413])
    str += '      %13s        %12s         %13s  420 : %12s\n\n' % ('','','',f[420])
    str += '501 : %13s        %12s   511 : %13s \n' % (f[501],'',f[511])
    return str


class PtextForm(QtGui.QDialog):
    def __init__(self,parent=None, etos=None, trimino=None):
        super(PtextForm, self).__init__(parent)
        layout = QtGui.QVBoxLayout()
        
        self.parent = parent
        self.fname = None #Όνομα αρχείου pdf για αποθήκευση της περιοδικής ΦΠΑ
        
        headLay = QtGui.QHBoxLayout()
        headLay.addWidget(dbf.makeTitle(u'Περιοδική ΦΠΑ'))
        self.letos = QtGui.QLabel(u'Έτος')
        self.letos.setMaximumSize(60, 60)
        self.etos = QtGui.QLineEdit()
        headLay.addWidget(self.letos)
        headLay.addWidget(self.etos)
        self.ltr = QtGui.QLabel(u'Τρίμηνο')
        self.tr = QtGui.QLineEdit()
        headLay.addWidget(self.ltr)
        headLay.addWidget(self.tr)
        self.go = QtGui.QPushButton(u'Πάμε')
        self.go.clicked.connect(self.fillData)
        headLay.addWidget(self.go)
        layout.addLayout(headLay)
        self.ptext = QtGui.QTextEdit(self)
        self.ptext.setFont(QtGui.QFont('Times',20))
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
        if trimino and etos:
            self.etos.setText(etos)
            self.tr.setText(trimino)
            self.fillData(etos, trimino)
        
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
        dialog.printer().setPageMargins(10,20,10,20,QtGui.QPrinter.Millimeter)
        dialog.paintRequested.connect(self.ptext.print_)
        dialog.exec_()
                
    def canAdd(self):
        return False
    
    def fillData(self, et=None,tr=None):
        if et:
            etos = et
        else:
            etos = self.etos.text()
        if tr:    
            tri = tr
        else:
            tri = self.tr.text()
            
        tri  =self.tr.text()
        sqlco = "SELECT cop, ono, pat,afm FROM co WHERE id=1"
        
        sql = sqla.format(etos,tri)
        
        if self.parent:
            db = self.parent.db
        else:
            self.ptext.setHtml(u"f2 Line 499 : Δεν υπάρχει σύνδεση με βάση")
            return
            #db = 'C:/Users/tedlaz/Desktop/tso.ee3'
        arr ,b = dbf.getDbRows(sql, db)
        cod ,b = dbf.getDbRows(sqlco, db)
        sqlQuart = "SELECT trp FROM tr WHERE id=%s" % tri
        quart ,b= dbf.getDbRows(sqlQuart, db)
        qu = '%s' % quart[0]
        hdata = {'etos':etos,'tr':qu,'epon':cod[0][0],'onom':cod[0][1],'patr':cod[0][2],'afm':cod[0][3]}
        self.fname = u'fpa-%s-%s-%s' % (cod[0][0],etos,tri)
        htmh = txth.format(**hdata)
        farr =[]
        if arr:
            for lin in arr:
                farr.append([lin[2],lin[3],lin[4]])
        fpadict = fpaCheck(farr)
        for key in fpadict:
            fpadict[key] = locale.format("%0.2f", fpadict[key], grouping=True)
        htm = txta.format(**fpadict)
        self.ptext.setHtml(htmh+htm)
    
if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    
    tf = PtextForm()
    tf.show() 
    sys.exit(app.exec_())
