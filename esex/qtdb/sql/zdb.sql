BEGIN TRANSACTION;
CREATE TABLE fkey(
fln PRIMARY KEY,
sq1 TEXT NOT NULL -- SQL για SELECT ( εμφάνιση )
);
INSERT INTO fkey VALUES('syn_id','SELECT id, afm,epon FROM syn');
INSERT INTO fkey VALUES('et_id','SELECT id, etp FROM et');
INSERT INTO fkey VALUES('dt_id','SELECT id, etp FROM dt');
INSERT INTO fkey VALUES('sr_id','SELECT id, srp FROM sr');
INSERT INTO fkey VALUES('es_id','SELECT id, dat, par FROM es');
INSERT INTO fkey VALUES('ds_id','SELECT id, dat, par FROM ds');
CREATE TABLE zfld(
fln PRIMARY KEY,   -- Όνομα πεδίου
flp TEXT NOT NULL, -- Περιγραφή 
flt TEXT NOT NULL DEFAULT '' -- Τύπος
);
INSERT INTO zfld VALUES('afm','ΑΦΜ','');
INSERT INTO zfld VALUES('ar','Αριθμός','');
INSERT INTO zfld VALUES('co_id','Επιχείρηση','');
INSERT INTO zfld VALUES('cop','Επωνυμία','');
INSERT INTO zfld VALUES('dat','Ημερομηνία','');
INSERT INTO zfld VALUES('dfpa','Δ.ΦΠΑ','');
INSERT INTO zfld VALUES('doy','ΔΟΥ','');
INSERT INTO zfld VALUES('dra','Δραστηριότητα','');
INSERT INTO zfld VALUES('ds_id','Κεφαλίδα','');
INSERT INTO zfld VALUES('dt_id','Λογαριασμός','');
INSERT INTO zfld VALUES('fpa','ΦΠΑ','');
INSERT INTO zfld VALUES('ejv','Έξοδα','');
INSERT INTO zfld VALUES('ejfpa','ΦΠΑ','');
INSERT INTO zfld VALUES('epon','Επωνυμία','');
INSERT INTO zfld VALUES('es_id','Έσοδα','');
INSERT INTO zfld VALUES('esfpa','ΦΠΑ','');
INSERT INTO zfld VALUES('esv','Έσοδα','');
INSERT INTO zfld VALUES('et_id','Τύπος Εγγρ.','');
INSERT INTO zfld VALUES('etos','Χρήση','');
INSERT INTO zfld VALUES('etp','Περιγραφή','');
INSERT INTO zfld VALUES('id','ΑΑ','');
INSERT INTO zfld VALUES('ldt','Ημ/νία','');
INSERT INTO zfld VALUES('logp','Μήνυμα','');
INSERT INTO zfld VALUES('minas','Μήνας','');
INSERT INTO zfld VALUES('num','Αριθμός','');
INSERT INTO zfld VALUES('odo','Οδός','');
INSERT INTO zfld VALUES('odos','Οδός','');
INSERT INTO zfld VALUES('ono','Όνομα','');
INSERT INTO zfld VALUES('par','Παραστατικό','');
INSERT INTO zfld VALUES('parno','Αριθμός παρ/κών','');
INSERT INTO zfld VALUES('pat','Πατρώνυμο','');
INSERT INTO zfld VALUES('pel_id','Πελάτης','');
INSERT INTO zfld VALUES('pfpa','Ποσ.ΦΠΑ(%)','');
INSERT INTO zfld VALUES('pol','Πόλη','');
INSERT INTO zfld VALUES('poli','Πόλη','');
INSERT INTO zfld VALUES('pro_id','Προμηθευτής','');
INSERT INTO zfld VALUES('quarter','Τρίμηνο','');
INSERT INTO zfld VALUES('sr_id','Σειρά','');
INSERT INTO zfld VALUES('srp','Σειρά','');
INSERT INTO zfld VALUES('syg_id','Συγκεντρωτική','');
INSERT INTO zfld VALUES('syn_id','Συναλασσόμενος','');
INSERT INTO zfld VALUES('tfpa','ΦΠΑ','');
INSERT INTO zfld VALUES('theo_id','Τύπος παραστατικού','');
INSERT INTO zfld VALUES('tk','Τ.Κ.','');
INSERT INTO zfld VALUES('ttot','ΣΥΝΟΛΟ','');
INSERT INTO zfld VALUES('tval','ΑΞΙΑ','');
INSERT INTO zfld VALUES('ypp','Υποκατάστημα','');
INSERT INTO zfld VALUES('yp_id','Υπ/μα','');
INSERT INTO zfld VALUES('val','Αξία','');
INSERT INTO zfld VALUES('lkd','Ημ/νία κλειδώματος','');
CREATE TABLE ztbl(
tbn PRIMARY KEY,   -- Όνομα πίνακα
tbp TEXT NOT NULL, -- Περιγραφή
tbpm TEXT NOT NULL,-- Περιγραφή σε πληθυντικό
tsql TEXT,         -- SQL για select  
csql TEXT          -- SQL για τη δημιουργία του πίνακα    
);
INSERT INTO ztbl VALUES('ds','Έξοδο','Έξοδα','SELECT ds.id,yp.ypp,ds.dat,ds.par,pro.epon,ds.tval,ds.tfpa,ds.ttot FROM ds INNER JOIN yp On yp.id=ds.yp_id INNER JOIN pro On pro.id=ds.pro_id',NULL);
INSERT INTO ztbl VALUES('dsd','Έξοδο αναλυτικά','Έξοδα αναλυτικά','SELECT dsd.id,dsd.ds_id,dt.etp,dsd.val, dsd.fpa, dsd.val+dsd.fpa as tot FROM dsd INNER JOIN dt ON dt.id=dsd.dt_id',NULL);
INSERT INTO ztbl VALUES('dt','Τύπος εγγραφής εξόδων','Τύποι εγγραφής εξόδων',NULL,NULL);
INSERT INTO ztbl VALUES('es','Έσοδο','Έσοδα','SELECT es.id,yp.ypp,es.dat,sr.srp,es.par,pel.epon,es.tval,es.tfpa,es.ttot FROM es INNER JOIN yp On yp.id=es.yp_id INNER JOIN sr On sr.id=es.sr_id INNER JOIN pel On pel.id=es.pel_id',NULL);
INSERT INTO ztbl VALUES('esd','Έσοδο αναλυτικά','Έσοδα αναλυτικά','SELECT esd.id,esd.es_id,et.etp,esd.val, esd.fpa, esd.val+esd.fpa as tot FROM esd INNER JOIN et ON et.id=esd.et_id',NULL);
INSERT INTO ztbl VALUES('et','Τύπος εγγραφής Εσόδων','Τύποι εγγραφής εσόδων',NULL,NULL);
INSERT INTO ztbl VALUES('pel','Πελάτης','Πελάτες','SELECT id,afm,epon from pel',NULL);
INSERT INTO ztbl VALUES('pro','Προμηθευτής','Προμηθευτές',NULL,NULL);
INSERT INTO ztbl VALUES('yp','Υποκατάστημα','Υποκαταστήματα',NULL,NULL);
INSERT INTO ztbl VALUES('lg','Ιστορικό','Ιστορικό',NULL,NULL);
INSERT INTO ztbl VALUES('lk','Ημ/νία κλειδώματος','Ημ/νία κλειδώματος',NULL,NULL);
INSERT INTO ztbl VALUES('co','Στοιχεία επιχείρησης','Στοιχεία επιχείρησης',NULL,NULL);
CREATE TABLE rtp(
rnm  PRIMARY KEY,  --Ονομα αναφοράς
rtit TEXT NOT NULL UNIQUE, -- Τίτλος αναφοράς
rsql TEXT NOT NULL --sql αναφοράς
);
INSERT INTO rtp VALUES('tim_ana_pelati','Συγκεντρωτική Πωλήσεων','SELECT pel.afm,pel.epon,count(es.id) as parno,sum(es.tval) as tval
FROM es
INNER JOIN pel on pel.id=es.pel_id
WHERE pel.syg_id=1 AND es.tval >= 300
GROUP BY pel.id');
--Για τη δημιουργία tree (ΠΡΟΣΟΧΗ : Το άθροισμα των tdepth+txtv+numv θα πρέπει να
--είναι ίσο ακριβώς με τον αριθμό των πεδίων που επιστρέφει το trsql
CREATE TABLE tree(
tname TEXT NOT NULL PRIMARY KEY, -- Όνομα tree
mname TEXT NOT NULL UNIQUE, --Όνομα σε μενού
tdepth INTEGER NOT NULL,  --Βάθος του tree
txtv INTEGER NOT NULL,    --Αριθμός πεδίων κειμένου
numv INTEGER NOT NULL,    --Αριθμός πεδίων με αριθμητικά δεδομένα 
trsql TEXT NOT NULL  --SQL που θα εκτελεστεί για να γεμίσει το tree
);
INSERT INTO tree VALUES('esodtr','Έσοδα',5,1,3,'SELECT strftime(''%Y'',es.dat) as etos,tr.trp as quarter,mi.mip as minas,strftime(''%d/%m/%Y'',es.dat) as dt,sr.srp || '' '' || es.par || '' '' || pel.epon as pel, et.etp as etp,esd.val as val,esd.fpa as fpa, esd.val+esd.fpa as tot
from es
INNER JOIN sr ON sr.id=es.sr_id
INNER JOIN pel ON pel.id=es.pel_id
INNER JOIN esd ON es.id = esd.es_id
INNER JOIN et ON et.id = esd.et_id
INNER JOIN tr on tr.id = (cast(strftime(''%m'', es.dat) as integer) + 2) / 3 
INNER JOIN mi on mi.id = strftime(''%m'',es.dat)
ORDER BY es.dat, es.sr_id,es.par');
INSERT INTO tree VALUES('esex','Έσοδα - Έξοδα',7,1,5,'SELECT strftime(''%Y'',es.dat) as etos,tr.trp as quarter,mi.mip as minas,''Έσοδα'' as esej,strftime(''%d/%m/%Y'',es.dat) as dat,sr.srp || '' '' || es.par || '' '' || pel.epon as epon, et.etp as etp,esd.val as esv,esd.fpa as esfpa, 0 as ejv,0 as ejfpa,esd.fpa - 0 as dfpa,es.dat as sortdat
from es
INNER JOIN sr ON sr.id=es.sr_id
INNER JOIN pel ON pel.id=es.pel_id
INNER JOIN esd ON es.id = esd.es_id
INNER JOIN et ON et.id = esd.et_id
INNER JOIN tr on tr.id = (cast(strftime(''%m'', es.dat) as integer) + 2) / 3 
INNER JOIN mi on mi.id = strftime(''%m'',es.dat)
UNION
SELECT strftime(''%Y'',ds.dat) as etos,tr.trp as quarter,mi.mip as minas,''Έξοδα'' as esej,strftime(''%d/%m/%Y'',ds.dat) as dt,ds.par || '' '' || pro.epon, dt.etp,0 as es1,0 as es2,dsd.val,dsd.fpa, 0-dsd.fpa as dfpa,ds.dat
from ds
INNER JOIN pro ON pro.id=ds.pro_id
INNER JOIN dsd ON ds.id = dsd.ds_id
INNER JOIN dt ON dt.id = dsd.dt_id
INNER JOIN tr on tr.id = (cast(strftime(''%m'', ds.dat) as integer) + 2) / 3 
INNER JOIN mi on mi.id = strftime(''%m'',ds.dat)
ORDER BY sortdat desc');
INSERT INTO tree VALUES('prom','Προμηθευτές-Παραστατικά',3,0,3,'SELECT pro.afm || '' '' || pro.epon as afmepon, strftime(''%Y'',ds.dat) as etos,strftime(''%d/%m/%Y'',ds.dat) || '' Παρ : '' || ds.par as hmpar, ds.tval,ds.tfpa,ds.ttot,ds.dat
FROM ds
INNER JOIN pro ON pro.id=ds.pro_id 
ORDER BY pro.epon,ds.dat');
INSERT INTO tree VALUES('pelat','Πελάτες-Παραστατικά',3,0,3,'SELECT pel.afm || '' '' || pel.epon as afmepon, strftime(''%Y'',es.dat) as etos,strftime(''%d/%m/%Y'',es.dat) || '' Παρ : '' || es.par as hmpar, es.tval,es.tfpa,es.ttot,es.dat
FROM es
INNER JOIN pel ON pel.id=es.pel_id 
ORDER BY pel.epon,es.dat');
COMMIT;
