BEGIN TRANSACTION;
--Βοηθητικός πίνακας κλειδώματος ημερομηνίας εγγραφής
CREATE TABLE IF NOT EXISTS lk(
id INTEGER NOT NULL PRIMARY KEY,
lkd DATE NOT NULL UNIQUE
);
INSERT INTO lk VALUES(1,'1999-12-31');
--Βοηθητικός πίνακας (Τιμές Ναι/Όχι 0,1)
CREATE TABLE IF NOT EXISTS yn(
id INTEGER NOT NULL PRIMARY KEY,
ynp TEXT NOT NULL UNIQUE
);
INSERT INTO yn VALUES(0,'Όχι');
INSERT INTO yn VALUES(1,'Ναι');
CREATE TABLE IF NOT EXISTS lg(
id INTEGER NOT NULL PRIMARY KEY,
ldt TEXT NOT NULL,  --Ημερομηνία - Ώρα (πχ 2013-01-31 20:30:15)
logp TEXT NOT NULL  --Σχόλια
);
--Τρίμηνα
CREATE TABLE IF NOT EXISTS tr (
id integer NOT NULL PRIMARY KEY,
trp TEXT NTO NULL UNIQUE
);
INSERT INTO tr VALUES(1,'Α τρίμηνο (Ιαν-Φεβ-Μαρ)');
INSERT INTO tr VALUES(2,'Β τρίμηνο (Απρ-Μαι-Ιουν)');
INSERT INTO tr VALUES(3,'Γ τρίμηνο (Ιούλ-Αύγ-Σεπτ)');
INSERT INTO tr VALUES(4,'Δ τρίμηνο (Οκτ-Νοε-Δεκ)');
--Μήνες
CREATE TABLE IF NOT EXISTS mi (
id text NOT NULL PRIMARY KEY,
mip TEXT NTO NULL UNIQUE
);
INSERT INTO mi VALUES('01','Ιανουάριος');
INSERT INTO mi VALUES('02','Φεβρουάριος');
INSERT INTO mi VALUES('03','Μάρτιος');
INSERT INTO mi VALUES('04','Απρίλιος');
INSERT INTO mi VALUES('05','Μάϊος');
INSERT INTO mi VALUES('06','Ιούνιος');
INSERT INTO mi VALUES('07','Ιούλιος');
INSERT INTO mi VALUES('08','Αύγουστος');
INSERT INTO mi VALUES('09','Σεπτέμβριος');
INSERT INTO mi VALUES('10','Οκτώβριος');
INSERT INTO mi VALUES('11','Νοέμβριος');
INSERT INTO mi VALUES('12','Δεκέμβριος');
--Στοιχεία εταιρείας
CREATE TABLE IF NOT EXISTS co (
    id integer NOT NULL PRIMARY KEY,
    cop varchar(60) NOT NULL UNIQUE,
    ono varchar(20) NOT NULL,
    pat varchar(20) NOT NULL,
    ame varchar(10) NOT NULL UNIQUE,
    afm varchar(9) NOT NULL UNIQUE,
    doy varchar(60) NOT NULL,
    dra varchar(60) NOT NULL,
    pol varchar(30) NOT NULL,
    odo varchar(30) NOT NULL,
    num varchar(5) NOT NULL,
    tk varchar(5) NOT NULL
);
INSERT INTO co VALUES (1,'No Name','','','','','','','','','','');
--Υποκατάστημα
CREATE TABLE IF NOT EXISTS yp(
id INTEGER NOT NULL PRIMARY KEY, --Κωδικός Υποκαταστήματος (1 για το κεντρικό)
co_id INTEGER NOT NULL REFERENCES co(id),
ypp TEXT NOT NULL UNIQUE --Όνομα υποκαταστήματος (το βασικό λέγεται κεντρικό)
);
INSERT INTO yp VALUES (1,1,'ΚΕΝΤΡΙΚΟ');
--Βοηθητικό για συγκεντρωτική
CREATE TABLE IF NOT EXISTS syg(
id INTEGER NOT NULL PRIMARY KEY,
sygp TEXT NOt NULL UNIQUE
);
INSERT INTO syg VALUES(0,'Όχι');
INSERT INTO syg VALUES(1,'Ναι');
--Πελάτες
CREATE TABLE IF NOT EXISTS pel(
id INTEGER NOT NULL PRIMARY KEY,
afm VARCHAR(9) NOT NULL UNIQUE,--Αριθμός Φορολογικού Μητρώου
epon TEXT NOT NULL UNIQUE,     --Επωνυμία
ccod TEXT,                     --Κωδικός Χώρας (online)
addr TEXT,                     --Διεύθυνση (online)   
rdat DATE,                     --Ημερομηνία αίτησης (online) 
doy TEXT,                      --ΔΟΥ (Δημόσια Οικονομική ΕΦορία)
poli TEXT,                     --Πόλη
odos TEXT,                     --Οδός
ar TEXT,                       --Αριθμός
tk VARCHAR(5),                 --Ταχυδρομικός κωδικός
til TEXT,                      --Τηλέφωνο
mail TEXT,                     --e-mail
syg_id INTEGER NOT NULL DEFAULT 1 REFERENCES syg(id) --1 Εάν μπαίνει στη συγκεντρωτική , 0 διαφορετικά
);
INSERT INTO pel VALUES(0,'0','Πελάτες Λιανικής','','','','','','','','','','',0);

