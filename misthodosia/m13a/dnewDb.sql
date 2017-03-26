BEGIN TRANSACTION;
CREATE TABLE "auth_permission" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
);
INSERT INTO "auth_permission" VALUES(1,'Can add group',2,'add_group');
INSERT INTO "auth_permission" VALUES(2,'Can add permission',1,'add_permission');
INSERT INTO "auth_permission" VALUES(3,'Can add user',3,'add_user');
INSERT INTO "auth_permission" VALUES(4,'Can change group',2,'change_group');
INSERT INTO "auth_permission" VALUES(5,'Can change permission',1,'change_permission');
INSERT INTO "auth_permission" VALUES(6,'Can change user',3,'change_user');
INSERT INTO "auth_permission" VALUES(7,'Can delete group',2,'delete_group');
INSERT INTO "auth_permission" VALUES(8,'Can delete permission',1,'delete_permission');
INSERT INTO "auth_permission" VALUES(9,'Can delete user',3,'delete_user');
INSERT INTO "auth_permission" VALUES(10,'Can add content type',4,'add_contenttype');
INSERT INTO "auth_permission" VALUES(11,'Can change content type',4,'change_contenttype');
INSERT INTO "auth_permission" VALUES(12,'Can delete content type',4,'delete_contenttype');
INSERT INTO "auth_permission" VALUES(13,'Can add session',5,'add_session');
INSERT INTO "auth_permission" VALUES(14,'Can change session',5,'change_session');
INSERT INTO "auth_permission" VALUES(15,'Can delete session',5,'delete_session');
INSERT INTO "auth_permission" VALUES(16,'Can add site',6,'add_site');
INSERT INTO "auth_permission" VALUES(17,'Can change site',6,'change_site');
INSERT INTO "auth_permission" VALUES(18,'Can delete site',6,'delete_site');
INSERT INTO "auth_permission" VALUES(19,'Can add log entry',7,'add_logentry');
INSERT INTO "auth_permission" VALUES(20,'Can change log entry',7,'change_logentry');
INSERT INTO "auth_permission" VALUES(21,'Can delete log entry',7,'delete_logentry');
INSERT INTO "auth_permission" VALUES(22,'Can add Αποδοχές εργαζομένου',24,'add_promis');
INSERT INTO "auth_permission" VALUES(23,'Can add Αποχώρηση εργαζομένου',26,'add_apo');
INSERT INTO "auth_permission" VALUES(24,'Can add Δίμηνο',12,'add_dimino');
INSERT INTO "auth_permission" VALUES(25,'Can add Ειδικότητα',15,'add_eid');
INSERT INTO "auth_permission" VALUES(26,'Can add Εργαζόμενος βασικά στοιχεία',17,'add_fpr');
INSERT INTO "auth_permission" VALUES(27,'Can add Εργαζόμενος πρόσληψη',22,'add_pro');
INSERT INTO "auth_permission" VALUES(28,'Can add Εργαζόμενος πρόσληψη Σύμβαση Εργασίας',23,'add_symb');
INSERT INTO "auth_permission" VALUES(29,'Can add Εργαζόμενος συμπληρωματικά στοιχεία',18,'add_fprd');
INSERT INTO "auth_permission" VALUES(30,'Can add Εταιρεία',9,'add_co');
INSERT INTO "auth_permission" VALUES(31,'Can add Λεπτομέρεια μισθοδοσίας',35,'add_misd');
INSERT INTO "auth_permission" VALUES(32,'Can add Μισθοδοσία',33,'add_mis');
INSERT INTO "auth_permission" VALUES(33,'Can add Μονάδα χρόνου',27,'add_mxr');
INSERT INTO "auth_permission" VALUES(34,'Can add Παρουσία',29,'add_par');
INSERT INTO "auth_permission" VALUES(35,'Can add Παρουσία F',31,'add_parf');
INSERT INTO "auth_permission" VALUES(36,'Can add Παρουσία αναλυτικά',30,'add_pard');
INSERT INTO "auth_permission" VALUES(37,'Can add Περίοδος',14,'add_period');
INSERT INTO "auth_permission" VALUES(38,'Can add Πρόγραμμα εργασίας',21,'add_orar');
INSERT INTO "auth_permission" VALUES(39,'Can add Τρίμηνο',13,'add_trimino');
INSERT INTO "auth_permission" VALUES(40,'Can add Τύπος Σύμβασης',20,'add_symtyp');
INSERT INTO "auth_permission" VALUES(41,'Can add Τύπος αποδοχών',19,'add_aptyp');
INSERT INTO "auth_permission" VALUES(42,'Can add Τύπος αποχώρησης',25,'add_apotyp');
INSERT INTO "auth_permission" VALUES(43,'Can add Τύπος επιχείρησης',8,'add_cotyp');
INSERT INTO "auth_permission" VALUES(44,'Can add Τύπος μισθοδοσίας',32,'add_mist');
INSERT INTO "auth_permission" VALUES(45,'Can add Τύπος μισθολογικού δεδομένου',34,'add_mtyp');
INSERT INTO "auth_permission" VALUES(46,'Can add Τύπος παρουσίας',28,'add_ptyp');
INSERT INTO "auth_permission" VALUES(47,'Can add Υποκατάστημα',10,'add_coy');
INSERT INTO "auth_permission" VALUES(48,'Can add Φύλο',16,'add_sex');
INSERT INTO "auth_permission" VALUES(49,'Can add Χρήση',11,'add_xrisi');
INSERT INTO "auth_permission" VALUES(50,'Can change Αποδοχές εργαζομένου',24,'change_promis');
INSERT INTO "auth_permission" VALUES(51,'Can change Αποχώρηση εργαζομένου',26,'change_apo');
INSERT INTO "auth_permission" VALUES(52,'Can change Δίμηνο',12,'change_dimino');
INSERT INTO "auth_permission" VALUES(53,'Can change Ειδικότητα',15,'change_eid');
INSERT INTO "auth_permission" VALUES(54,'Can change Εργαζόμενος βασικά στοιχεία',17,'change_fpr');
INSERT INTO "auth_permission" VALUES(55,'Can change Εργαζόμενος πρόσληψη',22,'change_pro');
INSERT INTO "auth_permission" VALUES(56,'Can change Εργαζόμενος πρόσληψη Σύμβαση Εργασίας',23,'change_symb');
INSERT INTO "auth_permission" VALUES(57,'Can change Εργαζόμενος συμπληρωματικά στοιχεία',18,'change_fprd');
INSERT INTO "auth_permission" VALUES(58,'Can change Εταιρεία',9,'change_co');
INSERT INTO "auth_permission" VALUES(59,'Can change Λεπτομέρεια μισθοδοσίας',35,'change_misd');
INSERT INTO "auth_permission" VALUES(60,'Can change Μισθοδοσία',33,'change_mis');
INSERT INTO "auth_permission" VALUES(61,'Can change Μονάδα χρόνου',27,'change_mxr');
INSERT INTO "auth_permission" VALUES(62,'Can change Παρουσία',29,'change_par');
INSERT INTO "auth_permission" VALUES(63,'Can change Παρουσία F',31,'change_parf');
INSERT INTO "auth_permission" VALUES(64,'Can change Παρουσία αναλυτικά',30,'change_pard');
INSERT INTO "auth_permission" VALUES(65,'Can change Περίοδος',14,'change_period');
INSERT INTO "auth_permission" VALUES(66,'Can change Πρόγραμμα εργασίας',21,'change_orar');
INSERT INTO "auth_permission" VALUES(67,'Can change Τρίμηνο',13,'change_trimino');
INSERT INTO "auth_permission" VALUES(68,'Can change Τύπος Σύμβασης',20,'change_symtyp');
INSERT INTO "auth_permission" VALUES(69,'Can change Τύπος αποδοχών',19,'change_aptyp');
INSERT INTO "auth_permission" VALUES(70,'Can change Τύπος αποχώρησης',25,'change_apotyp');
INSERT INTO "auth_permission" VALUES(71,'Can change Τύπος επιχείρησης',8,'change_cotyp');
INSERT INTO "auth_permission" VALUES(72,'Can change Τύπος μισθοδοσίας',32,'change_mist');
INSERT INTO "auth_permission" VALUES(73,'Can change Τύπος μισθολογικού δεδομένου',34,'change_mtyp');
INSERT INTO "auth_permission" VALUES(74,'Can change Τύπος παρουσίας',28,'change_ptyp');
INSERT INTO "auth_permission" VALUES(75,'Can change Υποκατάστημα',10,'change_coy');
INSERT INTO "auth_permission" VALUES(76,'Can change Φύλο',16,'change_sex');
INSERT INTO "auth_permission" VALUES(77,'Can change Χρήση',11,'change_xrisi');
INSERT INTO "auth_permission" VALUES(78,'Can delete Αποδοχές εργαζομένου',24,'delete_promis');
INSERT INTO "auth_permission" VALUES(79,'Can delete Αποχώρηση εργαζομένου',26,'delete_apo');
INSERT INTO "auth_permission" VALUES(80,'Can delete Δίμηνο',12,'delete_dimino');
INSERT INTO "auth_permission" VALUES(81,'Can delete Ειδικότητα',15,'delete_eid');
INSERT INTO "auth_permission" VALUES(82,'Can delete Εργαζόμενος βασικά στοιχεία',17,'delete_fpr');
INSERT INTO "auth_permission" VALUES(83,'Can delete Εργαζόμενος πρόσληψη',22,'delete_pro');
INSERT INTO "auth_permission" VALUES(84,'Can delete Εργαζόμενος πρόσληψη Σύμβαση Εργασίας',23,'delete_symb');
INSERT INTO "auth_permission" VALUES(85,'Can delete Εργαζόμενος συμπληρωματικά στοιχεία',18,'delete_fprd');
INSERT INTO "auth_permission" VALUES(86,'Can delete Εταιρεία',9,'delete_co');
INSERT INTO "auth_permission" VALUES(87,'Can delete Λεπτομέρεια μισθοδοσίας',35,'delete_misd');
INSERT INTO "auth_permission" VALUES(88,'Can delete Μισθοδοσία',33,'delete_mis');
INSERT INTO "auth_permission" VALUES(89,'Can delete Μονάδα χρόνου',27,'delete_mxr');
INSERT INTO "auth_permission" VALUES(90,'Can delete Παρουσία',29,'delete_par');
INSERT INTO "auth_permission" VALUES(91,'Can delete Παρουσία F',31,'delete_parf');
INSERT INTO "auth_permission" VALUES(92,'Can delete Παρουσία αναλυτικά',30,'delete_pard');
INSERT INTO "auth_permission" VALUES(93,'Can delete Περίοδος',14,'delete_period');
INSERT INTO "auth_permission" VALUES(94,'Can delete Πρόγραμμα εργασίας',21,'delete_orar');
INSERT INTO "auth_permission" VALUES(95,'Can delete Τρίμηνο',13,'delete_trimino');
INSERT INTO "auth_permission" VALUES(96,'Can delete Τύπος Σύμβασης',20,'delete_symtyp');
INSERT INTO "auth_permission" VALUES(97,'Can delete Τύπος αποδοχών',19,'delete_aptyp');
INSERT INTO "auth_permission" VALUES(98,'Can delete Τύπος αποχώρησης',25,'delete_apotyp');
INSERT INTO "auth_permission" VALUES(99,'Can delete Τύπος επιχείρησης',8,'delete_cotyp');
INSERT INTO "auth_permission" VALUES(100,'Can delete Τύπος μισθοδοσίας',32,'delete_mist');
INSERT INTO "auth_permission" VALUES(101,'Can delete Τύπος μισθολογικού δεδομένου',34,'delete_mtyp');
INSERT INTO "auth_permission" VALUES(102,'Can delete Τύπος παρουσίας',28,'delete_ptyp');
INSERT INTO "auth_permission" VALUES(103,'Can delete Υποκατάστημα',10,'delete_coy');
INSERT INTO "auth_permission" VALUES(104,'Can delete Φύλο',16,'delete_sex');
INSERT INTO "auth_permission" VALUES(105,'Can delete Χρήση',11,'delete_xrisi');
CREATE TABLE "auth_group_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("group_id", "permission_id")
);
CREATE TABLE "auth_group" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
);
CREATE TABLE "auth_user_user_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("user_id", "permission_id")
);
CREATE TABLE "auth_user_groups" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
    UNIQUE ("user_id", "group_id")
);
CREATE TABLE "auth_user" (
    "id" integer NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "password" varchar(128) NOT NULL,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL,
    "is_superuser" bool NOT NULL,
    "last_login" datetime NOT NULL,
    "date_joined" datetime NOT NULL
);
INSERT INTO "auth_user" VALUES(1,'ted','','','t@s.com','pbkdf2_sha256$10000$U204XOamXfd1$mVhO9x5n9TYWIr1Ifu4CP0OORmFY0Zl2Tm4hCsV7koE=',1,1,1,'2013-02-15 18:31:54.677000','2013-02-15 18:31:54.677000');
CREATE TABLE "django_content_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
);
INSERT INTO "django_content_type" VALUES(1,'permission','auth','permission');
INSERT INTO "django_content_type" VALUES(2,'group','auth','group');
INSERT INTO "django_content_type" VALUES(3,'user','auth','user');
INSERT INTO "django_content_type" VALUES(4,'content type','contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES(5,'session','sessions','session');
INSERT INTO "django_content_type" VALUES(6,'site','sites','site');
INSERT INTO "django_content_type" VALUES(7,'log entry','admin','logentry');
INSERT INTO "django_content_type" VALUES(8,'Τύπος επιχείρησης','m12','cotyp');
INSERT INTO "django_content_type" VALUES(9,'Εταιρεία','m12','co');
INSERT INTO "django_content_type" VALUES(10,'Υποκατάστημα','m12','coy');
INSERT INTO "django_content_type" VALUES(11,'Χρήση','m12','xrisi');
INSERT INTO "django_content_type" VALUES(12,'Δίμηνο','m12','dimino');
INSERT INTO "django_content_type" VALUES(13,'Τρίμηνο','m12','trimino');
INSERT INTO "django_content_type" VALUES(14,'Περίοδος','m12','period');
INSERT INTO "django_content_type" VALUES(15,'Ειδικότητα','m12','eid');
INSERT INTO "django_content_type" VALUES(16,'Φύλο','m12','sex');
INSERT INTO "django_content_type" VALUES(17,'Εργαζόμενος βασικά στοιχεία','m12','fpr');
INSERT INTO "django_content_type" VALUES(18,'Εργαζόμενος συμπληρωματικά στοιχεία','m12','fprd');
INSERT INTO "django_content_type" VALUES(19,'Τύπος αποδοχών','m12','aptyp');
INSERT INTO "django_content_type" VALUES(20,'Τύπος Σύμβασης','m12','symtyp');
INSERT INTO "django_content_type" VALUES(21,'Πρόγραμμα εργασίας','m12','orar');
INSERT INTO "django_content_type" VALUES(22,'Εργαζόμενος πρόσληψη','m12','pro');
INSERT INTO "django_content_type" VALUES(23,'Εργαζόμενος πρόσληψη Σύμβαση Εργασίας','m12','symb');
INSERT INTO "django_content_type" VALUES(24,'Αποδοχές εργαζομένου','m12','promis');
INSERT INTO "django_content_type" VALUES(25,'Τύπος αποχώρησης','m12','apotyp');
INSERT INTO "django_content_type" VALUES(26,'Αποχώρηση εργαζομένου','m12','apo');
INSERT INTO "django_content_type" VALUES(27,'Μονάδα χρόνου','m12','mxr');
INSERT INTO "django_content_type" VALUES(28,'Τύπος παρουσίας','m12','ptyp');
INSERT INTO "django_content_type" VALUES(29,'Παρουσία','m12','par');
INSERT INTO "django_content_type" VALUES(30,'Παρουσία αναλυτικά','m12','pard');
INSERT INTO "django_content_type" VALUES(31,'Παρουσία F','m12','parf');
INSERT INTO "django_content_type" VALUES(32,'Τύπος μισθοδοσίας','m12','mist');
INSERT INTO "django_content_type" VALUES(33,'Μισθοδοσία','m12','mis');
INSERT INTO "django_content_type" VALUES(34,'Τύπος μισθολογικού δεδομένου','m12','mtyp');
INSERT INTO "django_content_type" VALUES(35,'Λεπτομέρεια μισθοδοσίας','m12','misd');
CREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" datetime NOT NULL
);
CREATE TABLE "django_site" (
    "id" integer NOT NULL PRIMARY KEY,
    "domain" varchar(100) NOT NULL,
    "name" varchar(50) NOT NULL
);
INSERT INTO "django_site" VALUES(1,'example.com','example.com');
CREATE TABLE "django_admin_log" (
    "id" integer NOT NULL PRIMARY KEY,
    "action_time" datetime NOT NULL,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "content_type_id" integer REFERENCES "django_content_type" ("id"),
    "object_id" text,
    "object_repr" varchar(200) NOT NULL,
    "action_flag" smallint unsigned NOT NULL,
    "change_message" text NOT NULL
);
CREATE TABLE "z_dbtbl"(
    "id" integer NOT NULL PRIMARY KEY,
    "tblnam" varchar(30) NOT NULL UNIQUE,
    "tbllbl" varchar(30) NOT NULL,
    "tblupd" integer NOT NULL
);
INSERT INTO "z_dbtbl" VALUES(1,'m12_apdp','Περίοδοι ΑΠΔ',0);
INSERT INTO "z_dbtbl" VALUES(2,'m12_apo','Αποχωρήσεις Εργαζομένων',0);
INSERT INTO "z_dbtbl" VALUES(3,'m12_apotyp','Τύποι αποχώρησης',0);
INSERT INTO "z_dbtbl" VALUES(4,'m12_aptyp','Τύποι αποδοχών',0);
INSERT INTO "z_dbtbl" VALUES(5,'m12_co','Στοιχεία επιχείρησης',0);
INSERT INTO "z_dbtbl" VALUES(6,'m12_cotyp','Τύποι επιχείρησης',0);
INSERT INTO "z_dbtbl" VALUES(7,'m12_coy','Παραρτήματα',0);
INSERT INTO "z_dbtbl" VALUES(8,'m12_dimino','Δίμηνα',0);
INSERT INTO "z_dbtbl" VALUES(9,'m12_eid','Ειδικότητες',0);
INSERT INTO "z_dbtbl" VALUES(10,'m12_fpr','Στοιχεία εργαζομένων',0);
INSERT INTO "z_dbtbl" VALUES(11,'m12_fprd','Λοιπά στοιχεία εργαζομένων',0);
INSERT INTO "z_dbtbl" VALUES(12,'m12_mis','Μισθοδοσίες',0);
INSERT INTO "z_dbtbl" VALUES(13,'m12_misd','Μισθοδοσίες αναλυτικά',0);
INSERT INTO "z_dbtbl" VALUES(14,'m12_mist','Τύποι Μισθοδοσίας',0);
INSERT INTO "z_dbtbl" VALUES(15,'m12_mtyp','Μισθολογικά στοιχεία',0);
INSERT INTO "z_dbtbl" VALUES(16,'m12_mxr','Χρονικές περίοδοι',0);
INSERT INTO "z_dbtbl" VALUES(17,'m12_orar','Ωράρια',0);
INSERT INTO "z_dbtbl" VALUES(18,'m12_par','Παρουσίες',0);
INSERT INTO "z_dbtbl" VALUES(19,'m12_pard','Παρουσίες αναλυτικά',0);
INSERT INTO "z_dbtbl" VALUES(20,'m12_parf','Παρουσίες αναλυτικά κλπ',0);
INSERT INTO "z_dbtbl" VALUES(21,'m12_period','Περίοδοι',0);
INSERT INTO "z_dbtbl" VALUES(22,'m12_pro','Προσλήψεις',0);
INSERT INTO "z_dbtbl" VALUES(23,'m12_promis','Αποδοχές',0);
INSERT INTO "z_dbtbl" VALUES(24,'m12_ptyp','Τύποι παρουσιών',0);
INSERT INTO "z_dbtbl" VALUES(25,'m12_sex','Φύλα',0);
INSERT INTO "z_dbtbl" VALUES(26,'m12_symb','Συμβάσεις',0);
INSERT INTO "z_dbtbl" VALUES(27,'m12_symbtyp','Τύποι συμβάσεων',0);
INSERT INTO "z_dbtbl" VALUES(28,'m12_trimino','Τρίμηνα',0);
INSERT INTO "z_dbtbl" VALUES(29,'m12_xrisi','Χρήσεις',0);
CREATE TABLE "z_dbkey"(
    "id" integer NOT NULL PRIMARY KEY,
    "keynam" varchar(30) NOT NULL UNIQUE,
    "keysql1" text NOT NULL,
    "keysql2" text
);
INSERT INTO "z_dbkey" VALUES(1,'ptyp_id','SELECT id, ptypp FROM m12_ptyp','');
CREATE TABLE "z_dbfld" (
    "id" integer NOT NULL PRIMARY KEY,
    "fldnam" varchar(30) NOT NULL UNIQUE,
    "fldlbl" varchar(30) NOT NULL,
    "fldreq" integer NOT NULL,
    "fldtyp" varchar(3) NOT NULL
);
INSERT INTO "z_dbfld" VALUES(1,'id','ΑΑ',1,'int');
INSERT INTO "z_dbfld" VALUES(2,'trimp','Τρίμηνο',1,'txt');
INSERT INTO "z_dbfld" VALUES(3,'perapo','Από περίοδο',1,'txt');
INSERT INTO "z_dbfld" VALUES(4,'pereos','Έως περίοδο',1,'txt');
INSERT INTO "z_dbfld" VALUES(5,'apold','Ημ/νία Απόλυσης',1,'dat');
INSERT INTO "z_dbfld" VALUES(6,'pro_id','Εργαζόμενος',1,'key');
INSERT INTO "z_dbfld" VALUES(7,'apot','Τύπος αποχώρησης',1,'txt');
INSERT INTO "z_dbfld" VALUES(8,'apotypp','Τύπος αποχώρησης',1,'txt');
INSERT INTO "z_dbfld" VALUES(9,'aptypp','Τύπος αποδοχών',1,'txt');
INSERT INTO "z_dbfld" VALUES(10,'cop','Επωνυμία',1,'txt');
INSERT INTO "z_dbfld" VALUES(11,'ono','Όνομα',1,'txt');
INSERT INTO "z_dbfld" VALUES(12,'pat','Πατρώνυμο',1,'txt');
INSERT INTO "z_dbfld" VALUES(13,'cotyp_id','Τύπος επιχείρησης',1,'key');
INSERT INTO "z_dbfld" VALUES(14,'ame','Αρ.Μητρώου ΙΚΑ',1,'txt');
INSERT INTO "z_dbfld" VALUES(15,'afm','ΑΦΜ',1,'txt');
INSERT INTO "z_dbfld" VALUES(16,'doy','ΔΟΥ',1,'txt');
INSERT INTO "z_dbfld" VALUES(17,'dra','Δραστηριότητα',1,'txt');
INSERT INTO "z_dbfld" VALUES(18,'pol','Πόλη',1,'txt');
INSERT INTO "z_dbfld" VALUES(19,'odo','Οδός',1,'txt');
INSERT INTO "z_dbfld" VALUES(20,'num','Αριθμός',1,'txt');
INSERT INTO "z_dbfld" VALUES(21,'tk','ΤΚ',1,'txt');
INSERT INTO "z_dbfld" VALUES(22,'ikac','Κωδ.Παρ.ΙΚΑ',1,'txt');
INSERT INTO "z_dbfld" VALUES(23,'ikap','Παράρτημα ΙΚΑ',1,'txt');
INSERT INTO "z_dbfld" VALUES(24,'cotyp','Κωδ.Τύπου Επιχ/σης',1,'txt');
INSERT INTO "z_dbfld" VALUES(25,'cotypp','Τύπος επιχείρησης',1,'txt');
INSERT INTO "z_dbfld" VALUES(26,'co_id','Επιχείρηση',1,'key');
INSERT INTO "z_dbfld" VALUES(27,'coyp','Παράρτημα',1,'txt');
INSERT INTO "z_dbfld" VALUES(28,'kad','ΚΑΔ (ΙΚΑ)',1,'txt');
INSERT INTO "z_dbfld" VALUES(29,'dimp','Δίμηνο',1,'txt');
INSERT INTO "z_dbfld" VALUES(30,'eidp','Ειδικότητα',1,'txt');
INSERT INTO "z_dbfld" VALUES(31,'keid','Κωδ.Ειδικότητας (ΙΚΑ)',1,'txt');
INSERT INTO "z_dbfld" VALUES(32,'epon','Επώνυμο',1,'txt');
INSERT INTO "z_dbfld" VALUES(33,'onom','Όνομα',1,'txt');
INSERT INTO "z_dbfld" VALUES(34,'patr','Πατρώνυμο',1,'txt');
INSERT INTO "z_dbfld" VALUES(35,'mitr','Μητρώνυμο',1,'txt');
INSERT INTO "z_dbfld" VALUES(36,'sex_id','Φύλο',1,'box');
INSERT INTO "z_dbfld" VALUES(37,'igen','Ημ.Γέννησης',1,'dat');
INSERT INTO "z_dbfld" VALUES(39,'amka','ΑΜΚΑ',1,'txt');
INSERT INTO "z_dbfld" VALUES(40,'aika','Αρ.Μητρ.ΙΚΑ',1,'txt');
INSERT INTO "z_dbfld" VALUES(41,'fpr_id','Εργαζόμενος',1,'key');
INSERT INTO "z_dbfld" VALUES(42,'dat','Ημ/νία Ισχύος',1,'dat');
INSERT INTO "z_dbfld" VALUES(43,'mars','Οικογ.Κατάσταση',1,'txt');
INSERT INTO "z_dbfld" VALUES(44,'pedi','Παιδιά',1,'int');
INSERT INTO "z_dbfld" VALUES(45,'xrisi_id','Χρήση',1,'int');
INSERT INTO "z_dbfld" VALUES(46,'period_id','Περίοδος',1,'txt');
INSERT INTO "z_dbfld" VALUES(47,'mist_id','Τύπος Μισθοδοσίας',1,'key');
INSERT INTO "z_dbfld" VALUES(48,'imnia','Ημ/νία Υπολογισμού',1,'dat');
INSERT INTO "z_dbfld" VALUES(49,'mis_id','Μισθοδοσία',1,'key');
INSERT INTO "z_dbfld" VALUES(50,'mtyp_id','Τύπος',1,'txt');
INSERT INTO "z_dbfld" VALUES(51,'val','Τιμή',1,'dec');
INSERT INTO "z_dbfld" VALUES(52,'mistp','Τύπος Μισθοδοσίας',1,'txt');
INSERT INTO "z_dbfld" VALUES(53,'mtypp','Τύπος',1,'txt');
INSERT INTO "z_dbfld" VALUES(54,'mxrp','Μονάδα χρόνου',1,'txt');
INSERT INTO "z_dbfld" VALUES(55,'orar','Ωράριο',1,'txt');
INSERT INTO "z_dbfld" VALUES(56,'mbdo','Μέρες εργασίας / βδομάδα',1,'int');
INSERT INTO "z_dbfld" VALUES(57,'obdo','Ώρες εργασιας / βδομάδα',1,'int');
INSERT INTO "z_dbfld" VALUES(58,'par_id','Παρουσίες',1,'key');
INSERT INTO "z_dbfld" VALUES(59,'ptyp','Τύπος παρουσίας',1,'txt');
INSERT INTO "z_dbfld" VALUES(60,'pos','Ποσότητα',1,'dec');
INSERT INTO "z_dbfld" VALUES(61,'period','Κωδ.Περιόδου',1,'txt');
INSERT INTO "z_dbfld" VALUES(62,'periodd','Περίοδος',1,'txt');
INSERT INTO "z_dbfld" VALUES(63,'dimino_id','Δίμηνο',1,'txt');
INSERT INTO "z_dbfld" VALUES(64,'trimino_id','Τρίμηνο',1,'box');
INSERT INTO "z_dbfld" VALUES(65,'prod','Ημ/νια πρόσληψης',1,'dat');
INSERT INTO "z_dbfld" VALUES(66,'coy_id','Παράρτημα',1,'key');
INSERT INTO "z_dbfld" VALUES(67,'eid_id','Ειδικότητα',1,'key');
INSERT INTO "z_dbfld" VALUES(68,'proy','Προυπηρεσία',1,'int');
INSERT INTO "z_dbfld" VALUES(69,'aptyp_id','Τύπος αποδοχών',1,'key');
INSERT INTO "z_dbfld" VALUES(70,'apod','Αποδοχές',1,'dec');
INSERT INTO "z_dbfld" VALUES(71,'poso','Αποδοχές',1,'dec');
INSERT INTO "z_dbfld" VALUES(72,'ptypp','Τύπος παρουσίας',1,'txt');
INSERT INTO "z_dbfld" VALUES(73,'mxr_id','Μονάδα Χρόνου',1,'txt');
INSERT INTO "z_dbfld" VALUES(74,'sexp','Φύλο',1,'txt');
INSERT INTO "z_dbfld" VALUES(75,'xrisi','Χρήση',1,'int');
INSERT INTO "z_dbfld" VALUES(76,'xrisip','Περιγραφή Χρήσης',1,'txt');
INSERT INTO "z_dbfld" VALUES(77,'onomatep','Ονοματεπώνυμο',1,'txt');
CREATE TABLE "z_calc" (
    "id" integer NOT NULL PRIMARY KEY,
    "calcp" varchar(30) NOT NULL UNIQUE,
    "cversion" varchar(15) NOT NULL UNIQUE,
    "cperiod" integer NOT NULL,
    "cxrisi" integer NOT NULL
);
INSERT INTO "z_calc" VALUES(1,'misthodosia','1.00.00',1,1);
CREATE TABLE "z_calcd" (
    "id" integer NOT NULL PRIMARY KEY,
    "calc_id" integer NOT NULL REFERENCES "z_calc" ("id"),
    "varnam" varchar(30) NOT NULL UNIQUE,
    "formula" text NOT NULL
);
INSERT INTO "z_calcd" VALUES(1,1,'apod','meres * imsthio');
INSERT INTO "z_calcd" VALUES(2,1,'ika','apod * pika / 100');
INSERT INTO "z_calcd" VALUES(3,1,'ikaenos','apod * pikaenos / 100');
INSERT INTO "z_calcd" VALUES(4,1,'ikaetis','ika-ikaenos');
INSERT INTO "z_calcd" VALUES(5,1,'forologiteo','apod - ikaenos');
INSERT INTO "z_calcd" VALUES(6,1,'foro','foros(forologiteo)');
INSERT INTO "z_calcd" VALUES(7,1,'kratiseis','forologiteo+foro');
INSERT INTO "z_calcd" VALUES(8,1,'pliroteo','apod - kratiseis');
CREATE TABLE "m12_cotyp" (
    "id" integer NOT NULL PRIMARY KEY,
    "cotyp" varchar(1) NOT NULL UNIQUE,
    "cotypp" varchar(1) NOT NULL UNIQUE
);
INSERT INTO "m12_cotyp" VALUES(1,'0','Εταιρία');
INSERT INTO "m12_cotyp" VALUES(2,'1','Φυσικό πρόσωπο');
CREATE TABLE "m12_co" (
    "id" integer NOT NULL PRIMARY KEY,
    "cop" varchar(60) NOT NULL UNIQUE,
    "ono" varchar(20) NOT NULL,
    "pat" varchar(20) NOT NULL,
    "cotyp_id" integer NOT NULL REFERENCES "m12_cotyp" ("id"),
    "ame" varchar(10) NOT NULL UNIQUE,
    "afm" varchar(9) NOT NULL UNIQUE,
    "doy" varchar(60) NOT NULL,
    "dra" varchar(60) NOT NULL,
    "pol" varchar(30) NOT NULL,
    "odo" varchar(30) NOT NULL,
    "num" varchar(5) NOT NULL,
    "tk" varchar(5) NOT NULL,
    "ikac" varchar(3) NOT NULL,
    "ikap" varchar(50) NOT NULL
);
CREATE TABLE "m12_coy" (
    "id" integer NOT NULL PRIMARY KEY,
    "co_id" integer NOT NULL REFERENCES "m12_co" ("id"),
    "coyp" varchar(60) NOT NULL UNIQUE,
    "kad" varchar(4) NOT NULL
);
CREATE TABLE "m12_xrisi" (
    "id" integer NOT NULL PRIMARY KEY,
    "xrisi" varchar(4) NOT NULL UNIQUE,
    "xrisip" varchar(50) NOT NULL UNIQUE
);
CREATE TABLE "m12_dimino" (
    "id" integer NOT NULL PRIMARY KEY,
    "dimp" varchar(60) NOT NULL UNIQUE
);
INSERT INTO "m12_dimino" VALUES(1,'1ο Δίμηνο (Ιανουάριος - Φεβρουάριος)');
INSERT INTO "m12_dimino" VALUES(2,'2ο Δίμηνο (Μάρτιος - Απρίλιος)');
INSERT INTO "m12_dimino" VALUES(3,'3ο Δίμηνο (Μάϊος - Ιούνιος)');
INSERT INTO "m12_dimino" VALUES(4,'4ο Δίμηνο (Ιούλιος - Αύγουστος)');
INSERT INTO "m12_dimino" VALUES(5,'5ο Δίμηνο (Σεπτέμβριος - Οκτώβριος)');
INSERT INTO "m12_dimino" VALUES(6,'6ο Δίμηνο (Νοέμβριος - Δεκέμβριος)');
CREATE TABLE "m12_trimino" (
    "id" integer NOT NULL PRIMARY KEY,
    "trimp" varchar(60) NOT NULL UNIQUE,
    "perapo" varchar(2) NOT NULL UNIQUE,
    "pereos" varchar(2) NOT NULL UNIQUE
);
INSERT INTO "m12_trimino" VALUES(1,'1ο Τρίμηνο (Ιαν-Φεβ-Μαρτ)','01','03');
INSERT INTO "m12_trimino" VALUES(2,'2ο Τρίμηνο (Απρ-Μαι-Ιουν)','04','06');
INSERT INTO "m12_trimino" VALUES(3,'3ο Τρίμηνο (Ιουλ-Αυγ-Σεπτ)','07','09');
INSERT INTO "m12_trimino" VALUES(4,'4ο Τρίμηνο (Οκτ-Νοε-Δεκ)','10','12');
CREATE TABLE "m12_apdp" (
    "id" integer NOT NULL PRIMARY KEY,
    "trimp" varchar(60) NOT NULL UNIQUE,
    "perapo" varchar(2) NOT NULL UNIQUE,
    "pereos" varchar(2) NOT NULL UNIQUE
);
INSERT INTO "m12_apdp" VALUES(1,'1.Ιανουάριος','01','01');
INSERT INTO "m12_apdp" VALUES(2,'2.Φεβρουάριος','02','02');
INSERT INTO "m12_apdp" VALUES(3,'3.Μάρτιος','03','03');
INSERT INTO "m12_apdp" VALUES(4,'4.Απρίλιος','04','04');
INSERT INTO "m12_apdp" VALUES(5,'5.Μάϊος','05','05');
INSERT INTO "m12_apdp" VALUES(6,'6.Ιούνιος','06','06');
INSERT INTO "m12_apdp" VALUES(7,'7.Ιούλιος','07','07');
INSERT INTO "m12_apdp" VALUES(8,'8.Αύγουστος','08','08');
INSERT INTO "m12_apdp" VALUES(9,'9.Σεπτέμβριος','09','09');
INSERT INTO "m12_apdp" VALUES(10,'10.Οκτώβριος','10','10');
INSERT INTO "m12_apdp" VALUES(11,'11.Νοέμβριος','11','11');
INSERT INTO "m12_apdp" VALUES(12,'12.Δεκέμβριος','12','12');
CREATE TABLE "m12_period" (
    "id" integer NOT NULL PRIMARY KEY,
    "period" varchar(2) NOT NULL UNIQUE,
    "periodp" varchar(20) NOT NULL UNIQUE,
    "dimino_id" integer NOT NULL REFERENCES "m12_dimino" ("id"),
    "trimino_id" integer NOT NULL REFERENCES "m12_trimino" ("id")
);
INSERT INTO "m12_period" VALUES(1,'01','Ιανουάριος',1,1);
INSERT INTO "m12_period" VALUES(2,'02','Φεβρουάριος',1,1);
INSERT INTO "m12_period" VALUES(3,'03','Μάρτιος',2,1);
INSERT INTO "m12_period" VALUES(4,'04','Απρίλιος',2,2);
INSERT INTO "m12_period" VALUES(5,'05','Μάϊος',3,2);
INSERT INTO "m12_period" VALUES(6,'06','Ιούνιος',3,2);
INSERT INTO "m12_period" VALUES(7,'07','Ιούλιος',4,3);
INSERT INTO "m12_period" VALUES(8,'08','Αύγουστος',4,3);
INSERT INTO "m12_period" VALUES(9,'09','Σεπτέμβριος',5,3);
INSERT INTO "m12_period" VALUES(10,'10','Οκτώβριος',5,4);
INSERT INTO "m12_period" VALUES(11,'11','Νοέμβριος',6,4);
INSERT INTO "m12_period" VALUES(12,'12','Δεκέμβριος',6,4);
CREATE TABLE "m12_eid" (
    "id" integer NOT NULL PRIMARY KEY,
    "eidp" varchar(60) NOT NULL UNIQUE,
    "keid" varchar(60) NOT NULL UNIQUE
);
CREATE TABLE "m12_sex" (
    "id" integer NOT NULL PRIMARY KEY,
    "sexp" varchar(10) NOT NULL UNIQUE
);
INSERT INTO "m12_sex" VALUES(0,'Άνδρας');
INSERT INTO "m12_sex" VALUES(1,'Γυναίκα');
CREATE TABLE "m12_fpr" (
    "id" integer NOT NULL PRIMARY KEY,
    "epon" varchar(20) NOT NULL,
    "onom" varchar(20) NOT NULL,
    "patr" varchar(20) NOT NULL,
    "mitr" varchar(20) NOT NULL,
    "sex_id" integer NOT NULL REFERENCES "m12_sex" ("id"),
    "igen" date NOT NULL,
    "afm" varchar(9) NOT NULL,
    "amka" varchar(11) NOT NULL,
    "aika" varchar(7) NOT NULL,
    "pol" varchar(30) NOT NULL,
    "odo" varchar(30) NOT NULL,
    "num" varchar(5) NOT NULL,
    "tk" varchar(5) NOT NULL,
    UNIQUE ("epon", "onom", "patr", "mitr")
);
CREATE TABLE "m12_fprd" (
    "id" integer NOT NULL PRIMARY KEY,
    "fpr_id" integer NOT NULL REFERENCES "m12_fpr" ("id"),
    "dat" date NOT NULL,
    "mars" varchar(1) NOT NULL,
    "pedi" integer NOT NULL,
    UNIQUE ("fpr_id", "dat")
);
CREATE TABLE "m12_aptyp" (
    "id" integer NOT NULL PRIMARY KEY,
    "aptypp" varchar(20) NOT NULL UNIQUE
);
INSERT INTO "m12_aptyp" VALUES(1,'Μισθός');
INSERT INTO "m12_aptyp" VALUES(2,'Ημερομίσθιο');
INSERT INTO "m12_aptyp" VALUES(3,'Ωρομίσθιο');
CREATE TABLE "m12_symtyp" (
    "id" integer NOT NULL PRIMARY KEY,
    "symtyp" varchar(20) NOT NULL UNIQUE,
    "olerg" bool NOT NULL
);
INSERT INTO "m12_symtyp" VALUES(1,'ΑΟΡΙΣΤΟΥ ΧΡΟΝΟΥ',1);
INSERT INTO "m12_symtyp" VALUES(2,'ΜΕΡΙΚΗΣ ΑΠΑΣΧΟΛΗΣΗΣ',0);
CREATE TABLE "m12_orar" (
    "id" integer NOT NULL PRIMARY KEY,
    "orar" varchar(100) NOT NULL UNIQUE,
    "mbdo" decimal NOT NULL,
    "obdo" decimal NOT NULL
);
CREATE TABLE "m12_pro" (
    "id" integer NOT NULL PRIMARY KEY,
    "prod" date NOT NULL,
    "fpr_id" integer NOT NULL REFERENCES "m12_fpr" ("id"),
    "coy_id" integer NOT NULL REFERENCES "m12_coy" ("id"),
    "eid_id" integer NOT NULL REFERENCES "m12_eid" ("id"),
    "proy" integer NOT NULL,
    "aptyp_id" integer NOT NULL REFERENCES "m12_aptyp" ("id"),
    "apod" decimal NOT NULL,
    UNIQUE ("prod", "fpr_id")
);
CREATE TABLE "m12_symb" (
    "id" integer NOT NULL PRIMARY KEY,
    "symd" date NOT NULL,
    "pro_id" integer NOT NULL REFERENCES "m12_pro" ("id"),
    "xrisi_id" integer NOT NULL REFERENCES "m12_xrisi" ("id"),
    "period_id" integer NOT NULL REFERENCES "m12_period" ("id"),
    "symtyp_id" integer NOT NULL REFERENCES "m12_symtyp" ("id"),
    "orar_id" integer NOT NULL REFERENCES "m12_orar" ("id"),
    "dial" varchar(20) NOT NULL,
    UNIQUE ("pro_id", "xrisi_id", "period_id")
);
CREATE TABLE "m12_promis" (
    "id" integer NOT NULL PRIMARY KEY,
    "pro_id" integer NOT NULL REFERENCES "m12_pro" ("id"),
    "xrisi_id" integer NOT NULL REFERENCES "m12_xrisi" ("id"),
    "period_id" integer NOT NULL REFERENCES "m12_period" ("id"),
    "poso" decimal NOT NULL,
    UNIQUE ("pro_id", "xrisi_id", "period_id")
);
CREATE TABLE "m12_apotyp" (
    "id" integer NOT NULL PRIMARY KEY,
    "apotypp" varchar(30) NOT NULL UNIQUE
);
CREATE TABLE "m12_apo" (
    "id" integer NOT NULL PRIMARY KEY,
    "apold" date NOT NULL,
    "pro_id" integer NOT NULL UNIQUE REFERENCES "m12_pro" ("id"),
    "apot" varchar(1) NOT NULL
);
CREATE TABLE "m12_mxr" (
    "id" integer NOT NULL PRIMARY KEY,
    "mxrp" varchar(20) NOT NULL UNIQUE
);
INSERT INTO "m12_mxr" VALUES(1,'Ημέρες');
INSERT INTO "m12_mxr" VALUES(2,'Ωρες');
CREATE TABLE "m12_ptyp" (
    "id" integer NOT NULL PRIMARY KEY,
    "ptypp" varchar(20) NOT NULL UNIQUE,
    "mxr_id" integer NOT NULL REFERENCES "m12_mxr" ("id")
);
INSERT INTO "m12_ptyp" VALUES(1,'Κανονικές εργάσιμες',1);
INSERT INTO "m12_ptyp" VALUES(2,'Κανονική άδεια',1);
INSERT INTO "m12_ptyp" VALUES(3,'Λοιπές άδειες με αποδοχές',1);
INSERT INTO "m12_ptyp" VALUES(4,'Αδικαιολόγητη απουσία',1);
INSERT INTO "m12_ptyp" VALUES(5,'Άδεια χωρίς αποδοχές',1);
INSERT INTO "m12_ptyp" VALUES(6,'Ασθένεια < 3',1);
INSERT INTO "m12_ptyp" VALUES(7,'Ασθένεια > 3',1);
INSERT INTO "m12_ptyp" VALUES(8,'Υπερωρίες',2);
INSERT INTO "m12_ptyp" VALUES(9,'Υπερεργασία',2);
INSERT INTO "m12_ptyp" VALUES(10,'Κυριακές-Αργίες',1);
INSERT INTO "m12_ptyp" VALUES(11,'Νυχτερινή προσαύξηση',2);
CREATE TABLE "m12_par" (
    "id" integer NOT NULL PRIMARY KEY,
    "xrisi_id" integer NOT NULL REFERENCES "m12_xrisi" ("id"),
    "period_id" integer NOT NULL REFERENCES "m12_period" ("id"),
    UNIQUE ("xrisi_id", "period_id")
);
CREATE TABLE "m12_pard" (
    "id" integer NOT NULL PRIMARY KEY,
    "par_id" integer NOT NULL REFERENCES "m12_par" ("id"),
    "pro_id" integer NOT NULL REFERENCES "m12_pro" ("id"),
    "ptyp_id" integer NOT NULL REFERENCES "m12_ptyp" ("id"),
    "pos" decimal NOT NULL,
    UNIQUE ("par_id", "pro_id", "ptyp_id")
);
CREATE TABLE "m12_parf" (
    "id" integer NOT NULL PRIMARY KEY,
    "xrisi_id" integer NOT NULL REFERENCES "m12_xrisi" ("id"),
    "period_id" integer NOT NULL REFERENCES "m12_period" ("id"),
    "pro_id" integer NOT NULL REFERENCES "m12_pro" ("id"),
    "kerg" decimal NOT NULL,
    "kad" decimal NOT NULL,
    "asl3" decimal NOT NULL,
    "asm3" decimal NOT NULL,
    UNIQUE ("xrisi_id", "period_id", "pro_id")
);
CREATE TABLE "m12_mist" (
    "id" integer NOT NULL PRIMARY KEY,
    "mistp" varchar(20) NOT NULL UNIQUE
);
INSERT INTO "m12_mist" VALUES(1,'Τακτικές αποδοχές');
INSERT INTO "m12_mist" VALUES(2,'Αποδοχές υπαλλήλων ΝΠΔΔ κλπ.');
INSERT INTO "m12_mist" VALUES(3,'Δώρο Χριστουγέννων');
INSERT INTO "m12_mist" VALUES(4,'Δώρο Πάσχα');
INSERT INTO "m12_mist" VALUES(5,'Επίδομα αδείας');
INSERT INTO "m12_mist" VALUES(6,'Επίδομα ισολογισμού');
INSERT INTO "m12_mist" VALUES(7,'Αποδοχές αδειών εποχικά απασχ/νων Ξενοδ/λων');
INSERT INTO "m12_mist" VALUES(8,'Αποδοχές ασθενείας');
INSERT INTO "m12_mist" VALUES(9,'Αναδρομικές αποδοχές');
INSERT INTO "m12_mist" VALUES(10,'Bonus');
INSERT INTO "m12_mist" VALUES(11,'Υπερωρίες');
INSERT INTO "m12_mist" VALUES(12,'Αμοιβή με το κομμάτι (Φασόν)');
INSERT INTO "m12_mist" VALUES(13,'Τεκμαρτές αποδοχές');
INSERT INTO "m12_mist" VALUES(14,'Λοιπές αποδοχές');
INSERT INTO "m12_mist" VALUES(15,'Λοιπές αποδοχές για κλάδο ΕΤΕΑΜ');
INSERT INTO "m12_mist" VALUES(16,'Αμοιβές κατ''αποκοπήν/ΕΦΑΠΑΞ');
INSERT INTO "m12_mist" VALUES(17,'Εισφορές χωρίς αποδοχές');
INSERT INTO "m12_mist" VALUES(18,'Κανονικές αποδοχές πληρ/των Μεσογ τουρ πλοίων');
INSERT INTO "m12_mist" VALUES(19,'Αποδοχές αδείας πληρ/των Μεσογ τουρ πλοίων');
INSERT INTO "m12_mist" VALUES(20,'Αποδοχές ασφαλιζομένων στο ΕΤΕΑΜ');
CREATE TABLE "m12_mis" (
    "id" integer NOT NULL PRIMARY KEY,
    "xrisi_id" integer NOT NULL REFERENCES "m12_xrisi" ("id"),
    "period_id" integer NOT NULL REFERENCES "m12_period" ("id"),
    "mist_id" integer NOT NULL REFERENCES "m12_mist" ("id"),
    "imnia" date NOT NULL,
    UNIQUE ("xrisi_id", "period_id", "mist_id")
);
CREATE TABLE "m12_mtyp" (
    "id" integer NOT NULL PRIMARY KEY,
    "mtypp" varchar(50) NOT NULL UNIQUE,
    "mtypv" varchar(30) NOT NULL UNIQUE
);
INSERT INTO "m12_mtyp" VALUES(1,'Ημέρες εργασίας','mer_ergasias');
INSERT INTO "m12_mtyp" VALUES(2,'Ημέρες Κανονικής Αδείας','mer_kan_adeias');
INSERT INTO "m12_mtyp" VALUES(3,'Ημέρες Ασθένειας μικρ.3','mer_asth_less3');
INSERT INTO "m12_mtyp" VALUES(4,'Ημέρες Ασθένειας μεγ.3','mer_asth_more3');
INSERT INTO "m12_mtyp" VALUES(5,'Ημέρες αδικαιολόγητης απουσίας','mer_adikaiologites');
INSERT INTO "m12_mtyp" VALUES(6,'Ημέρες Κυριακών Εορτών','mer_kyriakes_giortes');
INSERT INTO "m12_mtyp" VALUES(20,'Υπερωρίες','yperories');
INSERT INTO "m12_mtyp" VALUES(21,'Ώρες Νυχτερινής προσαύξησης','or_nyxterines');
INSERT INTO "m12_mtyp" VALUES(100,'Ημερομίσθιο','imeromisthio');
INSERT INTO "m12_mtyp" VALUES(101,'Μισθός','misthos');
INSERT INTO "m12_mtyp" VALUES(109,'Ημέρες για υπολογισμό','mer_gia_ypologismo');
INSERT INTO "m12_mtyp" VALUES(110,'Ημέρες ΙΚΑ','mer_ika');
INSERT INTO "m12_mtyp" VALUES(200,'Αποδοχές Περιόδου','apodoxes_periodoy');
INSERT INTO "m12_mtyp" VALUES(500,'ΙΚΑ εργαζόμενος','ika_ergazomenos');
INSERT INTO "m12_mtyp" VALUES(501,'ΙΚΑ εργοδότης','ika_ergodotis');
INSERT INTO "m12_mtyp" VALUES(502,'ΙΚΑ αποδωτέο','ika');
INSERT INTO "m12_mtyp" VALUES(503,'Τύπος Αποδοχών','typos_apodoxon');
INSERT INTO "m12_mtyp" VALUES(504,'ΚΠΚ','kpk');
INSERT INTO "m12_mtyp" VALUES(505,'Ποσοστό ΙΚΑ εργαζομένου','percent_ika_ergazomenos');
INSERT INTO "m12_mtyp" VALUES(506,'Ποσοστό ΙΚΑ','percent_ika_ergodotis');
INSERT INTO "m12_mtyp" VALUES(599,'Φορολογητέο','forologiteo');
INSERT INTO "m12_mtyp" VALUES(600,'ΦΜΥ που παρακρατήθηκε','fmy_poy_parakratithike');
INSERT INTO "m12_mtyp" VALUES(601,'ΦΜΥ που αναλογεί','fmy_poy_analogei');
INSERT INTO "m12_mtyp" VALUES(610,'Ειδικό επίδομα αλληλεγγύης','eidiko_epidoma_alilegiis');
INSERT INTO "m12_mtyp" VALUES(700,'Συνολικές κρατήσεις εργαζομένου','synolikes_kratiseis_ergazomenoy');
INSERT INTO "m12_mtyp" VALUES(900,'Πληρωτέο σε εργαζόμενο','pliroteo_se_ergazomeno');
CREATE TABLE "m12_misd" (
    "id" integer NOT NULL PRIMARY KEY,
    "mis_id" integer NOT NULL REFERENCES "m12_mis" ("id"),
    "pro_id" integer NOT NULL REFERENCES "m12_pro" ("id"),
    "mtyp_id" integer NOT NULL REFERENCES "m12_mtyp" ("id"),
    "val" decimal NOT NULL,
    UNIQUE ("mis_id", "pro_id", "mtyp_id")
);
CREATE INDEX "auth_permission_1bb8f392" ON "auth_permission" ("content_type_id");
CREATE INDEX "auth_group_permissions_425ae3c4" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_1e014c8f" ON "auth_group_permissions" ("permission_id");
CREATE INDEX "auth_user_user_permissions_403f60f" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_1e014c8f" ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX "auth_user_groups_403f60f" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_425ae3c4" ON "auth_user_groups" ("group_id");
CREATE INDEX "django_session_3da3d3d8" ON "django_session" ("expire_date");
CREATE INDEX "django_admin_log_403f60f" ON "django_admin_log" ("user_id");
CREATE INDEX "django_admin_log_1bb8f392" ON "django_admin_log" ("content_type_id");
CREATE INDEX "m12_co_2a8a6e4c" ON "m12_co" ("cotyp_id");
CREATE INDEX "m12_coy_6e3c5e94" ON "m12_coy" ("co_id");
CREATE INDEX "m12_period_43b5e628" ON "m12_period" ("dimino_id");
CREATE INDEX "m12_period_7ea223cb" ON "m12_period" ("trimino_id");
CREATE INDEX "m12_fpr_5cb3bfcf" ON "m12_fpr" ("sex_id");
CREATE INDEX "m12_fprd_82026a9" ON "m12_fprd" ("fpr_id");
CREATE INDEX "m12_pro_82026a9" ON "m12_pro" ("fpr_id");
CREATE INDEX "m12_pro_7ccf5b3c" ON "m12_pro" ("coy_id");
CREATE INDEX "m12_pro_68fcafc5" ON "m12_pro" ("eid_id");
CREATE INDEX "m12_pro_5e583f27" ON "m12_pro" ("aptyp_id");
CREATE INDEX "m12_symb_28eb1be6" ON "m12_symb" ("pro_id");
CREATE INDEX "m12_symb_68f77cb2" ON "m12_symb" ("xrisi_id");
CREATE INDEX "m12_symb_73a1677f" ON "m12_symb" ("period_id");
CREATE INDEX "m12_symb_205799ba" ON "m12_symb" ("symtyp_id");
CREATE INDEX "m12_symb_76a7212e" ON "m12_symb" ("orar_id");
CREATE INDEX "m12_promis_28eb1be6" ON "m12_promis" ("pro_id");
CREATE INDEX "m12_promis_68f77cb2" ON "m12_promis" ("xrisi_id");
CREATE INDEX "m12_promis_73a1677f" ON "m12_promis" ("period_id");
CREATE INDEX "m12_ptyp_7ee90f0" ON "m12_ptyp" ("mxr_id");
CREATE INDEX "m12_par_68f77cb2" ON "m12_par" ("xrisi_id");
CREATE INDEX "m12_par_73a1677f" ON "m12_par" ("period_id");
CREATE INDEX "m12_pard_50a5e1e" ON "m12_pard" ("par_id");
CREATE INDEX "m12_pard_28eb1be6" ON "m12_pard" ("pro_id");
CREATE INDEX "m12_pard_7bfe9593" ON "m12_pard" ("ptyp_id");
CREATE INDEX "m12_parf_68f77cb2" ON "m12_parf" ("xrisi_id");
CREATE INDEX "m12_parf_73a1677f" ON "m12_parf" ("period_id");
CREATE INDEX "m12_parf_28eb1be6" ON "m12_parf" ("pro_id");
CREATE INDEX "m12_mis_68f77cb2" ON "m12_mis" ("xrisi_id");
CREATE INDEX "m12_mis_73a1677f" ON "m12_mis" ("period_id");
CREATE INDEX "m12_mis_6598417d" ON "m12_mis" ("mist_id");
CREATE INDEX "m12_misd_a6531b6" ON "m12_misd" ("mis_id");
CREATE INDEX "m12_misd_28eb1be6" ON "m12_misd" ("pro_id");
CREATE INDEX "m12_misd_1413af60" ON "m12_misd" ("mtyp_id");
COMMIT;
