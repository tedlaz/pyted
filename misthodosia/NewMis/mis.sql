--Τύπος επιχείρησης
CREATE TABLE IF NOT EXISTS co_t (
id INTEGER PRIMARY KEY, --Κωδικός τύπου επιχείρησης
scot VARCHAR(50) NOT NULL UNIQUE --Περιγραφή τύπου επιχείρησης
);
INSERT INTO co_t VALUES(0,'Εταιρία');
INSERT INTO co_t VALUES(1,'Φυσικό πρόσωπο');
--Στοιχεία εταιρείας
CREATE TABLE IF NOT EXISTS co (
id INTEGER PRIMARY KEY,
scop VARCHAR(60) NOT NULL UNIQUE, --Όνομα επιχείρησης
sono VARCHAR(20) NOT NULL, --Επώνυμο
spat VARCHAR(20) NOT NULL, --Πατρώνυμο
cco_t INTEGER NOT NULL REFERENCES co_t (id),
sek VARCHAR(80) NOT NULL, -- Ονοματεπώνυμο εκπροσώπου
jame VARCHAR(10) NOT NULL UNIQUE, --Αριθμός Μητρώου ΙΚΑ επιχείρησης
jafm VARCHAR(9) NOT NULL UNIQUE,  --Αριθμός Φορολογικού Μητρώου
sdoy VARCHAR(60) NOT NULL, --Όνομα Δημόσιας Οικονομικής Εφορίας
sdra VARCHAR(60) NOT NULL, --Περιγραφή δραστηριότητας
jikac VARCHAR(3) NOT NULL, --Κωδικός Υποκαταστήματος ΙΚΑ
sikap VARCHAR(50) NOT NULL --Περιγραφή Υποκαταστήματος ΙΚΑ
);
INSERT INTO co VALUES (1,'Εταιρεία','','',0,'','','','','','','');
--Στοιχεία υποκαταστήματος
CREATE TABLE IF NOT EXISTS coy (
id INTEGER PRIMARY KEY,
cco INTEGER NOT NULL REFERENCES co (id),
scoyp VARCHAR(60) NOT NULL UNIQUE, --Όνομα παραρτήματος
jkad VARCHAR(4) NOT NULL, --Κωδικός αριθμός δραστηριότητας υποκαταστήματος
spol VARCHAR(30) NOT NULL, --Πόλη
sodo VARCHAR(30) NOT NULL, --Οδός
snum VARCHAR(5) NOT NULL,  --Αριθμός
jtk  VARCHAR(5) NOT NULL  --Ταχυδρομικός κωδικός
);
INSERT INTO coy VALUES(1,1,'Κεντρικό','','','','','');
--Φύλο 
CREATE TABLE IF NOT EXISTS sex (
id INTEGER PRIMARY KEY,
ssex VARCHAR(10) NOT NULL UNIQUE -- Άνδρας ή Γυναίκα
);
INSERT INTO sex VALUES(0,'Άνδρας');
INSERT INTO sex VALUES(1,'Γυναίκα');
--Βασικά Στοιχεία Εργαζομένων 
CREATE TABLE IF NOT EXISTS er (
id INTEGER PRIMARY KEY,
sepo VARCHAR(20) NOT NULL, --Επώνυμο
sono VARCHAR(20) NOT NULL, --Όνομα
spat VARCHAR(20) NOT NULL, --Όνομα πατέρα
smit VARCHAR(20) NOT NULL, --Όνομα μητέρας
csex INTEGER NOT NULL REFERENCES sex (id),
dgen DATE NOT NULL, --Ημερομηνία γέννησης
jafm VARCHAR(9) NOT NULL, --ΑΦΜ
staf VARCHAR(20) NOT NULL, --Αριθμός ταυτότητας
jamka VARCHAR(11) NOT NULL, --ΑΜΚΑ
jika VARCHAR(7) NOT NULL, --Αριθμός Μητρώου ΙΚΑ
spol VARCHAR(30) NOT NULL, --Πόλη
sodo VARCHAR(30) NOT NULL, --Οδός
snum VARCHAR(5) NOT NULL, --Αριθμός
jtk VARCHAR(5) NOT NULL, --Ταχυδρομικός κώδικας
jtel VARCHAR(10), --Τηλέφωνο
smail VARCHAR(50), --e-mail 
UNIQUE (sepo, sono, spat, smit)
);
--Ειδικότητες εργασίας
CREATE TABLE IF NOT EXISTS eid (
id INTEGER PRIMARY KEY,
seid VARCHAR(60) NOT NULL UNIQUE, --Περιγραφή ειδικότητας
jeid INTEGER NOT NULL UNIQUE --Κωδικό ΙΚΑ ειδικότητας εργασίας
);
--Τύπος αποδοχών
CREATE TABLE IF NOT EXISTS aptyp (
id INTEGER PRIMARY KEY,
saptyp VARCHAR(20) NOT NULL UNIQUE --περιγραφή τύπου απδοχών
);
INSERT INTO aptyp VALUES(1,'Μισθός');
INSERT INTO aptyp VALUES(2,'Ημερομίσθιο');
INSERT INTO aptyp VALUES(3,'Ωρομίσθιο');
--Στοιχεία πρόσληψης εργαζομένων
CREATE TABLE IF NOT EXISTS erp (
id INTEGER PRIMARY KEY,
zer INTEGER NOT NULL REFERENCES er (id), --Εργαζόμενος
dpro DATE NOT NULL, --Ημερομηνία πρόσληψης
csye INTEGER NOT NULL REFERENCES sye (id), --Είδος σύμβασης (Ορισμένου, αορίστου)
eli DATE, --Ημερομηνία λήξης σύμβασης (εάν υπάρχει)  
zcoy INTEGER NOT NULL REFERENCES coy (id), --Υποκατάστημα
zeid INTEGER NOT NULL REFERENCES eid (id), --Ειδικότητα εργασίας
iproy INTEGER NOT NULL, --Προυπηρεσία στην ειδικότητα σε έτη
csyt INTEGER NOT NULL REFERENCES syt (id), --Τύπος απασχόλησης (Πλήρης, μερική , εκ περιτροπής)
imer INTEGER NOT NULL, --Ημέρες εβδομαδιαίας απασχόλησης
nor  DECIMAL NOT NULL, --ώρες απασχόλησης ανα βδομάδα 
tora VARCHAR(100) NOT NULL, --Ωράριο απασχόλησης
captyp INTEGER NOT NULL REFERENCES aptyp (id), --Τύπος αποδοχών 
napod DECIMAL NOT NULL, --Αποδοχές
UNIQUE (zer, dpro)
);
--Τύπος Αποχώρησης εργαζομένων
CREATE TABLE IF NOT EXISTS erat (
id INTEGER PRIMARY KEY,
serat VARCHAR(30) NOT NULL UNIQUE
);
INSERT INTO erat VALUES(1,'Οικιοθελής αποχώρηση');
INSERT INTO erat VALUES(2,'Απόλυση');
INSERT INTO erat VALUES(3,'Συνταξιοδότηση');
--Στοιχεία Αποχώρησης εργαζομένων
CREATE TABLE IF NOT EXISTS erpa (
id INTEGER PRIMARY KEY,
zerp INTEGER NOT NULL REFERENCES erp (id), --Πρόσληψη εργαζομένου
derpa DATE NOT NULL, --Ημερομηνία αποχώρησης
cerat INTEGER NOT NULL REFERENCES erat (id), --τύπος Αποχώρησης
UNIQUE(zerp,derpa)
); 
--Χρήσεις
CREATE TABLE IF NOT EXISTS xr (
id INTEGER PRIMARY KEY,
ix INTEGER NOT NULL UNIQUE -- eg 2013
);
--Μήνες
CREATE TABLE IF NOT EXISTS xrm (
id INTEGER PRIMARY KEY,
sxrm VARCHAR(15) NOT NULL UNIQUE --month
);
INSERT INTO xrm VALUES(1,'Ιανουάριος');
INSERT INTO xrm VALUES(2,'Φεβρουάριος');
INSERT INTO xrm VALUES(3,'Μάρτιος');
INSERT INTO xrm VALUES(4,'Απρίλιος');
INSERT INTO xrm VALUES(5,'Μάϊος');
INSERT INTO xrm VALUES(6,'Ιούνιος');
INSERT INTO xrm VALUES(7,'Ιούλιος');
INSERT INTO xrm VALUES(8,'Αύγουστος');
INSERT INTO xrm VALUES(9,'Σεπτέμβριος');
INSERT INTO xrm VALUES(10,'Οκτώβριος');
INSERT INTO xrm VALUES(11,'Νοέμβριος');
INSERT INTO xrm VALUES(12,'Δεκέμβριος');
--Είδος σύμβασης
CREATE TABLE IF NOT EXISTS sye (
id INTEGER PRIMARY KEY,
ssye VARCHAR(30) NOT NULL UNIQUE --Περιγραφή τύπου σύμβασης
);
INSERT INTO sye VALUES(1,'Αορίστου χρόνου');
INSERT INTO sye VALUES(2,'Ορισμένου χρόνου');
--Τύπος απασχόλησης
CREATE TABLE IF NOT EXISTS syt (
id INTEGER PRIMARY KEY,
ssyt VARCHAR(50) NOT NULL UNIQUE --Περιγραφή τύπου απασχόλησης
);
INSERT INTO syt VALUES(1,'Πλήρης απασχόληση');
INSERT INTO syt VALUES(2,'Μερική απασχόληση');
INSERT INTO syt VALUES(3,'Εκ περιτροπής απασχόληση');
--Παρουσίες
CREATE TABLE IF NOT EXISTS p (
id INTEGER PRIMARY KEY,
cxr INTEGER NOT NULL REFERENCES xr(id), --Χρήση
cxrm INTEGER NOT NULL REFERENCES xrm(id), --Μήνας
bok INTEGER NOT NULL DEFAULT 0, --Έτοιμη για υπολογισμό ή όχι (1:True/0:False)
UNIQUE (cxr,cxrm)
);
--Παρουσίες εργαζομένων
CREATE TABLE IF NOT EXISTS pe (
id INTEGER PRIMARY KEY,
zp INTEGER NOT NULL REFERENCES p(id), --Περίοδος (Χρήση-Μήνας)
zerp INTEGER NOT NULL REFERENCES erp(id), --Εργαζόμενος
ndn DECIMAL NOT NULL DEFAULT 0, --Μέρες εργασίας
ndk DECIMAL NOT NULL DEFAULT 0, --Κυριακές - αργίες (για προσαύξηση)
non DECIMAL NOT NULL DEFAULT 0, --Ώρες για νυχτερινή προσαύξηση
UNIQUE (zp,zerp)
);
--Απουσίες εργαζομένων λόγω ασθένειας
CREATE TABLE IF NOT EXISTS pea (
id INTEGER PRIMARY KEY,
zpe INTEGER NOT NULL REFERENCES pe(id), --Αναφορά σε παρουσία περιόδου εργαζομένου
dpeaa DATE NOT NULL, --Πρώτη ημέρα απουσίας
dpeae DATE NOT NULL, --Τελευταία ημέρα απουσίας
ndl3 DECIMAL NOT NULL DEFAULT 0, --Ημέρες ασθένειας < 3
ndm3 DECIMAL NOT NULL DEFAULT 0, --Ημέρες ασθένειας > 3
ndxk DECIMAL NOT NULL DEFAULT 0, --Ημέρες ασθένειας χωρίς κάλυψη
nepi DECIMAL NOT NULL DEFAULT 0, --Επίδομα ΙΚΑ
UNIQUE (zpe,dpeaa)
);
--menus
CREATE TABLE IF NOT EXISTS zmn (
id INTEGER PRIMARY KEY,
smn VARCHAR(30) NOT NULL UNIQUE
);
INSERT INTO zmn VALUES(0,'Εκτός Μενού');
--Custom Views
CREATE TABLE IF NOT EXISTS zv (
id INTEGER PRIMARY KEY,
svname VARCHAR(20) NOT NULL UNIQUE,
stbl VARCHAR(20) NOT NULL,
svlbl VARCHAR(50) NOT NULL,
tsql TEXT NOT NULL,
zzmn INTEGER NOT NULL DEFAULT 0
);
--Labels for fields
CREATE TABLE IF NOT EXISTS zlbl (
id INTEGER PRIMARY KEY,
sfld VARCHAR(20) NOT NULL UNIQUE, --field name
slbl VARCHAR(10) NOT NULL UNIQUE, --Small Label
slblf VARCHAR(60) --Full label
);
CREATE TABLE IF NOT EXISTS zt(
id INTEGER PRIMARY KEY,
stnam VARCHAR(60) NOT NULL UNIQUE, --table name
stlbl VARCHAR(30) NOT NULL UNIQUE, --table label
tsqlv VARCHAR(255) NOT NULL, --table human viewable representation
tsqlf VARCHAR(255) NOT NULL, --table values(id,description) for foreign key
tuniq VARCHAR(255) NOT NULL --unuque field combination (eg (sepo,sono))
);