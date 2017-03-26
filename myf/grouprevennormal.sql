--Grouped Revenues normal
select afm as pelafm, grdec(sum(aji)) as poso,
 grdec(sum(fpa)) as fpa, count(afm) as no, 'normal' as partype
from pp
where (teg='ΤΠΛ' or teg='ΤΠΥ')  and (dat between '%s' and '%s')
group by afm
order by afm;
