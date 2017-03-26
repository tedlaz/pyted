# -*- coding: utf-8 -*-
import os
import sqlite3_methods as sqlm
import check_vat
sqlcreate = '''
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS vat(
id_vat VARCHAR(15) PRIMARY KEY,
country VARCHAR(3) NOT NULL DEFAULT('EL'),
prnam TEXT NOT NULL UNIQUE,
prnams TEXT NOT NULL UNIQUE,
addr TEXT,
rdate DATE
);
CREATE TABLE IF NOT EXISTS lmoi(
id INTEGER PRIMARY KEY,
lmos TEXT NOT NULL UNIQUE,
lmosp TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS tr(
id INTEGER PRIMARY KEY,
imnia DATE NOT NULL,
par TEXT NOT NULL,
trp TEXT NOT NULL,
UNIQUE (imnia,par)
);
CREATE TABLE IF NOT EXISTS trd(
id_tr INTEGET NOT NULL REFERENCES tr(id),
id_no INTEGER NOT NULL,
id_lmoi INTEGER NOT NULL REFERENCES lmoi(id),
id_vat VARCHAR(15) REFERENCES vat(id_vat),
trdp TEXT,
xr DECIMAL NOT NULL DEFAULT 0,
pi DECIMAL NOT NULL DEFAULT 0,
PRIMARY KEY (id_tr, id_no)
);
CREATE VIEW imerologio AS SELECT tr.id, tr.imnia, tr.par, tr.trp,
trd.id_no, lmoi.lmos, lmoi.lmosp, trd.id_vat, vat.prnams, trd.trdp, trd.xr, trd.pi
FROM tr
INNER JOIN trd ON tr.id=trd.id_tr
INNER JOIN lmoi ON trd.id_lmoi=lmoi.id
LEFT JOIN vat ON vat.id_vat=trd.id_vat
ORDER BY tr.imnia, tr.id, trd.id_no;
COMMIT;
'''


def create_database(dbname):
    return (sqlm.dbScript({'script': sqlcreate, 'db': dbname}))


def check_database_for_lmos(lmos, db):
    if (not lmos) or (not db):
        return None
    sql = "SELECT id FROM lmoi WHERE lmos='%s'" % lmos
    result = sqlm.dbRows({'sql': sql, 'db': db})
    if result['rowNumber'] == 1:
        return result['rows'][0][0]
    else:
        return None


def insert_lmo(lmos, lmosp, db):
    idl = sqlm.uid()
    sql = "INSERT INTO lmoi VALUES('%s','%s','%s');" % (idl, lmos, lmosp)
    result = sqlm.dbCommit({'sql': sql, 'db': db})
    return result['lastId']


def insert_vat(vat, db):
    # print('edo insert_pr vat=%s' % vat)
    if not vat:
        return
    sqli = "INSERT INTO vat VALUES ('%s','%s','%s','%s','%s','%s')"
    sqls = "SELECT id_vat FROM vat WHERE id_vat='%s'" % vat
    if sqlm.dbRows({'sql': sqls, 'db': db})['rowNumber'] > 0:
        return
    print('Just try to find VAT ...')
    result = check_vat.checkVat(vat)
    if result['valid']:
        country = result.countryCode
        if '||' in result.name:
            name, names = result.name.split('||')
        else:
            name = result.name
            names = name
        rdate = result.requestDate
        addr = result.address
        sql = sqli % (vat, country, name, names, addr, rdate)
        sqlm.dbCommit({'sql': sql, 'db': db})
    else:
        print('Be careful !!! Not a valid vat or server or Internet is down ')


class Lmoi():

    def __init__(self, pin):
        self.id = pin.get('id', sqlm.uid())
        self.lmos = pin['lmos']
        self.lmosp = pin['lmosp']

    def to_str(self):
        st1 = "%15s %15s %30s" % (self.id, self.lmos, self.lmosp)
        return st1

    def to_dict(self):
        dic = {}
        dic['id'] = self.id
        dic['lmos'] = self.lmos
        dic['lmosp'] = self.lmosp
        return dic

    def save_to_db(self, db):
        sqli = "INSERT INTO lmoi VALUES('%s','%s','%s')"
        lid = check_database_for_lmos(self.lmos, db)
        if lid:
            print('lmos %s already exists in database' % self.lmos)
            self.id = lid
            return self.id
        sql = sqli % (self.id, self.lmos, self.lmosp)
        result = sqlm.dbCommit({'sql': sql, 'db': db})
        return result['lastId']


