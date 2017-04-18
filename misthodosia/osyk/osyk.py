# -*- coding: utf-8 -*-
'''
Κατεβάζουμε από το site του ΙΚΑ :
http://www.ika.gr/gr/infopages/downloads/home.cfm#down2
το τελευταίο ενημερωμένο αρχείο με τον οδηγό σύνδεσης κωδικών.
'''
import zipfile
import os
import download_osyk as dos
URLF = "http://www.ika.gr/gr/infopages/downloads/osyk.zip"


def get_file_data(fname, zipfname='osyk.zip'):
    """Returns"""
    osykfile = os.path.join(os.path.dirname(__file__), zipfname)
    if not os.path.exists(osykfile):
        dos.download(URLF)
    with zipfile.ZipFile(osykfile) as osyk:
        with osyk.open(fname) as eidf:
            osyk = eidf.read().decode('CP1253')  # Εναλλακτικά ISO8859-7
    return osyk


def split_strip(txt, sep='|'):
    '''Χωρίζει κείμενο σε λίστα με βάση ένα χαρακτήρα διαχωρισμού (Default το |)

    input parameters
      txt=Κείμενο για split, se=Χαρακτήρας διαχωρισμού (Default='|')

    returns
      List [] with splited and striped text elements
    '''
    splited = txt.split(sep)
    for i, _ in enumerate(splited):
        splited[i] = splited[i].strip()
    return splited


def eid_find(eid, fname='dn_eid.txt'):
    '''Εύρεση ειδικότητας με βάση τον κωδικό

    input parameters
      eid=Κωδικός Ειδικότητας

    returns
      tuple (Κωδικός ειδικότητας, περιγραφή ειδικότητας)
    '''
    eid = '%s' % eid
    for lin in get_file_data(fname).split('\n'):
        sps = split_strip(lin)
        if eid == sps[0]:
            return (sps[0], sps[1])
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
        sps = split_strip(lin)
        if kad == sps[0]:
            return (sps[0], sps[1])
    return None


def kad_list(kadno='', fname='dn_kad.txt'):
    '''
    input parameters
      kad=Κωδικός Αριθμός δραστηριότητας

    returns
      List [[kad1, kadper1], [kad2, kadper2], ..]
    '''
    kadno = '%s' % kadno
    kads = []
    for line in get_file_data(fname).split("\n"):
        if len(line) < 6:
            continue
        sps = split_strip(line)
        if kadno == '':
            kads.append(sps)
        else:
            if sps[0].startswith(kadno):
                kads.append(sps)
    return kads


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
    kad = '%s' % kad  # Make sure kad is string
    per = int(per)  # Make sure per is integer for comparison
    arr = []
    chck = {}
    i = 0
    for lin in get_file_data(fname).split("\n"):
        sps = split_strip(lin)
        if kad == sps[0]:
            # Here we compaire
            if per >= int(sps[3]) and per <= int(sps[4]):
                ckv = '%s%s' % (sps[0], sps[1])
                if ckv not in chck:
                    _, eidp = eid_find(sps[1])
                    arr.append([sps[0], sps[1], sps[2], sps[3], sps[4], eidp])
                    chck[ckv] = i
                    i = i + 1
    return arr


def eid_kad_string(kad, period):
    """Print eids"""
    tmpl = '%6s %3s %s\n'
    tsr = 'Ειδικότητες εργασίας για τον %s την περίοδο %s\n' % (kad, period)
    for eid in eid_kad_list(kad, period):
        tsr += tmpl % (eid[1], eid[2], eid[5])
    return tsr


def kpk_find(kpk, per, fname='dn_kpk.txt'):
    '''
    input parameters
      kpk=Κωδ.Πακέτου κάλυψης, per=Περίοδος(YYYMM)

    returns
      tuple (ΚΠΚ, Περιγραφή, Εργ%, Εργοδότης%, Σύνολο%, περίοδος ισχύος)
    '''
    kpk = '%s' % kpk  # Make sure kpk is text
    per = int(per)
    for lin in get_file_data(fname).split("\n"):
        sps = split_strip(lin)
        if kpk == sps[0]:
            if per >= int(sps[5]):
                return (sps[0], sps[1], sps[2], sps[3], sps[4], sps[5])
    return None


def kadeidkpk_find(kad, eid, per, fname='dn_kadeidkpk.txt'):
    '''
    input parameters
      kad=Κωδ.Αρ.Δραστ, eid=Ειδικότητα, per=Περίοδος

    returns
      tuple (ΚΑΔ, ΕΙΔ, Περίοδος, ΚΠΚ, tuple(kpk_find))
    '''
    kad = str(kad)  # Make sure kad is string
    eid = str(eid)  # Make sure eid is string
    per = int(per)  # Make sure per is integer for comparison
    for lin in get_file_data(fname).split("\n"):
        sps = split_strip(lin)
        if kad == sps[0] and eid == sps[1]:
            if per >= int(sps[3]) and per <= int(sps[4]):
                return (kad, eid, per, sps[2], kpk_find(sps[2], per))
    return None


def doy_list(fname='doy.txt'):
    """Returns a list with doys"""
    arr = []
    with open(fname) as fil:
        for lin in fil:
            lin = lin.decode('utf-8')
            txt = u'%s' % lin.rstrip('\n')
            arr.append(txt.split('-'))
    return arr


def ika_list(fname='ika.txt'):
    """Returns a list with ika ypokatastimata"""
    arr = []
    with open(fname) as fil:
        for lin in fil:
            lin = lin.decode('utf-8')
            txt = u'%s' % lin.rstrip('\n')
            arr.append(txt.split('-'))
    return arr


if __name__ == "__main__":
    PER = 201602
    # print(eid_kad_string(5540, PER))
    print(eid_find(311400))
    print(kadeidkpk_find(5540, 311400, PER))
    # print(kad_list())
