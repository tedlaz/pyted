select sum(xr), sum(pi), sum(xr)-sum(pi) as d
from logistiki_lmo
inner join logistiki_tran_d on logistiki_lmo.id=logistiki_tran_d.lmos_id
where code like '3%';