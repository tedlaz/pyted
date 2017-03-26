# -*- coding: utf-8 -*-
'''
fields must start with:
  b : True or False   
  i : Integer
  s : String Values
  j : Like s but masked to take digits as text input
  n : Numeric with two decimals field
  t : Text values 
  z : Integer Foreign key 
  c : Integer Foreign key combo box
  d : Date 
  e : Date or empty string 
  f : DateTime 
  w : String of form [1,1,1,1,1,0,0] (see specifications) 
'''
from pyappgen.model import tables, fields, ddata, startSql, fillTreeMenu, recFields, tblFlds, reprFlds

#Create your model here
#tables.add('tname',u'Περιγραφή πίνακα', u'Περιγραφή στον πληθυντικό','field1,field2,..',unique(fld1,fld2..))
#fields.add(fname, labelSmall, labelBig, isNull=False, isUnique=False)
tables.add('co_t',u'Τύπος Επιχείρησης',u'Τύποι Επιχείρησης')
fields.add('scot',u'Τύπος',u'Τύπος Επιχείρησης')

tables.add('sex',u'Φύλο',u'Φύλο')
fields.add('ssex',u'Φύλο',u'Φύλο')

tables.add('xrm',u'Μήνας',u'Μήνες')
fields.add('sxrm',u'Μήνας',u'Μήνας') 

tables.add('apt',u'Τύπος Αποδοχών',u'Τύποι Αποδοχών')
fields.add('sapt',u'Τύπος Απασχ.',u'Τύπος Απασχόλησης')

tables.add('at',u'Τύπος Απασχόλησης',u'Τύποι Απασχόλησης')
fields.add('sat',u'Τύπος Αποδοχών',u'Τύπος Αποδοχών')

tables.add('sye',u'Είδος Σύμβασης',u'Είδη Συμβάσεων')
fields.add('ssue',u'Είδος Σύμβασης',u'Είδος Σύμβασης')

tables.add('er',u'Εργαζόμενος',u'Εργαζόμενοι','sepo, sono')
fields.add('sepo',u'Επώνυμο',u'Επώνυμο εργαζομένου')
fields.add('sono',u'Όνομα',u'Όνομα εργαζομένου')
fields.add('spat',u'Πατρώνυμο',u'Όνομα πατέρα')
fields.add('smit',u'Μητρώνυμο',u'Όνομα μητέρας')
fields.addFK('csex')
fields.add('dgen',u'Ημ.Γεν.',u'Ημερομηνία Γέννησης')
fields.add('jafm',u'Α.Φ.Μ.',u'Αριθμός Φορολογικού Μητρώου')
fields.add('jamka',u'ΑΜΚΑ',u'Αρ.Μητρ.Κοιν.Ασφάλισης')
fields.add('jika',u'Α.Μ.ΙΚΑ',u'Αριθμός Μητρώου ΙΚΑ')
fields.add('spol',u'Πόλη',u'Διεύθυνση Πόλη')
fields.add('sodo',u'Οδός',u'Διεύθυνση Οδός')
fields.add('snum',u'Αριθμός',u'Διεύθυνση Αριθμός')
fields.add('jtk',u'Ταχ.Κωδικός',u'Διεύθυνση Ταχυδρομικός Κωδικός')
fields.add('jtel',u'Τηλέφωνο',u'Αριθμός Τηλεφώνου')
fields.add('jkin',u'Κινητό',u'Αριθμός Κινητού Τηλεφώνου')
fields.add('smail',u'E-mail',u'E-mail')

tables.add('co',u'Στοιχεία Επιχείρησης',u'Στοιχεία Επιχείρησης','scop, scono')
fields.add('scop',u'Επωνυμία',u'Επωνυμία Επιχείρησης')
fields.add('scono',u'Επώνυμο',u'Επώνυμο (Για περίπτωση Ατομικής')
fields.add('scpat',u'Πατρώνυμο',u'Πατρώνυμο (Για περίπτωση Ατομικής)')
fields.addFK('cco_t')
fields.add('sek',u'Εκπρόσωπος',u'Ονοματεπώνυμο Εκπροσώπου')
fields.add('jame',u'Α.Μ.ΙΚΑ',u'Αριθμός Μητρώου ΙΚΑ Επιχείρησης')
fields.add('jafm',u'ΑΦΜ',u'Αριθμός Φορολογικού Μητρώου Επιχείρησης')
fields.add('sdoy',u'ΔΟΥ',u'Όνομα ΔΟΥ')
fields.add('sdra',u'Δραστηριότητα',u'Περιγραφή Δραστηριότητας')
fields.add('jikac',u'Κωδ.Υπ.ΙΚΑ',u'Κωδικός Υποκαταστήματος ΙΚΑ')
fields.add('sikap',u'Υπ.ΙΚΑ',u'Υποκατάστημα ΙΚΑ')

