# -*- coding: utf-8 -*-

import reportl.classReport as cr

from PyQt4 import QtGui, Qt
import utils.dbutils as adb
from qtprint import qt_table_report as qttr
sqlHeader = '''
SELECT m12_mis.id, m12_xrisi.xrisi , m12_period.periodp,m12_mist.mistp, m12_mis.mist_id
FROM m12_mis
INNER JOIN m12_xrisi on m12_xrisi.id=m12_mis.xrisi_id
INNER JOIN m12_period on m12_period.id=m12_mis.period_id
INNER JOIN m12_mist on m12_mist.id=m12_mis.mist_id
WHERE m12_mis.id=%s
'''
sqlrows = '''
SELECT m12_fpr.epon || ' ' ||  m12_fpr.onom,m12_eid.eidp, m12_misdf.misim, 
       m12_misdf.meres, m12_misdf.apod, m12_misdf.ikaer, m12_misdf.ikaet, 
       m12_misdf.ika, m12_misdf.fmy, m12_misdf.eea, m12_misdf.tker,m12_misdf.plir
FROM m12_misdf
INNER JOIN m12_mis on m12_mis.id=m12_misdf.mis_id
INNER JOIN m12_pro on m12_pro.id=m12_misdf.pro_id
INNER JOIN m12_fpr on m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_eid on m12_eid.id=m12_pro.eid_id
WHERE m12_misdf.mis_id=%s
'''
sqlFooter = '''
SELECT * FROM m12_co
'''


sql1 = '''
select  m12_fpr.epon || ' ' || m12_fpr.onom as onomatep, m12_eid.eidp,
sum( case when mtyp_id=100 then val end) as imeromisthio,
sum( case when mtyp_id=110 then val end) as imeres,
sum( case when mtyp_id=200 then val end) as apodoxes,
sum( case when mtyp_id=500 then val end) as ikaEnos,
sum( case when mtyp_id=501 then val end) as ikaEtis,
sum( case when mtyp_id=502 then val end) as ika,
sum( case when mtyp_id=600 then val end) as fmy,
sum( case when mtyp_id=610 then val end) as eea,
sum( case when mtyp_id=700 then val end) as kratEnos,
sum( case when mtyp_id=900 then val end) as plir
from m12_misd
inner join m12_mis on m12_mis.id=m12_misd.mis_id
inner join m12_pro on  m12_pro.id=m12_misd.pro_id
inner join m12_fpr on m12_fpr.id=m12_pro.fpr_id
inner join m12_eid on m12_eid.id=m12_pro.eid_id
where mis_id=%s
group by mis_id,pro_id
'''

def makeRpt(misNo,pdfName,db):
    head = adb.getDbOneRow(sqlHeader % misNo, db)
    footd = adb.getDbOneRow(sqlFooter,db)
    if int(head[4]) == 1:
        h1 = head[2]
    else:
        h1 = head[3]
    title  = u'Μισθοδοσία για την περίοδο : %s %s' % (h1,head[1])
    title2 = u'Τύπος : %s' % head[3]
    foot   = u'%s  ΑΦΜ: %s ΔΟΥ: %s' % (footd[1],footd[6],footd[7]) 
    titles = [u'AA',u'Ονοματεπώνυμο',u'Ειδικότητα',u'Ημ/σθιο',u'Μέρες',u'Αποδοχές',
              u'ΙΚΑ Εργ/νου',u'ΙΚΑ Εργοδότη',u'ΙΚΑ',u'ΦΜΥ',u'Eιδ.Επ. Αληλεγγ.',u'Kρατήσεις Eργ/νου',u'Πληρωτέο']

    typeArr =     ['t','tc','n','i','n','n','n','n','n','n','n','n']
    sumArr  =     [ 0 , 0  , 0 , 0 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ]
    sizeArr = [20 ,150 ,80 ,50 ,40 ,50 ,50 ,50 ,50 ,50 ,50 ,50 ,50 ]
    
    v = cr.makePrintTable(adb.getDbRows(sql1 % misNo,db),typeArr,sumArr,True)

    rep = cr.pdfReport(portrait=False)

    rep.makepdf(title,titles,v,sizeArr,pdfName,title2,foot)
    return True

class testprn1(QtGui.QDialog):
    def __init__(self,misNo,pdfName,db):
        QtGui.QDialog.__init__(self)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        
        head = adb.getDbOneRow(sqlHeader % misNo, db)
        footd = adb.getDbOneRow(sqlFooter,db)
        if int(head[4]) == 1:
            h1 = head[2]
        else:
            h1 = head[3] 
        title  = u'Μισθοδοσία για την περίοδο : %s %s' % (h1,head[1])
        title2 = u'Τύπος : %s' % head[3] 
        foot   = u'%s  ΑΦΜ: %s ΔΟΥ: %s' % (footd[1],footd[6],footd[7])
        hlabels = [u'Ονοματεπώνυμο',u'Ειδικότητα',u'Ημ/σθιο',u'Μέρες',u'Αποδοχές',
                  u'ΙΚΑ Εργ/νου',u'ΙΚΑ Εργοδότη',u'ΙΚΑ',u'ΦΜΥ',u'Eιδ.Επ. Αληλεγγ.',u'Kρατήσεις Eργ/νου',u'Πληρωτέο'] 
                        

        data = adb.getDbRows(sql1 % misNo,db)
        colSizes=[20,14,7,7,8,8,8,8,7,7,7,8]
        colTypes=[ 0,0,2,1,2,2,2,2,2,2,2,2] 
        colAlign=[ 0,0,1,1,2,2,2,2,2,2,2,2]
        colSum  =[ 0,0,0,1,1,1,1,1,1,1,1,1] 
        f ={'orientation'  :1,
            'pdfName'      :pdfName,
            'fontFamily'   :'Helvetica', 
            'ReportHeader1':title,
            'ReportHeader2':title2,
            'ReportHeader3':u'',
            'headerLabels':hlabels,
            'columnSizes' :colSizes,
            'columnToSum' :colSum,
            'columnTypes' :colTypes,
            'columnAlign' :colAlign,
            'footerLine'  :False,
            'footerText'  :foot,
            'footerPageNumberText':u'Σελίδα',
            'data'        :data
            }              
        self.rep = qttr.qtTableReport(f)

        tstButton = QtGui.QPushButton('test')
        tstButton.clicked.connect(self.onClick)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(tstButton)
        self.setLayout(layout)
        
    def onClick(self):
        self.rep.printPreview()

if __name__ == '__main__':
    
    import sys

    app = QtGui.QApplication(sys.argv)
    window = testprn1(6,'a.pdf','c:/ted/mis.sql3')
    #window.initData()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())

    #makeRpt(1,'a.pdf','c:/ted/mis.sql3')
