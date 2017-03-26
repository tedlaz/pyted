PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
insert into mpar ("id", "par", "parp") values ('1', 'mer', 'Ημέρες εργασίας');
insert into mpar ("id", "par", "parp") values ('2', 'mad', 'Ημέρες κανονικής άδειας');
insert into mpar ("id", "par", "parp") values ('3', 'madx', 'Ημέρες Άδειας χωρίς αποδοχές');
insert into mpar ("id", "par", "parp") values ('4', 'map', 'Ημέρες αδικαιολόγητης απουσίας');
insert into mpar ("id", "par", "parp") values ('5', 'mky', 'Κυριακές-Αργίες μέρες(Προσαύξηση)');
insert into mpar ("id", "par", "parp") values ('6', 'mas', 'Ημέρες ασθένειας');
insert into mpar ("id", "par", "parp") values ('7', 'mas3', 'Ασθένεια μέχρι 3 ημέρες');
insert into mpar ("id", "par", "parp") values ('8', 'mas3m', 'Ημέρες ασθένειας πάνω απο 3');
insert into mpar ("id", "par", "parp") values ('20', 'ony', 'Νυχτερινές ώρες(προσαύξηση)');
insert into mpar ("id", "par", "parp") values ('21', 'oky', 'Κυριακές-Αργίες ώρες(Προσαύξηση)');
insert into mpar ("id", "par", "parp") values ('22', 'oyp', 'Υπερωρίες ώρες');
insert into mpar ("id", "par", "parp") values ('23', 'oypn', 'Υπερωρίες ώρες νύχτα(προσαύξηση)');
insert into mpar ("id", "par", "parp") values ('24', 'oypκ', 'Υπερωρίες ώρες Κυριακές-Αργίες(προσαύξηση)');
insert into mpar ("id", "par", "parp") values ('50', 'am', 'Μικτές αποδοχές');
insert into mpar ("id", "par", "parp") values ('51', 'af', 'Φορολογητέες αποδοχές');
insert into mpar ("id", "par", "parp") values ('52', 'ap', 'Aποδοχές πληρωτέες');
insert into mpar ("id", "par", "parp") values ('70', 'kfa', 'Φόρος που αναλογεί');
insert into mpar ("id", "par", "parp") values ('71', 'kf', 'Φόρος που παρακρατήθηκε');
insert into mpar ("id", "par", "parp") values ('72', 'kika', 'Κρατήσεις ΙΚΑ');
insert into mpar ("id", "par", "parp") values ('73', 'kikan', 'Κρατήσεις ΙΚΑ εργαζομένου');
insert into mpar ("id", "par", "parp") values ('74', 'kikae', 'Κρατήσεις ΙΚΑ εργοδότη');
insert into mpar ("id", "par", "parp") values ('75', 'kea', 'Εισφορά αλληλεγγύης');
insert into mpar ("id", "par", "parp") values ('100', 'pika', 'Ποσοστό ΙΚΑ');
insert into mpar ("id", "par", "parp") values ('101', 'pikan', 'Ποσοστό ΙΚΑ εργαζόμενου');
insert into mpar ("id", "par", "parp") values ('102', 'pikae', 'Ποσοστό ΙΚΑ εργοδότη');
insert into mpar ("id", "par", "parp") values ('900', 'ten', 'Συνολικές κρατήσεις εργαζομένου');
insert into mpar ("id", "par", "parp") values ('901', 'tet', 'Συνολικές κρατήσεις εργοδότη');
insert into mpar ("id", "par", "parp") values ('902', 'tk', 'Συνολικό κόστος');
INSERT INTO "apastyp" VALUES(1,'Πλήρης');
INSERT INTO "apastyp" VALUES(2,'Μερική');
INSERT INTO "apastyp" VALUES(3,'Εκ περιτροπής');
INSERT INTO "atyp" VALUES(1,'Οικιοθελής αποχώρηση');
INSERT INTO "atyp" VALUES(2,'Απόλυση');
INSERT INTO "atyp" VALUES(3,'Συνταξιοδότηση');
INSERT INTO "oik" VALUES(1,'Άγαμος');
INSERT INTO "oik" VALUES(2,'Έγγαμος');
INSERT INTO "oik" VALUES(3,'Διαζευγμένος');
INSERT INTO "sex" VALUES(1,'Άνδρας');
INSERT INTO "sex" VALUES(2,'Γυναίκα');
INSERT INTO "symbtyp" VALUES(1,'Αορίστου χρόνου');
INSERT INTO "symbtyp" VALUES(2,'Ορισμένου χρόνου');
INSERT INTO "symbtyp" VALUES(3,'Έργου');
INSERT INTO "taftyp" VALUES(1,'Αστυνομική');
INSERT INTO "taftyp" VALUES(2,'Διαβατήριο');
INSERT INTO "taftyp" VALUES(3,'Άδεια οδήγησης');
INSERT INTO "cop" VALUES(1,'Κεντρικό','');
INSERT INTO "aptyp" VALUES(1,'Ημερομίσθιος');
INSERT INTO "aptyp" VALUES(2,'Μισθωτός');
INSERT INTO "ertyp" VALUES(1,'Εργάτης');
INSERT INTO "ertyp" VALUES(2,'Υπάλληλος');
INSERT INTO "gnoseis" VALUES(1,'Ανώτατες');
INSERT INTO "gnoseis" VALUES(2,'Απόφοιτος Γενικού Λυκείου');
INSERT INTO "mist" VALUES(1,'Τακτικές αποδοχές');
INSERT INTO "mist" VALUES(2,'Αποδοχές Υπαλλήλων ΝΠΔΔ');
INSERT INTO "mist" VALUES(3,'Δώρο Χριστουγέννων');
INSERT INTO "mist" VALUES(4,'Δώρο Πάσχα');
INSERT INTO "mist" VALUES(5,'Επίδομα Αδείας');
INSERT INTO "mist" VALUES(6,'Επίδομα Ισολογισμού');
INSERT INTO "mist" VALUES(7,'Αποδοχές αδειών εποχικών απασχολουμένων');
INSERT INTO "mist" VALUES(8,'Αποδοχές Ασθενείας');
INSERT INTO "mist" VALUES(9,'Αναδρομικές Αποδοχές');
INSERT INTO "mist" VALUES(10,'Bonus');
INSERT INTO "mist" VALUES(11,'Υπερωρίες');
INSERT INTO "mist" VALUES(12,'Αμοιβή με το κομμάτι (ΦΑΣΟΝ)');
INSERT INTO "mist" VALUES(13,'Τεκμαρτές αποδοχές');
INSERT INTO "mist" VALUES(14,'Λοιπές Αποδοχές');
INSERT INTO "per" VALUES(1,'Ιανουάριος');
INSERT INTO "per" VALUES(2,'Φεβρουάριος');
INSERT INTO "per" VALUES(3,'Μάρτιος');
INSERT INTO "per" VALUES(4,'Απρίλιος');
INSERT INTO "per" VALUES(5,'Μάϊος');
INSERT INTO "per" VALUES(6,'Ιούνιος');
INSERT INTO "per" VALUES(7,'Ιούλιος');
INSERT INTO "per" VALUES(8,'Αύγουστος');
INSERT INTO "per" VALUES(9,'Σεπτέμβριος');
INSERT INTO "per" VALUES(10,'Οκτώβριος');
INSERT INTO "per" VALUES(11,'Νοέμβριος');
INSERT INTO "per" VALUES(12,'Δεκέμβριος');

