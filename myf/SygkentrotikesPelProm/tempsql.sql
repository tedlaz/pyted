PRAGMA user_version = 10115 ;
PRAGMA user_version ;
pragma compile_options;
CREATE VIEW vtr_trd AS
SELECT aa as id, par || ' ' || per as par, imnia as dat, lmo as lmo, lmop, xr, pi
FROM im;
-- Describe IM
CREATE TABLE im(
imno INTEGER,
imnia DATE,
par TEXT,
aa INTEGER NOT NULL,
lmo TEXT NOT NULL,
lmop TEXT NOT NULL,
par2 TEXT,
par2Imnia DATE,
per TEXT,
xr NUMERIC NOT NULL,
pi NUMERIC NOT NULL
);

CREATE VIEW vtr_trd AS
SELECT tran.id, tran.par, tran.imnia as dat, lmos.code as lmo, lmos.per as lmop, trand.xr, trand.pi
FROM trand
INNER JOIN tran ON tran.id=trand.tran_id
INNER JOIN lmos ON lmos.id=trand.lmos_id;

select id from vtr_trd where lmo='71.00.01.023';

SELECT tr.id, lmo.lmo, trd.xr - trd.pi as val
FROM tr
INNER JOIN trd ON tr.id=trd.id_tr
INNER JOIN lmo ON lmo.id=trd.id_lmo
where tr.id in (select id from vtr_trd where lmo='64.00.02.024');

create view kin as 
SELECT ki.id, kid.id as det, cat.cat, typ.typ, ki.dat, ki.no, ki.afm, ki.per, eg.eg, ori.ori, kid.fpa, kid.val, kid.val * kid.fpa / 100 as pfpa
FROM ki
INNER JOIN kid ON ki.id=kid.ki_id
INNER JOIN cat ON cat.id=ki.cat_id
INNER JOIN typ ON typ.id=ki.typ_id
INNER JOIN ori ON ori.id=ki.ori_id
INNER JOIN eg ON eg.id=kid.eg_id;

CREATE VIRTUAL TABLE ted USING fts5(directory UNINDEXED, path, size UNINDEXED, date UNINDEXED);

SELECT sum(trd.xr) - sum(trd.pi) * -1 AS yp
FROM trd
INNER JOIN lmo ON lmo.id=trd.id_lmo
INNER JOIN tr ON tr.id=trd.id_tr
WHERE substr(lmo.lmo, 1, 7) BETWEEN '54.00.0' AND '54.00.8'
 AND tr.dat BETWEEN 2016-01-01 AND 2016-03-31
ORDER BY lmo.lmo;

-- Describe MYFTOXML
select
myf.typ, myf.myfc, myf.tafm, syn.afm, syn.ono, sum(myf.aji) as eeposo, sum(myf.fpa) as eefpa, sum(myf.tposo) as myfposo, sum(myf.tfpa) myffpa, count(myf.id) as noo, myf.partype
from myf
inner join syn on syn.afm=myf.tafm
where myf.dat between '2015-01-01' and '2015-12-31'
group by myf.myfc, myf.tafm, myf.partype
order by myf.typ, myf.myfc, myf.tafm, myf.partype desc;

select myfc, partype, sum(aji), sum(fpa), sum(tposo), sum(tfpa) from myf 
group by myfc, partype
order by typ, myfc, partype;

--ΜΥΦ σε μια sql !!!
select 
case 
   when (pp.dat between '2015-01-01' and '2015-03-31') then '2015t1' 
   when (pp.dat between '2015-04-01' and '2015-06-30') then '2015t2'
   when (pp.dat between '2015-07-01' and '2015-09-30') then '2015t3' 
   when (pp.dat between '2015-10-01' and '2015-12-31') then '2015tt4'  
   else 'problem' 
end as tst,
pp.typ, tt.myfc,
case 
   when tt.myfc='cash' then '000'
   when tt.myfc='exp0' then '000'
   when tt.myfc='expk' then '000'
   when tt.myfc='rev0' then '000'
   when (tt.myfc='exp' and syn.koybas=1) then '000'
   else pp.afm 
