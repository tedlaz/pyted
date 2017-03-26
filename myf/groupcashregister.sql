--Group Cash Register
select '' as tamNo, grdec(sum(aji)) as poso, grdec(sum(fpa)) as fpa
from pp
where (teg='ΑΠΛ' or teg='ΑΠΥ' or teg='ΕΠΛ')  and dat between '%s' and '%s';
