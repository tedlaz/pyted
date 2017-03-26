BEGIN TRANSACTION;

PRAGMA user_version = 1001;
PRAGMA application_id = 123123123;
CREATE TABLE IF NOT EXISTS cat(
id INTEGER PRIMARY KEY,
cat TEXT NOT NULL UNIQUE,
ac TEXT NOT NULL,
syn INTEGER NOT NULL DEFAULT 1
);
INSERT INTO cat VALUES(7, 'Έσοδα', '30.00', 1);
INSERT INTO cat VALUES(26, 'Έξοδα', '50.00', -1);

CREATE TABLE IF NOT EXISTS typ(
id TEXT PRIMARY KEY,
typ TEXT NOT NULL UNIQUE,
syn INTEGER NOT NULL DEFAULT 1
);
INSERT INTO typ VALUES('normal', 'Κανονικό', 1);
INSERT INTO typ VALUES('credit', 'Πιστωτικό', -1);

CREATE TABLE IF NOT EXISTS ori(
id TEXT PRIMARY KEY,
ori TEXT NOT NULL UNIQUE,
ac TEXT NOT NULL
);
INSERT INTO ori VALUES('ell', 'Εσωτερικού', '0');
INSERT INTO ori VALUES('eur', 'Ενδοκοινοτικές', '1');
INSERT INTO ori VALUES('exo', 'Εξωτερικού', '2');

-- ΤΡΟΠΟΙ ΕΙΣΠΡΑΞΗΣ/ΠΛΗΡΩΜΗΣ
CREATE TABLE IF NOT EXISTS pli(
id INTEGER PRIMARY KEY,
pli TEXT NOT NULL UNIQUE
);
INSERT INTO pli VALUES(1, 'Πίστωση');
INSERT INTO pli VALUES(2, 'Μετρητά σε ταμείο');
INSERT INTO pli VALUES(3, 'Μετρητά σε τράπεζα');

--ΠΑΡΑΡΤΗΜΑΤΑ
CREATE TABLE IF NOT EXISTS par(
id INTEGER PRIMARY KEY,
par TEXT NOT NULL UNIQUE
);
INSERT INTO par VALUES(1, 'Κεντρικό');

--ΣΥΝΑΛΑΣΣΟΜΕΝΟΙ
CREATE TABLE IF NOT EXISTS syn(
id TEXT PRIMARY KEY, --ΕΔΩ ID ΕΙΝΑΙ ΤΟ ΑΦΜ
epo TEXT UNIQUE NOT NULL,
ep2 TEXT NOT NULL,
ccd TEXT,  --Κωδικός χώρας. Για την Ελλάδα είναι EL
adr TEXT,  --Διεύθυνση
vda DATE --VALIDATION DATE
);

--ΚΙΝΗΣΕΙΣ ΑΓΟΡΩΝ, ΕΞΟΔΩΝ , ΕΣΟΔΩΝ
CREATE TABLE IF NOT EXISTS ki(
id INTEGER PRIMARY KEY,
par_id INTEGER NOT NULL REFERENCES par(id), --ΠΑΡΑΡΤΗΜΑ
cat_id INTEGER NOT NULL REFERENCES cat(id), --ΕΣΟΔΑ/ΕΞΟΔΑ
typ_id TEXT NOT NULL REFERENCES typ(id) DEFAULT 'normal', --ΚΑΝΟΝΙΚΟ/ΠΙΣΤΩΤΙΚΟ
ori_id TEXT NOT NULL REFERENCES ori(id) DEFAULT 'ell', --ΕΣΩΤΕΡΙΚΟ/ΕΝΔΟΚΟΙΝΟΤΙΚΟ/ΕΞΩΤΕΡΙΚΟ
dat DATE NOT NULL, --ΗΜΕΡΟΜΗΝΙΑ ΕΓΓΡΑΦΗΣ
pno TEXT NOT NULL, --ΤΥΠΟΣ ΚΑΙ ΑΡΙΘΜΟΣ ΠΑΡΑΣΤΑΤΙΚΟΥ
afm TEXT NOT NULL, --ΑΡΙΘΜΟΣ ΦΟΡΟΛΟΓΙΚΟΥ ΜΗΤΡΩΟΥ
pli_id INTEGER NOT NULL REFERENCES pli(id), --ΤΡΟΠΟΣ ΠΛΗΡΩΜΗΣ
per TEXT,  --ΠΕΡΙΓΡΑΦΗ
UNIQUE (cat_id, typ_id, dat, afm, pno)
);
CREATE TABLE IF NOT EXISTS kid(
id INTEGER PRIMARY KEY,--
ki_id INTEGER NOT NULL REFERENCES ki(id),
lm_id TEXT NOT NULL REFERENCES lm(id),
pfpa DECIMAL NOT NULL DEFAULT 0, --ΠΟΣΟΣΤΟ ΦΠΑ
efpa INTEGER NOT NULL DEFAULT 1, --ΑΝ ΕΚΠΙΠΤΕΙ 1 ΔΙΑΦΟΡΕΤΙΚΑ 0
val DECIMAL NOT NULL DEFAULT 0, --ΑΞΙΑ
fpa DECIMAL NOT NULL DEFAULT 0, --ΦΠΑ
UNIQUE (ki_id, lm_id, pfpa)
);

--ΚΙΝΗΣΕΙΣ ΜΕΤΑΦΟΡΑΣ (ΠΛΗΡΩΜΕΣ ΚΛΠ)
CREATE TABLE IF NOT EXISTS kie(
id INTEGER PRIMARY KEY,
dat DATE NOT NULL,
pno TEXT NOT NULL,
eg_id INTEGER NOT NULL REFERENCES eg(id),
eg_id2 INTEGER NOT NULL REFERENCES eg(id),
val DECIMAL NOT NULL DEFAULT 0,
UNIQUE (dat, pno)
);

