# -*- coding: utf-8 -*-
'''
Κατεβάζουμε από το site του ΙΚΑ :
http://www.ika.gr/gr/infopages/downloads/home.cfm#down2
το τελευταίο ενημερωμένο αρχείο με τον οδηγό σύνδεσης κωδικών.
'''
import zipfile
import os


def get_file_data(fname, zipfname='osyk.zip'):
    osykfile = os.path.join(os.path.dirname(__file__), zipfname)
    with zipfile.ZipFile(osykfile) as osyk:
        with osyk.open(fname) as eidf:
            osyk = eidf.read().decode('CP1253')  # Εναλλακτικά ISO8859-7
    return osyk


def split_strip(txt, se='|'):
    '''Χωρίζει κείμενο σε λίστα με βάση ένα χαρακτήρα διαχωρισμού (Default το |)

    input parameters
      txt=Κείμενο για split, se=Χαρακτήρας διαχωρισμού (Default='|')

    returns
      List [] with splited and striped text elements
    '''
    sp = txt.split(se)
    for i in range(len(sp)):
        sp[i] = sp[i].strip()
    return sp


def eid_find(eid, fname='dn_eid.txt'):
    '''Εύρεση ειδικότητας με βάση τον κωδικό

    input parameters
      eid=Κωδικός Ειδικότητας

    returns
      tuple (Κωδικός ειδικότητας, περιγραφή ειδικότητας)
    '''
    for lin in get_file_data(fname).split('\n'):
        sp = split_strip(lin)
        if eid == sp[0]:
            return (sp[0], sp[1])
    return None


def kad_find(kad, fname='dn_kad.txt'):
    '''Εύρεση εγγραφής ΚΑΔ με βάση τον κωδικό

    input parameters
      kad=Αριθμός ΚΑΔ(Κωδικός αριθμός δραστηριότητας)

    returns
      tuple (ΚΑΔ, Περιγραφή ΚΑΔ)

    Finds and returns record with given no
    '''
    for lin in get_file_data(fname).split("\n"):
        sp = split_strip(lin)
        if kad == sp[0]:
            return (sp[0], sp[1])
    return None


def kad_list(no='', fname='dn_kad.txt'):
    '''
    input parameters
      kad=Κωδικός Αριθμός δραστηριότητας

    returns
      List [[kad1, kadper1], [kad2, kadper2], ..]
    '''
    no = '%s' % no
    valArr = []
    for line in get_file_data(fname).split("\n"):
        sp = split_strip(line)
        if no == '':
            valArr.append(sp)
        else:
            if sp[0].startswith(no):
                valArr.append(sp)
    return valArr


def eid_kad_list(kad, per, fname='dn_kadeidkpk.txt'):
    '''
    input parameters
      kad=Κωδ.Αρ.Δραστηριότητας, per=Περίοδος(YYYYMM) πχ 201301

    returns
      tuple (ΚΑΔ, ΕΙΔ, Περίοδος από, ΚΠΚ, Περίοδος έως, Περιγρ.Ειδικότητας)

    Σχόλια
    Τα αρχεία του ΙΚΑ δεν είναι σε μερικές περιπτώσεις κανονικοποιημένα
    με αποτέλεσμα να υπάρχουν για ΚΑΔ, ΕΙΔ, περίοδο διπλές εγγραφές.
    Λύση προς το παρόν είναι η επιλογή μόνο της πρώτης εγγραφής.
    '''
    arr = []
    chck = {}
    i = 0
    for lin in get_file_data(fname).split("\n"):
        sp = split_strip(lin)
        if kad == sp[0]:
            if per >= sp[3] and per <= sp[4]:
                ckv = '%s%s' % (sp[0], sp[1])
                if ckv not in chck:
                    eidcode, eidp = eid_find(sp[1])
                    arr.append([sp[0], sp[1], sp[3], sp[2], sp[4], eidp])
                    chck[ckv] = i
                    i = i + 1
    return arr


def kpk_find(kpk, per, fname='dn_kpk.txt'):
    '''
    input parameters
      kpk=Κωδ.Πακέτου κάλυψης, per=Περίοδος(YYYMM)

    returns
      tuple (ΚΠΚ, Περιγραφή, Εργ%, Εργοδότης%, Σύνολο%, περίοδος ισχύος)
    '''
    for lin in get_file_data(fname).split("\n"):
        sp = split_strip(lin)
        if kpk == sp[0]:
            if per >= sp[5]:
                return (sp[0], sp[1], sp[2], sp[3], sp[4], sp[5])
    return None


def kadeidkpk_find(kad, eid, per, fname='dn_kadeidkpk.txt'):
    '''
    input parameters
      kad=Κωδ.Αρ.Δραστ, eid=Ειδικότητα, per=Περίοδος

    returns
      tuple (ΚΑΔ, ΕΙΔ, Περίοδος, ΚΠΚ, tuple(kpk_find))
    '''
    for lin in get_file_data(fname).split("\n"):
        sp = split_strip(lin)
        if kad == sp[0] and eid == sp[1]:
            if per >= sp[3] and per <= sp[4]:
                return (kad, eid, per, sp[2], kpk_find(sp[2], per))
    return None


def doy_list(fname='doy.txt'):
    arr = []
    with open(fname) as fil:
        for lin in fil:
            lin = lin.decode('utf-8')
            txt = u'%s' % lin.rstrip('\n')
            arr.append(txt.split('-'))
    return arr


def ika_list(fname='ika.txt'):
    arr = []
    with open(fname) as fil:
        for lin in fil:
            lin = lin.decode('utf-8')
            txt = u'%s' % lin.rstrip('\n')
            arr.append(txt.split('-'))
    return arr
