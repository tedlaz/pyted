# -*- coding: utf-8 -*-
'''
Created on May 4, 2015

@author: tedlaz
'''
import os
from utils import sqlite3_methods as tu

db = "tst.db"
sqlC = u"CREATE table if not exists lmos (id INTEGER PRIMARY KEY, code TEXT, per TEXT);\n"
sqlC += u"INSERT INTO lmos VALUES(1, '20.01.00.013', 'Αγορές εμπορευμάτων εσωτερικού 13%');\n"
sqlC += u"INSERT INTO lmos VALUES(2, '38.00.00.000', 'Ταμείο Κεντρικού');\n"
sqlC += u"INSERT INTO lmos VALUES(3, '38.03.00.000', 'Eurobank');\n"
sqlC += u"INSERT INTO lmos VALUES(4, '50.00.00.000', 'Προμηθευτές');\n"
sqlC += u"INSERT INTO lmos VALUES(5, '30.00.00.000', 'Πελάτες');\n"
sqlC += u"INSERT INTO lmos VALUES(6, '54.00.02.013', 'ΦΠΑ Αγορών 13%');\n"
sqlC += u"INSERT INTO lmos VALUES(7, '54.00.02.023', 'ΦΠΑ Αγορών 23%');\n"
sql = "SELECT id, code , per FROM lmos ORDER BY code"
sql1 = "SELECT id, code , per FROM lmos WHERE code like '%%%s%%' ORDER BY code"
sql2 = "SELECT id, code , per FROM lmos WHERE grup(per) like '%%%s%%' ORDER BY per"
button_text_value ={'val': 1,
                    'fld1': u'38.03.0003',
                    'fld2': u'Eurobank',
                    'sql': sql,
                    'sql1': sql1,
                    'sql2': sql2,
                    'db': db}

def create_tst_db():
    tu.dbScript({'script': sqlC, 'db': db})
    print('db %s created !!' % db)


def delete_tst_db():
    os.remove(db)


if __name__ == '__main__':
    pass
