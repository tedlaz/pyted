--Grouped Revenues credit
select afm as pelafm, grdec(sum(aji) * -1) as poso,
 grdec(sum(fpa) * -1) as fpa, count(afm) as no, 'credit' as partype
from pp
where (teg='ΠΙΣ' or teg='ΤΠΕ')  and (dat between '%s' and '%s')
group by afm
order by afm;
