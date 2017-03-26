# -*- coding: utf-8 -*-
'''
Created on 25 Φεβ 2013

@author: tedlaz
'''
t={}
t['m12_apo'] = [u'Αποχώρηση Εργαζομένου',u'Αποχωρήσεις Εργαζομένων']
t['m12_apotyp'] = [u'',u'']
t['m12_aptyp'] = [u'Τύπος Αποδοχών',u'Τύποι Αποδοχών']
t['m12_co'] = [u'Στοιχεία Επιχείρησης',u'Στοιχεία Επιχειρήσεων']
t['m12_cotyp'] = [u'Τύπος επιχείρησης',u'Τύποι επιχειρήσεων']
t['m12_coy'] = [u'Παράρτημα',u'Παραρτήματα']
t['m12_dimino'] = [u'Δίμηνο',u'Δίμηνα']
t['m12_eid'] = [u'Ειδικότητα',u'Ειδικότητες']
t['m12_fpr'] = [u'Στοιχεία εργαζομένου',u'Στοιχεία εργαζομένων']
t['m12_fprd'] = [u'',u'']
t['m12_mis'] = [u'Μισθοδοσία',u'Μισθοδοσίες']
t['m12_misd'] = [u'Μισθοδοσία αναλυτικά',u'Μισθοδοσίες αναλυτικά']
t['m12_mtyp'] = [u'',u'']
t['m12_mxr'] = [u'',u'']
t['m12_orar'] = [u'Ωράριο',u'Ωράρια']
t['m12_par'] = [u'Παρουσία',u'Παρουσίες']
t['m12_pard'] = [u'Παρουσία αναλυτικά',u'Παρουσίες αναλυτικά']
t['m12_period'] = [u'Περίοδος',u'Περίοδοι']
t['m12_pro'] = [u'Πρόσληψη',u'Προσλήψεις']
t['m12_promis'] = [u'',u'']
t['m12_ptyp'] = [u'',u'']
t['m12_sex'] = [u'Φύλο',u'Φύλα']
t['m12_symb'] = [u'Σύμβαση',u'Συμβάσεις']
t['m12_trimino'] = [u'Τρίμηνο',u'Τρίμηνα']
t['m12_xrisi'] = [u'Χρήση',u'Χρήσεις']

f={}
f['sex_id']    = ["SELECT id, sexp FROM m12_sex", u'αα|Φύλο']
f['co_id']     = ["SELECT id, cop FROM m12_co", u'αα|Επιχείρηση']
f['cotyp_id']  = ['SELECT id, cotypp FROM m12_cotyp', u'αα|Τύπος Επιχείρισης']
f['coy_id']    = ["SELECT id, coyp FROM m12_coy", u'αα|Παράρτημα']
f['period_id'] = ["SELECT id, periodp FROM m12_period", u'αα|Μήνας']
f['xrisi_id']  = ["SELECT id, xrisi FROM m12_xrisi", u'αα|Χρήση']
f['eid_id']    = ["SELECT id, eidp FROM m12_eid", u'αα|Ειδικότητα']
f['fpr_id']    = ["SELECT id, epon || ' ' || onom FROM m12_fpr", u'αα|Εργαζόμενος']
f['aptyp_id']  = ["SELECT id, aptypp FROM m12_aptyp", u'aa|Τύπος Αποδοχών']
f['mist_id']   = ["SELECT id, mistp FROM m12_mist", u'aa|Τύπος Μισθοδοσίας']
f['pro_id']    = ['''SELECT m12_pro.id, m12_pro.prod || ' ' || m12_fpr.epon || ' ' || m12_fpr.onom 
                    FROM m12_pro INNER JOIN m12_fpr ON m12_fpr.id=m12_pro.fpr_id''', u'αα|Πρόσληψη']

f['par_id'] = ['''SELECT m12_par.id, xrisi || ' ' || periodp as xrisiper FROM m12_par INNER JOIN m12_xrisi ON m12_xrisi.id=m12_par.xrisi_id INNER JOIN m12_period ON m12_period.id=m12_par.period_id''', u'αα|Περίοδος Παρουσίας']

