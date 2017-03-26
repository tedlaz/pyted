import sqlite3
import os

application_path = os.path.dirname(__file__)
dbFilePath = os.path.join(application_path, 'db.db')

_conn = sqlite3.connect(dbFilePath, check_same_thread=False)
_conn.row_factory = sqlite3.Row
_cursor = _conn.cursor()

def rowsd(sql, par):
    _cursor.execute(sql, par)
    rows = _cursor.fetchall()
    arrayOfDictionaries = []
    for row in rows:
        arrayOfDictionaries.append(dict(zip(row.keys(), row)))
    return arrayOfDictionaries

class TodoModel:
    def __init__(self):
        pass

    @classmethod
    def add_item(cls, epo, ono, pat):
        sql = 'INSERT INTO erg(epo, ono, pat) VALUES(?, ?, ?)'
        _cursor.execute(sql, (epo, ono, pat))
        _conn.commit()

    @classmethod
    def retrieve_last_N_items(cls, n):
        sql = 'SELECT * FROM erg ORDER BY id DESC LIMIT ?'
        return rowsd(sql, (n, ))

    @classmethod
    def retrieve_all(cls):
        sql = 'SELECT * FROM erg ORDER BY id DESC'
        return rowsd(sql)
