BEGIN TRANSACTION;
CREATE TABLE dapx(
id INTEGER PRIMARY KEY,
ej_id INTEGER NOT NULL,
dia_id INTEGER NOT NULL,
val INTEGER NOT NULL DEFAULT 0,
UNIQUE (ej_id, dia_id)
);
INSERT INTO "dapx" VALUES(1,4,1,270);
INSERT INTO "dapx" VALUES(2,1,2,204);
INSERT INTO "dapx" VALUES(3,2,2,139);
INSERT INTO "dapx" VALUES(4,3,2,204);
INSERT INTO "dapx" VALUES(5,4,2,150);
INSERT INTO "dapx" VALUES(6,1,3,159);
INSERT INTO "dapx" VALUES(7,2,3,108);
INSERT INTO "dapx" VALUES(8,3,3,159);
INSERT INTO "dapx" VALUES(9,4,3,115);
INSERT INTO "dapx" VALUES(10,1,4,243);
INSERT INTO "dapx" VALUES(11,2,4,249);
INSERT INTO "dapx" VALUES(12,3,4,243);
INSERT INTO "dapx" VALUES(13,4,4,178);
INSERT INTO "dapx" VALUES(14,1,5,120);
INSERT INTO "dapx" VALUES(15,2,5,122);
INSERT INTO "dapx" VALUES(16,3,5,120);
INSERT INTO "dapx" VALUES(17,4,5,87);
INSERT INTO "dapx" VALUES(18,1,6,274);
INSERT INTO "dapx" VALUES(19,2,6,382);
INSERT INTO "dapx" VALUES(20,3,6,274);
INSERT INTO "dapx" VALUES(21,4,6,200);
INSERT INTO "dapx" VALUES(22,1,1,0);
INSERT INTO "dapx" VALUES(23,2,1,0);
INSERT INTO "dapx" VALUES(24,3,1,0);
CREATE TABLE dia(
id INTEGER PRIMARY KEY,
dia TEXT NOT NULL,
dno INTEGER NOT NULL DEFAULT 0,
orofos INTEGER NOT NULL,
owner TEXT NOT NULL,
guest TEXT NOT NULL
);
INSERT INTO "dia" VALUES(1,'Φροντιστήριο',0,0,'Νεόπουλος','Άγνωστος');
INSERT INTO "dia" VALUES(2,'Διαμ1',1,1,'Νεόπουλος','Άγνωστος');
INSERT INTO "dia" VALUES(3,'Διαμ2',2,1,'Νεόπουλος','Άγνωστος');
INSERT INTO "dia" VALUES(4,'Διαμ3',3,2,'Νεόπουλος','Άγνωστος');
INSERT INTO "dia" VALUES(5,'Διαμ4',4,2,'Νεόπουλος','Άγνωστος');
INSERT INTO "dia" VALUES(6,'Διαμ5',5,3,'Λάζαρος','Άγνωστος');
CREATE TABLE ej(
id INTEGER PRIMARY KEY,
ej TEXT NOT NULL
);
INSERT INTO "ej" VALUES(1,'Θέρμανση');
INSERT INTO "ej" VALUES(2,'Ασανσέρ - ΔΕΗ');
INSERT INTO "ej" VALUES(3,'Καθαριότητα');
INSERT INTO "ej" VALUES(4,'MAlakis');
INSERT INTO "ej" VALUES(5,'MAlakis');
CREATE TABLE koi(
id INTEGER PRIMARY KEY,
kdat DATE NOT NULL UNIQUE, --Ημερομηνία έκδοσης
koip TEXT NOT NULL UNIQUE, --Περίοδος
sxol TEXT NOT NULL --Σχόλιο
);
INSERT INTO "koi" VALUES(1,'2015-01-31','Ιανουάριος 2015',' ');
INSERT INTO "koi" VALUES(2,'2015-02-28','Φεβρουάριος 2015',' ');
CREATE TABLE koid(
id INTEGER PRIMARY KEY,
koi_id INTEGER NOT NULL,
dia_id INTEGER NOT NULL,
dia TEXT NOT NULL,
enoikiastis TEXT NOT NULL,
idioktitis TEXT NOT NULL,
orofos INTEGER NOT NULL,
diano INTEGER NOT NULL, --Αριθμός διαμερίσματος
UNIQUE (koi_id, dia_id)
);
CREATE TABLE koidd(
id INTEGER PRIMARY KEY,
koi_id INTEGER NOT NULL,
dia_id INTEGER NOT NULL,
ej_id INTEGER NOT NULL,
dapani TEXT NOT NULL, --Όνομα κατηγορίας δαπάνης
xiliosta INTEGER NOT NULL DEFAULT 0, --Χιλιοστά διαμερίσματος
total DECIMAL NOT NULL DEFAULT 0, --Συνολική δαπάνη
poso DECIMAL NOT NULL DEFAULT 0, --Αναλογία διαμερίσματος
UNIQUE (koi_id, dia_id, ej_id)
);
CREATE TABLE par(
id INTEGER PRIMARY KEY,
koi_id INTEGER NOT NULL,
no TEXT NOT NULL, --Αριθμός παραστατικού
pdate DATE NOT NULL, --Ημερομηνία παραστατικού
ej_id INTEGER NOT NULL,
parp TEXT NOT NULL, --Περιγραφή εξόδου
poso DECIMAL NOT NULL DEFAULT 0,
UNIQUE (koi_id, no)
);
INSERT INTO "par" VALUES(1,1,'ΤΔΑ21','2015-01-10',1,'Δαπάνη 1',24.32);
INSERT INTO "par" VALUES(2,2,'ΑΠ34','2015-01-24',2,'Δαπάνη 2',14);
INSERT INTO "par" VALUES(3,1,'ΑΠ335','2015-01-24',1,'Δαπάνη 3',25);
CREATE TABLE pp(
id INTEGER PRIMARY KEY,
pname TEXT NOT NULL UNIQUE,
plbl TEXT NOT NULL UNIQUE,
pval TEXT NOT NULL
);
INSERT INTO "pp" VALUES(1,'diax || '' '' ||  j','Διαχειριστής','Θεόδωρος Λάζαρος');
INSERT INTO "pp" VALUES(2,'adress','Διεύθυνση','Σισμανογλείου 17 & Σπάρτης');
CREATE TABLE ta (id integer primary key, epo text, ono text);
INSERT INTO "ta" VALUES(1,'Mastoras','Giorgos');
INSERT INTO "ta" VALUES(2,'Mayr','Niko');
CREATE TABLE tb (id integer primary key, ta_id integer, ej_id integer, tsv2 text);
INSERT INTO "tb" VALUES(1,1,1,'xxv');
INSERT INTO "tb" VALUES(2,1,10,'test');
INSERT INTO "tb" VALUES(3,1,20,'teste');
INSERT INTO "tb" VALUES(4,2,33,'testwe');
INSERT INTO "tb" VALUES(5,2,44,'testewee');
CREATE VIEW "vpar" AS SELECT par.id, par.koi_id, koi.koip, par.no, par.pdate, par.ej_id, ej.ej, par.parp, par.poso
FROM par
INNER JOIN koi ON koi.id=par.koi_id
INNER JOIN ej ON ej.id=par.ej_id;
CREATE VIEW "vdapx" AS SELECT dapx.id, dapx.ej_id, ej.ej, dapx.dia_id, dia.dia, dapx.val
FROM dapx
INNER JOIN ej  ON ej.id=dapx.ej_id
INNER JOIN dia  ON dia.id=dapx.dia_id
ORDER BY ej_id, dia_id;
CREATE VIEW "vpar_sum" AS
SELECT koi.id as koi_id, koi.koip, ej.id as ej_id, ej.ej, sum(par.poso) as sposo
FROM par
INNER JOIN koi ON koi.id=par.koi_id
INNER JOIN ej ON ej.id=par.ej_id
GROUP BY koi.id, par.ej_id;
COMMIT;
