select
case
  when dat between '2016-01-01' and '2016-03-31' then '2016-03-31'
  when dat between '2016-04-01' and '2016-06-30' then '2016-06-30'
  when dat between '2016-07-01' and '2016-09-30' then '2016-09-30'
  when dat between '2016-10-01' and '2016-12-31' then '2016-12-31'
  else '000-00-00'
end as trimino,
case
  when length(afm) < 9 and eee=1 and typ=1 then '3.cashregister'
  when length(afm) = 9 and eee=1 and typ=1 then '1.revenue'
  when length(afm) < 9 and eee=1 and typ=2 then '0.error'
  when length(afm) = 9 and eee=1 and typ=2 then '2.expense'
  else '0.ektos'
end as typos,
eee, typ, afm,note, count(aji), sum(aji), sum(fpa),  sum(maji), sum(mfpa)
from ee
group by trimino, typos, eee, typ, afm, note
order by trimino, typos, eee, typ, afm, note