INSERT INTO "kratos" VALUES(1,'Ελλάδα');
INSERT INTO "kratos" VALUES(2,'Αγία Λουκία');
INSERT INTO "kratos" VALUES(3,'Άγιος Βικέντιος και Γρεναδίνες');
INSERT INTO "kratos" VALUES(4,'Άγιος Χριστόφορος και Νέβις');
INSERT INTO "kratos" VALUES(5,'Αγκόλα');
INSERT INTO "kratos" VALUES(6,'Αζερμπαϊτζάν');
INSERT INTO "kratos" VALUES(7,'Αίγυπτος');
INSERT INTO "kratos" VALUES(8,'Αιθιοπία');
INSERT INTO "kratos" VALUES(9,'Αϊτή');
INSERT INTO "kratos" VALUES(10,'Ακτή Ελεφαντοστού');
INSERT INTO "kratos" VALUES(11,'Αλβανία');
INSERT INTO "kratos" VALUES(12,'Αλγερία');
INSERT INTO "kratos" VALUES(13,'Αμερικανική Σαμόα');
INSERT INTO "kratos" VALUES(14,'Ανατολικό Τιμόρ');
INSERT INTO "kratos" VALUES(15,'Ανγκουίλλα');
INSERT INTO "kratos" VALUES(16,'Ανδόρρα');
INSERT INTO "kratos" VALUES(17,'Αντίγκουα και Μπαρμπούντα');
INSERT INTO "kratos" VALUES(18,'Αργεντινή');
INSERT INTO "kratos" VALUES(19,'Αρμενία');
INSERT INTO "kratos" VALUES(20,'Αυστραλία');
INSERT INTO "kratos" VALUES(21,'Αυστρία');
INSERT INTO "kratos" VALUES(22,'Αφγανιστάν');
INSERT INTO "kratos" VALUES(23,'Βανουάτου');
INSERT INTO "kratos" VALUES(24,'Βατικανό');
INSERT INTO "kratos" VALUES(25,'Βέλγιο');
INSERT INTO "kratos" VALUES(26,'Βενεζουέλα');
INSERT INTO "kratos" VALUES(27,'Βιετνάμ');
INSERT INTO "kratos" VALUES(28,'Βολιβία');
INSERT INTO "kratos" VALUES(29,'Βόρεια Κορέα');
INSERT INTO "kratos" VALUES(30,'Βοσνία-Ερζεγοβίνη');
INSERT INTO "kratos" VALUES(31,'Βουλγαρία');
INSERT INTO "kratos" VALUES(32,'Βραζιλία');
INSERT INTO "kratos" VALUES(33,'Γαλλία');
INSERT INTO "kratos" VALUES(34,'Γερμανία');
INSERT INTO "kratos" VALUES(35,'Γεωργία');
INSERT INTO "kratos" VALUES(36,'Γκάμπια');
INSERT INTO "kratos" VALUES(37,'Γκαμπόν');
INSERT INTO "kratos" VALUES(38,'Γκάνα');
INSERT INTO "kratos" VALUES(39,'Γουατεμάλα');
INSERT INTO "kratos" VALUES(40,'Γουιάνα');
INSERT INTO "kratos" VALUES(41,'Γουινέα');
INSERT INTO "kratos" VALUES(42,'Γουινέα-Μπισσάου');
INSERT INTO "kratos" VALUES(43,'Γρενάδα');
INSERT INTO "kratos" VALUES(44,'Δανία');
INSERT INTO "kratos" VALUES(45,'Δομινικανή Δημοκρατία');
INSERT INTO "kratos" VALUES(46,'Ελ Σαλβαδόρ');
INSERT INTO "kratos" VALUES(47,'Ελβετία');
INSERT INTO "kratos" VALUES(48,'Ενωμένα Αραβικά Εμιράτα');
INSERT INTO "kratos" VALUES(49,'Ερυθραία');
INSERT INTO "kratos" VALUES(50,'Εσθονία');
INSERT INTO "kratos" VALUES(51,'Ζάμπια');
INSERT INTO "kratos" VALUES(52,'Ζιμπάμπουε');
INSERT INTO "kratos" VALUES(53,'Ηνωμένες Πολιτείες');
INSERT INTO "kratos" VALUES(54,'Ηνωμένο Βασίλειο');
INSERT INTO "kratos" VALUES(55,'Ιαπωνία');
INSERT INTO "kratos" VALUES(56,'Ινδία');
INSERT INTO "kratos" VALUES(57,'Ινδονησία');
INSERT INTO "kratos" VALUES(58,'Ιορδανία');
INSERT INTO "kratos" VALUES(59,'Ιράκ');
INSERT INTO "kratos" VALUES(60,'Ιράν');
INSERT INTO "kratos" VALUES(61,'Ιρλανδία');
INSERT INTO "kratos" VALUES(62,'Ισημερινή Γουινέα');
INSERT INTO "kratos" VALUES(63,'Ισημερινός');
INSERT INTO "kratos" VALUES(64,'Ισλανδία');
INSERT INTO "kratos" VALUES(65,'Ισπανία');
INSERT INTO "kratos" VALUES(66,'Ισραήλ');
INSERT INTO "kratos" VALUES(67,'Ιταλία');
INSERT INTO "kratos" VALUES(68,'Καζακστάν');
INSERT INTO "kratos" VALUES(69,'Καμερούν');
INSERT INTO "kratos" VALUES(70,'Καμπότζη');
INSERT INTO "kratos" VALUES(71,'Καναδάς');
INSERT INTO "kratos" VALUES(72,'Κατάρ');
INSERT INTO "kratos" VALUES(73,'Κεντροαφρικανική Δημοκρατία');
INSERT INTO "kratos" VALUES(74,'Κένυα');
INSERT INTO "kratos" VALUES(75,'Κίνα');
INSERT INTO "kratos" VALUES(76,'Κιργιζία');
INSERT INTO "kratos" VALUES(77,'Κιριμπάτι');
INSERT INTO "kratos" VALUES(78,'Κολομβία');
INSERT INTO "kratos" VALUES(79,'Κομόρες');
INSERT INTO "kratos" VALUES(80,'Κογκό');
INSERT INTO "kratos" VALUES(81,'Κόστα Ρίκα');
INSERT INTO "kratos" VALUES(82,'Κούβα');
INSERT INTO "kratos" VALUES(83,'Κουβέιτ');
INSERT INTO "kratos" VALUES(84,'Κροατία');
INSERT INTO "kratos" VALUES(85,'Κύπρος');
INSERT INTO "kratos" VALUES(86,'Λάος');
INSERT INTO "kratos" VALUES(87,'Λεσόθο');
INSERT INTO "kratos" VALUES(88,'Λεττονία');
INSERT INTO "kratos" VALUES(89,'Λευκορωσία');
INSERT INTO "kratos" VALUES(90,'Λίβανος');
INSERT INTO "kratos" VALUES(91,'Λιβερία');
INSERT INTO "kratos" VALUES(92,'Λιβύη');
INSERT INTO "kratos" VALUES(93,'Λιθουανία');
INSERT INTO "kratos" VALUES(94,'Λίχτενσταϊν');
INSERT INTO "kratos" VALUES(95,'Λουξεμβούργο');
INSERT INTO "kratos" VALUES(96,'Μαδαγασκάρη');
INSERT INTO "kratos" VALUES(97,'Μαλαισία');
INSERT INTO "kratos" VALUES(98,'Μαλάουι');
INSERT INTO "kratos" VALUES(99,'Μαλδίβες');
INSERT INTO "kratos" VALUES(100,'Μάλι');
INSERT INTO "kratos" VALUES(101,'Μάλτα');
INSERT INTO "kratos" VALUES(102,'Μαρόκο');
INSERT INTO "kratos" VALUES(103,'Μάρσαλ (Νήσοι)');
INSERT INTO "kratos" VALUES(104,'Μαυρίκιος');
INSERT INTO "kratos" VALUES(105,'Μαυριτανία');
INSERT INTO "kratos" VALUES(106,'Μεξικό');
INSERT INTO "kratos" VALUES(107,'Μιανμάρ');
INSERT INTO "kratos" VALUES(108,'Μογγολία');
INSERT INTO "kratos" VALUES(109,'Μοζαμβίκη');
INSERT INTO "kratos" VALUES(110,'Μολδαβία');
INSERT INTO "kratos" VALUES(111,'Μονακό');
INSERT INTO "kratos" VALUES(112,'Μπανγκλαντές');
INSERT INTO "kratos" VALUES(113,'Μπαχάμες');
INSERT INTO "kratos" VALUES(114,'Μπαχρέιν');
INSERT INTO "kratos" VALUES(115,'Μπελίζ');
INSERT INTO "kratos" VALUES(116,'Μπενίν');
INSERT INTO "kratos" VALUES(117,'Μποτσουάνα');
INSERT INTO "kratos" VALUES(118,'Μπουρκίνα');
INSERT INTO "kratos" VALUES(119,'Μπουρούντι');
INSERT INTO "kratos" VALUES(120,'Μπρουνέι');
INSERT INTO "kratos" VALUES(121,'Ναμίμπια');
INSERT INTO "kratos" VALUES(122,'Ναουρού');
INSERT INTO "kratos" VALUES(123,'Νέα Ζηλανδία');
INSERT INTO "kratos" VALUES(124,'Νέα Καληδονία Νέα Καληδονία');
INSERT INTO "kratos" VALUES(125,'Νεπάλ');
INSERT INTO "kratos" VALUES(126,'Νήσοι Κουκ');
INSERT INTO "kratos" VALUES(127,'Νίγηρας');
INSERT INTO "kratos" VALUES(128,'Νιγηρία');
INSERT INTO "kratos" VALUES(129,'Νικαράγουα');
INSERT INTO "kratos" VALUES(130,'Νιούε');
INSERT INTO "kratos" VALUES(131,'Νορβηγία');
INSERT INTO "kratos" VALUES(132,'Νότια Αφρική');
INSERT INTO "kratos" VALUES(133,'Νότια Κορέα');
INSERT INTO "kratos" VALUES(134,'Ντομίνικα');
INSERT INTO "kratos" VALUES(135,'Ολλανδία');
INSERT INTO "kratos" VALUES(136,'Ομάν');
INSERT INTO "kratos" VALUES(137,'Ονδούρα');
INSERT INTO "kratos" VALUES(138,'Ουγγαρία');
INSERT INTO "kratos" VALUES(139,'Ουγκάντα');
INSERT INTO "kratos" VALUES(140,'Ουζμπεκιστάν');
INSERT INTO "kratos" VALUES(141,'Ουρουγουάη');
INSERT INTO "kratos" VALUES(142,'Ουκρανία');
INSERT INTO "kratos" VALUES(143,'Πακιστάν');
INSERT INTO "kratos" VALUES(144,'Παλάου');
INSERT INTO "kratos" VALUES(145,'Παναμάς');
INSERT INTO "kratos" VALUES(146,'Παπούα Νέα Γουινέα');
INSERT INTO "kratos" VALUES(147,'Παραγουάη');
INSERT INTO "kratos" VALUES(148,'Περού');
INSERT INTO "kratos" VALUES(149,'Πολωνία');
INSERT INTO "kratos" VALUES(150,'Πορτογαλία');
INSERT INTO "kratos" VALUES(151,'Πουέρτο Ρίκο');
INSERT INTO "kratos" VALUES(152,'Πράσινο Ακρωτήριo');
INSERT INTO "kratos" VALUES(153,'ΠΓΔΜ');
INSERT INTO "kratos" VALUES(154,'Ρουμανία');
INSERT INTO "kratos" VALUES(155,'Ρωσία');
INSERT INTO "kratos" VALUES(156,'Σαμόα');
INSERT INTO "kratos" VALUES(157,'Σάο Τομέ και Πρίνσιπε');
INSERT INTO "kratos" VALUES(158,'Σαουδική Αραβία');
INSERT INTO "kratos" VALUES(159,'Σενεγάλη');
INSERT INTO "kratos" VALUES(160,'Σερβία');
INSERT INTO "kratos" VALUES(161,'Σεϋχέλλες');
INSERT INTO "kratos" VALUES(162,'Σιγκαπούρη');
INSERT INTO "kratos" VALUES(163,'Σιέρα Λεόνε');
INSERT INTO "kratos" VALUES(164,'Σλοβακία');
INSERT INTO "kratos" VALUES(165,'Σλοβενία');
INSERT INTO "kratos" VALUES(166,'Σολομώντος(Νησιά)');
INSERT INTO "kratos" VALUES(167,'Σομαλία');
INSERT INTO "kratos" VALUES(168,'Σουαζιλάνδη');
INSERT INTO "kratos" VALUES(169,'Σουδάν');
INSERT INTO "kratos" VALUES(170,'Σουηδία');
INSERT INTO "kratos" VALUES(171,'Σουρινάμ');
INSERT INTO "kratos" VALUES(172,'Σρι Λάνκα');
INSERT INTO "kratos" VALUES(173,'Συρία');
INSERT INTO "kratos" VALUES(174,'Ταϊβάν');
INSERT INTO "kratos" VALUES(175,'Ταϊλάνδη');
INSERT INTO "kratos" VALUES(176,'Τανζανία');
INSERT INTO "kratos" VALUES(177,'Τατζικιστάν');
INSERT INTO "kratos" VALUES(178,'Τζαμάικα');
INSERT INTO "kratos" VALUES(179,'Τζιμπουτί');
INSERT INTO "kratos" VALUES(180,'Τόγκο');
INSERT INTO "kratos" VALUES(181,'Τόνγκα');
INSERT INTO "kratos" VALUES(182,'Τουβαλού');
INSERT INTO "kratos" VALUES(183,'Τουρκία');
INSERT INTO "kratos" VALUES(184,'Τουρκμενιστάν');
INSERT INTO "kratos" VALUES(185,'Τρινιντάντ και Τομπάγκο');
INSERT INTO "kratos" VALUES(186,'Τσαντ');
INSERT INTO "kratos" VALUES(187,'Τσεχία');
INSERT INTO "kratos" VALUES(188,'Τυνησία');
INSERT INTO "kratos" VALUES(189,'Υεμένη');
INSERT INTO "kratos" VALUES(190,'Υπερδνειστερία');
INSERT INTO "kratos" VALUES(191,'Φιλιππίνες');
INSERT INTO "kratos" VALUES(192,'Φινλανδία');
INSERT INTO "kratos" VALUES(193,'Φίτζι');
INSERT INTO "kratos" VALUES(194,'Χιλή');
INSERT INTO "ergpstype" VALUES(1,'Αρχική πρόσληψη');
INSERT INTO "ergpstype" VALUES(2,'Αλλαγή ωραρίου');
INSERT INTO "ergpstype" VALUES(3,'Αλλαγή μισθού');
COMMIT;
