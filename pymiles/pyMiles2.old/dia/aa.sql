select at_d.id, at_d.at_id, at_d.aa_id, aa.ac, aa.ap, at.dat, at.par, at.per, at_d.xp, at_d.vl,
case when xp=1 then vl else 0 end as xreosi,
case when xp=2 then vl else 0 end as pistosi
from at_d
inner join at on at.id=at_d.at_id
inner join aa on aa.id=at_d.aa_id;

create view lg as select id, dat, apo, per, lxr as lmo,  val as xr, 0 as pi from dt as k1
union select id, dat, apo, per, lpi, 0, val from dt as k2
order by dat, id, lmo;

CREATE TABLE dt(
id INTEGER PRIMARY KEY,
dat DATE NOT NULL,
apo TEXT NOT NULL,
lpi INTEGER NOT NULL,
lxr INTEGER NOT NULL,
val NUMERIC NOT NULL DEFAULT 0,
per TEXT)