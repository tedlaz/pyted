select tt.myfc,
case when (tt.myfc='cash' or tt.myfc='exp0' or tt.myfc='rev0') then '000' else pp.afm end as tafm,
sum(pp.aji) * tt.prosimo as poso,
sum(pp.fpa) * tt.prosimo as fpa,
count(afm) as no,
case when tt.prosimo=1 then 'normal' else 'credit' end as partype
from pp
inner join tt on tt.teg=pp.teg
where pp.dat between '2015-01-01' and '2015-12-31'
group by tt.myfc, tafm, tt.prosimo
order by tt.esex, tt.myfc, pp.afm, tt.prosimo desc;