end as tafm,
sum(pp.aji) * tt.prosimo as poso,
sum(pp.fpa) * tt.prosimo as fpa,
count(pp.afm) as no,
case when tt.prosimo=1 then 'normal' else 'credit' end as partype
from pp
inner join tt on tt.teg=pp.teg
inner join syn on syn.afm=pp.afm
group by tst, tt.myfc, tafm, tt.prosimo
order by tst, tt.esex, tt.myfc, tafm, tt.prosimo desc;

--ΜΥΦ από myf

select 
myfc, typ, tafm, sum(tposo) as fposo, sum(tfpa) ffpa, count(id) as noo, partype as pt
from myf
where dat between '2015-01-01' and '2015-12-31' 
group by myfc, tafm, partype
order by typ, myfc, tafm, partype desc;

--Αναλυτικά και ταξινομημένα για έλεγχο

select 
case 
   when (myf.dat between '2015-01-01' and '2015-03-31') then '2015t1' 
   when (myf.dat between '2015-04-01' and '2015-06-30') then '2015t2'
   when (myf.dat between '2015-07-01' and '2015-09-30') then '2015t3' 
   when (myf.dat between '2015-10-01' and '2015-12-31') then '2015t4'  
else 'problem' end as dframe,
* from myf
order by dframe, typ, myfc, dat, par;

--Αναλυτικά πριν από το γκρουπάρισμα
 select pp.id, pp.dat, pp.teg, tt.myfc, pp.typ, tt.esex, pp.par, pp.afm, 
case when (tt.myfc='cash' or tt.myfc='exp0' or tt.myfc='rev0') then '000' else pp.afm end as tafm,
pp.lmo, pp.aji, pp.fpa, 
case when tt.teg='ΛΟΙΠΑ23' then pp.aji /1.23 else pp.aji * tt.prosimo end as tposo, 
case when tt.teg='ΛΟΙΠΑ23' then (pp.aji / 1.23) * 0.23 else pp.fpa * tt.prosimo end as tfpa,
case when tt.prosimo=1 then 'normal' else 'credit' end as partype
from pp
inner join tt on tt.teg=pp.teg
where pp.dat between '2015-01-01' and '2015-12-31'
order by pp.id, pp.dat;


select * from myf
where afm='043972218';

update pp
set teg='ΛΟΙΠΑ1'
where teg='ΛΟΙΠΑΚΟΥΒΑΣ';

select myf.afm, syn.ono, myf.lmo, myf.dat, myf.teg, myf.par, myf.aji, myf.fpa, myf.tposo, myf.tfpa, myf.partype
from myf
inner join syn on myf.afm=syn.afm
where teg = 'ΛΟΙΠΑ'
order by myf.afm, myf.dat;

select * from myf
where typ <> esex;

create table syn( afm TEXT, ono text);

insert into syn 
select distinct afm, lmo from pp
order by afm;

select * from myf
ORDER BY typ, myfc, teg, dat;

update pp set afm='094421389' where lmo like '%ΑΤΤΙΚΗ%' ; where id in (51, 182, 412, 577, 735);
--update pp set teg='ΛΟΙΠΑΚΟΥΒΑΣ' where afm='094019245';

select  myf.id, myf.typ, myf.myfc, myf.dat, myf.par, myf.afm, myf.tafm, myf.lmo, syn.afm, syn.ono 
from myf
left join syn on syn.afm=myf.afm
order by myf.afm, myf.typ, myf.myfc, myf.dat;

select *  from myf
where myfc='exp' and afm=''
order by lmo, id;


--Συγκεντρωτικά ανά myfc
SELECT tt.myfc, sum(pp.aji) as poso, sum(pp.fpa) as fpa
from tt
inner join pp on tt.teg=pp.teg
group by tt.myfc
order by esex, myfc;

--Αναλυτικά ανα teg
select * from myf
where teg in ('ΤΠΕ', 'ΠΙΣ');

--Συγκεντρωτικά ανά teg
SELECT myfc, teg, sum(aji) as poso, sum(fpa) as fpa, count(id) as recNo
from myf
group by teg
order by typ, teg;

--Συνολα Βιβλίου Εσοδων εξόδων
select typ, sum(aji) as poso, sum(fpa) as fpa
from pp
where dat between '2015-01-01' and '2015-12-31'
group by typ
order by typ;