'''
Module db.py
Connect to sqlite database and perform crud functions

Example::

>>> from ted17 import db_context_manager as dbc
>>> with dbc.SqliteManager('path/to/sql3file') as db:
>>>     db.select('SELECT * from tbl1')
'''
import sqlite3
import os
from .grup import grup


PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def dataFromDB(dbf, sql):
    """Get data from database

    :param dbf: Database file path
    :param sql: SQL to run
    :return: list of tuples [(), (), ...]
    """
    con = sqlite3.connect(dbf)
    con.create_function("grup", 1, grup)
    cur = con.cursor()
    cur.execute(sql)
    rws = cur.fetchall()
    cur.close()
    con.close()
    return rws


class SqliteManager:
    '''
    Context manager class
    '''
    def __init__(self, dbfile):
        self.dbf = dbfile  #: This is a test
        self.active = False
        self.con = None
        self.cur = None

    def __enter__(self):
        self.con = sqlite3.connect(self.dbf)
        self.con.create_function("grup", 1, grup)
        self.cur = self.con.cursor()
        self.active = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.active:
            self.cur.close()
            self.con.close()

    def script(self, sqlscript):
        """Execute an sql script against self.dbf

        :param sqlscript: SQL to run
        :return: Nothing
        """
        self.con.executescript(sqlscript)
        return True

    def application_id(self):
        '''Get application_id from database file

        :return: application_id or -9
        '''
        sql = 'PRAGMA application_id;'
        try:
            rws = self.select(sql)
            return rws[0][0]
        except:
            return -9

    def set_application_id(self, idv):
        '''Set application_id to database file

        :param idv: application_id value to set
        :return: nothing
        '''
        self.script('PRAGMA application_id = %s;' % idv)

    def user_version(self):
        '''Get user_version from database file

        :return: user_version or -9
        '''
        sql = 'PRAGMA user_version;'
        try:
            rws = self.select(sql)
            return rws[0][0]
        except:
            return -9

    def set_user_version(self, version):
        '''Set user_version to database file

        :param version: version value to set
        :return: Nothing
        '''
        self.script('PRAGMA user_version = %s;' % version)

    def select(self, sql):
        '''Get a list of tuples with data

        :param sql: SQL to run
        :return: list of tuples of rows
        '''
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows

    def select_with_names(self, sql):
        '''Get a tuple with column names and a list of tuples with data

        :param sql: The sql to execute
        :return: (columnNam1, ...) [(dataLine1), (dataLine2), ...]
        '''
        self.cur.execute(sql)
        column_names = tuple([t[0] for t in self.cur.description])
        rows = self.cur.fetchall()
        return column_names, rows

    def select_as_dict(self, sql):
        '''Get a list of dictionaries

        :param sql: The sql to execute
        :return: [{}, {}, ...]
        '''
        self.cur.execute(sql)
        column_names = [t[0] for t in self.cur.description]
        rows = self.cur.fetchall()
        diclist = []
        for row in rows:
            dic = {}
            for i, col in enumerate(row):
                dic[column_names[i]] = col
            diclist.append(dic)
        diclen = len(diclist)
        if diclen > 0:
            return diclist
        return [{}]

    def select_master_detail_as_dic(self,
                                    idv,
                                    tablemaster,
                                    tabledetail=None,
                                    id_at_end=True):
        '''
        Get a specific record from table tablemaster.
        If we pass it a tabledetail value, it gets detail records too.

        :param idv: id value of record
        :param tablemaster: Master table name
        :param tabledetail: Detail table name
        :param id_at_end: If True Foreign key is like tablemaster_id
         else is like id_mastertable
        :return: dictionary with values
        '''
        if id_at_end:
            fkeytemplate = '%s_id'
        else:
            fkeytemplate = 'id_%s'

        id_field = fkeytemplate % tablemaster
        sql1 = "SELECT * FROM %s WHERE id='%s'" % (tablemaster, idv)
        sql2 = "SELECT * FROM %s WHERE %s='%s'" % (tabledetail, id_field, idv)
        dic = self.select_as_dict(sql1)[0]
        ldic = len(dic)
        if ldic == 0:
            return dic
        if tabledetail:
            dic['zlines'] = self.select_as_dict(sql2)
            # Remove id_field key
            for elm in dic['zlines']:
                del elm[id_field]
        return dic
