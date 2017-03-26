BEGIN TRANSACTION;

PRAGMA user_version = 2017;
PRAGMA application_id = 20170313;

--ΚΙΝΟΥΜΕΝΟΙ ΛΟΓΑΡΙΑΣΜΟΙ ΛΟΓΙΣΤΙΚΟΥ ΣΧΕΔΙΟΥ
CREATE TABLE IF NOT EXISTS lmo(
id INTEGER PRIMARY KEY,
lmo TEXT NOT NULL UNIQUE,
lmop TEXT NOT NULL UNIQUE
);

--ΗΜΕΡΟΛΟΓΙΟ ΕΓΓΡΑΦΗΣ
CREATE TABLE IF NOT EXISTS im(
id INTEGER PRIMARY KEY,
im TEXT NOT NULL UNIQUE
);
INSERT INTO im VALUES(1, 'ΑΝΟΙΓΜΑΤΟΣ/ΚΛΕΙΣΙΜΑΤΟΣ ΧΡΗΣΗΣ');
INSERT INTO im VALUES(2, 'ΓΕΝΙΚΟ');

--ΕΓΓΡΑΦΗ ΛΟΓΙΣΤΙΚΗΣ MASTER
CREATE TABLE IF NOT EXISTS tr(
id INTEGER PRIMARY KEY,
im_id INTEGER NOT NULL REFERENCES im(id) DEFAULT 2,
dat DATE NOT NULL, --ΗΜΕΡΟΜΗΝΙΑ
par TEXT NOT NULL, --ΑΡΙΘΜΟΣ ΠΑΡΑΣΤΑΤΙΚΟΥ
per TEXT NOT NULL  --ΣΧΟΛΙΑ ΕΓΓΡΑΦΗΣ
);

--ΕΓΓΡΑΦΗ ΛΟΓΙΣΤΙΚΗΣ DETAIL
CREATE TABLE IF NOT EXISTS trd(
id INTEGER PRIMARY KEY,
tr_id INTEGER NOT NULL REFERENCES tr(id),
lmo_id INTEGER NOT NULL REFERENCES lmo(id), --ΑΡΙΘΜΟΣ ΛΟΓΑΡΙΑΣΜΟΥ
per2 TEXT, --ΠΕΡΙΓΡΑΦΗ ΕΓΓΡΑΦΗΣ
_xr DECIMAL NOT NULL DEFAULT 0, --ΧΡΕΩΣΗ
_pi DECIMAL NOT NULL DEFAULT 0  --ΠΙΣΤΩΣΗ
);

CREATE VIEW vtr AS
SELECT tr.id, tr.im_id as imid, im.im, tr.dat, tr.par, tr.per, trd.id as trdid,
       trd.lmo_id as lmoid, lmo.lmo, lmo.lmop, trd.per2,
       trd._xr as xr, trd._pi as pi
FROM tr
INNER JOIN trd ON tr.id=trd.tr_id
INNER JOIN lmo ON lmo.id=trd.lmo_id
INNER JOIN im ON im.id=tr.im_id
;

CREATE VIEW vim AS
SELECT tr.id, tr.dat, tr.im_id as imid, im.im, tr.par, tr.per,
       sum(trd._xr) as txr, sum(trd._pi) as tpi,
       sum(trd._xr) - sum(trd._pi) as ypol
FROM tr
INNER JOIN trd ON tr.id=trd.tr_id
INNER JOIN im ON im.id=tr.im_id
GROUP BY tr.id
ORDER BY tr.dat, tr.id
;

COMMIT;