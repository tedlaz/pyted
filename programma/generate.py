import sqlite3


def dbselect(sql, db):
    con = sqlite3.connect(db)
    # con.create_function("grdec", 1, grdec)
    # con.create_function("dec1", 1, dec)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    con.close()

    arrayOfDictionaries = []
    for row in rows:
        arrayOfDictionaries.append(dict(zip(row.keys(), row)))
    return arrayOfDictionaries


def dbscript(sql, db):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.executescript(sql)
        con.commit()

    except sqlite3.Error as e:
        if con:
            con.rollback()
    finally:
        cur.close()
        con.close()


def generate_stud(napo, neos, taji):
    tmpl = "INSERT INTO stud VALUES ({id},'{ep}', '{on}', '{pa}', '{mi}', {ta});\n"
    sql = 'BEGIN TRANSACTION;\n'
    for i in range(napo, neos):
        idv = i
        ftm = {}
        ftm['id'] = idv
        ftm['ep'] = 'ep%s' % idv
        ftm['on'] = 'on%s' % idv
        ftm['pa'] = 'pa%s' % idv
        ftm['mi'] = 'mi%s' % idv
        ftm['ta'] = taji
        sql += tmpl.format(**ftm)
    sql += 'COMMIT;'
    return sql


def insert_stud(db, napo, neos, taji):
    sql = generate_stud(napo, neos+1, taji)
    dbscript(sql, db)
    print('everything ok')


if __name__ == '__main__':
    db = '/home/tedlaz/pyted/programma/prg.sql3'
    # print(dbselect('select * from stud', db))
    insert_stud(db, 1, 120, 1)
    insert_stud(db, 121, 200, 4)
    insert_stud(db, 201, 240, 5)
    insert_stud(db, 241, 300, 6)
    insert_stud(db, 301, 340, 7)
    insert_stud(db, 341, 360, 8)
