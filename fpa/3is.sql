--Sql για την ανάκτηση ισοζυγίου περιόδου της μορφής λογαριασμός --> υπόλοιπο
--πχ 24.00.023   100.00
--   70.00.023  -200.00
SELECT lmo.lmo, sum(trd.xr) - sum(trd.pi) AS yp
FROM trd
INNER JOIN lmo ON lmo.id=trd.id_lmo
INNER JOIN tr ON tr.id=trd.id_tr
WHERE substr(lmo.lmo, 1, 1) IN ('1', '2', '6', '7', '8')
 AND tr.dat BETWEEN '{apo}' AND '{eos}'
GROUP BY lmo.lmo
ORDER BY lmo.lmo;
