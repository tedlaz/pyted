# -*- coding: utf-8 -*-
'''
Created on 21 Δεκ 2012

@author: tedlaz
'''
from collections import OrderedDict

a1 = '''
SELECT m12_promis.pro_id, m12_xrisi.xrisi  || m12_period.period AS pr, m12_promis.poso
FROM m12_promis
INNER JOIN m12_xrisi ON m12_xrisi.id=m12_promis.xrisi_id
INNER JOIN m12_period ON m12_period.id=m12_promis.period_id
WHERE pr <= '201212' AND m12_promis.pro_id=1
ORDER BY pr DESC
'''
pivotSQL = '''
select
  ono
  , sum(case when par = 'apod' then val end) as apod
  , sum(case when par = 'ika' then val end) as ika
  , sum(case when par = 'ika2' then val end) as ika2
  , sum 
from tst

group by ono
ORDER BY ono DESC
;
'''

fprSQL  = 'select id , epon, onom,igen,pol,odo,num,tk from m12_fpr order by epon,onom'
fprSQLh = ['id',u'Επώνυμο',u'Όνομα',u'Ημ.Γέννησης',u'Πόλη',u'Οδός',u'Αριθμός',u'ΤΚ']

proSQL = '''
SELECT m12_pro.id, m12_pro.prod, m12_fpr.epon || ' ' || m12_fpr.onom as onomatep, m12_coy.coyp,m12_eid.eidp,m12_pro.proy, m12_aptyp.aptypp, m12_pro.apod, m12_apo.apold
FROM m12_pro
INNER JOIN m12_fpr on m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_coy on m12_coy.id=m12_pro.coy_id
INNER JOIN m12_eid on m12_eid.id=m12_pro.eid_id
INNER JOIN m12_aptyp on m12_aptyp.id=m12_pro.aptyp_id
LEFT JOIN m12_apo on m12_apo.pro_id=m12_pro.id
ORDER BY prod DESC
'''
proSQLh = [u'id',u'Ημ/νία Πρόσληψης',u'Εργαζόμενος',u'Υποκατάστημα',u'Ειδικότητα',u'Προυπηρεσία',u'Τύπος Αποδοχών',u'Αποδοχές',u'Απόλυση']

pardSQL = '''
SELECT m12_pard.id, m12_xrisi.xrisi || ' ' || m12_period.periodp, m12_fpr.epon || ' ' || m12_fpr.onom, m12_ptyp.ptypp,m12_pard.pos 
FROM m12_pard
INNER JOIN m12_par ON m12_par.id=m12_pard.par_id
INNER JOIN m12_xrisi ON m12_xrisi.id=m12_par.xrisi_id
INNER JOIN m12_period ON m12_period.id=m12_par.period_id
INNER JOIN m12_pro ON m12_pro.id=m12_pard.pro_id
INNER JOIN m12_fpr ON m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_ptyp ON m12_ptyp.id=m12_pard.ptyp_id
'''
pardSQLh = [u'id',u'Περίοδος',u'Εργαζόμενος',u'Τύπος παρουσίας',u'Τιμή']

xrisiSQL = '''SELECT * FROM m12_xrisi'''
xrisiSQLh = [u'id',u'Χρήση',u'Περιγραφή']

eidSQL  = '''SELECT * FROM m12_eid'''
eidSQLh = [u'id',u'Ειδικότητα',u'Κωδ.ΙΚΑ']

parSQL  = '''SELECT * FROM m12_par'''
parSQLh = [u'id',u'Χρήση',u'Περίοδος'] 

ypokSQL  = '''SELECT * FROM m12_coy'''
ypokSQLh = [u'id',u'Εταιρεία',u'Ονομασία',u'ΚΑΔ-ΙΚΑ']

apoSQL  = '''
SELECT m12_apo.id, m12_apo.apold,m12_fpr.epon || ' ' || m12_fpr.onom, m12_pro.prod, m12_apo.apot 
FROM m12_apo
INNER JOIN m12_pro ON m12_pro.id=m12_apo.pro_id
INNER JOIN m12_fpr ON m12_fpr.id=m12_pro.fpr_id
ORDER BY m12_apo.apold DESC 
'''
apoSQLh = [u'id',u'Ημερομηνία',u'Εργαζόμενος',u'Ημ.Πρόσληψης',u'Τύπος']

InsertParousiesSQL = '''
SELECT m12_pro.id, m12_pro.prod,m12_apo.apold,m12_pro.prod || ' ' || m12_fpr.epon|| ' ' || m12_fpr.onom as prosl 
FROM m12_pro 
INNER JOIN m12_fpr On m12_fpr.id=m12_pro.fpr_id 
LEFT JOIN m12_apo ON m12_apo.pro_id=m12_pro.id 
WHERE m12_pro.prod <= '%s-%s-31' AND ((m12_apo.apold IS NULL) OR (m12_apo.apold >= '%s-%s-01'))
'''
if __name__ == '__main__':
    a = OrderedDict()
    a['ena'] = 100
    a['dyo'] = 200
    for key in a:
        print '%s --> %s' % (key,a[key])