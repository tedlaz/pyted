# -*- coding: utf-8 -*-
#SQL που χρησιμοποιείται από το πρόγραμμα

onomatep = "SELECT id, epon || ' ' || onom as onomatep FROM m12_fpr"
fpr = '''
SELECT m12_fpr.id, epon, onom, patr, mitr, sexp, igen, afm,amka,aika,pol,odo,num,tk 
FROM m12_fpr
INNER JOIN m12_sex on m12_sex.id=m12_fpr.sex_id
'''
pro = '''
SELECT m12_pro.id, m12_pro.prod, m12_fpr.epon || ' ' || m12_fpr.onom as onomatep,
       m12_coy.coyp, m12_pro.proy, m12_aptyp.aptypp,m12_pro.apod
FROM m12_pro
INNER JOIN m12_fpr ON m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_coy ON m12_coy.id=m12_pro.coy_id
INNER JOIN m12_aptyp ON m12_aptyp.id=m12_pro.aptyp_id
'''
pro_open = '''
SELECT m12_pro.id, m12_pro.prod, m12_fpr.epon || ' ' || m12_fpr.onom as onomatep, 
      m12_coy.coyp,m12_eid.eidp,m12_pro.proy, m12_aptyp.aptypp, m12_pro.apod, m12_apo.apold
FROM m12_pro
INNER JOIN m12_fpr on m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_coy on m12_coy.id=m12_pro.coy_id
INNER JOIN m12_eid on m12_eid.id=m12_pro.eid_id
INNER JOIN m12_aptyp on m12_aptyp.id=m12_pro.aptyp_id
LEFT JOIN m12_apo on m12_apo.pro_id=m12_pro.id
WHERE   m12_apo.apold is null 
ORDER BY prod DESC
'''
pro_open1xrisi2period = '''
SELECT m12_pro.id, m12_pro.prod,m12_apo.apold,m12_pro.prod || ' ' || m12_fpr.epon|| ' ' || m12_fpr.onom as onomatep 
FROM m12_pro 
INNER JOIN m12_fpr On m12_fpr.id=m12_pro.fpr_id 
LEFT JOIN m12_apo ON m12_apo.pro_id=m12_pro.id 
WHERE m12_pro.prod <= '%s-%s-31' AND ((m12_apo.apold IS NULL) OR (m12_apo.apold >= '%s-%s-01'))
'''
pro_close= '''
SELECT m12_pro.id, m12_pro.prod, m12_fpr.epon || ' ' || m12_fpr.onom as onomatep, 
      m12_coy.coyp,m12_eid.eidp,m12_pro.proy, m12_aptyp.aptypp, m12_pro.apod, m12_apo.apold
FROM m12_pro
INNER JOIN m12_fpr on m12_fpr.id=m12_pro.fpr_id
INNER JOIN m12_coy on m12_coy.id=m12_pro.coy_id
INNER JOIN m12_eid on m12_eid.id=m12_pro.eid_id
INNER JOIN m12_aptyp on m12_aptyp.id=m12_pro.aptyp_id
LEFT JOIN m12_apo on m12_apo.pro_id=m12_pro.id
WHERE   m12_apo.apold is not null 
ORDER BY prod DESC
'''
co = '''
SELECT m12_co.id, m12_co.cop, m12_co.ono, m12_co.pat, m12_cotyp.cotypp, m12_co.ame,
       m12_co.afm, m12_co.doy, m12_co.dra, m12_co.pol, m12_pro.odo, m12_pro.num,
       m12_co.ikac, m12_co.ikap
FROM m12_co
INNER JOIN m12_cotyp ON m12_cotyp.id=m12_co.cotyp_id
'''


if __name__ == "__main__":
    import utils_db as udb
    db = 'c:/ted/testing.m13'
    udb.test_getDbRowsByFldName(pro_close, db)