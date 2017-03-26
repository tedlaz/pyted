BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS lmo (
	id INTEGER PRIMARY KEY,
	lcode VARCHAR(13) NOT NULL,
	lper VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS tr (
	id INTEGER PRIMARY KEY,
	kdate DATE NOT NULL,
	kpar VARCHAR(30) NOT NULL,
	kper VARCHAR(60) NOT NULL
);
CREATE TABLE IF NOT EXISTS trd (
	id INTEGER PRIMARY KEY,
	tr_id INTEGER NOT NULL REFERENCES tr(id),
	lmo_id INTEGER NOT NULL REFERENCES lmo(id),
	xr NUMERIC NOT NULL,
	pi NUMERIC NOT NULL
);
CREATE TABLE IF NOT EXISTS z (key TEXT PRIMARY KEY, val TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS zt (tbl TEXT PRIMARY KEY, tlbl TEXT NOT NULL UNIQUE, tlblp TEXT NOT NULL UNIQUE, rpr TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS zf (fld TEXT PRIMARY KEY, flbl TEXT NOT NULL UNIQUE, typos TEXT NOT NULL, nonull INTEGER NOT NULL DEFAULT 1);
INSERT INTO z VALUES('appname', 'Δοκιμαστική εφαρμογή');
INSERT INTO z VALUES('diadate', '2015-11-16');
INSERT INTO z VALUES('programmer', 'Ted Lazaros');
INSERT INTO z VALUES('version', '1.0');
INSERT INTO zf VALUES ('id', 'No', 'INTEGER', '1');
INSERT INTO zf VALUES ('kdate', 'Ημερομηνία', 'DATE', '1');
INSERT INTO zf VALUES ('kpar', 'Παραστατικό', 'VARCHAR(30)', '1');
INSERT INTO zf VALUES ('kper', 'Περιγραφή', 'VARCHAR(60)', '1');
INSERT INTO zf VALUES ('lcode', 'Λογαριασμός κωδ.', 'VARCHAR(13)', '1');
INSERT INTO zf VALUES ('lper', 'Λογαριασμός περ.', 'VARCHAR(100)', '1');
INSERT INTO zf VALUES ('pi', 'Πίστωση', 'NUMERIC', '1');
INSERT INTO zf VALUES ('xr', 'Χρέωση', 'NUMERIC', '1');
INSERT INTO zt VALUES ('lmo', 'Λογαριασμός', 'Λογαριασμοί', 'SELECT id, lcode || '' '' || lper as rpr FROM lmo');
INSERT INTO zt VALUES ('tr', 'Κίνηση λ/μού', 'Κινήσεις Λ/μών', 'SELECT id, kdate || '' '' || kpar || '' '' || kper as rpr FROM tr');
INSERT INTO zt VALUES ('trd', 'Γραμμή κίνησης', 'Γραμμές κίνησης', 'SELECT id, tr_id as rpr FROM trd');
COMMIT;
