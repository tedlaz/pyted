BEGIN TRANSACTION;
INSERT INTO diam VALUES (1, 'Φροντιστήριο', 0, 0, 100,'Νεόπουλος', 'Κρητικού');
INSERT INTO diam VALUES (2, 'Διαμ1', 1, 1, 100, 'Νεόπουλος', 'Άγνωστος');
INSERT INTO diam VALUES (3, 'Διαμ2', 2, 1, 100, 'Νεόπουλος', 'Άγνωστος');
INSERT INTO diam VALUES (4, 'Διαμ3', 3, 2, 100, 'Νεόπουλος', 'Άγνωστος');
INSERT INTO diam VALUES (5, 'Διαμ4', 4, 2, 100, 'Νεόπουλος', 'Άγνωστος');
INSERT INTO diam VALUES (6, 'Διαμ5', 5, 3, 100, 'Λάζαρος', 'Λάζαρος');
INSERT INTO dap VALUES(1,'Θέρμανση');
INSERT INTO dap VALUES(2,'Ασανσέρ - ΔΕΗ');
INSERT INTO dap VALUES(3,'Καθαριότητα');
INSERT INTO dap VALUES(4,'Αποχέτευση');
insert into xiliosta values ('1', '4', '1', '270');
insert into xiliosta values ('2', '1', '2', '204');
insert into xiliosta values ('3', '2', '2', '139');
insert into xiliosta values ('4', '3', '2', '204');
insert into xiliosta values ('5', '4', '2', '150');
insert into xiliosta values ('6', '1', '3', '159');
insert into xiliosta values ('7', '2', '3', '108');
insert into xiliosta values ('8', '3', '3', '159');
insert into xiliosta values ('9', '4', '3', '115');
insert into xiliosta values ('10', '1', '4', '243');
insert into xiliosta values ('11', '2', '4', '249');
insert into xiliosta values ('12', '3', '4', '243');
insert into xiliosta values ('13', '4', '4', '178');
insert into xiliosta values ('14', '1', '5', '120');
insert into xiliosta values ('15', '2', '5', '122');
insert into xiliosta values ('16', '3', '5', '120');
insert into xiliosta values ('17', '4', '5', '87');
insert into xiliosta values ('18', '1', '6', '274');
insert into xiliosta values ('19', '2', '6', '382');
insert into xiliosta values ('20', '3', '6', '274');
insert into xiliosta values ('21', '4', '6', '200');
COMMIT;