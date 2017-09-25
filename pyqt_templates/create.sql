CREATE TABLE IF NOT EXISTS co(
    id INTEGER PRIMARY KEY,
    sper
);

INSERT INTO co VALUES (1, 'Κεντρικό');
INSERT INTO co VALUES (2, 'Υποκατάστημα');

CREATE TABLE IF NOT EXISTS erg(
    id INTEGER PRIMARY KEY,
    co_cd INTEGER NOT NULL,
    sepo,
    sono,
    spat,
    smit,
    dgen
);

CREATE TABLE IF NOT EXISTS pro(
    id INTEGER PRIMARY KEY,
    erg_id INTEGER NOT NULL,
    dpro DATE,
    eeos DATE
);