#!/usr/bin/python2
# *- coding: utf-8 -*
# Δίνουμε ημερολόγιο εγγραφών γενικής λογιστικής και μας επιστρέφει
# sqlite database με τις εγγραφές !!!
import sqlite3

sql_create = '''CREATE TABLE IF NOT EXISTS pp(
id INTEGER PRIMARY KEY,
dat DATE NOT NULL,
teg TEXT NOT NULL,
typ INTEGER NOT NULL DEFAULT 0,
par TEXT NOT NULL,
afm TEXT,
lmo TEXT,
aji NUMERIC NOT NULL DEFAULT 0,
fpa NUMERIC NOT NULL DEFAULT 0
);
'''
sql_pp = u"INSERT INTO pp VALUES(%s, '%s', '%s', %s, '%s', '%s','%s', %s, %s);\n"


es = [u'ΤΠΛ', u'ΑΠΛ', u'ΤΠΥ', u'ΑΠΥ', u'ΠΙΣ', u'ΤΠΕ', u'ΕΠΛ']
ej = [u'ΛΟΙΠΑ', u'ΤΑΓ', u'ΠΑΓ']


def isnum(val):
    try:
        float(val)
    except ValueError:
        return False
    else:
        return True


def iso_num(num):
    num = num.strip()
    num = num.replace('.', '')
    num = num.replace(',', '.')
    return num


def iso_date(dat):
    day, month, year = dat.split('/')
    return '%s-%s-%s' % (year, month, day)


def remove_simple_quotes(strval):
    retval = strval.strip()
    retval = retval.replace("'", '')
    return retval


def iso_str(strval):
    tval = remove_simple_quotes(strval)
    return tval.strip()


def array_to_sql(arr, sql_template):
    sql = u''
    for el in arr:
        sql += sql_template % el
    # print(sql)
    return sql


PIN_ERROR, DB_ERROR, NULL_VAL, ONE_VAL, MANY_VAL = range(5)


def dbScript(pin):
    '''
    Generic sql script execution
    input
        script : one or many sql expressions divided by ;
        db  : database name
    output:
        1 if no error , 0 if error
        text message
    '''
    script = pin.get('script', None)
    db = pin.get('db', None)

    if (not script) or (not db):
        return {'status': PIN_ERROR,
                'msg': 'dbScript: script and/or db name are empty'}

    try:
        con = sqlite3.connect(db)  # @UndefinedVariable
        cur = con.cursor()
        cur.executescript(script)
        con.commit()
        status = NULL_VAL
        msg = 'dbScript: Everything executed Fine !!'
    except sqlite3.Error as e:
        if con:
            con.rollback()
        status = DB_ERROR
        msg = 'dbScript: %s' % e
    finally:
        cur.close()
        con.close()
    return {'status': status, 'msg': msg}


def parseee(eefile, encoding='WINDOWS-1253'):
    tid = 0
    dat = ''
    teg = ''
    typ = 0
    par = ''
    afm = ''
    lmo = ''
    aji = 0
    fpa = 0
    a_eet = []
    with open(eefile) as afile:
        for line in afile:
            line = line.decode(encoding)
            # first check if linesize > 152
            lline = len(line)
            if lline == 45:
                dat = iso_date(line[32:42])
            tid = iso_str(line[1:8])
            if isnum(tid):
                teg = iso_str(line[9:34])
                if teg in es:
                    typ = 1
                elif teg in ej:
                    typ = 2
                else:
                    typ = 0
                par = iso_str(line[35:66])
                afm = line[67:76]
                if isnum(afm):
                    lmo = iso_str(line[77:91])
                else:
                    afm = ''
                    lmo = iso_str(line[67:91])
                aji = iso_num(line[92:112])
                fpa = iso_num(line[113:133])
                a_eet.append((tid, dat, teg, typ, par, afm, lmo, aji, fpa))
    return a_eet


def create_sql(eefile):
    a_eet = parseee(eefile)
    sql = u'BEGIN TRANSACTION;\n'
    sql += array_to_sql(a_eet, sql_pp)
    sql += 'COMMIT TRANSACTION;'
    return sql


def run(eefile, dbname=None):
    if not dbname:
        imerol = eefile.split('.')
        dbname = '%s-pp.sql3' % imerol[0]
    ret1 = dbScript({'script': sql_create, 'db': dbname})
    ret2 = dbScript({'script': create_sql(eefile), 'db': dbname})
    return '%s\n%s' % (ret1, ret2)


if __name__ == '__main__':
    import os.path
    import argparse
    pars = argparse.ArgumentParser(description='Parse ee to sqlite3 pp')
    pars.add_argument('eefile', help='Esoda-Ejoda Text File to be parsed')
    pars.add_argument('-o', '--Out', help='sqlite3 file name')
    pars.add_argument('-v', '--verbose', action='store_true',
                      help='output detailed messages')
    pars.add_argument('--version', action='version', version='2.0')
    args = pars.parse_args()
    if not os.path.isfile(args.eefile):
        print('No such file : %s' % args.eefile)
    else:
        ret = run(args.eefile, args.Out)
        if args.verbose:
            print(ret)
