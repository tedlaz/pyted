# -*- coding: utf-8 -*-
'''
Created on 18 Νοε 2012

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore, Qt

from gui import ui_print_rpt_misthodosia
from qtprint import qt_table_report as qttr
import utils.dbutils as adb
sqlmis = '''
SELECT m12_mis.id, xrisi,periodp,mistp,imnia
FROM m12_mis
INNER JOIN m12_xrisi on m12_xrisi.id=m12_mis.xrisi_id
INNER JOIN m12_period on m12_period.id = m12_mis.period_id
INNER JOIN m12_mist on m12_mist.id=m12_mis.mist_id
ORDER BY xrisi DESC, m12_period.id DESC
'''
sqlHeader = '''
SELECT m12_mis.id, m12_xrisi.xrisi , m12_period.periodp,m12_mist.mistp,
       m12_mis.mist_id
FROM m12_mis
INNER JOIN m12_xrisi on m12_xrisi.id=m12_mis.xrisi_id
INNER JOIN m12_period on m12_period.id=m12_mis.period_id
INNER JOIN m12_mist on m12_mist.id=m12_mis.mist_id
WHERE m12_mis.id=%s
'''
sqlrows = '''
SELECT m12_fpr.epon || ' ' ||  m12_fpr.onom,m12_eid.eidp, m12_misdf.misim,
       m12_misdf.meres, m12_misdf.apod, m12_misdf.ikaer, m12_misdf.ikaet,
       m12_misdf.ika, m12_misdf.fmy, m12_misdf.eea, m12_misdf.tker,
       m12_misdf.plir
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


class dlg(QtGui.QDialog):
    def __init__(self, args=None, parent=None):
        super(dlg, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.ui = ui_print_rpt_misthodosia.Ui_Dialog()
        self.ui.setupUi(self)
        #
        self.makeConnections()

        if parent:
            self.db = parent.db
        else:
            self.db = ''
        self.populate()

    def makeMisData(self, misNo, pdfName):

        head = adb.getDbOneRow(sqlHeader % misNo, self.db)
        footd = adb.getDbOneRow(sqlFooter, self.db)
        if int(head[4]) == 1:
            h1 = head[2]
        else:
            h1 = head[3]
        title = u'Μισθοδοσία για την περίοδο : %s %s' % (h1, head[1])
        title2 = u'Τύπος : %s' % head[3]
        foot = u'%s  ΑΦΜ : %s ΔΟΥ : %s' % (footd[1], footd[6], footd[7])
        hlabels = [u'AA', u'Ονοματεπώνυμο', u'Ειδικότητα', u'Μισθός Ημ/σθιο',
                   u'Μέρες', u'Αποδοχές', u'ΙΚΑ Εργ/νου', u'ΙΚΑ Εργοδότη',
                   u'ΙΚΑ', u'ΦΜΥ', u'Eιδ.Επ. Αληλεγγ.', u'Kρατήσεις Eργ/νου',
                   u'Πληρωτέο']
        data = adb.getDbRowsCounted(sql1 % misNo, self.db)
        colSizes = [3, 18, 10, 7, 4, 7, 7, 7, 8, 7, 7, 8, 7]
        colTypes = [1, 0, 0, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2]
        colAlign = [1, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2]
        colSum = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        f = {'orientation': 1,
             'pdfName': pdfName,
             'fontFamily': 'Tahoma',
             'ReportHeader1': title,
             'ReportHeader2': title2,
             'ReportHeader3': u'',
             'headerLabels': hlabels,
             'columnSizes': colSizes,
             'columnToSum': colSum,
             'columnTypes': colTypes,
             'columnAlign': colAlign,
             'footerLine': True,
             'footerText': foot,
             'footerPageNumberText': u'Σελίδα',
             'data': data
             }
        self.rep = qttr.qtTableReport(f)

    def populate(self):
        from utils.qtutils import populateTableWidget
        headers = [u'ΑΑ', u'Χρήση', u'Περίοδος', u'Περιγραφή', u'Ημνία']
        populateTableWidget(self.ui.tblMis,
                            sqlmis,
                            headers,
                            self.db,
                            colWidths=[10, 50, 120, 140, 100])

    def makeConnections(self):
        QtCore.QObject.connect(self.ui.b_print,
                               QtCore.SIGNAL("clicked()"),
                               self.printToPdf)
        self.ui.tblMis.cellDoubleClicked.connect(self.printToPdf)

    def printToPdf(self):
        misid = self.ui.tblMis.item(self.ui.tblMis.currentRow(), 0).text()

        if misid:
            xri = self.ui.tblMis.item(self.ui.tblMis.currentRow(), 1).text()
            defaultPdfName = 'mis-%s-%s.pdf' % (xri, misid)
            self.makeMisData(misid, defaultPdfName)
            self.rep.printPreview()
            # self.rep.printPdf()
            # self.accept()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = dlg(sys.argv)
    form.show()
    app.exec_()
