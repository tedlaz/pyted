BEGIN TRANSACTION;
insert into ki values ('1', '7', 'normal', 'ell', '2016-09-20', 'ΤΔΑ233', '046949583', 1, NULL);
insert into ki values ('2', '26', 'normal', 'ell', '2016-09-20', 'ΤΔΑ56698', '055998669', 1, NULL);
insert into ki values ('3', '7', 'credit', 'ell', '2016-09-22', 'ΠΤ15', '046949583', 1, NULL);
insert into kid values ('1', '1', '70.00', '24', '100', '24');
insert into kid values ('2', '2', '20.01', '13', '100', '13');
insert into kid values ('3', '3', '70.00', '24', '50', '12');
COMMIT;
