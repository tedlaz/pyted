# -*- coding: utf-8 -*-
'''
Created on 28/2/2014

@author: tedlaz
'''
from qtdb import dbforms as dbf


def fillTreeMenu():
    """
    Here we create menu tree
    """
    mitems = []
    mitems.append(["es.fInsertEggrafi(dbt=self.db)",
                   u'Εγγραφές',
                   u'Νέα εγγραφή εσόδων',
                   'frm'])
    mitems.append(['ej.fInsertEggrafi(dbt=self.db)',
                   u'Εγγραφές',
                   u'Νέα εγγραφή εξόδων',
                   'frm'])
    sql2 = "SELECT rnm,'Αναφορές' as pin,rtit,'rpt' as typ,rsql FROM rtp"
    rvals = dbf.getDbRows(sql2, dbf.zdb)
    if rvals:
        mitems = mitems + list(rvals[0])
    mitems.append(["qtr.TreeForm('esex', self.db, self)", u'Αναφορές', u'Βιβλίο Εσόδων-Εξόδων', 'frm'])
    mitems.append(["qtr.TreeForm('prom', self.db, self)", u'Αναφορές', u'Προμηθευτές τιμολόγια', 'frm'])
    mitems.append(["qtr.TreeForm('pelat', self.db, self)", u'Αναφορές', u'Πελάτες τιμολόγια', 'frm'])
    mitems.append(["f2.PtextForm(self)", u'Αναφορές', u'Περιοδική ΦΠΑ', 'frm'])
    mitems.append(["minkat.PtextForm(self)", u'Αναφορές', u'Μηνιαία κατ.Εσοδ.Εξοδ', 'frm'])
    mitems.append(["dbf.fmasterDetail('pel','es',self.db,self)", u'Αναφορές', u'Πελάτες-Τιμολόγια', 'frm'])
    mitems.append(["dbf.fmasterDetail('pro','ds',self.db,self)", u'Αναφορές', u'Προμηθευτές-Τιμολόγια', 'frm'])
    mitems.append(["dbf.fmasterDetail('es','esd',self.db,self)", u'Αναφορές', u'Πωλήσεις Αναλυτικά', 'frm'])
    mitems.append(["dbf.fmasterDetail('ds','dsd',self.db,self)", u'Αναφορές', u'Αγορές Αναλυτικά', 'frm'])
    sql = "SELECT tbn,'Πίνακες' as pin,tbpm,'tbl' as typ FROM ztbl"
    dbitems = dbf.getDbRows(sql, dbf.zdb)
    if dbitems:
        mitems += list(dbitems[0])
    return mitems


htmlAbout = u'''
<b>ΕΕ Έκδοση : 0.1</b><br/>
<br/> Δημιουργήθηκε από τον Θεόδωρο Λάζαρο</a>.
<br/><br/>Άδεια χρήσης  :  <a href=\"http://www.gnu.org/licenses/gpl.html\"> GPL 3</a>
<br/><br/>Για περισσότερες πληροφορίες :
<br/><a href=\"http://users.otenet.gr/~o6gnvw/\">Ted Lazaros Pages</a>
'''


def applicationTitle():
    return u"Έσοδα-Έξοδα"


def dbExtension():
    return 'ee3'


def organizationName():
    return u"NT"


def organizationDomain():  # Not critical for registry entries
    return "NTDomain"


def applicationName():
    return "EsEj"