tables.add('coy',u'Παράρτημα',u'Παραρτήματα','scoyp')
fields.addFK('cco')
fields.add('scoyp',u'Παράρτημα',u'Όνομα Παραρτήματος')
fields.add('jkad',u'ΚΑΔ',u'Κωδικός Αριθμός Δραστηριότητας ΙΚΑ')
fields.add('scpol',u'Πόλη',u'Διεύθυνση Πόλη')
fields.add('scodo',u'Οδός',u'Διεύθυνση Οδός')
fields.add('scnum',u'Αριθμός',u'Διεύθυνση Αριθμός')
fields.add('jctk',u'Ταχ.Κωδικός',u'Διεύθυνση Ταχυδρομικός Κωδικός')

tables.add('eid',u'Ειδικότητα',u'Ειδικότητες','seid')
fields.add('seid',u'Ειδικότητα',u'Ειδικότητα εργασίας')
fields.add('jeid',u'Κωδικός',u'Κωδικός ειδικότητας IKA')

tables.add('erp',u'Πρόσληψη',u'Προσλήψεις','zer, derp')
fields.addFK('zer')
fields.add('derp',u'Ημ.Προσλ.',u'Ημερομηνία πρόσληψης')
fields.addFK('csye')
fields.add('eli',u'Ημ.Ληξ.Συμβ.',u'Ημερομηνία Λήξης Σύμβασης')
fields.addFK('ccoy')
fields.addFK('zeid')
fields.add('iproy',u'Προυπηρεσία',u'Προυπηρεσία σε Έτη')
fields.addFK('cat')
fields.add('imer',u'Μέρες/Βδ.',u'Ημέρες εβδομαδιαίας απασχόλησης')
fields.add('nor',u'Ώρες/Βδ.',u'Ώρες εβδομαδιαίας απασχόλησης')
fields.add('tora',u'Ωράριο',u'Ωράριο εβδομαδιαίας απασχόλησης')
fields.addFK('capt')
fields.add('napod',u'Αποδοχές',u'Αποδοχές')

tables.add('endt',u'Τύπος Αποχώρησης',u'Τύποι Αποχωρήσης')
fields.add('sendt',u'Τύπος Αποχώρησης',u'Τύπος Αποχώρησης')

tables.add('erpa',u'Αποχώρηση',u'Αποχωρήσεις')
fields.add('dapox',u'Ημ/νία',u'Ημερομηνία αποχώρησης')
fields.addFK('zerp')
fields.addFK('cendt')

#INSERT DATA TO DB
ddata.add('co_t',[0,u'Εταιρεία'])
ddata.add('co_t',[1,u'Φυσικό πρόσωπο'])

ddata.add('sex', [0,u'Άνδρας'])
ddata.add('sex', [1,u'Γυναίκα'])

ddata.add('xrm', [1,u'Ιανουάριος'])
ddata.add('xrm', [2,u'Φεβρουάριος'])
ddata.add('xrm', [3,u'Μάρτιος'])
ddata.add('xrm', [4,u'Απρίλιος'])
ddata.add('xrm', [5,u'Μάϊος'])
ddata.add('xrm', [6,u'Ιούνιος'])
ddata.add('xrm', [7,u'Ιούλιος'])
ddata.add('xrm', [8,u'Αυγουστος'])
ddata.add('xrm', [9,u'Σεπτέμβριος'])
ddata.add('xrm', [10,u'Οκτώβριος'])
ddata.add('xrm', [11,u'Νοέμβριος'])
ddata.add('xrm', [12,u'Δεκέμβριος'])

ddata.add('at', [1,u'Πλήρης Απασχόληση'])
ddata.add('at', [2,u'Μερική Απασχόληση'])
ddata.add('at', [3,u'Εκ Περιτροπής Απασχόληση'])

ddata.add('apt', [1,u'Μισθός'])
ddata.add('apt', [2,u'Ημερομίσθιο'])
ddata.add('apt', [3,u'Ωρομίσθιο'])

ddata.add('sye', [1,u'Αορίστου χρόνου'])
ddata.add('sye', [2,u'Ορισμένου χρόνου'])

ddata.add('endt', [1,u'Απόλυση'])
ddata.add('endt', [2,u'Οικιοθελής αποχώρηση'])
ddata.add('endt', [3,u'Συνταξιοδότηση'])

ddata.add('co', [1, u'Κενό', u' ', u' ', u'0', u' ', u' ', u' ', u' ', u' ', u' ',u' '])
ddata.add('coy', [1, u'1', u'Κεντρικό', u' ', u' ', u' ', u' ', u' '])


if __name__ == '__main__':
    print startSql()
    print ddata.data
    #print recFields('zerpa')
    #print reprFlds('erpa',1)
    #print recFieldsIJ('zerp')
    #print tables._rfieldsArray('erpa')