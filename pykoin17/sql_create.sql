BEGIN TRANSACTION;
--Διαμέρισμα
CREATE TABLE IF NOT EXISTS diam(
id INTEGER PRIMARY KEY,
diam TEXT NOT NULL, --Όνομα διαμερίσματος
dno INTEGER NOT NULL UNIQUE, --Αριθμός διαμερίσματος
orofos INTEGER NOT NULL, --Όροφος
metra NUMERIC NOT NULL DEFAULT 0, --Τετραγωνικά μέτρα
owner TEXT NOT NULL, --Ιδιοκτήτης
guest TEXT NOT NULL --Ένοικος
);


--Κατηγορία δαπάνης 
CREATE TABLE IF NOT EXISTS dap(
id INTEGER PRIMARY KEY,
dap TEXT NOT NULL UNIQUE --Όνομα δαπάνης (πχ καθαριότητα, ασανσέρ κλπ)
);

--Χιλιοστά ανα διαμέρισμα / κατηγορία δαπάνης
CREATE TABLE IF NOT EXISTS xiliosta(
id INTEGER PRIMARY KEY,
dap_id INTEGER NOT NULL, --Κατηγορία δαπάνης
diam_id INTEGER NOT NULL, --Διαμέρισμα
val INTEGER NOT NULL DEFAULT 0, --Αναλογούντα χιλιοστά
UNIQUE (dap_id, diam_id)
);

--Κοινόχρηστα έξοδα
CREATE TABLE IF NOT EXISTS koi(
id INTEGER PRIMARY KEY,
kdat DATE NOT NULL UNIQUE, --Ημερομηνία έκδοσης
koip TEXT NOT NULL UNIQUE, --Περίοδος
sxol TEXT NOT NULL --Σχόλιο
);

--Κοινόχρηστα έξοδα / Παραστατικά
CREATE TABLE IF NOT EXISTS koid(
id INTEGER PRIMARY KEY,
koi_id INTEGER NOT NULL,
pdate DATE NOT NULL, --Ημερομηνία παραστατικού
pno TEXT NOT NULL, --Αριθμός παραστατικού
parp TEXT NOT NULL, --Περιγραφή εξόδου
dap_id INTEGER NOT NULL, --Κατηγορία δαπάνης
poso DECIMAL NOT NULL DEFAULT 0, --Ποσό
owner INTEGER NOT NULL DEFAULT 0, --Αν δεν αφορά τον ιδιοκτήτη 0
UNIQUE (pdate, pno)
);

--Koinoxrista / Διαμέρισμα
CREATE TABLE IF NOT EXISTS koid(
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

--Κοινόχρηστα / Διαμέρισμα / Δαπάνη
CREATE TABLE IF NOT EXISTS koidd(
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

--Παράμετροι γενικές
CREATE TABLE IF NOT EXISTS pp(
id INTEGER PRIMARY KEY,
pname TEXT NOT NULL UNIQUE,
plbl TEXT NOT NULL UNIQUE,
pval TEXT NOT NULL
);
CREATE VIEW vpar AS 
SELECT par.id, par.koi_id, koi.koip, par.no, par.pdate, par.ej_id, ej.ej, 
par.parp, par.poso
FROM par
INNER JOIN koi ON koi.id=par.koi_id
INNER JOIN ej ON ej.id=par.ej_id;

CREATE VIEW vdapx AS
SELECT dapx.id, dapx.ej_id, ej.ej, dapx.dia_id, dia.dia, dapx.val
FROM dapx
INNER JOIN ej ON ej.id=dapx.ej_id
INNER JOIN dia  ON dia.id=dapx.dia_id
ORDER BY ej_id, dia_id;

CREATE VIEW vpar_sum AS
SELECT koi.id as koi_id, koi.koip, ej.id as ej_id, ej.ej, sum(par.poso) as sposo
FROM par
INNER JOIN koi ON koi.id=par.koi_id
INNER JOIN ej ON ej.id=par.ej_id
GROUP BY koi.id, par.ej_id;

COMMIT;
