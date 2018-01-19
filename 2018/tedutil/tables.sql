PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS zt(
stbl TEXT NOT NULL PRIMARY KEY,
snam TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS zfl(
sfld TEXT NOT NULL PRIMARY KEY,
slbl TEXT NOT NULL UNIQUE
);
INSERT INTO zfl VALUES('id', 'ΑΑ');


INSERT INTO zt VALUES('apasxolisitype', 'Καθεστώτα απασχόλησης');
INSERT INTO zfl VALUES('apasxolisitype_cd', 'Καθεστώς απασχόλησης');
CREATE TABLE IF NOT EXISTS apasxolisitype (
id integer NOT NULL PRIMARY KEY,
sapasxolisit varchar(50) NOT NULL UNIQUE);
INSERT INTO zfl VALUES('sapasxolisit', 'Τύπος Απασχόλησης');
INSERT INTO apasxolisitype VALUES(1,'Πλήρης');
INSERT INTO apasxolisitype VALUES(2,'Μερική');
INSERT INTO apasxolisitype VALUES(3,'Έκ περιτροπής');


INSERT INTO zt VALUES('apodoxestype', 'Τύποι αποδοχών');
INSERT INTO zfl VALUES('apodoxestype_cd', 'Τύπος αποδοχών');
CREATE TABLE IF NOT EXISTS apodoxestype (
id integer NOT NULL PRIMARY KEY,
sapodoxest varchar(20) NOT NULL UNIQUE);
INSERT INTO zfl VALUES('sapodoxest', 'Τύπος Αποδοχών');
INSERT INTO apodoxestype VALUES(1,'Μισθός');
INSERT INTO apodoxestype VALUES(2,'Ημερομίσθιο');
INSERT INTO apodoxestype VALUES(3,'Ωρομίσθιο');


INSERT INTO zt VALUES('apoxorisitype', 'Τύποι αποχώρησης');
INSERT INTO zfl VALUES('apoxorisitype_cd', 'Τύπος αποχώρησης');
CREATE TABLE IF NOT EXISTS apoxorisitype (
id integer NOT NULL PRIMARY KEY,
sapoxorisit varchar(50) NOT NULL UNIQUE
);
INSERT INTO zfl VALUES('sapoxorisit', 'Τύπος Αποχώρησης');
INSERT INTO apoxorisitype VALUES(1,'Απόλυση χωρίς προειδοποίηση');
INSERT INTO apoxorisitype VALUES(2,'Απόλυση με προειδοποίηση');
INSERT INTO apoxorisitype VALUES(3,'Οικιοθελής αποχώρηση');
INSERT INTO apoxorisitype VALUES(4,'Αποχώρηση λόγω λήξης σύμβασης ορισμένου χρόνου');
INSERT INTO apoxorisitype VALUES(5,'Αποχώρηση λόγω λήξης σύμβασης έργου');
INSERT INTO apoxorisitype VALUES(6,'Συνταξιοδότηση');


INSERT INTO zt VALUES('company', 'Στοιχεία εταιρίας');
INSERT INTO zfl VALUES('company_id', 'Στοιχεία εταιρίας');
CREATE TABLE IF NOT EXISTS company (
id integer NOT NULL PRIMARY KEY,
skey varchar(50) NOT NULL,
sval varchar(100) NOT NULL
);
INSERT INTO zfl VALUES('skey', 'Κλειδί');
INSERT INTO zfl VALUES('sval', 'Τιμή');
INSERT INTO company VALUES(1,'afm','');
INSERT INTO company VALUES(2,'eponymia','');


INSERT INTO zt VALUES('eidikotita', 'Ειδικότητες');
INSERT INTO zfl VALUES('eidikotita_id', 'Ειδικότητα');
CREATE TABLE IF NOT EXISTS eidikotita (
id integer NOT NULL PRIMARY KEY,
seidikotitap varchar(50) NOT NULL UNIQUE,
qeidika varchar(6) NOT NULL
);
INSERT INTO zfl VALUES('seidikotitap', 'Περιγραφή ειδικότητας');
INSERT INTO zfl VALUES('qeidika', 'Κωδικός ειδικότητας ΙΚΑ');


INSERT INTO zt VALUES('ergazomenos', 'Εργαζόμενοι');
INSERT INTO zfl VALUES('ergazomenos_id', 'Εργαζόμενος');
CREATE TABLE IF NOT EXISTS ergazomenos (
id INTEGER NOT NULL PRIMARY KEY,
seponymo VARCHAR(50) NOT NULL,
sonoma VARCHAR(50) NOT NULL,
spateras VARCHAR(50) NOT NULL,
smitera VARCHAR(50) NOT NULL,
sex_cd INTEGER NOT NULL REFERENCES sex(id),
dbirthdate DATE NOT NULL,
oikogkat_cd INTEGER NOT NULL REFERENCES oikogkat(id),
qafm VARCHAR(9) NOT NULL UNIQUE,
qmika VARCHAR(10) NOT NULL UNIQUE,
qamka VARCHAR(11) NOT NULL UNIQUE,
xora_cd INTEGER NOT NULL REFERENCES xora(id),
taftotitatype_cd INTEGER NOT NULL REFERENCES taftotitatype(id),
staftotita VARCHAR(20) NOT NULL,
ipaidia INTEGER NOT NULL DEFAULT 0,
sadress VARCHAR(60) NOT NULL,
qmobile VARCHAR(10) NOT NULL);
INSERT INTO zfl VALUES('seponymo', 'Επώνυμο');
INSERT INTO zfl VALUES('sonoma', 'Όνομα');
INSERT INTO zfl VALUES('spateras', 'Όνομα πατέρα');
INSERT INTO zfl VALUES('smitera', 'Όνομα μητέρας');
INSERT INTO zfl VALUES('dbirthdate', 'Ημ/νία γέννησης');
INSERT INTO zfl VALUES('qafm', 'ΑΦΜ');
INSERT INTO zfl VALUES('qmika', 'Αρ.Μητρώου ΙΚΑ');
INSERT INTO zfl VALUES('qamka', 'ΑΜΚΑ');
INSERT INTO zfl VALUES('staftotita', 'Αριθμός ταυτότητας');
INSERT INTO zfl VALUES('ipaidia', 'Παιδιά');
INSERT INTO zfl VALUES('sadress', 'Διεύθυνση');
INSERT INTO zfl VALUES('qmobile', 'Κινητό');
create VIEW ergazomenos_rpr as select id, seponymo || ' ' || sonoma as rpr from ergazomenos;

INSERT INTO zt VALUES('ergazomenostype', 'Τύποι εργαζομένων');
INSERT INTO zfl VALUES('ergazomenostype_cd', 'Τύπος εργαζομένου');
CREATE TABLE IF NOT EXISTS ergazomenostype (
id integer NOT NULL PRIMARY KEY,
sergazomenost varchar(12) NOT NULL UNIQUE
);
INSERT INTO zfl VALUES('sergazomenost', 'Τύπος Eργαζομένου');
INSERT INTO ergazomenostype VALUES(1,'Εργάτης');
INSERT INTO ergazomenostype VALUES(2,'Υπάλληλος');


INSERT INTO zt VALUES('imtype', 'Ημερολόγια');
INSERT INTO zfl VALUES('imtype_cd', 'ημερολόγιο');
CREATE TABLE IF NOT EXISTS imtype (
id integer NOT NULL PRIMARY KEY,
simtype varchar(30) NOT NULL);
INSERT INTO zfl VALUES('simtype', 'Ημερολόγιο');
INSERT INTO imtype VALUES(1,'Ανοίγματος χρήσης');
INSERT INTO imtype VALUES(2,'Γενικό ημερολόγιο');
INSERT INTO imtype VALUES(3,'Απογραφών/Ισολογισμών');


INSERT INTO zt VALUES('logariasmo', 'Λογαριασμοί');
INSERT INTO zfl VALUES('logariasmo_id', 'Λογαριασμός');
CREATE TABLE IF NOT EXISTS logariasmo (
id integer NOT NULL PRIMARY KEY,
slcod varchar(20) NOT NULL,
slper varchar(80) NOT NULL
);
INSERT INTO zfl VALUES('slcod', 'Κωδικός Λ/μού');
INSERT INTO zfl VALUES('slper', 'Περιγραφή Λ/μού');


INSERT INTO zt VALUES('minas', 'Μήνες');
INSERT INTO zfl VALUES('minas_cd', 'Μήνας');
CREATE TABLE IF NOT EXISTS minas (
id integer NOT NULL PRIMARY KEY,
sminas varchar(15) NOT NULL UNIQUE
);
INSERT INTO zfl VALUES('sminas', 'μήνας');
INSERT INTO minas VALUES(1,'Ιανουάριος');
INSERT INTO minas VALUES(2,'Φεβρουάριος');
INSERT INTO minas VALUES(3,'Μάρτιος');
INSERT INTO minas VALUES(4,'Απρίλιος');
INSERT INTO minas VALUES(5,'Μάϊος');
INSERT INTO minas VALUES(6,'Ιούνιος');
INSERT INTO minas VALUES(7,'Ιούλιος');
INSERT INTO minas VALUES(8,'Αύγουστος');
INSERT INTO minas VALUES(9,'Σεπτέμβριος');
INSERT INTO minas VALUES(10,'Οκτώβριος');
INSERT INTO minas VALUES(11,'Νοέμβριος');
INSERT INTO minas VALUES(12,'Δεκέμβριος');


INSERT INTO zt VALUES('misthodosia', 'Μισθοδοσίες');
INSERT INTO zfl VALUES('misthodosia_id', 'Μισθοδοσία');
CREATE TABLE IF NOT EXISTS misthodosia (
id integer NOT NULL PRIMARY KEY,
xrisi_cd integer NOT NULL REFERENCES xrisi(id),
minas_cd integer NOT NULL REFERENCES minas(id),
misthodosiatype_cd integer NOT NULL REFERENCES misthodosiatype(id),
proslipsi_id integer NOT NULL REFERENCES proslipsi(id),
emapo DATE NOT NULL,
emeos varchar(10) NOT NULL,
imeresika integer NOT NULL DEFAULT 0, 
imeresargia integer NOT NULL DEFAULT 0,
ioresargia integer NOT NULL DEFAULT 0,
ioresnyχta integer NOT NULL DEFAULT 0,
iasthenial3 integer NOT NULL DEFAULT 0,
iastheniam3 integer NOT NULL DEFAULT 0,
napodoxesp decimal NOT NULL DEFAULT 0,
nepidomaika decimal NOT NULL DEFAULT 0,
npikaergazomenoy decimal NOT NULL DEFAULT 0,
npikaergodoti decimal NOT NULL DEFAULT 0,
npika decimal NOT NULL DEFAULT 0,
nikaergazomenoy decimal NOT NULL DEFAULT 0,
nikaergodoti decimal NOT NULL DEFAULT 0,
nika decimal NOT NULL DEFAULT 0,
nfmy decimal NOT NULL DEFAULT 0,
neea decimal NOT NULL DEFAULT 0,
npli decimal NOT NULL DEFAULT 0);
INSERT INTO zfl VALUES('emapo', 'Ημ/νία από');
INSERT INTO zfl VALUES('emeos', 'Ημ/νία έως');
INSERT INTO zfl VALUES('imeresika', 'Ημέρες');
INSERT INTO zfl VALUES('imeresargia', 'Αργίες');
INSERT INTO zfl VALUES('ioresargia', 'Ώρες αργίας');
INSERT INTO zfl VALUES('ioresnyχta', 'Νυχτερινές ώρες');
INSERT INTO zfl VALUES('iasthenial3', 'Μέρες ασθένειας <=3 ');
INSERT INTO zfl VALUES('iastheniam3', 'Μέρες ασθένειας > 3');
INSERT INTO zfl VALUES('napodoxesp', 'Αποδοχές περιόδου');
INSERT INTO zfl VALUES('nepidomaika', 'Επίδομα ΙΚΑ');
INSERT INTO zfl VALUES('npikaergazomenoy', 'Ποσοστό ΙΚΑ εργαζομένου');
INSERT INTO zfl VALUES('npikaergodoti', 'Ποσοστό ΙΚΑ εργοδότη');
INSERT INTO zfl VALUES('npika', 'Ποσοστό ΙΚΑ συνολικά');
INSERT INTO zfl VALUES('nikaergazomenoy', 'Κρατήσεις ΙΚΑ εργαζομένου');
INSERT INTO zfl VALUES('nikaergodoti', 'Κρατήσεις ΙΚΑ εργοδότη');
INSERT INTO zfl VALUES('nika', 'Κρατήσεις ΙΚΑ συνολικά');
INSERT INTO zfl VALUES('nfmy', 'ΦΜΥ');
INSERT INTO zfl VALUES('neea', 'Ειδ.επιδ.Αλλ.');
INSERT INTO zfl VALUES('npli', 'Πληρωτέο');


INSERT INTO zt VALUES('misthodosiatype', 'Τύποι μισθοδοσίας');
INSERT INTO zfl VALUES('misthodosiatype_cd', 'Τύπος μισθοδοσίας');
CREATE TABLE IF NOT EXISTS misthodosiatype (
id integer NOT NULL PRIMARY KEY,
smisthodosiat varchar(30) NOT NULL UNIQUE,
smisthodosiaika varchar(2) NOT NULL UNIQUE
);
INSERT INTO zfl VALUES('smisthodosiat', 'Τύπος Μισθοδοσίας');
INSERT INTO zfl VALUES('smisthodosiaika', 'Κωδικός ΙΚΑ μισθοδοσίας');
INSERT INTO misthodosiatype VALUES(1,'Τακτικές αποδοχές','01');
INSERT INTO misthodosiatype VALUES(3,'Δώρο Χριστουγέννων','03');
INSERT INTO misthodosiatype VALUES(4,'Δώρο Πάσχα','04');
INSERT INTO misthodosiatype VALUES(5,'Επίδομα Αδείας','05');
INSERT INTO misthodosiatype VALUES(6,'Επίδομα Ισολογισμού','06');
INSERT INTO misthodosiatype VALUES(8,'Αποδοχές Ασθενείας','08');
INSERT INTO misthodosiatype VALUES(9,'Αναδρομικές αποδοχές','09');
INSERT INTO misthodosiatype VALUES(10,'Bonus','10');
INSERT INTO misthodosiatype VALUES(11,'Υπερωρίες','11');
INSERT INTO misthodosiatype VALUES(14,'Λοιπές αποδοχές','14');
INSERT INTO misthodosiatype VALUES(99,'Αποζημίωση Απόλυσης','99');


INSERT INTO zt VALUES('oikogkat', 'Οικογενειακή Κατάσταση');
INSERT INTO zfl VALUES('oikogkat_cd', 'Οικογενειακή κατάσταση');
CREATE TABLE IF NOT EXISTS oikogkat (
id integer NOT NULL PRIMARY KEY,
soikogkat varchar(60) NOT NULL UNIQUE
);
INSERT INTO zfl VALUES('soikogkat', 'Οικογενειακή Kατάσταση');
INSERT INTO oikogkat VALUES(1,'Άγαμος');
INSERT INTO oikogkat VALUES(2,'Έγγαμος');


INSERT INTO zt VALUES('parartima', 'Παραρτήματα');
INSERT INTO zfl VALUES('parartima_cd', 'Παράρτημα');
CREATE TABLE IF NOT EXISTS parartima (
id integer NOT NULL PRIMARY KEY, 
spar varchar(50) NOT NULL UNIQUE,
qkad varchar(4) NOT NULL
);
INSERT INTO zfl VALUES('spar', 'παράρτημα');
INSERT INTO zfl VALUES('qkad', 'ΙΚΑ ΚΑΔ');
INSERT INTO parartima VALUES(1,'Κεντρικό','');


INSERT INTO zt VALUES('paroysiatype', 'Τύποι παρουσιών');
INSERT INTO zfl VALUES('paroysiatype_cd', 'Τύπος παρουσίας');
CREATE TABLE IF NOT EXISTS paroysiatype (
id integer NOT NULL PRIMARY KEY,
sparoysiat varchar(50) NOT NULL UNIQUE,
qparoysiaika varchar(2) NOT NULL UNIQUE
);
INSERT INTO zfl VALUES('sparoysiat', 'Τύπος Παρουσίας');
INSERT INTO zfl VALUES('qparoysiaika', 'Κωδικός ΙΚΑ παρουσίας');
INSERT INTO paroysiatype VALUES(1,'Τακτικές παρουσίες','01');
INSERT INTO paroysiatype VALUES(8,'Ασθένεια','08');
INSERT INTO paroysiatype VALUES(11,'Υπερωρίες','11');


INSERT INTO zt VALUES('paroysies', 'Παρουσίες');
INSERT INTO zfl VALUES('paroysies_id', 'Παρουσία');
CREATE TABLE IF NOT EXISTS paroysies (
id integer NOT NULL PRIMARY KEY,
xrisi_cd integer NOT NULL REFERENCES xrisi(id),
minas_cd integer NOT NULL REFERENCES minas(id));


INSERT INTO zt VALUES('paroysiesd', 'Παρουσίες αναλυτικά');
INSERT INTO zfl VALUES('paroysiesd_id', 'Παρουσία αναλυτικά');
CREATE TABLE IF NOT EXISTS paroysiesd(
id integer NOT NULL PRIMARY KEY,
paroysies_id integer NOT NULL REFERENCES paroysies(id),
proslipsi_id integer NOT NULL REFERENCES proslipsi(id),
paroysiatype_cd integer NOT NULL REFERENCES paroysiatype(id),
epapo date NOT NULL,
epeos date NOT NULL,
ipmeres integer NOT NULL DEFAULT 0,
ipmadeia integer NOT NULL,
ipmadeiaxorisapodoxes integer NOT NULL DEFAULT 0,
iporesnyxta integer NOT NULL DEFAULT 0,
ipmeresargia integer NOT NULL DEFAULT 0,
iporesargia integer NOT NULL DEFAULT 0,
ipmasthenial3 integer NOT NULL DEFAULT 0,
ipmastheniam3 integer NOT NULL DEFAULT 0,
ipmastheniaxorisapodoxes integer NOT NULL DEFAULT 0,
npepidomaika decimal NOT NULL DEFAULT 0,
iporesyperoria1 integer NOT NULL DEFAULT 0,
iopresyperoria2 integer NOT NULL DEFAULT 0);
INSERT INTO zfl VALUES('epapo', 'Περίοδος από');
INSERT INTO zfl VALUES('epeos', 'Περίοδος έως');
INSERT INTO zfl VALUES('ipmeres', 'Ημέρες εργασίας');
INSERT INTO zfl VALUES('ipmadeia', 'Ημέρες άδειας με αποδοχές');
INSERT INTO zfl VALUES('ipmadeiaxorisapodoxes', 'Ημέρες άδειας χωρίς αποδοχές');
INSERT INTO zfl VALUES('iporesnyxta', 'Ώρες νύχτα');
INSERT INTO zfl VALUES('ipmeresargia', 'Ημέρες αργίας');
INSERT INTO zfl VALUES('iporesargia', 'Ώρες Αργίας');
INSERT INTO zfl VALUES('ipmasthenial3', 'Ημέρες ασθένειας έως 3');
INSERT INTO zfl VALUES('ipmastheniam3', 'Ημέρες ασθένειας πάνω από 3');
INSERT INTO zfl VALUES('ipmastheniaxorisapodoxes', 'Ημέρες ασθένειας χωρίς αποδοχές');
INSERT INTO zfl VALUES('npepidomaika', 'Επίδομα ΙΚΑ ασθένειας');
INSERT INTO zfl VALUES('iporesyperoria1', 'Ώρες υπερωριών κλίμακας 1');
INSERT INTO zfl VALUES('iporesyperoria2', 'Ώρες υπερωριών κλίμακας 2');


INSERT INTO zt VALUES('proslipsi', 'Προσλήψεις');
INSERT INTO zfl VALUES('proslipsi_id', 'Πρόσληψη');
CREATE TABLE IF NOT EXISTS proslipsi (
id integer NOT NULL PRIMARY KEY,
dproslipsi date NOT NULL,
ergazomenos_id integer NOT NULL REFERENCES ergazomenos(id),
parartima_cd integer NOT NULL REFERENCES parartima(id),
apasxolisitype_cd integer NOT NULL REFERENCES apasxolisitype(id),
ergazomenostype_cd integer NOT NULL REFERENCES ergazomenostype(id),
symbasitype_cd integer NOT NULL REFERENCES symbasitype(id),
eidikotita_id integer NOT NULL REFERENCES eidikotita(id),
torario text NOT NULL,
wpdays TEXT NOT NULL,
apodoxestype_cd integer NOT NULL REFERENCES apodoxestype(id),
napodoxes decimal NOT NULL,
eapoxorisi date,
apoxorisitype_cd integer REFERENCES apoxorisitype(id));
INSERT INTO zfl VALUES('dproslipsi', 'Ημερομηνία πρόσληψης');
INSERT INTO zfl VALUES('torario', 'Ωράριο εργασίας');
INSERT INTO zfl VALUES('wdays', 'Ημέρες Εργασίας');
INSERT INTO zfl VALUES('napodoxes', 'Αποδοχές');
INSERT INTO zfl VALUES('eapoxorisi', 'Ημερομηνία αποχώρησης');


INSERT INTO zt VALUES('sex', 'Φύλα');
INSERT INTO zfl VALUES('sex_cd', 'Φύλο');
CREATE TABLE IF NOT EXISTS sex (
id integer NOT NULL PRIMARY KEY,
sex varchar(10) NOT NULL UNIQUE
);
INSERT INTO zfl VALUES('sex', 'φύλο');
INSERT INTO sex VALUES(1,'Άντρας');
INSERT INTO sex VALUES(2,'Γυναίκα');


INSERT INTO zt VALUES('symbasitype', 'Τύποι σύμβασης');
INSERT INTO zfl VALUES('symbasitype_cd', 'Τύπος σύμβασης');
CREATE TABLE IF NOT EXISTS symbasitype (
id integer NOT NULL PRIMARY KEY,
syt varchar(30) NOT NULL UNIQUE);
INSERT INTO zfl VALUES('syt', 'Τύπος Σύμβασης');
INSERT INTO symbasitype VALUES(1,'Αορίστου χρόνου');
INSERT INTO symbasitype VALUES(2,'Ορισμένου χρόνου');
INSERT INTO symbasitype VALUES(3,'Έργου');


INSERT INTO zt VALUES('taftotitatype', 'Τύποι ταυτότητας');
INSERT INTO zfl VALUES('taftotitatype_cd', 'Τύπος ταυτότητας');
CREATE TABLE IF NOT EXISTS taftotitatype (
id integer NOT NULL PRIMARY KEY,
stat varchar(60) NOT NULL UNIQUE);
INSERT INTO zfl VALUES('stat', 'Τύπος Tαυτότητας');
INSERT INTO taftotitatype VALUES(1,'ΔΕΛΤΙΟ ΑΣΤΥΝΟΜΙΚΗΣ ΤΑΥΤΟΤΗΤΑΣ');
INSERT INTO taftotitatype VALUES(2,'ΔΙΑΒΑΤΗΡΙΟ');


INSERT INTO zt VALUES('tran', 'Λογιστικά άρθρα');
INSERT INTO zfl VALUES('tran_id', 'Λογιστικό άρθρο');
CREATE TABLE IF NOT EXISTS tran (
id integer NOT NULL PRIMARY KEY,
imtype_cd integer NOT NULL REFERENCES imtype(id),
dtrdate date NOT NULL,
strpar varchar(20) NOT NULL,
strper varchar(50) NOT NULL);
INSERT INTO zfl VALUES('dtrdate', 'Ημερομηνία εγγραφής');
INSERT INTO zfl VALUES('strpar', 'Παραστατικό');
INSERT INTO zfl VALUES('strper', 'Περιγραφή άρθρου');


INSERT INTO zt VALUES('trand', 'Λογιστικές εγγραφές');
INSERT INTO zfl VALUES('trand_id', 'Λογιστική εγγραφή');
CREATE TABLE IF NOT EXISTS trand (
id integer NOT NULL PRIMARY KEY,
tran_id integer NOT NULL REFERENCES trantype (id),
logariasmo_id integer NOT NULL REFERENCES logariasmo(id),
trantype_cd integer NOT NULL REFERENCES trantype (id),
strdper varchar(80) NOT NULL,
nval decimal NOT NULL DEFAULT 0
);
INSERT INTO zfl VALUES('strdper', 'Περιγραφή εγγραφής');
INSERT INTO zfl VALUES('nval', 'Ποσό εγγραφής');


INSERT INTO zt VALUES('trantype', 'Τύποι εγγραφής');
INSERT INTO zfl VALUES('trantype_cd', 'Τύπος εγγραφής');
CREATE TABLE IF NOT EXISTS trantype (
id integer NOT NULL PRIMARY KEY,
strantype varchar(30) NOT NULL
);
INSERT INTO zfl VALUES('strantype', 'Τύπος Εγγραφής');
INSERT INTO trantype VALUES(1,'Χρέωση');
INSERT INTO trantype VALUES(2,'Πίστωση');


INSERT INTO zt VALUES('xora', 'Χώρες');
INSERT INTO zfl VALUES('xora_cd', 'Χώρα');
CREATE TABLE IF NOT EXISTS xora (
id integer NOT NULL PRIMARY KEY,
sxora varchar(80) NOT NULL UNIQUE);
INSERT INTO zfl VALUES('sxora', 'χώρα');
INSERT INTO xora VALUES(1,'Ελλάδα');
INSERT INTO xora VALUES(2,'Γαλλία');


INSERT INTO zt VALUES('xrisi', 'Χρήσεις');
INSERT INTO zfl VALUES('xrisi_cd', 'Χρήση');
CREATE TABLE IF NOT EXISTS xrisi (
id integer NOT NULL PRIMARY KEY,
sxrisi integer NOT NULL UNIQUE);
INSERT INTO zfl VALUES('sxrisi', 'xρήση');
INSERT INTO xrisi VALUES(1,2017);


COMMIT;
