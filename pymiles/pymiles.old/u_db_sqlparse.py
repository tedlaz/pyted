# -*- coding: utf-8 -*-
import sqlite3


def getmetadata(dbfilepath):
    sql = "SELECT name, sql FROM sqlite_master WHERE type='table'"
    con = sqlite3.connect(dbfilepath)
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows


def parse_sql(sqlcreate):
    splitchar = '~'
    fields = []
    # Keep only text between first and last parenthesis
    first_parenthesis_position = sqlcreate.find('(') + 1
    lasparpos = sqlcreate.rfind(')')
    stxt = sqlcreate[first_parenthesis_position:lasparpos]
    leftpar = 0
    txt = ''
    for ch in stxt:
        if ch == '(':
            leftpar += 1
        elif ch == ')':
            leftpar -= 1
        elif ch == '\n':
            ch = splitchar
        elif ch == ',':
            if not leftpar:
                ch = splitchar
        txt += ch
    # print(txt)
    # print('')
    txt = txt.upper()  # Make it all upper
    # uniqpos = txt.find('UNIQUE')
    # if uniqpos > 0 :  # Cut everything after UNIQUE
    #     txt = txt[:uniqpos]
    fields = txt.split('~')
    sfields = []
    unique = ''
    for field in fields:
        fstrip = field.strip()
        # print(fstrip)
        if fstrip[:2] == '--':
            continue
        if fstrip.startswith('UNIQUE'):
            unique += fstrip
            # print('----->unique:', unique)
            continue
        if len(fstrip) > 0:
            sfields.append(fstrip)
    # print(sfields, len(sfields))
    fnames = []
    ftypes = []
    tval = ''
    for field in sfields:
        fnames.append(field.split())
    # print(fnames)
    tfld = []
    for el in fnames:
        tf = {}
        tf['fname'] = el[0].lower()
        tf['type'] = el[1]
        if ('NOT' in el) and ('NULL' in el):
            tf['notnull'] = True
        else:
            tf['notnull'] = False
        tfld.append(tf)
    # print(tfld)
    return tfld


def return_meta(db):
    rows = getmetadata(db)
    val = {}
    for row in rows:
        val[row[0]] = parse_sql(row[1])
    return val


def str_meta(db):
    meta = return_meta(db)
    st_ = ''
    for table in sorted(meta.keys()):
        st_ += '%s :\n' % table
        for fld in meta[table]:
            st_ += '   %s %s\n' % (fld['fname'], fld['type'])
        st_ += '\n'
    return st_

if __name__ == '__main__':
    sql = "CREATE TABLE IF NOT EXISTS tst(id INTEGER PRIMARY KEY,"
    sql += " epo TEXT NOT    NULL references erg(id),  "
    sql += "   ono VARCHAR(30) not NULL DEFAULT 'ted'  UNIQUE, -- malakies kai kala\n"
    sql += "  poso DECIMAL(6,3),"
    sql += "  poaa DECIMAL(6,2),"
    sql += "  UNIQUE (epo, ono));"
    print(parse_sql(sql))
