--Υπολογισμός ΦΠΑ και σύγριση με αυτόν που έχει παργματικά γίνει εγγραφή
SELECT  esd.val, esd.fpa, esd.val*fpa.pfpa/100 as c1, (esd.val*fpa.pfpa/100)-esd.fpa as delta
FROM esd
INNER JOIN et ON et.id=esd.et_id
INNER JOIN fpa ON fpa.id=et.fpa_id;

--Αναλυτικές γραμμές εγγραφών
SELECT  es.id,es.dat,es.par,pel.afm,pel.epon,et.etp,esd.val,esd.fpa
FROM es
INNER JOIN esd ON es.id=esd.es_id
INNER JOIN pel ON pel.id=es.pel_id
INNER JOIN et ON et.id=esd.et_id;

--Σύνολα ανα κατηγορία ΦΠΑ
SELECT fpa.idp, sum(esd.val) as tval, sum(esd.fpa) as tfpa
FROM esd
INNER JOIN et ON et.id=esd.et_id
INNER JOIN fpa ON fpa.id=et.fpa_id
GROUP BY fpa.idp;

