BEGIN TRANSACTION;
-- Diamerismata
CREATE TABLE IF NOT EXISTS dia(
id INTEGER PRIMARY KEY,
dia TEXT NOT NULL,
dno INTEGER NOT NULL DEFAULT 0,
orofos INTEGER NOT NULL,
owner TEXT NOT NULL,
guest TEXT NOT NULL
);


--Katigoria dapanon (DEH - Kathariotita klp )
CREATE TABLE IF NOT EXISTS ej(
id INTEGER PRIMARY KEY,
ej TEXT NOT NULL UNIQUE
);

--Diamerismata X Kathgoria Dapanon xiliosta
CREATE TABLE IF NOT EXISTS dapx(
id INTEGER PRIMARY KEY,
ej_id INTEGER NOT NULL,
dia_id INTEGER NOT NULL,
val INTEGER NOT NULL DEFAULT 0,
UNIQUE (ej_id, dia_id)
);

--Koinoxrista
CREATE TABLE IF NOT EXISTS koi(
id INTEGER PRIMARY KEY,
kdat DATE NOT NULL UNIQUE, --Ημερομηνία έκδοσης
koip TEXT NOT NULL UNIQUE, --Περίοδος
sxol TEXT NOT NULL --Σχόλιο
);

--Parastatika ejodon
CREATE TABLE IF NOT EXISTS par(
id INTEGER PRIMARY KEY,
koi_id INTEGER NOT NULL,
no TEXT NOT NULL, --Αριθμός παραστατικού
pdate DATE NOT NULL, --Ημερομηνία παραστατικού
ej_id INTEGER NOT NULL,
parp TEXT NOT NULL, --Περιγραφή εξόδου
poso DECIMAL NOT NULL DEFAULT 0,
UNIQUE (koi_id, no)
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
