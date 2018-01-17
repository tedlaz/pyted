"""Sqlite functions"""
import sqlite3
from . import gr
DELETE, INSERT, UPDATE = range(3)


def fields_of(dbf, table_or_view):
    """A Tuple with table or view fields"""
    sql = 'SELECT * FROM %s LIMIT 0' % table_or_view
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        cur.execute(sql)
        column_names = [t[0] for t in cur.description]
        cur.close()
    return tuple(column_names)


def select(dbf, sql):
    with sqlite3.connect(dbf) as con:
        cur = con.cursor()
        con.create_function("grup", 1, gr.grup)
        try:
            cur.execute(sql)
        except sqlite3.OperationalError:
            return None
        names = tuple([t[0] for t in cur.description])
        rows = cur.fetchall()
    return gr.NamesTuples(names, rows)


def select_simple_safe(pardic):
    with sqlite3.connect(pardic['db']) as con:
        cur = con.cursor()
        try:
            cur.execute(pardic['sql'])
            # cur.execute("SELECT * FROM ?", ('cdb',))
        except sqlite3.OperationalError as err:
            print(err)
        rows = cur.fetchall()
    return rows


def search_complex_sql(dbf, table_name, search_string):
    """Find records with many key words in search_string"""
    search_list = search_string.split()
    search_sql = []
    flds = fields_of(dbf, table_name)
    search_field = " || ' ' || ".join(flds)
    sql = "SELECT * FROM %s \n" % table_name
    where = ''
    for search_str in search_list:
        grup_str = grup(search_str)
        tstr = " grup(%s) LIKE '%%%s%%'\n" % (search_field, grup_str)
        search_sql.append(tstr)
        where = 'WHERE'
    # if not search_string sql is simple select
    return sql + where + ' AND '.join(search_sql)


def sqlscript(dbf, sql):
    '''sql   : A set of sql commands (create, insert or update)'''
    try:
        con = sqlite3.connect(dbf)
        cur = con.cursor()
        cur.executescript(sql)
        con.commit()
    except sqlite3.Error:
        con.rollback()
        cur.close()
        con.close()
        return False
    last_inserted_id = cur.lastrowid
    cur.close()
    con.close()
    return last_inserted_id


def insert(dbf, sql):
    try:
        con = sqlite3.connect(dbf)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
    except sqlite3.Error as err:
        con.rollback()
        cur.close()
        con.close()
        return False, str(err)
    last_inserted_id = cur.lastrowid
    cur.close()
    con.close()
    return True, last_inserted_id


def save_to_db(dbf, sql_par):
    """Safely save data to database"""
    try:
        con = sqlite3.connect(dbf)
        cur = con.cursor()
        # 'INSERT INTO erg VALUES(?,?,?)', ('id', 'epo', 'ono')
        cur.execute(sql_par['sql'], sql_par['par'])
        con.commit()
    except sqlite3.Error as err:
        con.rollback()
        cur.close()
        con.close()
        return False, str(err)
    last_inserted_id = cur.lastrowid
    cur.close()
    con.close()
    return True, last_inserted_id


def create_sql(table, flds, vals, typ=INSERT):
    """flds, vals are tuples"""
    assert len(flds) == len(vals)
    assert flds[0] == 'id'
    sqlinsert = "INSERT INTO %s (%s) VALUES (%s)"
    sqlupdate = "UPDATE %s SET %s WHERE id=?"
    if typ == INSERT:
        qms = ['?' for fld in flds]
        sql = sqlinsert % (table, ', '.join(flds), ', '.join(qms))
        return {'sql': sql, 'par': vals}
    elif typ == UPDATE:
        qms = ['%s=?' % fld for fld in flds if fld != 'id']
        sql = sqlupdate % (table, ', '.join(qms))
        return {'sql': sql, 'par': vals[1:] + (vals[0],)}
    elif typ == DELETE:
        sql = "DELETE FROM %s WHERE id=?" % table
        return {'sql': sql, 'par': (vals[0],)}
    return None