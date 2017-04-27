-- Παράμετροι εταιρίας
CREATE TABLE IF NOT EXISTS co(
id INTEGER PRIMARY KEY,
cop varchar(60) NOT NULL UNIQUE,
ono varchar(20) NOT NULL,
pat varchar(20) NOT NULL,
ame varchar(10) NOT NULL UNIQUE,
afm varchar(9) NOT NULL UNIQUE
);

--Παραρτήματα
CREATE TABLE IF NOT EXISTS cop(
id INTEGER PRIMARY KEY,
cop TEXT NOT NULL UNIQUE,
doy varchar(60) NOT NULL,
dra varchar(60) NOT NULL,
pol varchar(30) NOT NULL,
odo varchar(30) NOT NULL,
num varchar(5) NOT NULL,
tk varchar(5) NOT NULL
);
INSERT INTO cop VALUES (1, 'Κεντρικό', '', '', '', '', '', '');

--Τύπος εγγραφής (Έσοδα, έξοδα, αγορές/πωλήσεις παγίων)
CREATE TABLE IF NOT EXISTS typee(
id INTEGER PRIMARY KEY,
typee TEXT NOT NULL UNIQUE
);
INSERT INTO typee VALUES (1, 'Έσοδα');
INSERT INTO typee VALUES (2, 'Έξοδα');
INSERT INTO typee VALUES (3, 'Αγορές Παγίων');
INSERT INTO typee VALUES (4, 'Πωλήσεις Παγίων');

--Τύπος εγγραφής (Χρεωστικό ή πιστωτικό)
CREATE TABLE IF NOT EXISTS typcd(
id INTEGER PRIMARY KEY,
typcd TEXT NOT NULL UNIQUE
);
INSERT INTO typcd VALUES (10, 'Normal');
INSERT INTO typcd VALUES (20, 'Credit');

--Τύπος εγγραφής (Εσωτερικό, Ενδοκοινοτική, Εξωτερικό)
CREATE TABLE IF NOT EXISTS typgr(
id INTEGER PRIMARY KEY,
typgr TEXT NOT NULL UNIQUE
);
INSERT INTO typgr VALUES (100, 'Εσωτερικό');
INSERT INTO typgr VALUES (200, 'Ενδοκοινοτικό');
INSERT INTO typgr VALUES (300, 'Εξωτερικό');

--Τύπος αναλυτικής γραμμής (ΠΧ Αγορές εμπορευμάτων 24% η Δαπάνες 24% χωρίς έκπτωση του ΦΠΑ)
CREATE TABLE IF NOT EXISTS typln(
id INTEGER PRIMARY KEY,
typln TEXT NOT NULL UNIQUE,
pfpa NUMERIC NOT NULL DEFAULT 0, --Ποσοστό ΦΠΑ
ekpiptei NUMERIC NOT NULL DEFAULT 1 --1 αν εκπίπτει 0 αν δεν εκπίπτει.
);
CREATE TABLE IF NOT EXISTS f2(
id INTEGER PRIMARY KEY,
f2 TEXT NOT NULL UNIQUE
);
INSERT INTO f2 VALUES (301, 'Εκροές 13%');
INSERT INTO f2 VALUES (302, 'Εκροές 6%');
INSERT INTO f2 VALUES (303, 'Εκροές 24%');
INSERT INTO f2 VALUES (304, 'Εκροές 9%');
INSERT INTO f2 VALUES (305, 'Εκροές 4%');
INSERT INTO f2 VALUES (306, 'Εκροές 17%');
INSERT INTO f2 VALUES (342, 'Ενδοκοινοτικές παραδόσεις');
INSERT INTO f2 VALUES (345, 'Ενδοκοινοτικές παροχές υπηρεσιών');
INSERT INTO f2 VALUES (348, 'Εξαγωγές & απαλλαγές πλοίων και αεροσκαφών');
INSERT INTO f2 VALUES (349, 'Εκροές με δικαίωμα έκπτωσης');
INSERT INTO f2 VALUES (310, 'Εκροές χωρίς δικαίωμα έκπτωσης');
INSERT INTO f2 VALUES (361, 'Αγορές & δαπάνες εσωτερικού');
INSERT INTO f2 VALUES (362, 'Αγορές & εισαγωγές παγίων');
INSERT INTO f2 VALUES (363, 'Λοιπές εισαγωγές εκτός παγίων');
INSERT INTO f2 VALUES (364, 'Ενδοκοινοτικές αποκτήσεις αγαθών');
INSERT INTO f2 VALUES (365, 'Ενδοκοινοτικές λήψεις υπηρεσιών');
INSERT INTO f2 VALUES (366, 'Λοιπές πράξεις λήπτη');