-- ΕΓΓΡΑΦΕΣ ΛΟΓΙΣΤΙΚΗΣ
CREATE TABLE IF NOT EXISTS lmo(
id TEXT PRIMARY KEY,
lmo TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tr(
id INTEGER PRIMARY KEY,
ki_id INTEGER REFERENCES ki(id), --Όταν έρχονται εγγραφές από το ki παίρνει τιμή
dat DATE NOT NULL, --ΗΜΕΡΟΜΗΝΙΑ
par TEXT NOT NULL, --ΑΡΙΘΜΟΣ ΠΑΡΑΣΤΑΤΙΚΟΥ
per TEXT NOT NULL   --ΣΧΟΛΙΑ ΕΓΓΡΑΦΗΣ
);

CREATE TABLE IF NOT EXISTS trd(
id INTEGER PRIMARY KEY,
tr_id INTEGER NOT NULL REFERENCES lg(id),
lmo_id INTEGER NOT NULL REFERENCES lmo(id), --ΑΡΙΘΜΟΣ ΛΟΓΑΡΙΑΣΜΟΥ
per2 TEXT, --ΠΕΡΙΓΡΑΦΗ ΕΓΓΡΑΦΗΣ
xr DECIMAL NOT NULL DEFAULT 0, --ΧΡΕΩΣΗ
pi DECIMAL NOT NULL DEFAULT 0  --ΠΙΣΤΩΣΗ
);

-- ΠΡΩΤΟΒΑΘΜΙΟΙ ΛΟΓΑΡΙΑΣΜΟΙ ΛΟΓΙΣΤΙΚΗΣ
CREATE TABLE IF NOT EXISTS lm(
id TEXT PRIMARY KEY,     --ΚΩΔΙΚΟΣ ΛΟΓΑΡΙΑΣΜΟΥ
lmp TEXT NOT NULL UNIQUE  --ΠΕΡΙΓΡΑΦΗ ΛΟΓΑΡΙΑΣΜΟΥ
);
INSERT INTO lm VALUES('10.00', 'Γήπεδα-Οικόπεδα');
INSERT INTO lm VALUES('10.01', 'Ορυχεία');
INSERT INTO lm VALUES('10.02', 'Μεταλλεία');
INSERT INTO lm VALUES('10.03', 'Λατομεία');
INSERT INTO lm VALUES('10.04', 'Αγροί');
INSERT INTO lm VALUES('10.05', 'Φυτείες');
INSERT INTO lm VALUES('10.06', 'Δάση');
INSERT INTO lm VALUES('10.99.01', 'Αποσβεσμένα Ορυχεία');
INSERT INTO lm VALUES('10.99.02', 'Αποσβεσμένα Μεταλλεία');
INSERT INTO lm VALUES('10.99.03', 'Αποσβεσμένα Λατομεία');
INSERT INTO lm VALUES('10.99.05', 'Αποσβεσμένες Φυτείες');
INSERT INTO lm VALUES('10.99.06', 'Αποσβεσμένα Δάση');
INSERT INTO lm VALUES('11.00', 'Κτίρια-Εγκαταστάσεις Κτιρίων');
INSERT INTO lm VALUES('11.01', 'Τεχνικά έργα εξυπηρετήσεως μεταφορών');
INSERT INTO lm VALUES('11.02', 'Λοιπά τεχνικά έργα');
INSERT INTO lm VALUES('11.03', 'Υποκείμενες σε απόσβεση διαμορφώσεις γηπέδων');
INSERT INTO lm VALUES('11.99.00', 'Αποσβεσμένα κτίρια-εγκαταστάσεις κτιρίων');
INSERT INTO lm VALUES('11.99.01', 'Αποσβεσμένα τεχνικά έργα εξυπηρετήσεως μεταφορών');
INSERT INTO lm VALUES('11.99.02', 'Αποσβεσμένα λοιπά τεχνικά έργα');
INSERT INTO lm VALUES('11.99.03', 'Αποσβεσμένες διαμορφώσεις γηπέδων');
INSERT INTO lm VALUES('12.00', 'Μηχανήματα');
INSERT INTO lm VALUES('12.01', 'Τεχνικές εγκαταστάσεις');
INSERT INTO lm VALUES('12.02', 'Φορητά μηχανήματα χειρός');
INSERT INTO lm VALUES('12.03', 'Εργαλεία');
INSERT INTO lm VALUES('12.04', 'Καλούπια-Ιδιοσυσκευές');
INSERT INTO lm VALUES('12.05', 'Μηχανολογικά όργανα');
INSERT INTO lm VALUES('12.06', 'Λοιπός μηχανολογικός εξοπλισμός');
INSERT INTO lm VALUES('12.07', 'Μηχανήματα σε ακίνητα τρίτων');
INSERT INTO lm VALUES('12.99.00', 'Αποσβεσμένα μηχανήματα');
INSERT INTO lm VALUES('12.99.01', 'Αποσβεσμένες τεχνικές εγκαταστάσεις');
INSERT INTO lm VALUES('12.99.02', 'Αποσβεσμένα φορητά μηχανήματα χειρός');
INSERT INTO lm VALUES('12.99.03', 'Αποσβεσμένα εργαλεία');
INSERT INTO lm VALUES('12.99.04', 'Αποσβεσμένα καλούπια-ιδιοσυσκευές');
INSERT INTO lm VALUES('12.99.05', 'Αποσβεσμένα μηχανολογικά όργανα');
INSERT INTO lm VALUES('12.99.06', 'Αποσβεσμένος λοιπός μηχανολογικός εξοπλισμός');
INSERT INTO lm VALUES('13.00', 'Αυτοκίνητα λεωφορεία');
INSERT INTO lm VALUES('13.01', 'Λοιπά επιβατικά αυτοκίνητα');
INSERT INTO lm VALUES('13.02', 'Αυτοκίνητα φορτηγά - Ρυμούλκες - Ειδικής Χρήσεως');
INSERT INTO lm VALUES('13.03', 'Σιδηροδρομικά οχήματα');
INSERT INTO lm VALUES('13.04', 'Πλωτά μέσα');
INSERT INTO lm VALUES('13.05', 'Εναέρια μέσα');
INSERT INTO lm VALUES('13.06', 'Μέσα εσωτερικών μεταφορών');
INSERT INTO lm VALUES('13.09', 'Λοιπά μέσα μεταφοράς');
INSERT INTO lm VALUES('13.99.00', 'Αποσβεσμένα αυτοκίνητα λεωφορεία');
INSERT INTO lm VALUES('13.99.01', 'Αποσβεσμένα λοιπά επιβατικά αυτοκίνητα');
INSERT INTO lm VALUES('13.99.02', 'Αποσβεσμένα φορτηγά - Ρυμούλκες - Ειδικής χρήσεως');
INSERT INTO lm VALUES('13.99.03', 'Αποσβεσμένα σιδηροδρομικά οχήματα');
INSERT INTO lm VALUES('13.99.04', 'Αποσβεσμένα πλωτά μέσα');
INSERT INTO lm VALUES('13.99.05', 'Αποσβεσμένα εναέρια μέσα');
INSERT INTO lm VALUES('13.99.06', 'Αποσβεσμένα μέσα εσωτερικών μεταφορών');
INSERT INTO lm VALUES('13.99.09', 'Αποσβεσμένα λοιπά μέσα μεταφοράς');
INSERT INTO lm VALUES('14.00', 'Έπιπλα');
INSERT INTO lm VALUES('14.01', 'Σκεύη');
INSERT INTO lm VALUES('14.02', 'Μηχανές γραφείων');
INSERT INTO lm VALUES('14.03', 'Ηλεκτρονικοί υπολογιστές');
INSERT INTO lm VALUES('14.04', 'Μέσα αποθηκεύσεως και μεταφοράς');
INSERT INTO lm VALUES('14.05', 'Επιστημονικά όργανα');
INSERT INTO lm VALUES('14.06', 'Ζώα για πάγια εκμετάλλευση');
INSERT INTO lm VALUES('14.08', 'Εξοπλισμός τηλεπικοινωνιών');
INSERT INTO lm VALUES('14.09', 'Λοιπός εξοπλισμός');
INSERT INTO lm VALUES('14.99.00', 'Αποσβεσμένα έπιπλα');
INSERT INTO lm VALUES('14.99.01', 'Αποσβεσμένα σκεύη');
INSERT INTO lm VALUES('14.99.02', 'Αποσβεσμένες μηχανές γραφείων');
INSERT INTO lm VALUES('14.99.03', 'Αποσβεσμένοι ηλεκτρονικοί υπολογιστές');
INSERT INTO lm VALUES('14.99.04', 'Αποσβεσμένα μέσα αποθηκεύσεως και μεταφοράς');
INSERT INTO lm VALUES('14.99.05', 'Αποσβεσμένα επιστημονικά όργανα');
INSERT INTO lm VALUES('14.99.06', 'Αποσβεσμένα ζώα για πάγια εκμετάλλευση');
INSERT INTO lm VALUES('14.99.08', 'Αποσβεσμένος εξοπλισμός τηλεπικοινωνιών');
INSERT INTO lm VALUES('14.99.09', 'Αποσβεσμένος λοιπός εξοπλισμός');
INSERT INTO lm VALUES('15.01', 'Κτίρια-Εγκ/σεις κτιρίων-Τεχνικά έργα υπό εκτέλεση');
INSERT INTO lm VALUES('15.02', 'Μηχ/τα-Τεχν.εγκ/σεις-Λοιπός μηχ.εξοπλ. υπό εκτέλεση');
INSERT INTO lm VALUES('15.03', 'Μεταφορικά μέσα υπό εκτέλεση');
INSERT INTO lm VALUES('15.04', 'Έπιπλα και λοιπός εξοπλισμός υπό εκτέλεση');
INSERT INTO lm VALUES('15.09', 'Προκαταβολές κτήσεως πάγιων στοιχείων');
INSERT INTO lm VALUES('16.00', 'Υπεραξία επιχειρήσεως (Goodwill)');
INSERT INTO lm VALUES('16.01', 'Δικαιώματα βιομηχανικής ιδιοκτησίας');
INSERT INTO lm VALUES('16.01.00', 'Διπλώματα ευρεσιτεχνίας');
INSERT INTO lm VALUES('16.01.01', 'Άδειες παραγωγής και εκμετάλλευσης (Licences)');
INSERT INTO lm VALUES('16.01.02', 'Σήματα');
INSERT INTO lm VALUES('16.01.03', 'Μέθοδοι (Know How)');
INSERT INTO lm VALUES('16.01.04', 'Πρότυπα');
INSERT INTO lm VALUES('16.01.05', 'Σχέδια');
INSERT INTO lm VALUES('16.02', 'Δικαιώματα εκμ/σης ορυχείων-μεταλλείων-λατομείων');
INSERT INTO lm VALUES('16.03', 'Λοιπές παραχωρήσεις');
INSERT INTO lm VALUES('16.04', 'Δικαιώματα χρήσεως ενσώματων πάγιων στοιχείων');
INSERT INTO lm VALUES('16.05', 'Λοιπά δικαιώματα');
INSERT INTO lm VALUES('16.10', 'Έξοδα ιδρύσεως και πρώτης εγκαταστάσεως');
INSERT INTO lm VALUES('16.11', 'Έξοδα ερευνών ορυχείων - μεταλλείων - λατομείων');
INSERT INTO lm VALUES('16.12', 'Έξοδα λοιπών ερευνών');
INSERT INTO lm VALUES('16.13', 'Έξοδα αυξήσεως κεφαλαίου και εκδόσεως ομολογιακών δανείων');
INSERT INTO lm VALUES('16.14', 'Έξοδα κτήσεως ακινητοποιήσεων');
INSERT INTO lm VALUES('16.15', 'Συν/κές διαφορές από πιστώσεις και δάνεια για κτήσεις πάγιων στοιχείων');
INSERT INTO lm VALUES('16.16', 'Διαφορές εκδόσεως και εξοφλήσεως ομολογιών');
INSERT INTO lm VALUES('16.17.00', 'Λογισμικά προγράμματα Η/Υ');
INSERT INTO lm VALUES('16.18', 'Τόκοι δανείων κατασκευαστικής περιόδου');
INSERT INTO lm VALUES('16.19', 'Λοιπά έξοδα πολυετούς αποσβέσεως');
INSERT INTO lm VALUES('16.90', 'Έξοδα μετεγκαταστάσεως της επιχειρήσεως');
INSERT INTO lm VALUES('16.98', 'Προκαταβολές κτήσεως ασώματων ακινητοποιήσεων');
INSERT INTO lm VALUES('16.99.00', 'Αποσβεσμένη υπεραξία επιχειρήσεως');
INSERT INTO lm VALUES('16.99.01', 'Αποσβεσμένα δικαιώματα βιομηχανικής ιδιοκτησίας');
INSERT INTO lm VALUES('16.99.02', 'Αποσβεσμένα δικαιώματα εκμ/σης ορυχείων-μεταλλείων-λατομείων');
INSERT INTO lm VALUES('16.99.03', 'Αποσβεσμένες λοιπές παραχωρήσεις');
INSERT INTO lm VALUES('16.99.04', 'Αποσβεσμένα δικαιώματα χρήσεως ενσώματων πάγιων στοιχείων');
INSERT INTO lm VALUES('16.99.05', 'Αποσβεσμένα λοιπά δικαιώματα');
INSERT INTO lm VALUES('16.99.10', 'Αποσβεσμένα έξοδα ιδρύσεως και πρώτης εγκαταστάσεως');
INSERT INTO lm VALUES('16.99.11', 'Αποσβεσμένα έξοδα ερευνών ορυχείων - μεταλλείων - λατομείων');
INSERT INTO lm VALUES('16.99.12', 'Αποσβεσμένα έξοδα λοιπών ερευνών');
INSERT INTO lm VALUES('16.99.13', 'Αποσβεσμένα έξοδα αυξήσεως κεφαλαίου και εκδόσεως ομολογιακών δανείων');
INSERT INTO lm VALUES('16.99.14', 'Αποσβεσμένα έξοδα κτήσεως ακινητοποιήσεων');
INSERT INTO lm VALUES('16.99.16', 'Αποσβεσμένες διαφορές εκδόσεως και εξοφλήσεως ομολογιών');
INSERT INTO lm VALUES('16.99.17', 'Αποσβεσμένα έξοδα αναδιοργανώσεως');
INSERT INTO lm VALUES('16.99.18', 'Αποσβεσμένοι τόκοι δανείων κατασκευαστικής περιόδου');
INSERT INTO lm VALUES('16.99.19', 'Αποσβεσμένα λοιπά έξοδα πολυετούς αποσβέσεως');
INSERT INTO lm VALUES('16.99.90', 'Αποσβεσμένα έξοδα μετεγκατεστάσεως της επιχειρήσεως');
INSERT INTO lm VALUES('18.00', 'Συμμετοχές σε συνδεμένες επιχειρήσεις');
INSERT INTO lm VALUES('18.01', 'Συμμετοχές σε λοιπές επιχειρήσεις');
INSERT INTO lm VALUES('18.02', 'Μακροπρόθεσμες απαιτήσεις κατά συνδεμένων επιχειρήσεων');
INSERT INTO lm VALUES('18.03', 'Μακροπρόθεσμες απαιτήσεις κατά συνδεμένων επιχειρήσεων σε Ξ.Ν.');
INSERT INTO lm VALUES('18.04', 'Μακροπρόθεσμες απαιτήσεις κατά λοιπών συμμετοχικού ενδιαφέροντος επιχειρήσεων');
INSERT INTO lm VALUES('18.05', 'Μακροπρόθεσμες απαιτήσεις κατά λοιπών συμμετοχικού ενδιαφέροντος επιχειρήσεων σε ΞΝ');
INSERT INTO lm VALUES('18.06', 'Μακροπρόθεσμες απαιτήσεις κατά εταίρων');
INSERT INTO lm VALUES('18.07', 'Γραμμάτια Εισπρακτέα μακροπρόθεσμα');
INSERT INTO lm VALUES('18.08', 'Γραμμάτια Εισπρακτέα μακροπρόθεσμα σε Ξ.Ν.');
INSERT INTO lm VALUES('18.09', 'Μη δουλευμένοι τόκοι γραμματίων εισπρακτέων μακροπρόθεσμων');
INSERT INTO lm VALUES('18.10', 'Μη δουλευμένοι τόκοι γραμματίων εισπρακτέων μακροπρόθεσμων σε Ξ.Ν.');
INSERT INTO lm VALUES('18.11', 'Δοσμένες εγγυήσεις');
INSERT INTO lm VALUES('18.12', 'Οφειλόμενο κεφάλαιο');
INSERT INTO lm VALUES('18.13', 'Λοιπές μακροπρόθεσμες απαιτήσεις');
INSERT INTO lm VALUES('18.14', 'Λοιπές μακροπρόθεσμες απαιτήσεις σε Ξ.Ν.');
INSERT INTO lm VALUES('18.15', 'Τίτλοι με χαρακτήρα ακινητοποιήσεων');
INSERT INTO lm VALUES('18.16', 'Τίτλοι με χαρακτήρα ακινητοποιήσεων σε Ξ.Ν.');
INSERT INTO lm VALUES('20.00', 'Απογραφή Εμπορευμάτων');
INSERT INTO lm VALUES('20.01', 'Αγορές εμπορευμάτων');
INSERT INTO lm VALUES('21', 'Προϊόντα έτοιμα & ημιτελή');
INSERT INTO lm VALUES('22', 'Υποπροϊόντα & υπολείμματα');
INSERT INTO lm VALUES('23', 'Παραγωγή σε εξέλιξη');
INSERT INTO lm VALUES('24.00', 'Απογραφή Α & Β Ύλες - Υλικά συσκευασίας');
INSERT INTO lm VALUES('24.01', 'Αγορές Α & Β Ύλες - Υλικά συσκ.');
INSERT INTO lm VALUES('25.00', 'Απογραφή Αναλώσιμα υλικά');
INSERT INTO lm VALUES('25.01', 'Αγορές αναλωσίμων');
INSERT INTO lm VALUES('26.00', 'Απογραφή Ανταλλακτικά παγίων');
INSERT INTO lm VALUES('26.01', 'Αγορές Ανταλλακτικών παγίων');
INSERT INTO lm VALUES('28.00', 'Απογραφή Είδη συσκευασίας');
INSERT INTO lm VALUES('28.01', 'Αγορές Ειδών συσκευασίας');
INSERT INTO lm VALUES('29', 'Αποθέματα υποκαταστημάτων');
INSERT INTO lm VALUES('30', 'Πελάτες');
INSERT INTO lm VALUES('31', 'Γραμμάτια εισπρακτέα');
INSERT INTO lm VALUES('32', 'Παραγγελίες στο εξωτερικό');
INSERT INTO lm VALUES('33', 'Χρεώστες διάφοροι');
INSERT INTO lm VALUES('34', 'Χρεώγραφα');
INSERT INTO lm VALUES('35', 'Λ/μοι διαχ.προκαταβολών');
INSERT INTO lm VALUES('36', 'ΜΕταβατικοί λ/μοι ενεργητικού');
INSERT INTO lm VALUES('38', 'Χρηματικά διαθέσιμα');
INSERT INTO lm VALUES('39', 'Απαιτήσεις & διαθ. υπ/των');
INSERT INTO lm VALUES('40', 'Κεφάλαιο');
INSERT INTO lm VALUES('41', 'Αποθεματικά-Διαφ.Αναπρ.-Επιχορηγ.');
INSERT INTO lm VALUES('42', 'Αποτελέσματα σε νέο');
INSERT INTO lm VALUES('43', 'Ποσά για αύξηση κεφαλαίου');
INSERT INTO lm VALUES('44', 'Προβλέψεις');
INSERT INTO lm VALUES('45', 'Μακροπρόθεσμες υποχρεώσεις');
INSERT INTO lm VALUES('50', 'Προμηθευτές');
INSERT INTO lm VALUES('51', 'Γραμμάτια πληρωτέα');
INSERT INTO lm VALUES('52', 'Τράπεζες');
INSERT INTO lm VALUES('53', 'Πιστωτές διάφοροι');
INSERT INTO lm VALUES('54', 'Υποχρεώσεις από φόρους-τέλη');
INSERT INTO lm VALUES('54.00', 'Φόρος Προστιθέμενης Αξίας');
INSERT INTO lm VALUES('55', 'Ασφαλιστικοί οργανισμοί');
INSERT INTO lm VALUES('55.00', 'ΙΚΑ');
INSERT INTO lm VALUES('56', 'Μεταβατικοί λ/μοί παθητικού');
INSERT INTO lm VALUES('60.00', 'Αμοιβές έμμισθου προσωπικού');
INSERT INTO lm VALUES('60.01', 'Αμοιβές ημερομίσθιου προσωπικού');
INSERT INTO lm VALUES('60.02', 'Παρεπόμενες αποδοχές & εξ. προσωπικού');
INSERT INTO lm VALUES('60.03', 'Εργοδοτικές εισφορές μισθωτών');
INSERT INTO lm VALUES('60.04', 'Εργοδοτικές εισφορές ημερομισθίων');
INSERT INTO lm VALUES('60.05', 'Αποζημιώσεις απόλυσης ή εξόδου');
INSERT INTO lm VALUES('61', 'Αμοιβές & έξοδα τρίτων');
INSERT INTO lm VALUES('61.ΟΟ', 'Αμοιβές & έξοδα τρίτων με παρ.φόρου');
INSERT INTO lm VALUES('62.00', 'Ηλεκτρικό ρεύμα παραγωγής');
INSERT INTO lm VALUES('62.01', 'Φωταέριο παραγωγής');
INSERT INTO lm VALUES('62.02', 'Ύδρευση παραγωγής');
INSERT INTO lm VALUES('62.03.00', 'Τηλεφωνικά');
INSERT INTO lm VALUES('62.03.02', 'Ταχυδρομικά');
INSERT INTO lm VALUES('62.04.00', 'Ενοίκια εδαφικών εκτάσεων');
INSERT INTO lm VALUES('62.04.01', 'Ενοίκια κτιρίων-τεχνικών έργων');
INSERT INTO lm VALUES('62.04.02', 'Ενοίκια Μηχ/των-Τεχ.Εγκ.-Λοιπού μηχ.εξ.');
INSERT INTO lm VALUES('62.04.03', 'Ενοίκια μεταφορικών μέσων');
INSERT INTO lm VALUES('62.04.04', 'Ενοίκια επίπλων');
INSERT INTO lm VALUES('62.04.05', 'Ενοίκια μηχανογραφικών μέσων');
INSERT INTO lm VALUES('62.04.06', 'Ενοίκια λοιπού εξοπλισμού');
INSERT INTO lm VALUES('62.04.07', 'Ενοίκια φωτοαντιγραφικών μέσων');
INSERT INTO lm VALUES('62.04.08', 'Ενοίκια φωτεινών επιγραφών');
INSERT INTO lm VALUES('62.04.10', 'Ενοίκια χρονομεριστικής μίσθωσης');
INSERT INTO lm VALUES('62.05.00', 'Ασφάλιστρα πυρός');
INSERT INTO lm VALUES('62.05.01', 'Ασφάλιστρα μεταφορικών μέσων');
INSERT INTO lm VALUES('62.05.02', 'Ασφάλιστρα μεταφορών');
INSERT INTO lm VALUES('62.05.03', 'Ασφάλιστρα πιστώσεων');
INSERT INTO lm VALUES('62.06', 'Αποθήκευτρα');
INSERT INTO lm VALUES('62.07.00', 'Επισκ.& συντ.Εδαφικών εκτάσεων');
INSERT INTO lm VALUES('62.07.01', 'Επισκ.& συντ.Κτιρίων-εγκ.-τεχ.εργ.');
INSERT INTO lm VALUES('62.07.02', 'Επισκ.& συντ.Μηχ/των-τεχ.εγκ.-λοιπού μηχ.εξ.');
INSERT INTO lm VALUES('62.07.03', 'Επισκ.& συντ.Μεταφορικών μέσων');
INSERT INTO lm VALUES('62.07.04', 'Επισκ.& συντ.Επίπλων & λοιπού εξοπλ.');
INSERT INTO lm VALUES('62.07.05', 'Επισκ.& συντ.Εμπορευμάτων');
INSERT INTO lm VALUES('62.07.06', 'Επισκ.& συντ.Έτοιμων προϊόντων');
INSERT INTO lm VALUES('62.07.07', 'Επισκ.& συντ.Λοιπών υλικών αγαθών');
INSERT INTO lm VALUES('62.98.00', 'Φωτισμός');
INSERT INTO lm VALUES('62.98.01', 'Φωταέριο');
INSERT INTO lm VALUES('62.98.02', 'Ύδρευση');
INSERT INTO lm VALUES('62.98.03', 'Έξοδα ξενοδοχείων για εξυπηρέτηση πελατών');
INSERT INTO lm VALUES('63.00', 'Φόρος εισοδήματος μη συμψηφιζόμενος');
INSERT INTO lm VALUES('63.01.01', 'Εισφορά ΟΓΑ χαρτοσήμου');
INSERT INTO lm VALUES('63.02.00', 'Χαρτόσημα συναλλαγματικών & αποδείξεων');
INSERT INTO lm VALUES('63.02.01', 'Χαρτόσημα λοιπών πράξεων');
INSERT INTO lm VALUES('63.03.00', 'Φόροι-Τέλη κυκλ.Επιβατικών αυτοκινήτων');
INSERT INTO lm VALUES('63.03.01', 'Φόροι-Τέλη κυκλ.Φορτηγών αυτοκινήτων');
INSERT INTO lm VALUES('63.03.02', 'Φόροι-Τέλη κυκλ.Σιδηροδρομικών οχημάτων');
INSERT INTO lm VALUES('63.03.03', 'Φόροι-Τέλη κυκλ.Πλωτών μέσων');
INSERT INTO lm VALUES('63.03.04', 'Φόροι-Τέλη κυκλ.Εναέριων μέσων');
INSERT INTO lm VALUES('63.04.00', 'Τέλη καθαριότητας & φωτισμού');
INSERT INTO lm VALUES('63.04.01', 'Φόροι & Τέλη ανεγειρομένων ακινήτων');
INSERT INTO lm VALUES('63.04.03', 'Τέλη ακίνητης περιουσίας');
INSERT INTO lm VALUES('63.05', 'Φόροι-Τέλη προβλεπόμενοι από διεθνείς οργανισμούς');
INSERT INTO lm VALUES('63.06', 'Λοιποί Φόροι-Τέλη εξωτερικού');
INSERT INTO lm VALUES('63.90', 'Τέλη υπέρ τρίτων επί κατασκευαζόμενων τεχν.έργων');
INSERT INTO lm VALUES('63.98.00', 'Χαρτόσημο μισθωμάτων');
INSERT INTO lm VALUES('64.00.00', 'Έξοδα κινήσεως ιδιόκτητων μετ.μέσων');
INSERT INTO lm VALUES('64.00.01', 'Έξ.μεταφοράς προσωπικού με μετ.μέσα τρίτων');
INSERT INTO lm VALUES('64.00.02', 'Έξ.μεταφοράς αγορών με μετ.μέσα τρίτων');
INSERT INTO lm VALUES('64.00.03', 'Έξ.μεταφοράς πωλήσεων με μετ.μέσα τρίτων');
INSERT INTO lm VALUES('64.00.04', 'Έξ.διακινήσεων με μετ.μέσα τρίτων');
INSERT INTO lm VALUES('64.01', 'Έξοδα ταξειδίων');
INSERT INTO lm VALUES('64.02.00', 'Διαφημίσεις από τον τύπο');
INSERT INTO lm VALUES('64.02.01', 'Διαφημίσεις από το ραδιόφωνο - τηλεόραση');
INSERT INTO lm VALUES('64.02.02', 'Διαφημίσεις από τον κινηματογράφο');
INSERT INTO lm VALUES('64.02.03', 'Διαφημίσεις από τα λοιπά μέσα ενημερώσεως');
INSERT INTO lm VALUES('64.02.04', 'Έξοδα λειτουργίας φωτεινών επιγραφών');
INSERT INTO lm VALUES('64.02.05', 'Έξοδα συνεδρίων - δεξιώσεων');
INSERT INTO lm VALUES('64.02.06', 'Έξοδα υποδοχής και φιλοξενείας');
INSERT INTO lm VALUES('64.02.07', 'Έξοδα προβολής δια λοιπών μεθόδων');
INSERT INTO lm VALUES('64.02.08', 'Έξοδα λόγω εγγυήσεως πωλήσεων');
INSERT INTO lm VALUES('64.02.09', 'Έξοδα αποστολής δειγμάτων');
INSERT INTO lm VALUES('64.02.10', 'Αξία χορηγούμενων δειγμάτων');
INSERT INTO lm VALUES('64.02.99', 'Διάφορα έξοδα προβολής και διαφημίσεως');
INSERT INTO lm VALUES('64.03', 'Έξοδα εκθέσεων - επιδείξεων');
INSERT INTO lm VALUES('64.04', 'Ειδικά έξοδα προώθησης εξαγωγών');
INSERT INTO lm VALUES('64.05.00', 'Συνδρομές σε περιοδικά και εφημερίδες');
INSERT INTO lm VALUES('64.05.01', 'Συνδρομές-Εισφορές σε επαγγελματικές οργανώσεις');
INSERT INTO lm VALUES('64.06', 'Δωρεές - επιχορηγήσεις');
INSERT INTO lm VALUES('64.07.00', 'Έντυπα');
INSERT INTO lm VALUES('64.07.01', 'Υλικά πολλαπλών εκτυπώσεων');
INSERT INTO lm VALUES('64.07.02', 'Έξοδα πολλαπλών εκτυπώσεων');
INSERT INTO lm VALUES('64.07.03', 'Γραφική ύλη και λοιπά υλικά γραφείων');
INSERT INTO lm VALUES('64.08.00', 'Καύσιμα και λοιπά υλικά θέρμανσης');
INSERT INTO lm VALUES('64.08.01', 'Υλικά καθαριότητας');
INSERT INTO lm VALUES('64.08.02', 'Υλικά φαρμακείου');
INSERT INTO lm VALUES('64.08.99', 'Λοιπά υλικά άμεσης ανάλωσης');
INSERT INTO lm VALUES('64.09.00', 'Έξοδα δημοσίεσης ισολογισμών & προσκλήσεων');
INSERT INTO lm VALUES('64.09.01', 'Έξοδα δημοσίευσης αγγελιών & ανακοινώσεων');
INSERT INTO lm VALUES('64.09.99', 'Έξοδα λοιπών δημοσιεύσεων');
INSERT INTO lm VALUES('64.10', 'Έξοδα συμμετοχών & χρεογράφων');
INSERT INTO lm VALUES('64.11', 'Διαφορές αποτίμησης συμμετοχών & χρεογράφων');
INSERT INTO lm VALUES('64.12', 'Ζημιές από πώληση συμμετοχών & χρεογράφων');
INSERT INTO lm VALUES('64.91', 'Ζημιές από πράξεις hedging');
INSERT INTO lm VALUES('64.98.00', 'Κοινόχρηστες δαπάνες');
INSERT INTO lm VALUES('64.98.01', 'Έξοδα λειτουργίας Οργάνων Διοικήσεως');
INSERT INTO lm VALUES('64.98.02', 'Δικαστικά και έξοδα εξώδικων ενεργειών');
INSERT INTO lm VALUES('64.98.03', 'Έξοδα συμβολαιογράφων');
INSERT INTO lm VALUES('64.98.04', 'Έξοδα λοιπών ελεύθερων επαγγελματιών');
INSERT INTO lm VALUES('64.98.05', 'Έξοδα διαφόρων τρίτων');
INSERT INTO lm VALUES('65.00', 'Τόκοι & έξοδα ομολογιακών δανείων');
INSERT INTO lm VALUES('65.01', 'Τόκοι & έξοδα λοιπών μακροπρόθεσμων υποχρεώσεων');
INSERT INTO lm VALUES('65.02', 'Προεξοφλητικοί τόκοι & έξοδα Τραπεζών');
INSERT INTO lm VALUES('65.03', 'Τόκοι & έξοδα χρηματοδοτήσεων Τραπεζών εγγυημένων με αξιόγραφα');
INSERT INTO lm VALUES('65.04', 'Τόκοι & έξοδα βραχυπρόθεσμων Τραπεζικών χορηγήσεων για εξαγωγές');
INSERT INTO lm VALUES('65.05', 'Τόκοι& έξοδα λοιπών βραχυπρόθεσμων Τραπεζικών χρηματοδοτήσεων');
INSERT INTO lm VALUES('65.06', 'Τόκοι & έξοδα λοιπών βραχυπρόθεσμων υποχρεώσεων');
INSERT INTO lm VALUES('65.07', 'Ειδικός φόρος τραπεζικών εργασιών & χ/μο συμβ. δανείων & χρημ/σεων');
INSERT INTO lm VALUES('65.08', 'Έξοδα ασφαλειών δανείων και χρηματοδοτήσεων');
INSERT INTO lm VALUES('65.09', 'Παροχές σε ομολογιούχους επί πλέον τόκου');
INSERT INTO lm VALUES('65.10', 'Προμήθειες εγγυητικών επιστολών');
INSERT INTO lm VALUES('65.90', 'Τόκοι & έξοδα εισπράξεως απαιτήσεων με σύμβαση Factoring');
INSERT INTO lm VALUES('65.98.00', 'Εισπρακτικά γραμματίων εισπρακτέων');
INSERT INTO lm VALUES('65.98.99', 'Διάφορα έξοδα τραπεζών');
INSERT INTO lm VALUES('65.99', 'Προϋπολογισμένοι-Προπληρωμένοι τόκοι & συναφή έξοδα');
INSERT INTO lm VALUES('66.00.01', 'Αποσβέσεις Ορυχείων');
INSERT INTO lm VALUES('66.00.02', 'Αποσβέσεις Μεταλλείων');
INSERT INTO lm VALUES('66.00.03', 'Αποσβέσεις Λατομείων');
INSERT INTO lm VALUES('66.00.05', 'Αποσβέσεις Φυτειών');
INSERT INTO lm VALUES('66.00.06', 'Αποσβέσεις Δασών');
INSERT INTO lm VALUES('66.01.00', 'Αποσβέσεις κτιρίων-εγκαταστάσεων κτιρίων');
INSERT INTO lm VALUES('66.01.01', 'Αποσβέσεις τεχνικών έργων εξυπηρετήσεως μεταφορών');
INSERT INTO lm VALUES('66.01.02', 'Αποσβέσεις λοιπών τεχνικών έργων');
INSERT INTO lm VALUES('66.01.03', 'Αποσβέσεις διαμορφώσεως γηπέδων');
INSERT INTO lm VALUES('66.02.00', 'Αποσβέσεις μηχανημάτων');
INSERT INTO lm VALUES('66.02.01', 'Αποσβέσεις τεχνικών εγκαταστάσεων');
INSERT INTO lm VALUES('66.02.02', 'Αποσβέσεις φορητών μηχανημάτων χειρός');
INSERT INTO lm VALUES('66.02.03', 'Αποσβέσεις εργαλείων');
INSERT INTO lm VALUES('66.02.04', 'Αποσβέσεις καλουπιών-ιδιοσυσκευών');
INSERT INTO lm VALUES('66.02.05', 'Αποσβέσεις μηχανολογικών οργάνων');
INSERT INTO lm VALUES('66.02.06', 'Αποσβέσεις λοιπού μηχανολογικού εξοπλισμού');
INSERT INTO lm VALUES('66.03.00', 'Αποσβέσεις αυτοκινήτων λεωφορείων');
INSERT INTO lm VALUES('66.03.01', 'Αποσβέσεις λοιπών επιβατικών αυτοκινήτων');
INSERT INTO lm VALUES('66.03.02', 'Αποσβέσεις αυτοκινήτων φορτηγών-Ρυμουλκών-Ειδικής χρήσης');
INSERT INTO lm VALUES('66.03.03', 'Αποσβέσεις σιδηροδρομικών οχημάτων');
INSERT INTO lm VALUES('66.03.04', 'Αποσβέσεις πλωτών μέσων');
INSERT INTO lm VALUES('66.03.05', 'Αποσβέσεις εναέριων μέσων');
INSERT INTO lm VALUES('66.03.06', 'Αποσβέσεις μέσων εσωτερικών μεταφορών');
INSERT INTO lm VALUES('66.03.09', 'Αποσβέσεις λοιπών μέσων μεταφοράς');
INSERT INTO lm VALUES('66.04.00', 'Αποσβέσεις επίπλων');
INSERT INTO lm VALUES('66.04.01', 'Αποσβέσεις σκευών');
INSERT INTO lm VALUES('66.04.02', 'Αποσβέσεις μηχανών γραφείων');
INSERT INTO lm VALUES('66.04.03', 'Αποσβέσεις ηλεκτρονικών υπολογιστών');
INSERT INTO lm VALUES('66.04.04', 'Αποσβέσεις μέσων αποθηκεύσεως και μεταφοράς');
INSERT INTO lm VALUES('66.04.05', 'Αποσβέσεις επιστημονικών οργάνων');
INSERT INTO lm VALUES('66.04.06', 'Αποσβέσεις ζώων για πάγια εκμετάλλευση');
INSERT INTO lm VALUES('66.04.08', 'Αποσβέσεις εξοπλισμού τηλεπικοινωνιών');
INSERT INTO lm VALUES('66.04.09', 'Αποσβέσεις λοιπού εξοπλισμού');
INSERT INTO lm VALUES('66.05.00', 'Αποσβέσεις υπεραξίας επιχειρήσεως');
INSERT INTO lm VALUES('66.05.01', 'Αποσβέσεις δικαιωμάτων βιομηχανικής ιδιοκτησίας');
INSERT INTO lm VALUES('66.05.02', 'Αποσβέσεις δικαιωμάτων εκμ/σης ορυχείων-μεταλλείων-λατομείων');
INSERT INTO lm VALUES('66.05.03', 'Αποσβέσεις λοιπών παραχωρήσεων');
INSERT INTO lm VALUES('66.05.04', 'Αποσβέσεις δικαιωμάτων χρήσεως ενσώματων πάγιων στοιχείων');
INSERT INTO lm VALUES('66.05.05', 'Αποσβέσεις λοιπών δικαιωμάτων');
INSERT INTO lm VALUES('66.05.10', 'Αποσβέσεις εξόδων ιδρύσεως & πρώτης εγκαταστάσεως');
INSERT INTO lm VALUES('66.05.11', 'Αποσβέσεις εξόδων ερευνών ορυχείων - μεταλλείων - λατομείων');
INSERT INTO lm VALUES('66.05.12', 'Αποσβέσεις εξόδων λοιπών ερευνών');
INSERT INTO lm VALUES('66.05.13', 'Αποσβέσεις εξόδων αυξήσεως κεφαλαίου & εκδόσεως ομολογιακών δανείων');
INSERT INTO lm VALUES('66.05.14', 'Αποσβέσεις εξόδων κτήσεως ακινητοποιήσεων');
INSERT INTO lm VALUES('66.05.16', 'Αποσβέσεις διαφορών εκδόσεως και εξοφλήσεως ομολογιών');
INSERT INTO lm VALUES('66.05.17', 'Αποσβέσεις εξόδων αναδιοργανώσεως');
INSERT INTO lm VALUES('66.05.18', 'Αποσβέσεις τόκων δανείων κατασκευαστικής περιόδου');
INSERT INTO lm VALUES('66.05.19', 'Αποσβέσεις λοιπών εξόδων πολυετούς αποσβέσεως');
INSERT INTO lm VALUES('66.99', 'Προϋπολογισμένες αποσβέσεις εκμεταλλεύσεως');
INSERT INTO lm VALUES('68.00', 'Προβλέψεις για αποζημίωση προσωπικού λόγω εξόδου από την υπηρεσία');
INSERT INTO lm VALUES('68.01', 'Προβλέψεις για υποτιμήσεις συμμετοχών και χρεογράφων');
INSERT INTO lm VALUES('68.09', 'Λοιπές προβλέψεις εκμεταλλεύσεως');
INSERT INTO lm VALUES('70.00', 'Πωλήσεις εμπορευμάτων');
INSERT INTO lm VALUES('71.00', 'Πωλήσεις προϊόντων ετοίμων & ημιτελών');
INSERT INTO lm VALUES('72.00', 'Πωλήσεις λοιπών αποθεμάτων & αχρ.υλικ.');
INSERT INTO lm VALUES('73.00', 'Έσοδα απο παροχή υπηρεσιών');
INSERT INTO lm VALUES('74.00', 'Επιχορηγήσεις & διάφορα έσοδα πωλήσεων');
INSERT INTO lm VALUES('75.00', 'Έσοδα παρεπομένων ασχολιών');
INSERT INTO lm VALUES('76.00', 'Έσοδα κεφαλαίων');
INSERT INTO lm VALUES('8', 'ΑΠΟΤΕΛΕΣΜΑΤΑ');



--------------------------------------------------------
--                 CREATE VIEWS                        |
--------------------------------------------------------
CREATE VIEW vki AS
SELECT ki.id, cat.cat, typ.typ, ori.ori, ki.dat, ki.pno, ki.afm, pli.pli, ki.per
FROM ki
INNER JOIN cat ON cat.id=ki.cat_id
INNER JOIN typ ON typ.id=ki.typ_id
INNER JOIN ori ON ori.id=ki.ori_id
INNER JOIN pli ON pli.id=ki.pli_id
;

CREATE VIEW vki_kid AS
SELECT ki.id, cat.cat, typ.typ, ki.dat, ki.pno, ki.afm, pli.pli, ki.per,
  kid.id AS det, lm.lmp, ori.ori, kid.pfpa, kid.val, kid.fpa
FROM ki
INNER JOIN kid ON ki.id=kid.ki_id
INNER JOIN cat ON cat.id=ki.cat_id
INNER JOIN typ ON typ.id=ki.typ_id
INNER JOIN ori ON ori.id=ki.ori_id
INNER JOIN pli ON pli.id=ki.pli_id
INNER JOIN lm ON lm.id=kid.lm_id
ORDER BY ki.id, kid.id
;

CREATE VIEW vtim AS
SELECT ki.id, cat.cat, typ.typ, ki.dat, ki.pno, ki.afm, ki.per,
   sum(kid.val) AS tval,
   sum(kid.fpa) AS tfpa,
   sum(kid.val) +  sum(kid.fpa) AS total
FROM ki
INNER JOIN kid ON ki.id=kid.ki_id
INNER JOIN cat ON cat.id=ki.cat_id
INNER JOIN typ ON typ.id=ki.typ_id
INNER JOIN ori ON ori.id=ki.ori_id
INNER JOIN lm ON lm.id=kid.lm_id
group by ki.id, cat.id, typ.id, ki.dat, ki.pno, ki.afm;

CREATE VIEW vtima AS
SELECT ki.id, cat.cat, typ.typ, ki.dat, ki.pno, ki.afm, ki.per,
   sum(kid.val) * cat.syn * typ.syn AS tval,
   sum(kid.fpa) * cat.syn * typ.syn AS tfpa,
   (sum(kid.val) +  sum(kid.fpa)) * cat.syn * typ.syn AS total
FROM ki
INNER JOIN kid ON ki.id=kid.ki_id
INNER JOIN cat ON cat.id=ki.cat_id
INNER JOIN typ ON typ.id=ki.typ_id
INNER JOIN ori ON ori.id=ki.ori_id
INNER JOIN lm ON lm.id=kid.lm_id
group by ki.id, cat.id, typ.id, ki.dat, ki.pno, ki.afm;

CREATE VIEW vtr_trd as
SELECT tr.id, tr.par, tr.dat, lmo.lmo, lmo.lmop, trd.xr, trd.pi
From trd
inner join lmo on trd.lmo_id=lmo.id
inner join tr on tr.id=trd.tr_id;

CREATE VIEW vbiblio as
SELECT ki.id, cat.cat, typ.typ, ki.dat, ki.pno, ki.afm, ki.per,
CASE
   WHEN efpa = 1 THEN sum(kid.val) * cat.syn * typ.syn
   WHEN efpa = 0 THEN (sum(kid.val) * cat.syn * typ.syn) + (sum(kid.fpa) * cat.syn * typ.syn)
END AS tval,
CASE
   WHEN efpa = 1 THEN sum(kid.fpa) * cat.syn * typ.syn
   WHEN efpa = 0 THEN 0
END AS tfpa,
(sum(kid.val) +  sum(kid.fpa)) * cat.syn * typ.syn AS total
FROM ki
INNER JOIN kid ON ki.id=kid.ki_id
INNER JOIN cat ON cat.id=ki.cat_id
INNER JOIN typ ON typ.id=ki.typ_id
INNER JOIN ori ON ori.id=ki.ori_id
INNER JOIN lm ON lm.id=kid.lm_id
group by ki.id, cat.id, typ.id, ki.dat, ki.pno, ki.afm;

--------------------------------------
-- ΠΙΝΑΚΕΣ ΥΠΟΣΥΣΤΗΜΑΤΟΣ ΜΙΣΘΟΔΟΣΙΑΣ |
--------------------------------------

--Στοιχεία εργαζομένων
CREATE TABLE IF NOT EXISTS erg(
id ΤΕΧΤ PRIMARY KEY, --Το ΑΜΚΑ είναι το ιδανικό κλειδί
epo TEXT NOT NULL, --Επώνυμο
ono TEXT NOT NULL, --Όνομα
pat TEXT NOT NULL, --Όνομα πατέρα
mit TEXT NOT NULL, --Όνομα μητέρας
bda DATE NOT NULL, --Ημερομηνία γέννησης
ypi TEXT NOT NULL, --Υπηκοότητα
afm TEXT NOT NULL UNIQUE, --Αριθμός Φορολογικού Μητρώου
ami TEXT NOT NULL UNIQUE, --Αριθμός Μητρώου ΙΚΑ
ata TEXT NOT NULL UNIQUE, --Αριθμός Ταυτότητας
aap TEXT NOT NULL, --Αριθμός Άδειας Εργασίας
dpo TEXT NOT NULL, --Διεύθυνση Πόλη
dod TEXT NOT NULL, --Διεύθυνση Οδός
dar TEXT NOT NULL, --Διεύθυνση Αριθμός
sex INTEGER NOT NULL, --Φύλο
oik TEXT NOT NULL, --Οικογενειακή κατάσταση
pai INTEGER NOT NULL DEFAULT 0, --Αριθμός παιδιών
UNIQUE (epo, ono, pat, mit)
);

--Παρουσίες εργαζομένου
CREATE TABLE IF NOT EXISTS epar(
id INTEGER PRIMARY KEY,
xrisi INTEGER NOT NULL, --Έτος
per TEXT NOT NULL, --Περίοδος (Μήνας). Τιμές 01, 02, ..., 12
erg_id INTEGER REFERENCES erg(id),
apo DATE, --Ημ/νία πρόσληψης. Συμπληρώνεται μόνο κατά την περίοδο της πρόσληψης
eos DATE, --Ημ/νία αποχώρησης. Μόνο κατά την περίοδο αποχώρησης
meres INTEGER NOT NULL DEFAULT 0, --Ημέρες κανονικής εργασίας
madeia INTEGER NOT NULL DEFAULT 0, -- Ημέρες σε κανονική (πληρωμένη) άδεια
onyxta INTEGER NOT NULL DEFAULT 0, --Νυχτερινές ώρες εργασίας για προσαύξηση 25%
oargia INTEGER NOT NULL DEFAULT 0, --Ώρες Κυρακής ή Αργίας για προσαύξηση 75%
margia INTEGER NOT NULL DEFAULT 0, --Μέρες Κυριακών/αργιών για προσαύξηση 75%
UNIQUE (xrisi, per, erg_id)
);

--Ασθένειες εργαζομένου
CREATE TABLE IF NOT EXISTS epasth(
id INTEGER PRIMARY KEY,
xrisi INTEGER NOT NULL,
per TEXT NOT NULL,
erg_id INTEGER REFERENCES erg(id),
apo DATE NOT NULL, --Πρώτη ημέρα ασθένειας
eos DATE NOT NULL, --Τελευταία ημέρα ασθένειας.
masl3 INTEGER NOT NULL DEFAULT 0, --Μέρες ασθένειας <= 3
masm3 INTEGER NOT NULL DEFAULT 0, --Μέρες ασθένειας > 3
mas0 INTEGER NOT NULL DEFAULT 0, --Μέρες ασθένειας χωρίς αποδοχές
eas NUMERIC NOT NULL DEFAULT 0, --Επίδομα ασθένειας ΙΚΑ
UNIQUE(xrisi, per, erg_id, apo)
);

--Υπερωρίες εργαζομένου
CREATE TABLE IF NOT EXISTS epyp(
id INTEGER PRIMARY KEY,
xrisi INTEGER NOT NULL,
per TEXT NOT NULL,
erg_id INTEGER REFERENCES erg(id),
oyp INTEGER NOT NULL DEFAULT 0, --Ώρες υπερωρίας
UNIQUE(xrisi, per, erg_id)
);

COMMIT;
