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


class DbException(Exception):
    """Exception to use with class Dbmanager"""
    pass


def connect(dbf, new_db=False):
    """
    :param dbf: Database file path
    :param new_db: True if you want to create a new database
    """
    if not new_db:
        assert os.path.exists(dbf)
    con = None
    cur = None
    try:
        con = sqlite3.connect(dbf)
        cur = con.cursor()
    except:
        pass
    return con, cur


def close(con, cur):
    """Close connection"""
    cur.close()
    con.close()


def select(dbf, sql, return_type=None):
    """select data records

    :param dbf: Database file path
    :param sql: SQL to run
    :param rtype: return type
    :return: list of tuples [(), (), ...]
    """
    if not sql[:6].upper() in ('SELECT', 'PRAGMA'):
        raise DbException('Wrong sql : %s' % sql)
    con, cur = connect(dbf)
    con.create_function("grup", 1, grup)
    try:
        cur.execute(sql)
    except sqlite3.OperationalError:
        return None
    column_names = tuple([t[0] for t in cur.description])
    rows = cur.fetchall()
    close(con, cur)
    rtypes = ('names-tuples', 'dicts')
    if return_type not in rtypes:
        return rows
    if return_type == 'names-tuples':
        return column_names, rows
    if return_type == 'dicts':
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


def table_records(dbf, table_name, return_type='tuples'):
    """Select all values of a table
    """
    sql = "SELECT * FROM %s" % table_name
    return select(dbf, sql, return_type)


def find_by_id(dbf, vid, table, rtype):
    sql1 = "SELECT * FROM %s WHERE id='%s'" % (table, vid)
    return select(dbf, sql1, rtype)


def find_by_id_md(dbf, idv, tablemaster, tabledetail=None, id_at_end=True):
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
    dic = select(dbf, sql1, 'dicts')[0]
    ldic = len(dic)
    if ldic == 0:
        return dic
    if tabledetail:
        dic['zlines'] = select(dbf, sql2, 'dicts')
        # Remove id_field key
        for elm in dic['zlines']:
            del elm[id_field]
    return dic


def find(dbf, table_name, search_string, rtype='dicts'):
    """Find records with multiple search strings

    :param table_name: Table or View name
    :param search_string: A string with space separated search values
    :return: List of dicts
    """
    search_list = search_string.split()
    search_sql = []
    flds = fields_of(dbf, table_name, False)
    search_field = " || ' ' || ".join(flds)
    sql = "SELECT * FROM %s \n" % table_name
    where = ''
    for search_str in search_list:
        grup_str = grup(search_str)
        tstr = " grup(%s) LIKE '%%%s%%'\n" % (search_field, grup_str)
        search_sql.append(tstr)
        where = 'WHERE'
    # if not search_string sql is simple select
    final_sql = sql + where + ' AND '.join(search_sql)
    return select(dbf, final_sql, rtype)


def tables_views(dbf, rel_type=None):
    """A tuple with database tables

    :param dbf: Database file path
    :param rel_type: 'tables', 'views' else tables and views
    """
    sql = "SELECT name FROM sqlite_master WHERE type='table' OR type='view';"
    if rel_type == 'tables':
        sql = "SELECT name FROM sqlite_master WHERE type='table';"
    elif rel_type == 'views':
        sql = "SELECT name FROM sqlite_master WHERE type='view';"
    val = select(dbf, sql)
    tbl = [el[0] for el in val]
    tbl.sort()
    return tuple(tbl)


def fields_of(dbf, table_or_view, with_id=True):
    """A Tuple with table or view fields

    :param table_or_view: Table or View name
    :param with_id: If True includes field named id
    """
    sql = 'SELECT * FROM %s LIMIT 0' % table_or_view
    con, cur = connect(dbf)
    cur.execute(sql)
    if with_id:
        column_names = [t[0] for t in cur.description]
    else:
        column_names = [t[0] for t in cur.description if t[0] != 'id']
    close(con, cur)
    return tuple(column_names)


def fields(dbf, rtype=None):
    """Returns fields of database

    :param dbf: Database file path
    :param rtype: 'table' , 'dict'
    :return: if rtype==None returns a list of fields sorted by name.

    If rtype=='table' returns a dict with tablenames as keys and list values of
    fields {table1: [fld1, fld2, ...], table2: [fl1, fl2, ..], ..}

    If rtype=='dict' returns a dict with fields as keys and list values of
    tables field belongs {fld1: [tbl1, tbl2, ..], fld2: [tbla, ...], ...}
    """
    tablesviews = tables_views(dbf)
    dfields = {}
    dtbflds = {}
    for vtv in tablesviews:
        relfields = fields_of(dbf, vtv)
        dtbflds[vtv] = list(relfields)
        for field in relfields:
            dfields[field] = dfields.get(field, [])
            dfields[field].append(vtv)
    if rtype == 'table':
        return dtbflds
    elif rtype == 'dict':
        return dfields
    return sorted(list(dfields.keys()))


def script(dbf, sqlscript):
    """Execute an sql script against self.dbf

    :param sqlscript: SQL to run
    :return: True if successfull execution
    """
    con, cur = connect(dbf)
    con.executescript(sqlscript)
    close(con, cur)
    return True


def create_db(dbf, sqlscript, user_version, app_id):
    """
    :param dbf: Database file path
    :param sqlscript: SQL script to run
    :param user_version: Set user_version
    :param app_id: Set application_id
    """
    con, cur = connect(dbf, True)
    con.executescript(sqlscript)
    con.executescript("PRAGMA user_version = %s" % user_version)
    con.executescript("PRAGMA application_id = %s" % app_id)
    close(con, cur)
    return True


def insert(dbf, sql):
    """Execute insert sql and get back id of inserted record

    :param sql: sql to run. Function checks that sql is insert sql
    :return: id of inserted record or None in case of failure
    """
    rid = None
    if not sql.upper().startswith('INSERT '):
        raise DbException('Wrong sql : %s' % sql)
    con, cur = open(dbf)
    cur.execute(sql)
    rid = cur.lastrowid
    close(con, cur)
    return rid


def pragmas(dbf):
    """Get user version and application id
    """
    sql_user_version = 'PRAGMA user_version;'
    sql_app_id = 'PRAGMA application_id;'
    user_version = select(dbf, sql_user_version)[0][0]
    app_id = select(dbf, sql_app_id)[0][0]
    return {'user_version': user_version, 'app_id': app_id}


def set_pragmas(dbf, user_version, app_id=None):
    """Set pragmas
    """
    if user_version:
        script(dbf, "PRAGMA user_version = %s;" % user_version)
    if app_id:
        script(dbf, "PRAGMA application_id = %s;" % app_id)


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
        # if not search_string sql is simple select
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

    def get_zlabels(self):
        sql = "SELECT * FROM zlbl"
        tuplfld = self.select(sql, return_type='tuples')
        labels = {}
        for line in tuplfld:
            labels[line[0]] = line[1]
        return labels

    def label(self, field):
        return self._zlabels.get(field, field)
