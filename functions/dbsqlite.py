# -*- coding: utf-8 -*-
import sqlite3


class Db():
    def __init__(self, db=':memory:'):
        self.db = db

    def rowst(self, sql, withColumnNames=False):
        '''
        Get a list of tuples of rows [(), (), ...]
        '''
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(sql)
        if withColumnNames:
            columnNames = [t[0] for t in cur.description]
        rws = cur.fetchall()
        cur.close()
        con.close()
        if withColumnNames:
            return columnNames, rws
        else:
            return rws

    def rowsd(self, sql):
        '''
        Get a list of dictionaries [{}, {}, ...]
        '''
        con = sqlite3.connect(self.db)
        #con.create_function("grdec", 1, grdec)
        #con.create_function("dec1", 1, dec)
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

    def columnames(self, sql):
        '''
        Get a list with column names
        '''
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(sql)
        columnNames = [t[0] for t in cur.description]
        cur.close()
        con.close()
        return columnNames


def test():
    t = Db()
    sql = "select 1 as a , 2 as b"
    print(t.rowst(sql, True))
    print(t.rowsd(sql))
    print(t.columnames(sql))

if __name__ == '__main__':
    test()
