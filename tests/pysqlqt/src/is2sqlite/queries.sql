select lmo.lmo, sum(trd.xr) as txr, sum(trd.pi) as tpi, sum(trd.xr) - sum(trd.pi) as typ
From trd inner join lmo on trd.id_lmo = lmo.id group by lmo
union 
select substr(lmo.lmo, 1, 8) as lmo3, sum(trd.xr) , sum(trd.pi) , sum(trd.xr) - sum(trd.pi) as typ
from trd inner join lmo on trd.id_lmo = lmo.id group by lmo3
union 
select substr(lmo.lmo, 1, 5) as lmo2, sum(trd.xr) , sum(trd.pi) , sum(trd.xr) - sum(trd.pi) as typ
from trd inner join lmo on trd.id_lmo = lmo.id group by lmo2
union 
select substr(lmo.lmo, 1, 2) as lmo1, sum(trd.xr) , sum(trd.pi) , sum(trd.xr) - sum(trd.pi) as typ
from trd inner join lmo on trd.id_lmo = lmo.id group by lmo1
union 
select substr(lmo.lmo, 1, 1) as lmo0, sum(trd.xr) , sum(trd.pi) , sum(trd.xr) - sum(trd.pi) as typ
from trd inner join lmo on trd.id_lmo = lmo.id
group by lmo0

SELECT tr.id, tr.dat, tr.par, lmo.lmo, lmo.lmop, trd.xr, trd.pi
FROM tr
INNER JOIN trd ON tr.id = trd.id_tr
INNER JOIN lmo ON lmo.id = trd.id_lmo

select trd.id, trd.id_tr, lmo.lmo, lmo.lmop, trd.xr, trd.pi
FROM trd INNER JOIN lmo ON lmo.id=trd.id_lmo
where trd.id_tr in (select trd.id_tr from trd INNER JOIN lmo  ON lmo.id=trd.id_lmo where lmo.lmo like '54.00.29%')
@
%5s %5s %12s %12.2f %12.2f
