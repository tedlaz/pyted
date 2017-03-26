select code, lmos_id, sum(xr), sum(pi), sum(xr)-sum(pi) as d
from logistiki_lmo
inner join logistiki_tran_d on logistiki_lmo.id=logistiki_tran_d.lmos_id
where code='38.00.00.0000'
group by lmos_id;