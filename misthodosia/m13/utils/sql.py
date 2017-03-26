# -*- coding: utf-8 -*-
'''
Created on 29 Μαρ 2013

@author: tedlaz
'''

fpr = 'select id , epon, onom,igen,pol,odo,num,tk from m12_fpr order by epon,onom'
fprh = ['id',u'Επώνυμο',u'Όνομα',u'Ημ.Γέννησης',u'Πόλη',u'Οδός',u'Αριθμός',u'ΤΚ']

pro = '''
SELECT m12_pro.id, m12_pro.prod, m12_fpr.epon || ' ' || m12_fpr.onom as onomatep, 
       m12_coy.coyp,m12_eid.eidp,m12_pro.proy, m12_aptyp.aptypp, m12_pro.apod, m12_apo.apod
FROM m12_pro
INNER JOIN m12_fpr on m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_coy on m12_coy.id=m12_pro.coy_id
INNER JOIN m12_eid on m12_eid.id=m12_pro.eid_id
INNER JOIN m12_aptyp on m12_aptyp.id=m12_pro.aptyp_id
LEFT JOIN m12_apo on m12_apo.pro_id=m12_pro.id
ORDER BY prod DESC
'''
proh = [u'id',u'Ημ/νία Πρόσληψης',u'Εργαζόμενος',u'Υποκατάστημα',u'Ειδικότητα',u'Προυπηρεσία',u'Τύπος Αποδοχών',u'Αποδοχές',u'Απόλυση']

pard = '''
SELECT m12_pard.id, m12_xrisi.xrisi || ' ' || m12_period.periodp, m12_fpr.epon || ' ' || m12_fpr.onom, m12_ptyp.ptypp,m12_pard.pos 
FROM m12_pard
INNER JOIN m12_par ON m12_par.id=m12_pard.par_id
INNER JOIN m12_xrisi ON m12_xrisi.id=m12_par.xrisi_id
INNER JOIN m12_period ON m12_period.id=m12_par.period_id
INNER JOIN m12_pro ON m12_pro.id=m12_pard.pro_id
INNER JOIN m12_fpr ON m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_ptyp ON m12_ptyp.id=m12_pard.ptyp_id
'''
pardh = [u'id',u'Περίοδος',u'Εργαζόμενος',u'Τύπος παρουσίας',u'Τιμή']

xrisi = '''SELECT * FROM m12_xrisi'''
xrisih = [u'id',u'Χρήση',u'Περιγραφή']

eid = '''SELECT * FROM m12_eid'''
eidh = [u'id',u'Ειδικότητα',u'Κωδ.ΙΚΑ']

par = '''SELECT * FROM m12_par'''
parh = [u'id',u'Χρήση',u'Περίοδος'] 

ypok = '''SELECT * FROM m12_coy'''
ypokh = [u'id',u'Εταιρεία',u'Ονομασία',u'ΚΑΔ-ΙΚΑ']

apo = '''
SELECT m12_apo.id, m12_apo.apod,m12_fpr.epon || ' ' || m12_fpr.onom, m12_pro.prod, m12_apo.apot 
FROM m12_apo
INNER JOIN m12_pro ON m12_pro.id=m12_apo.pro_id
INNER JOIN m12_fpr ON m12_fpr.id=m12_pro.fpr_id
ORDER BY m12_apo.apod DESC 
'''
apoh = [u'id',u'Ημερομηνία',u'Εργαζόμενος',u'Ημ.Πρόσληψης',u'Τύπος']

if __name__ == '__main__':
    pass