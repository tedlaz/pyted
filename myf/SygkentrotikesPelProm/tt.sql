BEGIN TRANSACTION;
CREATE TABLE tt(
teg TEXT PRIMARY KEY,
esex INTEGER NOT NULL,
myfc TEXT NOT NULL,
prosimo INTEGER NOT NULL DEFAULT 1);

create view myf as
select pp.id, pp.dat, pp.teg, tt.myfc, pp.typ, tt.esex, pp.par, pp.afm,
case
   when tt.myfc='cash' then '000'
   when tt.myfc='exp0' then '000'
   when tt.myfc='expk' then '000'
   when tt.myfc='rev0' then '000'
   when (tt.myfc='exp' and syn.koybas=1) then '000'
   else pp.afm
end as tafm,
pp.lmo, pp.aji, pp.fpa,
case when tt.teg='ΛΟΙΠΑ23' then pp.aji /1.23 else pp.aji * tt.prosimo end as tposo,
case when tt.teg='ΛΟΙΠΑ23' then (pp.aji / 1.23) * 0.23 else pp.fpa * tt.prosimo end as tfpa,
case when tt.prosimo=1 then 'normal' else 'credit' end as partype
from pp
inner join tt on tt.teg=pp.teg
inner join syn on syn.afm=pp.afm
order by pp.id, pp.dat;

create view myftoxml as
select
case
   when (myf.dat between '2015-01-01' and '2015-03-31') then '2015-03-31'
   when (myf.dat between '2015-04-01' and '2015-06-30') then '2015-06-30'
   when (myf.dat between '2015-07-01' and '2015-09-30') then '2015-09-30'
   when (myf.dat between '2015-10-01' and '2015-12-31') then '2015-12-31'
else 'problem' end as dframe,
myf.typ, myf.myfc, myf.tafm, syn.afm, syn.ono, sum(myf.aji) as eeposo, sum(myf.fpa) as eefpa, sum(myf.tposo) as myfposo, sum(myf.tfpa) myffpa, count(myf.id) as noo, myf.partype
from myf
inner join syn on syn.afm=myf.tafm
group by dframe, myf.myfc, myf.tafm, myf.partype
order by dframe, myf.typ, myf.myfc, myf.tafm, myf.partype desc;

CREATE VIEW myfcheck as
select
case
   when (myf.dat between '2015-01-01' and '2015-03-31') then '2015t1'
   when (myf.dat between '2015-04-01' and '2015-06-30') then '2015t2'
   when (myf.dat between '2015-07-01' and '2015-09-30') then '2015t3'
   when (myf.dat between '2015-10-01' and '2015-12-31') then '2015t4'
else 'problem' end as dframe, *
from myf
order by dframe, typ, myfc, dat, par;

insert into tt values ('ΑΠΛ', 1, 'cash', 1);
insert into tt values ('ΑΠΥ', 1, 'cash', 1);
insert into tt values ('ΕΠΛ', 1, 'cash', 1);
insert into tt values ('ΠΙΣ', 1, 'rev', -1);
insert into tt values ('ΤΠΕ', 1, 'rev', -1);
insert into tt values ('ΤΠΛ', 1, 'rev', 1);
insert into tt values ('ΤΠΛ0', 1, 'rev0', 1);
insert into tt values ('ΤΠΥ', 1, 'rev', 1);
insert into tt values ('ΛΟΙΠΑ', 2, 'exp0', 1);
insert into tt values ('ΛΟΙΠΑ0', 2, 'exp0', 1);
insert into tt values ('ΛΟΙΠΑ1', 2, 'exp', 1);
insert into tt values ('ΛΟΙΠΑ1Π', 2, 'exp', -1);
insert into tt values ('ΛΟΙΠΑ23', 2, 'exp', 1);
insert into tt values ('ΛΟΙΠΑΚΟΥΒΑΣ', 2, 'expk', 1);
insert into tt values ('ΠΑΓ', 2, 'exp', -1);
insert into tt values ('ΤΑΓ', 2, 'exp', 1);
insert into tt values ('ΤΑΓ0', 2, 'exp0', 1);
COMMIT;
