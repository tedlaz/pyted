--Παραμετρική select χωρίς περιγραφές λογαριασμών
--Ισοζύγιο Λογιστικής από ημερομηνία (apo) έως ημερομηνία (eos)
SELECT lmo.lmo, sum(trd.xr) AS txr, sum(trd.pi) AS tpi,
sum(trd.xr) - sum(trd.pi) AS typ
FROM trd
INNER JOIN lmo ON trd.id_lmo = lmo.id
INNER JOIN tr ON tr.id = trd.id_tr
WHERE tr.dat BETWEEN '{apo}' AND '{eos}'
GROUP BY lmo.lmo
ORDER BY lmo.lmo;
