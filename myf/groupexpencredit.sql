--Grouped expenses credit
select afm as proafm, grdec(sum(aji) * -1) as poso, grdec(sum(fpa) * -1) as fpa,
  count(afm) as no, 'credit' as partype, '0' as miyp
from pp
where teg='ΠΑΓ' and (dat between '%s' and '%s')
group by afm
order by afm;
