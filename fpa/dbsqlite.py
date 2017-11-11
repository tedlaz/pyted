# -*- coding: utf-8 -*-
'''dbsqlite module'''
import sqlite3


class Db():
    '''
    Db class
    '''
    def __init__(self, db=':memory:'):
        self.db = db

    def rowst(self, sql, with_column_names=False):
        '''
        Get a list of tuples of rows [(), (), ...]
        '''
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(sql)
        if with_column_names:
            column_names = [t[0] for t in cur.description]
        rws = cur.fetchall()
        cur.close()
        con.close()
        if with_column_names:
            return column_names, rws
        else:
            return rws

    def rowsd(self, sql):
        '''
        Get a list of dictionaries [{}, {}, ...]
        '''
        con = sqlite3.connect(self.db)
        # con.create_function("grdec", 1, grdec)
        # con.create_function("dec1", 1, dec)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        con.close()
        array_of_dictionaries = []
        for row in rows:
            array_of_dictionaries.append(dict(zip(row.keys(), row)))
        return array_of_dictionaries

    def columnames(self, sql):
        '''
        Get a list with column names
        '''
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(sql)
        column_names = [t[0] for t in cur.description]
        cur.close()
        con.close()
        return column_names


def test():
    dbf = Db()
    sql = "select 1 as a , 2 as b"
    print(dbf.rowst(sql, True))
    print(dbf.rowsd(sql))
    print(dbf.columnames(sql))


if __name__ == '__main__':
    test()