class Trd():
    '''
    Class representing transaction line
    '''
    def __init__(self, pin):
        self.id_tr = pin.get('id_tr', None)
        self.id_no = pin['id_no']  # Line number
        self.lmos = pin['lmos']
        self.id_lmoi = ''
        self.id_vat = pin.get('id_vat', '')
        self.trdp = pin.get('trdp', '')
        self.xr = pin.get('xr', 0)
        self.pi = pin.get('pi', 0)

    def is_ok(self):
        if self.xr != 0 and self.pi != 0:
            return False
        if self.xr == 0 and self.pi == 0:
            return False
        # Check if we need to set id_vat or not
        lm0 = self.lmos[:2]  # get the first 2 character of code
        if lm0 == '30' or lm0 == '50':
            if not self.id_vat:
                return False
        if self.id_vat:
            if not check_vat.is_possible_greek_vat(self.id_vat):
                print('VAT number %s is not valid' % self.id_vat)
                return False
        return True

    def to_dict(self):
        dic = {}
        dic['id_tr'] = self.id_tr
        dic['id_no'] = self.id_no
        dic['lmos'] = self.lmos
        dic['id_lmoi'] = self.id_lmoi
        dic['id_vat'] = self.id_vat
        dic['trdp'] = self.trdp
        dic['xr'] = self.xr
        dic['pi'] = self.pi
        return dic

    def to_sql_insert(self):
        sqli = "INSERT INTO trd VALUES('%s','%s','%s','%s','%s','%s','%s');\n"
        sql = sqli % (self.id_tr, self.id_no, self.id_lmoi, self.id_vat,
                      self.trdp, self.xr, self.pi)
        return sql

    def get_id_lmoi_from_db(self, db):
        self.id_lmoi = check_database_for_lmos(self.lmos, db)
        if self.id_lmoi:
            return True
        else:
            return False

    def to_str(self):
        st1 = '%(id_tr)15s %(id_no)3s %(lmos)15s %(id_vat)9s %(xr)10s %(pi)10s'
        return st1 % self.to_dict()


class Tr():
    def __init__(self, pin):
        self.id = pin.get('id', sqlm.uid())
        self.imnia = pin['imnia']
        self.par = pin['par']
        self.trp = pin['trp']
        self.lines = []
        self.line_no = 0
        self.txr = 0
        self.tpi = 0

    def __add_line(self, lmos, id_vat, trdp, xr, pi):
        line = Trd({'id_tr': self.id,
                    'id_no': self.line_no + 1,
                    'lmos': lmos,
                    'id_vat': id_vat,
                    'trdp': trdp,
                    'xr': xr,
                    'pi': pi
                    })
        if not line.is_ok():
            print('Error in line: %s' % line.to_dict())
            return
        self.lines.append(line)
        self.txr += line.xr
        self.tpi += line.pi
        self.line_no += 1

    def add_line_xr(self, lmos, xr, id_vat='', trdp=''):
        self.__add_line(lmos, id_vat, trdp, xr, 0)

    def add_line_pi(self, lmos, pi, id_vat='', trdp=''):
        self.__add_line(lmos, id_vat, trdp, 0, pi)

    def add_final_line(self, lmos, id_vat='', trdp=''):
        if self.line_no == 0 and self.txr == self.tpi:
            print('can not execute. Exiting')
            return
        if self.txr > self.tpi:
            self.__add_line(lmos, id_vat, trdp, 0, self.txr - self.tpi)
        else:
            self.__add_line(lmos, id_vat, trdp, self.tpi - self.txr, 0)

    def is_ok(self):
        if self.line_no > 1 and self.txr == self.tpi:
            return True
        else:
            return False

    def to_dict(self):
        dic = {}
        dic['id'] = self.id
        dic['imnia'] = self.imnia
        dic['par'] = self.par
        dic['trp'] = self.trp
        dic['lines'] = []
        for el in self.lines:
            dic['lines'].append(el.to_dict())
        return dic

    def to_str(self):
        li = '%15s %10s %10s %20s\n' % (self.id, self.imnia, self.par, self.trp)
        for line in self.lines:
            li += line.to_str() + '\n'
        return li

    def to_sql_insert(self):
        if not self.is_ok():
            return ''
        sql = "BEGIN TRANSACTION;\n"
        sqla = "INSERT INTO tr VALUES('%s','%s','%s','%s');\n"
        sql += sqla % (self.id, self.imnia, self.par, self.trp)
        for li in self.lines:
            sql += li.to_sql_insert()
        sql += "COMMIT;"
        return sql

    def save_to_db(self, db):
        if not self.is_ok():
            print('Not Valid Transaction . Aborting save to database')
            return False
        for li in self.lines:
            if not li.get_id_lmoi_from_db(db):
                print('Line with no valid lmo code')
                return False
            if li.id_vat:
                insert_vat(li.id_vat, db)
        result = sqlm.dbScript({'script': self.to_sql_insert(), 'db': db})
        return result['status']


if __name__ == '__main__':
    pass
