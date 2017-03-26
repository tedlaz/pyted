--Sql για την ανάκτηση του υπολοίπου φπα περιόδου
--(χρεωστικό θετικό, πιστωτικό αρνητικό)
SELECT (sum(trd.xr) - sum(trd.pi)) * -1 AS yp
FROM trd
INNER JOIN lmo ON lmo.id=trd.id_lmo
INNER JOIN tr ON tr.id=trd.id_tr
WHERE substr(lmo.lmo, 1, 7) BETWEEN '54.00.0' AND '54.00.8'
 AND tr.dat BETWEEN '{apo}' AND '{eos}'
ORDER BY lmo.lmo;
