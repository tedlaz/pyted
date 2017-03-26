BEGIN TRANSACTION;
--metadata tables, data
CREATE TABLE IF NOT EXISTS z(
param TEXT PRIMARY KEY,
val TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS zfld( --field metadata 
fld TEXT PRIMARY KEY,
lbl TEXT NOT NULL UNIQUE,
per TEXT NOT NULL UNIQUE,
min_size INTEGER NOT NULL DEFAULT 0,
max_size INTEGER NOT NULL DEFAULT 0,
widget TEXT NOT NULL DEFAULT 'text'
);

CREATE TABLE IF NOT EXISTS ztab(-- table metadata
tab TEXT PRIMARY KEY,
lbl TEXT NOT NULL UNIQUE,
lblp TEXT NOT NULL UNIQUE
);

-- application tables, basic data

INSERT INTO zfld VALUES ('id', 'Νο', 'Αριθμός εγγραφής', 1, 30, 'int');
INSERT INTO z VALUES ('version', '1.0');
INSERT INTO z VALUES ('app_name', 'Test application');
INSERT INTO z VALUES ('app_key', 'tst167');

CREATE TABLE IF NOT EXISTS erg( --Εργαζόμενοι
id INTEGER PRIMARY KEY,
epo TEXT NOT NULL,
ono TEXT NOT NULL,
pat TEXT NOT NULL,
mit TEXT NOT NULL,
bdat DATE NOT NULL,
UNIQUE (epo, ono, pat, mit)
);
INSERT INTO ztab VALUES ('erg', 'Εργαζόμενος', 'Εργαζόμενοι');
INSERT INTO zfld VALUES ('epo', 'Επώνυμο', 'Επώνυμο εργαζομένου', 3, 50, 'txt');
INSERT INTO zfld VALUES ('ono', 'Όνομα', 'Όνομα εργαζομένου', 3, 50, 'txt');
INSERT INTO zfld VALUES ('pat', 'Πατρώνυμο', 'Όνομα πατέρα', 3, 50, 'txt');
INSERT INTO zfld VALUES ('mit', 'Μητρώνυμο','Όνομα μητέρας', 3, 50, 'txt');
INSERT INTO zfld VALUES ('bdat', 'Ημ.Γενν.', 'Ημ/νία γέννησης', 10, 10, 'dat');

CREATE VIEW r_erg AS
SELECT id, epo || ' ' || ono as repr
FROM erg
;

CREATE TABLE IF NOT EXISTS eid( --Ειδικότητα εργασίας
id INTEGER PRIMARY KEY,
eidp TEXT NOT NULL UNIQUE
);
INSERT INTO ztab VALUES ('eid', 'Ειδικότητα', 'Ειδικότητες εργασίας');
INSERT INTO zfld VALUES ('eidp', 'Ειδικότητα', 'Ειδικότητα εργασίας', 5, 50, 'txt');

CREATE TABLE IF NOT EXISTS aptyp( --Τύπος αποδοχών
id INTEGER PRIMARY KEY,
aptyp TEXT NOT NULL UNIQUE
);
INSERT INTO ztab VALUES ('aptyp', 'Τύπος αποδοχών', 'Τύποι αποδοχών');
INSERT INTO zfld VALUES ('aptyp', 'Τύπος', 'Τύπος αποδοχών', 5, 50, 'txt');
INSERT INTO aptyp VALUES (1, 'Μισθωτός');
INSERT INTO aptyp VALUES (2, 'Ημερομίσθιος');
INSERT INTO aptyp VALUES (3, 'Ωρομίσθιος');

CREATE TABLE IF NOT EXISTS pro( --Προσλήψεις
id INTEGER PRIMARY KEY,
pdate DATE NOT NULL, --Ημερομηνία πρόσληψης
id_erg INTEGER NOT NULL REFERENCES erg(id), --Εργαζόμενος
id_eid INTEGER NOT NULL REFERENCES eid(id), --Ειδικότητα εργασίας
id_aptyp INTEGER NOT NULL REFERENCES aptyp(id), --Τύπος αποδοχών (μισθός/ ημέρομίσθιο)
apod NUMERIC NOT NULL DEFAULT 0,
UNIQUE (pdate, id_erg)
);
INSERT INTO ztab VALUES ('pro', 'Πρόσληψη', 'Προσλήψεις');
INSERT INTO zfld VALUES ('pdate', 'Ημ.Προσλ.', 'Ημερομηνία πρόσληψης', 10, 10, 'dat');
INSERT INTO zfld VALUES ('apod', 'Αποδοχές', 'Αποδοχές εργασίας', 1, 20, 'dec');
CREATE VIEW r_pro AS
SELECT pro.pdate, pro.id_erg, pro.id_eid, pro.id_aptyp, pro.apod,
erg.epo || ' ' || erg.ono as onomatep, 
eid.eidp as eidp,
aptyp.aptyp as aptyp 
FROM pro
INNER JOIN erg ON erg.id=pro.id_erg
INNER JOIN eid ON eid.id=pro.id_eid
INNER JOIN aptyp ON aptyp.id=pro.id_aptyp
;
INSERT INTO zfld VALUES ('onomatep', 'Ονοματεπώνυμο', 'Ονοματεπώνυμο εργαζομένου', 1, 50, 'txt');
COMMIT TRANSACTION;
