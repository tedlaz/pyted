select f2.cod, sum(trd.xr) as txr, sum(trd.pi) as tpi
from trd
inner join lmo on lmo.id=trd.id_lmo
inner join f2 on f2.lmos=lmo.lmo
inner join tr on tr.id=trd.id_tr
WHERE tr.dat BETWEEN '2016-04-01' AND '2016-06-30'
group by f2.cod
