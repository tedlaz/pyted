--Δημιουργία πίνακα εγγραφών εσόδων / εξόδων - Πελατών / προμηθευτών
CREATE TABLE pp(
id INTEGER PRIMARY KEY,
dat DATE NOT NULL,
teg TEXT NOT NULL,
typ INTEGER NOT NULL DEFAULT 0,
par TEXT NOT NULL,
afm TEXT,
lmo TEXT,
aji NUMERIC NOT NULL DEFAULT 0,
fpa NUMERIC NOT NULL DEFAULT 0
);