--Πολλά προς πολλά σύνδεση του f2 με τις αναλυτικές κινήσεις
CREATE TABLE IF NOT EXISTS  f2typln(
id INTEGER PRIMARY KEY,
f2_id INTEGER NOT NULL REFERENCES f2(id),
typln_id INTEGER NOT NULL REFERENCES typln(id)
);

CREATE TABLE IF NOT EXISTS syn(
afm TEXT PRIMARY KEY,
syn TEXT NOT NULL UNIQUE, --Επωνυμία συναλλασσομένου
xora TEXT NOT NULL DEFAULT 'Ελλάδα'
);
CREATE TABLE IF NOT EXISTS ee(
id INTEGER PRIMARY KEY,
cop_id INTEGER NOT NULL REFERENCES cop(id),
typee_id INTEGER NOT NULL REFERENCES typee(id),
typcd_id INTEGER NOT NULL REFERENCES typcd(id),
typgr_id INTEGER NOT NULL REFERENCES typgr(id),
syn_afm INTEGER NOT NULL REFERENCES syn(afm),
imnia DATE NOT NULL,
par TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS eed(
id INTEGER PRIMARY KEY,
ee_id INTEGER NOT NULL REFERENCES ee(id),
typln_id INTEGER NOT NULL REFERENCES typln(id),
val NUMERIC NOT NULL DEFAULT 0,
fpa NUMERIC NOT NULL DEFAULT 0
);

--views
CREATE VIEW bib1 AS
SELECT ee.id, cop.cop, typee.typee, typcd.typcd, typgr.typgr,
       syn.syn, ee.imnia, ee.par,
       typln.typln, eed.val, eed.fpa
FROM ee
INNER JOIN cop on cop.id=ee.cop_id
INNER JOIN typee on typee.id=ee.typee_id
INNER JOIN typcd on typcd.id=ee.typcd_id
INNER JOIN typgr on typgr.id=ee.typgr_id
INNER JOIN syn on syn.afm=ee.syn_afm
INNER JOIN eed on ee.id=eed.ee_id
INNER JOIN typln on typln.id=eed.typeln_id
;

CREATE VIEW bibt AS
SELECT ee.id, cop.cop, typee.typee, typcd.typcd, typgr.typgr,
       syn.syn, ee.imnia, ee.par,
       sum(eed.val) as tval, sum(eed.fpa) as tfpa,
       sum(eed.val) + sum(eed.fpa) as tposo
FROM ee
INNER JOIN cop on cop.id=ee.cop_id
INNER JOIN typee on typee.id=ee.typee_id
INNER JOIN typcd on typcd.id=ee.typcd_id
INNER JOIN typgr on typgr.id=ee.typgr_id
INNER JOIN syn on syn.afm=ee.syn_afm
INNER JOIN eed on ee.id=eed.ee_id
INNER JOIN typln on typln.id=eed.typeln_id
GROUP BY ee.id, ee.cop_id, ee.typee_id, ee.typcd_id,
         ee.typgr_id, ee.syn_afm, ee.imnia, ee.par
;

CREATE VIEW biblio AS
SELECT ee.id, cop.cop, typee.typee, typcd.typcd, typgr.typgr,
       syn.syn, ee.imnia, ee.par,
       typln.typln, eed.val, eed.fpa, typln.ekpiptei,
case when ekpiptei = 0 then
	case when typcd.typcd='Credit' then val * -1 + fpa * -1 else val + fpa end
	else case when typcd.typcd='Credit' then val * -1 else val end
	end as bval,
case when typcd.typcd='Credit' then fpa * -1 * typln.ekpiptei
                               else fpa * typln.ekpiptei end as bfpa
FROM ee
INNER JOIN cop on cop.id=ee.cop_id
INNER JOIN typee on typee.id=ee.typee_id
INNER JOIN typcd on typcd.id=ee.typcd_id
INNER JOIN typgr on typgr.id=ee.typgr_id
INNER JOIN syn on syn.afm=ee.syn_afm
INNER JOIN eed on ee.id=eed.ee_id
INNER JOIN typln on typln.id=eed.typeln_id