--Τάξη
CREATE TABLE IF NOT EXISTS taj(
id INTEGER PRIMARY KEY,
tajp TEXT NOT NULL UNIQUE,
taj_id INTEGER DEFAULT NULL REFERENCES taj(id)
);
INSERT INTO taj(id, tajp) VALUES (1, 'Α');
INSERT INTO taj(id, tajp) VALUES (2, 'Β');
INSERT INTO taj(id, tajp) VALUES (3, 'Γ');
INSERT INTO taj VALUES (4, 'ΒΑ', 2);
INSERT INTO taj VALUES (5, 'ΒΘ', 2);
INSERT INTO taj VALUES (6, 'ΓΑΣ', 3);
INSERT INTO taj VALUES (7, 'ΓΟΙΠ', 3);
INSERT INTO taj VALUES (8, 'ΓΘΣ', 3);

--Μαθητής
CREATE TABLE IF NOT EXISTS stud(
id INTEGER PRIMARY KEY,
sepo TEXT NOT NULL,
sono TEXT NOT NULL,
spat TEXT NOT NULL,
smit TEXT NOT NULL,
taj_id INTEGER NOT NULL REFERENCES taj(id),
UNIQUE(sepo, sono, spat, smit)
);
--Τμήμα
CREATE TABLE IF NOT EXISTS tmi(
id INTEGER PRIMARY KEY,
tmip TEXT NOT NULL UNIQUE,
taj_id INTEGER NOT NULL REFERENCES taj(id),
room_id INTEGER NOT NULL REFERENCES room(id)
);
--Τμήμα / Μαθητές
CREATE TABLE IF NOT EXISTS tmid(
id INTEGER PRIMARY KEY,
tmi_id INTEGER NOT NULL REFERENCES tmi(id),
stud_id INTEGER NOT NULL REFERENCES stud(id),
UNIQUE(tmi_id, stud_id)
);

--Ειδικότητα Καθηγητή
CREATE TABLE IF NOT EXISTS eid(
id INTEGER PRIMARY KEY,
eidp TEXT NOT NULL UNIQUE
);
INSERT INTO eid VALUES (1, 'Μαθηματικός');
INSERT INTO eid VALUES (2, 'Φιλόλογος');
INSERT INTO eid VALUES (3, 'Φυσικός');

--Καθηγητής
CREATE TABLE IF NOT EXISTS tea(
id INTEGER PRIMARY KEY,
tepo TEXT NOT NULL,
tono TEXT NOT NULL,
eid_id INTEGER NOT NULL REFERENCES eid(id),
UNIQUE(tepo, tono)
);
INSERT INTO tea VALUES (1, 'Laz', 'Ted', 1);
INSERT INTO tea VALUES (2, 'Daz', 'Pop', 2);
INSERT INTO tea VALUES (3, 'Laz', 'Kon', 3);

--Μάθημα
CREATE TABLE IF NOT EXISTS les(
id INTEGER PRIMARY KEY,
taj_id INTEGER NOT NULL REFERENCES taj(id),
lepp TEXT NOT NULL UNIQUE,
eid_id INTEGER NOT NULL REFERENCES eid(id),
ores INTEGER NOT NULL DEFAULT 1
);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Θρησκευτικά Α', 1, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Αρχαία Α', 2, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Νέα Ελληνικά Α', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Λογοτεχνία Α', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Άλγεβρα Α', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Γεωμετρία Α', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Φυσική Α', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Χημεία Α', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Βιολογία Α', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Ιστορία Α', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Πολιτική παιδεία Α', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Φυσική αγωγή Α', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Ερευνητική εργασία Α', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (1, 'Εφαρμογές πληροφορικής Α', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (2, 'Μαθηματικά Γενικής Β', 1, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (2, 'Αρχαία Γενικής Β', 2, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (2, 'Φυσική Γενικής Β', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (2, 'Φιλοσοφία Γενικής Β', 2, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (2, 'Αγγλικά Β', 2, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (2, 'Χημεία Γενικής Β', 2, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (3, 'Μαθηματικά Γενικής Γ', 1, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (3, 'Αρχαία Γενικής Γ', 2, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (3, 'Φυσική Γενικής Γ', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (4, 'Αρχαία Δέσμης Β', 2, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (4, 'Λατινικά Δέσμης Β', 2, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (5, 'Μαθηματικά Δέσμης Β', 1, 3);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (5, 'Φυσική Δέσμης Β', 3, 2);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (6, 'Αρχαία Δέσμης Γ', 2, 3);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (7, 'Οικονομικά Δέσμης Γ', 1, 3);
INSERT INTO les (taj_id, lepp, eid_id, ores) VALUES (8, 'Μαθηματικά Δέσμης Γ', 1, 2);

--Αίθουσα
CREATE TABLE IF NOT EXISTS room(
id INTEGER PRIMARY KEY,
roomno TEXT NOT NULL UNIQUE,
atoma INTEGER NOT NULL DEFAULT 0 --Χωρητικότητα αίθουσας
);

INSERT INTO room values (1, '01', 26);
INSERT INTO room values (2, '11', 25);
INSERT INTO room values (3, '12', 26);
INSERT INTO room values (4, '13', 26);
INSERT INTO room values (5, '14', 26);
INSERT INTO room values (6, '15', 26);
INSERT INTO room values (7, '16', 26);
INSERT INTO room values (8, '17', 26);
INSERT INTO room values (9, 'Χημείο', 26);
INSERT INTO room values (10,'21', 26);
INSERT INTO room values (11,'22', 26);
INSERT INTO room values (12,'23', 26);
INSERT INTO room values (13,'24', 26);
INSERT INTO room values (14,'25', 26);
INSERT INTO room values (15,'26', 26);
INSERT INTO room values (16,'27', 26);
INSERT INTO room values (17,'Φυσικής', 26);

SELECT SUM(atoma) as capacity FROM room;

select count(id) from stud;

delete from stud;


create view lessons as
select stud.id, stud.sepo, taj.tajp, les.lepp, les.ores
from stud
inner join taj on taj.id = stud.taj_id
inner join les on taj.id=les.taj_id
union
select stud.id, stud.sepo, taj1.tajp, les.lepp, les.ores
from stud
inner join taj on taj.id = stud.taj_id
inner join taj as taj1 on taj1.id=taj.taj_id
inner join les on taj.taJ_id=les.taj_id
where taj1.tajp <> 'Α'
order by stud.id;
