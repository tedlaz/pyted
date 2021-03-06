BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS zfld (
	id INTEGER PRIMARY KEY,
	fld TEXT NOT NULL UNIQUE,
	flbl TEXT NOT NULL,
	zftyp_id INTEGER REFERENCES zftyp(id),
	nonull INTEGER NOT NULL,
	max INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS zftyp (
	id INTEGER PRIMARY KEY,
	ftyp TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS zt (
	id INTEGER PRIMARY KEY,
	tbl TEXT NOT NULL UNIQUE,
	zttyp_id INTEGER REFERENCES zttyp(id),
	tlbl TEXT NOT NULL UNIQUE,
	tlblp TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS zt_d (
	id INTEGER PRIMARY KEY,
	zt_id INTEGER NOT NULL REFERENCES zt(id),
	zfld_id INTEGER NOT NULL REFERENCES zfld(id),
	uniq YESNO NOT NULL,
	tuniq YESNO NOT NULL,
	rpr YESNO NOT NULL
);
CREATE TABLE IF NOT EXISTS zttyp (
	id INTEGER PRIMARY KEY,
	ttyp TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS zkv (
	id INTEGER PRIMARY KEY,
	key TEXT NOT NULL UNIQUE,
	val TEXT NOT NULL
);

INSERT INTO zttyp VALUES (1, 'table');
INSERT INTO zttyp VALUES (2, 'view');

INSERT INTO zftyp VALUES (1, 'BOOLEAN');
INSERT INTO zftyp VALUES (2, 'DATE');
INSERT INTO zftyp VALUES (3, 'DATEN');
INSERT INTO zftyp VALUES (4, 'INTEGER');
INSERT INTO zftyp VALUES (5, 'INTEGERS');
INSERT INTO zftyp VALUES (6, 'NUMERIC');
INSERT INTO zftyp VALUES (7, 'NUMERICS');
INSERT INTO zftyp VALUES (8, 'TEXT');
INSERT INTO zftyp VALUES (9, 'IDBUTTON');
INSERT INTO zftyp VALUES (10, 'IDCOMBO');
INSERT INTO zftyp VALUES (11, 'VARCHAR');
INSERT INTO zftyp VALUES (12, 'VARCHARN');
INSERT INTO zftyp VALUES (13, 'WEEKDAYS');
INSERT INTO zftyp VALUES (14, 'YESNO');

INSERT INTO zkv VALUES (1, 'appname', 'Test Application');
INSERT INTO zkv VALUES (2, 'version', '0.1');
INSERT INTO zkv VALUES (3, 'programmer', 'Ted Lazaros');

COMMIT;
