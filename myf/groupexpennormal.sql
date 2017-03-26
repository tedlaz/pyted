--Grouped expenses normal
select afm as proafm, grdec(sum(aji)) as poso, grdec(sum(fpa)) as fpa,
   count(afm) as no, 'normal' as partype, '0' as miyp
from pp
where (teg='ΤΑΓ' or teg='ΛΟΙΠΑ1') and (dat between '%s' and '%s')
group by afm
order by afm;
