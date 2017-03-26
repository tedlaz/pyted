BEGIN TRANSACTION;

PRAGMA user_version = 1002;
PRAGMA application_id = 123123124;

--Τύπος παραστατικού (Χρεωστικό ή πιστωτικό)
CREATE TABLE IF NOT EXISTS note(
id INTEGER PRIMARY KEY,
notep TEXT NOt NULL UNIQUE
);
INSERT INTO note VALUES(1, 'normal');
INSERT INTO note VALUES(2, 'credit');

--Τύπος εγγραφής
CREATE TABLE IF NOT EXISTS typ(
id INTEGER PRIMARY KEY,
typp TEXT NOT NULL UNIQUE
);

INSERT INTO typ VALUES(1, 'revenue');
INSERT INTO typ VALUES(2, 'cashregister');
INSERT INTO typ VALUES(3, 'expense');
INSERT INTO typ VALUES(4, 'otherExpenses');

--Συναλλασσόμενοι
CREATE TABLE IF NOT EXISTS syn(
afm TEXT PRIMARY KEY, 
name TEXT NOT NULL,
NonObl INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS myf(
id INTEGER PRIMARY KEY,
typ_id INTEGER NOT NULL REFERENCES typ(id),
note_id INTEGER NOT NULL REFERENCES note(id),
imnia DATE NOT NULL,
parno TEXT DEFAULT '',
afm TEXT DEFAULT '',
amount DECIMAL NOT NULL DEFAULT 0,
tax DECIMAL NOT NULL DEFAULT 0,
taxek INTEGER DEFAULT '', --Αν ο ΦΠΑ εκπίπτει (Γιά τα έξοδα) 1 αλλιώς 0
cashid TEXT DEFAULT '', --Αριθμός Ταμιακής Μηχανής (Για χειρόγραφες κενό, 0 για όλες τις μηχανές
NonObl INTEGER DEFAULT '' --Μη υπόχρεος (Για typ = expense) 
);

--Έσοδα χονδρικής
CREATE TABLE IF NOT EXISTS esx(
id INTEGER PRIMARY KEY,
imnia DATE NOT NULL,
note_id INTEGER NOT NULL REFERENCES note(id),
afm TEXT NOT NULL,
parno TEXT NOT NULL,
amount DECIMAL NOT NULL DEFAULT 0,
tax DECIMAL NOT NULL DEFAULT 0
);

--Έσοδα Λιανικής
CREATE TABLE IF NOT EXISTS esl(
id INTEGER PRIMARY KEY,
imnia DATE NOT NULL,
cashreg_id TEXT NOT NULL DEFAULT '', --Νο Ταμιακής Μηχανής (Για χειρόγραφες κενό, 0 για όλες τις μηχανές μαζί)
zno TEXT NOT NULL,
amount DECIMAL NOT NULL DEFAULT 0,
tax DECIMAL NOT NULL DEFAULT 0
);

CREATE VIEW myfv AS
SELECT myf.id, typ.typp, note.notep, myf.imnia, myf.parno, myf.afm, 
       myf.amount, myf.tax, myf.taxek, myf.cashid,myf.nonObl
FROM myf
INNER JOIN typ ON typ.id=myf.typ_id
INNER JOIN note ON note.id=myf.note_id;

CREATE VIEW myft AS
SELECT typ.typp, myf.afm, syn.afm, note.notep, myf.cashid, 
       sum(myf.amount) AS tamount, sum(myf.tax) AS ttax
FROM myf
INNER JOIN typ ON typ.id=myf.typ_id
INNER JOIN note ON note.id=myf.note_id
LEFT JOIN syn ON syn.afm=myf.afm
GROUP BY typ.id, myf.afm, note.id, myf.cashid
ORDER BY typ.id, myf.afm, note.id, myf.cashid;

COMMIT;
