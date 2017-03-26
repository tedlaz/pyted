#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Input form
'''
import sys
import os
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import tedqt as qted
from tedutil.dec import dec
from tedutil import db as s2d
from lmocreate import mlmo
from suds.client import Client  # To setup run : sudo pip install suds-jurko


CPATH = os.path.dirname(os.path.abspath(__file__))


def vatol(afm, country_code='EL'):
    '''
    VAT Check online
    using SOAP client
    returns dictionary with:
    countryCode, vatNumber, requestDate, valid, name, address
    '''
    url = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    result = {'valid': False}
    try:
        client = Client(url, timeout=10)
        result = client.service.checkVat(country_code, afm)
    except:
        result['conError'] = True
    return result


class Insert(Qw.QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)

        self.db = db
        self._ui()

    def _ui(self):
        self.setWindowTitle(u'Εισαγωγή Παραστατικών Πωλήσεων / Αγορών')
        p1 = "SELECT id || ' ' || epo FROM syn WHERE id='%s'"
        p9 = ("SELECT id, id || ' ' || epo as val FROM syn "
              "WHERE grup(val) LIKE '%%%s%%'")
        lori = [['ell', u'Έσωτερικό'],
                ['eur', u'Ενδοκοινοτικό'],
                ['exo', u'Εξωτερικό']]
        ltyp = [['normal', u'Κανονικό'], ['credit', u'Πιστωτικό']]
        lpli = [[1, u'Μετρητά'], [2, u'Πίστωση']]
        self.flds = {'id': qted.wIntSpin(),
                     'dat': qted.wDat(),
                     'cat_id': qted.wTxtCombo(26, [[7, u'Έσοδα'],
                                              [26, u'Έξοδα']]),
                     'ori_id': qted.wTxtCombo('ell', lori),
                     'typ_id': qted.wTxtCombo('normal', ltyp),
                     'pno': qted.wTxtLine(),
                     'afm': qted.wTxtButton('', p1, p9, self.db, self),
                     'per': qted.wTxtLine(),
                     'pli_id': qted.wTxtCombo(1, lpli),
                     'par_id': qted.wTxtCombo(1, [[1, u'Κεντρικό']])
                     }

        mainLayout = Qw.QVBoxLayout(self)
        glay = Qw.QGridLayout()
        glay.addWidget(Qw.QLabel(u'Έσοδα/έξοδα'), 0, 0)
        glay.addWidget(self.flds['cat_id'], 0, 1)
        self.flds['cat_id'].currentIndexChanged.connect(self.showHideefpa)

        glay.addWidget(Qw.QLabel(u'Προέλευση'), 1, 2)
        glay.addWidget(self.flds['ori_id'], 1, 3)

        glay.addWidget(Qw.QLabel(u'Τύπος'), 1, 0)
        glay.addWidget(self.flds['typ_id'], 1, 1)

        glay.addWidget(Qw.QLabel(u'Ημερομηνία'), 2, 0)
        glay.addWidget(self.flds['dat'], 2, 1)

        glay.addWidget(Qw.QLabel(u'Τρόπος πληρωμής'), 2, 2)
        glay.addWidget(self.flds['pli_id'], 2, 3)

        glay.addWidget(Qw.QLabel(u'Παράρτημα'), 0, 2)
        glay.addWidget(self.flds['par_id'], 0, 3)

        glay.addWidget(Qw.QLabel(u'ΑΦΜ/Επωνυμία'), 3, 0)
        glay.addWidget(self.flds['afm'], 3, 1, 1, 2)

        glay.addWidget(self.flds['per'], 3, 3, 1, 3)

        glay.addWidget(Qw.QLabel(u'Παραστατικό'), 4, 0)
        glay.addWidget(self.flds['pno'], 4, 1)

        self.bAddLine = Qw.QPushButton(u'Νέα γραμμή')
        glay.addWidget(self.bAddLine, 4, 4, 1, 2)

        mainLayout.addLayout(glay)

        self.tbl = Qw.QTableWidget(self)
        # self.tbl.setStyleSheet(dbf.tblStyle)
        # self.tbl.setItemDelegate(ValidatedItemDelegate())
        # self.tbl.verticalHeader().setDefaultSectionSize(25)
        self.tbl.setAlternatingRowColors(True)
        self.tbl.setColumnCount(7)
        hds = [u'Λογαριασμός', u'ΦΠΑ%', u'Αξία', u'ΦΠΑ',
               u'Σύνολο', u'Εκπ', 'id']
        self.tbl.setHorizontalHeaderLabels(hds)
        self.tbl.setColumnWidth(0, 300)
        mainLayout.addWidget(self.tbl)

        self.ffld = {'tval': qted.wNum(),
                     'tfpa': qted.wNum(),
                     'ttot': qted.wNum()}

        alr = Qc.Qt.AlignRight | Qc.Qt.AlignTrailing | Qc.Qt.AlignVCenter

        for el in self.ffld:
            self.ffld[el].setAlignment(alr)
            self.ffld[el].setReadOnly(True)

        flay = Qw.QGridLayout()
        flay.addWidget(Qw.QLabel(u'Καθαρή Αξία'), 0, 0)
        flay.addWidget(Qw.QLabel(u'ΦΠΑ'), 0, 1)
        flay.addWidget(Qw.QLabel(u'Σύνολο'), 0, 2)
        flay.addWidget(self.ffld['tval'], 1, 0)
        flay.addWidget(self.ffld['tfpa'], 1, 1)
        flay.addWidget(self.ffld['ttot'], 1, 2)
        sp = Qw.QSpacerItem(110, 20, Qw.QSizePolicy.Expanding,
                            Qw.QSizePolicy.Minimum)
        flay.addItem(sp, 1, 3)
        self.bSave = Qw.QPushButton(u'Αποθήκευση')
        flay.addWidget(self.bSave, 0, 4, 2, 1)
        mainLayout.addLayout(flay)

        self.setLayout(mainLayout)
        self.resize(900, 400)

        self.bAddLine.clicked.connect(self.newrow)
        self.bSave.clicked.connect(self.save)
        self.bAddLine.setFocusPolicy(Qc.Qt.NoFocus)
        self.bSave.setFocusPolicy(Qc.Qt.NoFocus)
        self.flds['afm'].valNotFound.connect(self.addNewPerson)
        # self.tbl.cellClicked.connect(self.cChanged)
        self.newrow()

    @Qc.pyqtSlot(str)
    def addNewPerson(self, val):
        tmpl = u'ΑΦΜ: {id}\nΕπωνυμία: {epo}\nΔιεύθυνση : {adr}'
        Qw.QMessageBox.critical(self, u"Λάθος", u'Η τιμή %s δεν υπάρχει' % val)
        if len(val) == 9:
            syn = vatol(val)
            if syn['valid']:
                f = {}
                f['ccd'] = '%s' % syn['countryCode']
                f['id'] = '%s' % syn['vatNumber']
                f['vda'] = '%s' % syn['requestDate']
                nams = syn['name'].strip().split('||')
                if len(nams) == 1:
                    f['epo'] = '%s' % syn['name']
                    f['ep2'] = ''
                else:
                    f['epo'] = nams[0]
                    f['ep2'] = nams[1]
                f['adr'] = '%s' % syn['address']
                savedid = s2d.insert('syn', f, self.db)
                self.flds['afm'].set(val)

    def calcTotals(self):
        tpos = tfpa = ttot = dec(0)
        for i in range(self.tbl.rowCount()):
            tpos += self.tbl.cellWidget(i, 2).get()
            tfpa += self.tbl.cellWidget(i, 3).get()
            ttot += self.tbl.cellWidget(i, 4).get()
        self.ffld['tval'].set(tpos)
        self.ffld['tfpa'].set(tfpa)
        self.ffld['ttot'].set(ttot)

    def chposo(self):  # Αλλαγή ποσού
        for i in range(self.tbl.rowCount()):
            pfpa = dec(self.tbl.cellWidget(i, 1).get() / dec(100))
            poso = self.tbl.cellWidget(i, 2).get()
            fpa = dec(pfpa * poso)
            tot = poso + fpa
            self.tbl.cellWidget(i, 3).set(fpa)
            self.tbl.cellWidget(i, 4).set(tot)
        self.calcTotals()

    def chtot(self):  # Αλλαγή ΦΠΑ
        for i in range(self.tbl.rowCount()):
            pfpap = dec(1 + self.tbl.cellWidget(i, 1).get() / dec(100))
            tot = self.tbl.cellWidget(i, 4).get()
            poso = dec(tot / pfpap)
            fpa = tot - poso
            self.tbl.cellWidget(i, 2).set(poso)
            self.tbl.cellWidget(i, 3).set(fpa)
        self.calcTotals()

    def chfpa(self):  # Αλλαγή Συνόλου
        for i in range(self.tbl.rowCount()):
            pfpa = dec(self.tbl.cellWidget(i, 1).get() / dec(100))
            if pfpa == 0:
                self.tbl.cellWidget(i, 3).set(0)
                return
            fpa = self.tbl.cellWidget(i, 3).get()
            poso = dec(fpa / pfpa)
            tot = poso + fpa
            self.tbl.cellWidget(i, 2).set(poso)
            self.tbl.cellWidget(i, 4).set(tot)
        self.calcTotals()

    def reset(self):  # Μηδενισμός φόρμας
        self.flds['pno'].set('')
        for i in range(self.tbl.rowCount()):
            self.tbl.cellWidget(i, 2).set(0)
            self.tbl.cellWidget(i, 3).set(0)
            self.tbl.cellWidget(i, 4).set(0)
        self.calcTotals()

    def newrow(self):
        '''Adding a row'''
        rowidx = self.tbl.rowCount()
        self.tbl.setRowCount(rowidx + 1)

        sq1 = "SELECT id || ' ' || lmp FROM lm WHERE id='%s'"
        sq9 = ("SELECT id, id || ' ' || lmp as val FROM lm "
               "WHERE grup(val) LIKE '%%%s%%'")
        self.tbl.setCellWidget(rowidx,
                               0, qted.wTxtButton('', sq1, sq9, self.db, self))
        pfpa = [[0, u'Χωρίς ΦΠΑ'], [13, '13%'], [17, '17%'], [24, '24%']]
        self.tbl.setCellWidget(rowidx, 1, qted.wTxtCombo(24, pfpa))
        self.tbl.setCellWidget(rowidx, 2, qted.wNum())
        self.tbl.setCellWidget(rowidx, 3, qted.wNum())
        self.tbl.setCellWidget(rowidx, 4, qted.wNum())
        efpa = [[0, u'Όχι'], [1, u'Ναί']]
        self.tbl.setCellWidget(rowidx, 5, qted.wTxtCombo(1, efpa))
        self.tbl.setCellWidget(rowidx, 6, qted.wIntSpin())
        self.tbl.cellWidget(rowidx, 1).currentIndexChanged.connect(self.chposo)
        self.tbl.cellWidget(rowidx, 2).editingFinished.connect(self.chposo)
        self.tbl.cellWidget(rowidx, 3).editingFinished.connect(self.chfpa)
        self.tbl.cellWidget(rowidx, 4).editingFinished.connect(self.chtot)
        self.showHideefpa()

    def showHideefpa(self):
        '''Hides or Shows fpa column'''
        if self.flds['cat_id'].get() == 7:
            self.tbl.hideColumn(5)
        else:
            self.tbl.showColumn(5)

    def dic(self):
        '''Create a dictionary from values'''
        tdi = {}
        for fld in self.flds:
            tdi[fld] = self.flds[fld].get()
        tdi['zlines'] = []

        for i in range(self.tbl.rowCount()):
            # Εάν έχουμε μηδενική τιμή αγνοούμε τη γραμμή
            if self.tbl.cellWidget(i, 2).get() == 0:
                continue
            vd1 = {}
            vd1['lm_id'] = self.tbl.cellWidget(i, 0).get()
            vd1['pfpa'] = self.tbl.cellWidget(i, 1).get()
            vd1['val'] = self.tbl.cellWidget(i, 2).get()
            vd1['fpa'] = self.tbl.cellWidget(i, 3).get()
            vd1['efpa'] = self.tbl.cellWidget(i, 5).get()
            vd1['id'] = self.tbl.cellWidget(i, 6).get()
            tdi['zlines'].append(vd1)
        return tdi

    def dicl(self, ki_id=''):
        typid = self.flds['typ_id'].get()
        if typid == 'normal':
            synt1 = dec(1)
        else:
            synt1 = dec(-1)
        lg = {}
        lg['ki_id'] = ki_id
        lg['dat'] = self.flds['dat'].get()
        lg['par'] = self.flds['pno'].get()
        lg['per'] = self.flds['per'].get()
        lg['zlines'] = []
        catid = self.flds['cat_id'].get()
        tsum = dec(0)
        for i in range(self.tbl.rowCount()):
            if self.tbl.cellWidget(i, 2).get() == 0:
                continue
            xorid = self.flds['ori_id'].currentIndex()
            cod = self.tbl.cellWidget(i, 0).get()
            pfpa = self.tbl.cellWidget(i, 1).get()
            ajia = self.tbl.cellWidget(i, 2).get() * synt1
            fpa = self.tbl.cellWidget(i, 3).get() * synt1
            tsum += ajia + fpa
            efpa = self.tbl.cellWidget(i, 5).get()
            if efpa == 0:
                ajia += fpa
                fpa = dec(0)
                pfpa = 0
            clmo, flmo, lfpa, cfpa = mlmo(cod, pfpa, xorid)
            if catid == 26:
                lg['zlines'].append({'lmo_id': clmo,
                                     'per2': flmo,
                                     'xr': ajia,
                                     'pi': dec(0)})
                if fpa != 0:
                    lg['zlines'].append({'lmo_id': lfpa,
                                         'per2': cfpa,
                                         'xr': fpa,
                                         'pi': dec(0)})
            elif catid == 7:
                lg['zlines'].append({'lmo_id': clmo,
                                     'per2': flmo,
                                     'pi': ajia,
                                     'xr': dec(0)})
                if fpa != 0:
                    lg['zlines'].append({'lmo_id': lfpa,
                                         'per2': cfpa,
                                         'pi': fpa,
                                         'xr': dec(0)})
        if catid == 7:
            lm = '30.00.00.%s' % self.flds['afm'].get()
            pr = u'Πελάτες'
            lg['zlines'].append({'lmo_id': lm,
                                 'per2': pr,
                                 'xr': tsum,
                                 'pi': dec(0)})
        elif catid == 26:
            lm = '50.00.00.%s' % self.flds['afm'].get()
            pr = u'Προμηθευτές'
            lg['zlines'].append({'lmo_id': lm,
                                 'per2': pr,
                                 'pi': tsum,
                                 'xr': dec(0)})
        return lg

    def validate(self):
        '''Valitade form data'''
        errors = u''
        eri = 0
        if len(self.flds['pno'].get()) < 2:
            eri += 1
            errors += '%s.Δεν υπάρχει παραστατικό\n' % eri
        if self.ffld['ttot'].get() == 0:
            eri += 1
            errors += '%s.Δεν υπάρχουν αναλυτικές γραμμές με τιμές\n' % eri
        if errors:
            Qw.QMessageBox.critical(self, u"Υπάρχουν λάθη", errors)
            return False
        else:
            return True

    def save(self):
        '''Save data to Database'''
        # Qw.QMessageBox.information(self, u"ee", '%s' % self.dic())
        # Qw.QMessageBox.information(self, u"Λογιστική", '%s' % self.dicl())
        # return
        if not self.validate():
            return
        try:
            sql = s2d.md2sql('ki', 'kid', self.dic())
            # print(sql)
            s2d.execute_script(self.db, sql)
            res = '%s' % s2d.rowst(self.db, "SELECT MAX(id) FROM ki;")[0][0]
            sql2 = s2d.md2sql('tr', 'trd', self.dicl(res))
            # print(sql2)
            s2d.execute_script(self.db, sql2)
        except Exception as exp:
            Qw.QMessageBox.critical(self, u"Πρόβλημα", '%s' % exp)
            return
        Qw.QMessageBox.information(self,
                                   u"Επιτυχία", 'Αριθμός εγγραφής %s' % res)
        self.reset()


if __name__ == '__main__':
    APP = Qw.QApplication(sys.argv)
    UI = Insert('/home/tedlaz/pyted/tederp/tst.db')
    UI.show()
    sys.exit(APP.exec_())
