BEGIN TRANSACTION;
--Oikogeneiaki katastasi
CREATE TABLE okat(
id INTEGER PRIMARY KEY,
okatp TEXT NOT NULL UNIQUE
);
INSERT INTO okat VALUES (1, 'Άγαμος');
INSERT INTO okat VALUES (2, 'Έγγαμος');

CREATE TABLE sex(
id INTEGER PRIMARY KEY,
sexp TEXT NOT NULL UNIQUE
);
INSERT INTO sex VALUES (1, 'Άνδρας');
INSERT INTO sex VALUES (2, 'Γυναίκα');

--Stoixeia fysikoy prosopoy
CREATE TABLE fpr(
id INTEGER PRIMARY KEY,
epo TEXT NOT NULL,
ono TEXT NOT NULL,
pat TEXT NOT NULL,
mit TEXT NOT NULL,
sex_id INTEGER NOT NULL references sex(id),
dat DATE NOT NULL,
amka TEXT NOT NULL UNIQUE,
afm TEXT NOT NULL UNIQUE,
mika TEXT NOT NULL UNIQUE,
taft TEXT NOT NULL,
xora TEXT NOT NULL, --Ethnikotita
okat_id INTEGER NOT NULL REFERENCES okat(id), --Oikogeneiaki katastasi
kids INTEGER NOT NULL DEFAULT 0, --Arithmos paidion
poli TEXT NOT NULL, --Diefthinsi poli
odos TEXT NOT NULL, --Diefthinsi odos
num TEXT NOT NULL, --Diefthinsi arithmos
tk TEXT, --Diefthinsi tk
tel TEXT, --Tilefono
mob TEXT, --Mobile phone
email TEXT, --e-mail
UNIQUE (epo, ono, pat, mit)
);

--Paroysies taktikes
CREATE TABLE parn(
id INTEGER PRIMARY KEY,
pro_id INTEGER NOT NULL REFERENCES pro(id),
xrisi INTEGER NOT NULL,
minas INTEGER NOT NULL,
meres NUMERIC NOT NULL DEFAULT 0,
adeia NUMERIC NOT NULL DEFAULT 0,
nyxta NUMERIC NOT NULL DEFAULT 0,
argme NUMERIC NOT NULL DEFAULT 0,
argor NUMERIC NOT NULL DEFAULT 0,
UNIQUE (pro_id, xrisi, minas)
);

--Astheneia
CREATE TABLE para(
id INTEGER PRIMARY KEY,
pro_id INTEGER NOT NULL REFERENCES pro(id),
xrisi INTEGER NOT NULL,
minas INTEGER NOT NULL,
apo INTEGER NOT NULL,
eos INTEGER NOT NULL,
merl3 NUMERIC NOT NULL DEFAULT 0,
merm3 NUMERIC NOT NULL DEFAULT 0,
epid NUMERIC NOT NULL DEFAULT 0,
UNIQUE (pro_id, xrisi, minas, apo)
);

--Yperories
CREATE TABLE pary(
id INTEGER PRIMARY KEY,
pro_id INTEGER NOT NULL REFERENCES pro(id),
xrisi INTEGER NOT NULL,
minas INTEGER NOT NULL,
apo INTEGER NOT NULL,
eos INTEGER NOT NULL,
yper NUMERIC NOT NULL DEFAULT 0,
UNIQUE (pro_id, xrisi, minas, apo)
);

--Parartima / ypokatastima
CREATE TABLE ypo(
id INTEGER PRIMARY KEY,
ypop TEXT NOT NULL UNIQUE, --Onomasia parartimatos
kad INTEGER NOT NULL --Kodikos Arithmos Drastiriotitas ika
);
INSERT INTO ypo VALUES (1, 'Κεντρικό', 0);

--Eidikotites ergasias
CREATE TABLE eid(
id INTEGER PRIMARY KEY,
eidp TEXT NOT NULL UNIQUE, --perigrafi eidikotitas
eid INTEGER NOT NULL --Kodikos eidikotitas ika
);

--Typos apodoxon ergazomenou (Misthos, Imeromisthio, Oromisthio)
CREATE TABLE apd(
id INTEGER PRIMARY KEY,
apdp TEXT NOT NULL UNIQUE
);
INSERT INTO apd VALUES (1, 'Μισθός');
INSERT INTO apd VALUES (2, 'Ημερομίσθιο');
INSERT INTO apd VALUES (3, 'Ωρομίσθιο');

--Xronikos Typos symbasis ergazomenou (Aoristou xronoy, Orismenou xronoy, Ergou) Meriki Apasxolisi, Pliris, Ek Peritropis)
CREATE TABLE symx(
id INTEGER PRIMARY KEY,
symxp TEXT NOT NULL UNIQUE
);
INSERT INTO symx VALUES(1, 'Αορίστου χρόνου');
INSERT INTO symx VALUES(2, 'Ορισμένου χρόνου');
INSERT INTO symx VALUES(3, 'Έργου');

--Typos Apasxolisis (Meriki Apasxolisi, Pliris, Ek Peritropis)
CREATE TABLE symt(
id INTEGER PRIMARY KEY,
symtp TEXT NOT NULL UNIQUE
);
INSERT INTO symt VALUES(1, 'Πλήρης');
INSERT INTO symt VALUES(2, 'Μερική');
INSERT INTO symt VALUES(3, 'Εκ περιτροπής');

--Proslipsi ergazomenou
CREATE TABLE pro(
id INTEGER PRIMARY KEY,
pdat DATE NOT NULL, --Hmerominia proslipsis
fpr_id INTEGER NOT NULL REFERENCES erg(id), --Fysiko Prosopo
ypo_id INTEGER NOT NULL REFERENCES ypo(id), --Parartima
eid_id INTEGER NOT NULL REFERENCES eid(id), --Eidikotita
UNIQUE (fpr_id, pdat)
);

--Symbaseis ergasias
CREATE TABLE sym(
id INTEGER PRIMARY KEY,
pro_id INTEGER NOT NULL REFERENCES pro(id),
sdat DATE NOT NULL,
nmeres NUMERIC NOT NULL DEFAULT 25, --Normal working days per month
nores NUMERIC NOT NULL DEFAULT 40, --Normal working hours per week
nwmeres NUMERIC NOT NULL DEFAULT 6, --Normal working days per week
symx_id INTEGER NOT NULL REFERENCES symx(id) DEFAULT 1, --Xronikos Typos Symbasis
symt_id INTEGER NOT NULL REFERENCES symt(id) DEFAULT 1, --Typos Apasxolisis
apd_id INTEGER NOT NULL REFERENCES apd(id) DEFAULT 1, --Typos apodoxon (misthos, imeromisthio)
apod NUMERIC NOT NULL DEFAULT 0,
UNIQUE (pro_id, sdat)
);

--Typos Apoxorisis Ergazomenou (Apolysi, oikiothelis, syntajiodotisi)
CREATE TABLE apt(
id INTEGER PRIMARY KEY,
aptp TEXT NOT NULL UNIQUE
);
INSERT INTO apt VALUES (1, 'Οικιοθελής αποχώρηση');
INSERT INTO apt VALUES (2, 'Απόλυση');
INSERT INTO apt VALUES (3, 'Συνταξιοδότηση');

--Apoxorisi ergazomenoy
CREATE TABLE prof(
id INTEGER PRIMARY KEY,
adat DATE NOT NULL, --Hmerominia apoxorisis
pro_id INTEGER NOT NULL UNIQUE REFERENCES pro(id), --proslipsi
apt_id INTEGER NOT NULL REFERENCES apt(id) --Typos apoxorisis
);

COMMIT;