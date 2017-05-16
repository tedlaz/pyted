'''
Module db.py
Connect to sqlite database and perform crud functions

Example::

>>> from ted17 import db_context_manager as dbc
>>> with dbc.SqliteManager('path/to/sql3file') as db:
>>>     db.select('SELECT * from tbl1')
'''
import sqlite3
from .grup import grup


class DbException(Exception):
    """Exception to use with class Dbmanager"""
    pass


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
        self.in_context_mode = False
        self.active = False
        self.con = None
        self.cur = None

    def __enter__(self):
        self.con = sqlite3.connect(self.dbf)
        self.con.create_function("grup", 1, grup)
        self.cur = self.con.cursor()
        self.in_context_mode = True
        self.active = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.active:
            self.cur.close()
            self.con.close()
        self.in_context_mode = False

    def _open(self):
        if self.in_context_mode:
            return
        if not self.active:
            self.con = sqlite3.connect(self.dbf)
            self.con.create_function("grup", 1, grup)
            self.cur = self.con.cursor()
            self.active = True

    def _close(self):
        if self.in_context_mode:
            return
        if self.active:
            self.cur.close()
            self.con.close()
        self.cur = None
        self.con = None
        self.active = False

    def script(self, sqlscript):
        """Execute an sql script against self.dbf

        :param sqlscript: SQL to run
        :return: Nothing
        """
        self._open()
        self.con.executescript(sqlscript)
        self._close()
        return True

    def insert(self, sql):
        """Execute insert sql and get back id of inserted record

        :param sql: sql to run. Function checks that sql is insert sql
        :return: id of inserted record or None in case of failure
        """
        rid = None
        if not sql.upper().startswith('INSERT '):
            raise DbException('Wrong sql : %s' % sql)
        self._open()
        self.cur.execute(sql)
        rid = self.cur.lastrowid
        self._close()
        return rid

    def select(self, sql, return_type='tuples'):
        '''Get a list of tuples with data

        :param sql: SQL to run
        :return: List of tuples of rows
        '''
        if not sql[:6] in ('SELECT', 'PRAGMA'):
            raise DbException('Wrong sql : %s' % sql)
        function = None
        if return_type == 'tuples':
            function = self._select
        elif return_type == 'names-tuples':
            function = self._select_with_names
        elif return_type == 'dicts':
            function = self._select_as_dict
        else:
            function = self._select
        return function(sql)

    def find_records(self, table_name, search_string, rtype='dicts'):
        """Find records with multiple search strings

        :param table_name: Table or View name
        :param search_string: A string with space separated search values
        :return: List of dicts
        """
        search_list = search_string.split()
        search_sql = []
        fields = self.fields(table_name, False)
        search_field = " || ' ' || ".join(fields)
        sql = "SELECT * FROM %s \n" % table_name
        where = ''
        for search_str in search_list:
            grup_str = grup(search_str)
            tstr = " grup(%s) LIKE '%%%s%%'\n" % (search_field, grup_str)
            search_sql.append(tstr)
            where = 'WHERE'
        final_sql = sql + where + ' AND '.join(search_sql)
        return self.select(final_sql, rtype)

    def find_record_by_id(self, table, idval, rtype='dicts'):
        """Find a specific record in database, teble with id = idval

        :param table: Table or View name
        :param idval: Value of id
        :return: dictionary with values or {}
        """
        sql = "SELECT * FROM %s WHERE id='%s'" % (table, idval)
        rows = self.select(sql, rtype)
        return rows

    def select_table(self, table_name, return_type='tuples'):
        """Select all values of a table
        """
        sql = "SELECT * FROM %s" % table_name
        return self.select(sql, return_type)

    def select_key_val(self, sql):
        """Select val from table where key=keyval
        """
        rows = self.select(sql)
        lrows = len(rows)
        if lrows > 0:
            return rows[0][0]

    def _select(self, sql):
        '''Get a list of tuples with data

        :param sql: SQL to run
        :return: List of tuples of rows
        '''
        if not sql[:6] in ('SELECT', 'PRAGMA'):
            raise DbException('Wrong sql : %s' % sql)
        self._open()
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        self._close()
        return rows

    def _select_with_names(self, sql):
        '''Get a tuple with column names and a list of tuples with data

        :param sql: The sql to execute
        :return: (columnNam1, ...) [(dataLine1), (dataLine2), ...]
        '''
        self._open()
        self.cur.execute(sql)
        column_names = tuple([t[0] for t in self.cur.description])
        rows = self.cur.fetchall()
        self._close()
        return column_names, rows

    def _select_as_dict(self, sql):
        '''Get a list of dictionaries

        :param sql: The sql to execute
        :return: [{}, {}, ...]
        '''
        self._open()
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
        self._close()
        if diclen > 0:
            return diclist
        return [{}]

    def select_md(self, idv, tablemaster, tabledetail=None, id_at_end=True):
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
        dic = self._select_as_dict(sql1)[0]
        ldic = len(dic)
        if ldic == 0:
            return dic
        if tabledetail:
            dic['zlines'] = self._select_as_dict(sql2)
            # Remove id_field key
            for elm in dic['zlines']:
                del elm[id_field]
        return dic

    def tables(self):
        """A tuple with database tables"""
        sql = "SELECT name FROM sqlite_master WHERE type = 'table';"
        val = self.select(sql)
        tbl = [el[0] for el in val]
        tbl.sort()
        return tuple(tbl)

    def views(self):
        """A Tuple with database views"""
        sql = "SELECT name FROM sqlite_master WHERE type = 'view';"
        val = self.select(sql)
        viw = [el[0] for el in val]
        viw.sort()
        return tuple(viw)

    def fields(self, table_or_view, with_id=True):
        """A Tuple with table or view fields

        :param table_or_view: Table or View name
        """
        sql = 'SELECT * FROM %s LIMIT 0' % table_or_view
        self._open()
        self.cur.execute(sql)
        if with_id:
            column_names = [t[0] for t in self.cur.description]
        else:
            column_names = [t[0] for t in self.cur.description if t[0] != 'id']
        self._close()
        return tuple(column_names)

    def application_id(self):
        '''Get application_id from database file

        :return: application_id or -9
        '''
        sql = 'PRAGMA application_id;'
        self._open()
        try:
            app_id = self.select(sql)[0][0]
        except:
            app_id = 0
        self._close()
        return app_id

    def set_application_id(self, idv):
        '''Set application_id to database file

        :param idv: application_id value to set
        :return: nothing
        '''
        self._open()
        self.script('PRAGMA application_id = %s;' % idv)
        self._close()

    def user_version(self):
        '''Get user_version from database file

        :return: user_version or -9
        '''
        sql = 'PRAGMA user_version;'
        self._open()
        try:
            user_version = self.select(sql)[0][0]
        except:
            user_version = 0
        self._close()
        return user_version

    def set_user_version(self, version):
        '''Set user_version to database file

        :param version: version value to set
        :return: Nothing
        '''
        self._open()
        self.script('PRAGMA user_version = %s;' % version)
        self._close()