--Προμηθευτές
CREATE TABLE IF NOT EXISTS pro(
id INTEGER NOT NULL PRIMARY KEY,
afm VARCHAR(9) NOT NULL UNIQUE,--Αριθμός Φορολογικού Μητρώου
epon TEXT NOT NULL UNIQUE,     --Επωνυμία
ccod TEXT,                     --Κωδικός Χώρας (online)
addr TEXT,                     --Διεύθυνση (online)   
rdat DATE,                     --Ημερομηνία αίτησης (online) 
doy TEXT,                      --ΔΟΥ (Δημόσια Οικονομική ΕΦορία)
poli TEXT,                     --Πόλη
odos TEXT,                     --Οδός
ar TEXT,                       --Αριθμός
tk VARCHAR(5),                 --Ταχυδρομικός κωδικός
til TEXT,                      --Τηλέφωνο
mail TEXT,                     --e-mail
syg_id INTEGER NOT NULL DEFAULT 1 REFERENCES syg(id) --1 Εάν μπαίνει στη συγκεντρωτική , 0 διαφορετικά
);
INSERT INTO pro VALUES(0,'0','Χωρίς προμηθευτή','','','','','','','','','','',0);
--Τύπος εγγραφής εσόδων
CREATE TABLE IF NOT EXISTS et( 
id INTEGER NOT NULL PRIMARY KEY,
etp TEXT NOT NULL UNIQUE, --Περιγραφή τύπου εγγραφής 
pfpa DECIMAL NOT NULL DEFAULT 0, --Συντελεστής ΦΠΑ
f2_id INTEGER NOT NULL DEFAULT 0 --ΚΩΔΙΚΟΣ ΕΝΤΥΠΟΥ ΦΠΑ
);
INSERT INTO et VALUES(1,'ΠΩΛΗΣΕΙΣ ΛΙΑΝΙΚΗΣ 13% ΦΠΑ',13,301);
INSERT INTO et VALUES(2,'ΠΩΛΗΣΕΙΣ ΛΙΑΝΙΚΗΣ 23% ΦΠΑ',23,303);
--Βοηθητικό Παραστατικών (Πχ θεωρημένα , αθεώρητα ,ταμιακή μηχανή κλπ)
CREATE TABLE IF NOT EXISTS theo(
id INTEGER NOT NULL PRIMARY KEY,
theop TEXT NOt NULL UNIQUE
);
INSERT INTO theo VALUES(0,'Θεωρημένο χειρόγραφο');
INSERT INTO theo VALUES(1,'Θεωρημένο μηχανογραφημένο');
INSERT INTO theo VALUES(2,'Αθεώρητο χειρόγραφο');
INSERT INTO theo VALUES(3,'Ταμειακή μηχανή');
--Σειρές παραστατικών που εκδίδουμε (π.χ. Ζ881, ΤΔΑ Χειρόγραφο Σειρ.Α κλπ)
CREATE TABLE IF NOT EXISTS sr( 
id INTEGER NOT NULL PRIMARY KEY,
srp TEXT NOT NULL UNIQUE, --Περιγραφή σειράς  
theo_id DECIMAL NOT NULL REFERENCES theo(id) --Άν είναι θεωρημένο ή όχι
); 
--Τα δεδομένα εσόδων αποθηκεύονται σε δομή master-detail με τους παρακάτω πίνακες
CREATE TABLE IF NOT EXISTS es(
id INTEGER NOT NULL PRIMARY KEY,
yp_id INTEGER NOT NULL DEFAULT 1 REFERENCES yp(id), --Βλέπει σε πίνακα υποκαταστήματος 
dat DATE NOT NULL,               --Ημερομηνία παραστατικού
sr_id INTEGER NOT NULL REFERENCES sr(id), --Σειρά παραστατικού - Αριθμός Ταμιακής 
par VARCHAR(20) NOT NULL,        --Αριθμός παραστατικού
pel_id INTEGER NOT NULL REFERENCES syn(id), --Κωδικός Πελάτη
tval DECIMAL NOT NULL,    --Συνολική καθαρή αξία παραστατικού
tfpa DECIMAL NOT NULL,    --Συνολική αξία ΦΠΑ παραστατικού
ttot DECIMAL NOT NULL,    --Τελική συνολική Αξία παραστατικού
UNIQUE(dat,sr_id,par)
);
CREATE TABLE IF NOT EXISTS esd(
id INTEGER NOT NULL PRIMARY KEY,
es_id INTEGER NOT NULL REFERENCES es(id), --Δείχνει στον πίνακα es (master)
et_id INTEGER NOT NULL REFERENCES et(id), --Δείχνει στον πίνακα et (Τύπος εγγραφής εσόδων) 
val DECIMAL NOT NULL,
fpa DECIMAL NOT NULL DEFAULT 0,
UNIQUE(es_id,et_id)
);
--Τύπος εγγραφής εξόδων
CREATE TABLE IF NOT EXISTS dt( 
id INTEGER NOT NULL PRIMARY KEY,
etp TEXT NOT NULL UNIQUE, --Περιγραφή τύπου εγγραφής 
pfpa DECIMAL NOT NULL DEFAULT 0, --Συντελεστής ΦΠΑ
f2_id INTEGER NOT NULL DEFAULT 1 --ΚΩΔΙΚΟΣ ΕΝΤΥΠΟΥ ΦΠΑ
);
INSERT INTO dt VALUES(1,'ΑΓΟΡΕΣ ΕΜΠΟΡΕΥΜΑΤΩΝ 13% ΦΠΑ',13,351);
INSERT INTO dt VALUES(2,'ΑΓΟΡΕΣ ΕΜΠΟΡΕΥΜΑΤΩΝ 23% ΦΠΑ',23,353);
INSERT INTO dt VALUES(3,'ΔΑΠΑΝΕΣ 23% ΦΠΑ',23,357);
INSERT INTO dt VALUES(4,'ΔΑΠΑΝΕΣ 13% ΦΠΑ',13,357);
INSERT INTO dt VALUES(5,'ΔΑΠΑΝΕΣ ΧΩΡΙΣ ΦΠΑ',0,1);
INSERT INTO dt VALUES(6,'ΑΓΟΡΕΣ ΠΑΓΙΩΝ 23% ΦΠΑ',23,353);
INSERT INTO dt VALUES(7,'ΑΓΟΡΕΣ ΠΑΓΙΩΝ ΧΩΡΙΣ ΦΠΑ',0,1);
--Τα δεδομένα εξόδων αποθηκεύονται σε δομή master-detail με τους παρακάτω πίνακες
CREATE TABLE IF NOT EXISTS ds(
id INTEGER NOT NULL PRIMARY KEY,
yp_id INTEGER NOT NULL DEFAULT 1 REFERENCES yp(id), --Βλέπει σε πίνακα υποκαταστήματος 
dat DATE NOT NULL,               --Ημερομηνία παραστατικού
par VARCHAR(20) NOT NULL,        --Αριθμός παραστατικού
pro_id INTEGER NOT NULL REFERENCES syn(id), --Κωδικός Πελάτη
tval DECIMAL NOT NULL,    --Συνολική καθαρή αξία παραστατικού
tfpa DECIMAL NOT NULL,    --Συνολική αξία ΦΠΑ παραστατικού
ttot DECIMAL NOT NULL,    --Τελική συνολική Αξία παραστατικού
UNIQUE(dat,par)
);
CREATE TABLE IF NOT EXISTS dsd(
id INTEGER NOT NULL PRIMARY KEY,
ds_id INTEGER NOT NULL REFERENCES ds(id), --Δείχνει στον πίνακα es (master)
dt_id INTEGER NOT NULL REFERENCES dt(id), --Δείχνει στον πίνακα et (Τύπος εγγραφής εσόδων) 
val DECIMAL NOT NULL,
fpa DECIMAL NOT NULL DEFAULT 0,
UNIQUE(ds_id,dt_id)
);
--Πίνακας ΦΠΑ
CREATE TABLE f2(
id INTEGER PRIMARY KEY,
f2p TEXT NOT NULL UNIQUE,
f2t INTEGER NOT NULL DEFAULT 0 -- 0 για έξοδα 1 για έσοδα
);
INSERT INTO f2 VALUES (1,'Έξοδα χωρίς ΦΠΑ',0);
INSERT INTO f2 VALUES (301,'Εκροές 13%',1);
INSERT INTO f2 VALUES (302,'Εκροές 6,5%',1);
INSERT INTO f2 VALUES (303,'Εκροές 23%',1);
INSERT INTO f2 VALUES (304,'Εκροές 9%',1);
INSERT INTO f2 VALUES (305,'Εκροές 5%',1);
INSERT INTO f2 VALUES (306,'Εκροές 16%',1);
INSERT INTO f2 VALUES (308,'Εκροές εκτός Ελλάδος με δικ.έκπτωσης',1);
INSERT INTO f2 VALUES (309,'Ενδοκ.παραδ. εξαγωγές & λοιπές εκροές απαλ/νες με δικ.έκπτωσης',1);
INSERT INTO f2 VALUES (310,'Εκροές απαλ/νες & εξαιρ. χωρίς δικ. έκπτωσης',1);
INSERT INTO f2 VALUES (341,'Συνολικές ενδοκοινοτικές αποκτήσεις',0);
INSERT INTO f2 VALUES (342,'Συνολικές ενδοκοινοτικές παραδόσεις',1);
INSERT INTO f2 VALUES (343,'Πράξεις λήπτη αγαθών και υπηρεσιών',1);
INSERT INTO f2 VALUES (344,'Ενδοκοινοτικές λήψεις υπηρεσιών αρθρ.14 παρ 2α',0);
INSERT INTO f2 VALUES (345,'Ενδοκοινοτικές παροχές υπηρεσιών αρθρ.14 παρ 2α',1);
INSERT INTO f2 VALUES (351,'Εισροές 13%',0);
INSERT INTO f2 VALUES (352,'Εισροές 6,5%',0);
INSERT INTO f2 VALUES (353,'Εισροές 23%',0);
INSERT INTO f2 VALUES (354,'Εισροές 9%',0);
INSERT INTO f2 VALUES (355,'Εισροές 5%',0);
INSERT INTO f2 VALUES (356,'Εισροές 16%',0);
INSERT INTO f2 VALUES (357,'Δαπάνες, γεν.έξοδα φορολογητέα',0);
COMMIT;