f['ptyp_id']= ["SELECT id, ptypp FROM m12_ptyp",u'αα|Τύποι Παρουσίας']
l = {}
l['afm-m12_co'] = u'ΑΦΜ'
l['afm-m12_fpr'] = u'ΑΦΜ'
l['aika-m12_fpr'] = u'ΑρΜητρώουΙΚΑ'
l['ame-m12_co'] = u'ΑρΜητρώουΙΚΑ'
l['amka-m12_fpr'] = u'ΑΜΚΑ'
l['apold-m12_apo'] = u'Ημνία Απόλυσης'
l['apod-m12_pro'] = u'Αποδοχές'
l['apot-m12_apo'] = u'Τύπος'
l['apotypp-m12_apotyp'] = u''
l['aptyp_id-m12_pro'] = u'Τύπος αποδοχών'
l['aptypp-m12_aptyp'] = u'Τύπος αποδοχών'
l['asl3-m12_parf'] = u'Ασθένεια < 3'
l['asm3-m12_parf'] = u'Ασθένεια > 3'
l['co_id-m12_coy'] = u'Εταιρεία'
l['cop-m12_co'] = u'Επωνυμία/Επώνυμο'
l['cotyp-m12_cotyp'] = u'Τύπος Επιχείρησης'
l['cotyp_id-m12_co'] = u'Τύπος Επιχείρησης'
l['cotypp-m12_cotyp'] = u'Τύπος Επιχείρησης'
l['coy_id-m12_pro'] = u'Παράρτημα'
l['coyp-m12_coy'] = u'Παράρτημα'
l['dat-m12_fprd'] = u''
l['dial-m12_symb'] = u''
l['dimino_id-m12_period'] = u''
l['dimp-m12_dimino'] = u''
l['doy-m12_co'] = u'ΔΟΥ'
l['dra-m12_co'] = u'Δραστηριότητα'
l['eid_id-m12_pro'] = u'Ειδικότητα'
l['eidp-m12_eid'] = u''
l['epon-m12_fpr'] = u'Επώνυμο'
l['fpr_id-m12_fprd'] = u'Εργαζόμενος'
l['fpr_id-m12_pro'] = u'Εργαζόμενος'
l['igen-m12_fpr'] = u'Ημ.Γέννησης'
l['ikac-m12_co'] = u'Κωδ.Παρ.ΙΚΑ'
l['ikap-m12_co'] = u'Παράρτημα ΙΚΑ'
l['imnia-m12_mis'] = u'Ημ/νία Έκδοσης'
l['kad-m12_coy'] = u'Κωδ.Αρ.Δραστηριότητας'
l['kad-m12_eid'] = u'Κωδ.Ειδικότητας'
l['kad-m12_parf'] = u'OFF'
l['kerg-m12_parf'] = u'OFF'
l['mars-m12_fprd'] = u''
l['mbdo-m12_orar'] = u''
l['mis_id-m12_misd'] = u''
l['mist_id-m12_mis'] = u'Τύπος Μισθοδοσίας'
l['mistp-m12_mist'] = u''
l['mitr-m12_fpr'] = u'Μητρώνυμο'
l['mtyp_id-m12_misd'] = u''
l['mtypp-m12_mtyp'] = u''
l['mxr_id-m12_ptyp'] = u''
l['mxrp-m12_mxr'] = u''
l['num-m12_co'] = u'Αριθμός'
l['num-m12_fpr'] = u'Αριθμός'
l['obdo-m12_orar'] = u''
l['odo-m12_co'] = u'Οδός'
l['odo-m12_fpr'] = u'Οδός'
l['olerg-m12_symtyp'] = u''
l['ono-m12_co'] = u'Όνομα'
l['onom-m12_fpr'] = u'Όνομα'
l['orar-m12_orar'] = u'Ωράριο'
l['orar_id-m12_symb'] = u'Ωράριο'
l['par_id-m12_pard'] = u'Χρήση-Περίοδος'
l['pat-m12_co'] = u'Πατρώνυμο'
l['patr-m12_fpr'] = u'Πατρώνυμο'
l['pedi-m12_fprd'] = u'Παιδιά'
l['perapo-m12_trimino'] = u'Από'
l['pereos-m12_trimino'] = u'Έως'
l['period-m12_period'] = u'Κωδ.ΠΕριόδου'
l['period_id-m12_mis'] = u'Περίοδος'
l['period_id-m12_par'] = u'Περίοδος'
l['period_id-m12_parf'] = u'Περίοδος'
l['period_id-m12_promis'] = u'Περίοδος'
l['period_id-m12_symb'] = u'Περίοδος'
l['periodp-m12_period'] = u'Περίοδος'
l['pol-m12_co'] = u'Πόλη'
l['pol-m12_fpr'] = u'Πόλη'
l['pos-m12_pard'] = u'Τιμή'
l['poso-m12_promis'] = u'Αποδοχές'
l['pro_id-m12_apo'] = u'Πρόσληψη'
l['pro_id-m12_misd'] = u'Πρόσληψη'
l['pro_id-m12_pard'] = u'Πρόσληψη'
l['pro_id-m12_parf'] = u'Πρόσληψη'
l['pro_id-m12_promis'] = u'Πρόσληψη'
l['pro_id-m12_symb'] = u'Πρόσληψη'
l['prod-m12_pro'] = u'Ημ/νία Πρόσληψης'
l['proy-m12_pro'] = u'Προυπηρεσία'
l['ptyp_id-m12_pard'] = u'Τύπος Παρουσίας'
l['ptypp-m12_ptyp'] = u'Τύπος Παρουσίας'
l['sex_id-m12_fpr'] = u'Φύλο'
l['sexp-m12_sex'] = u'Φύλο'
l['symd-m12_symb'] = u''
l['symtyp-m12_symtyp'] = u'Τύπος Σύμβασης'
l['symtyp_id-m12_symb'] = u'Τύπος Σύμβασης'
l['tk-m12_co'] = u'ΤΚ'
l['tk-m12_fpr'] = u'ΤΚ'
#l['taft-m12_fpr'] = u'Ταυτότητα'
l['trimino_id-m12_period'] = u'Τρίμηνο'
l['trimp-m12_trimino'] = u'Τρίμηνο'
l['val-m12_misd'] = u'Τιμή'
l['xrisi-m12_xrisi'] = u'Χρήση'
l['xrisi_id-m12_mis'] = u'Χρήση'
l['xrisi_id-m12_par'] = u'Χρήση'
l['xrisi_id-m12_parf'] = u'Χρήση'
l['xrisi_id-m12_promis'] = u'Χρήση'
l['xrisi_id-m12_symb'] = u'Χρήση'
l['xrisip-m12_xrisi'] = u'Χρήση'


if __name__ == '__main__':
    try:
        a = f['co_id']
    except:
        a = 'Not ok'
    print a