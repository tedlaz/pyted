'''
Module db_context_manager.py
Connect to sqlite database and perform crud functions
'''
import sqlite3
import os


PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
print(PATH)


def grup(txtVal):
    '''
    Trasforms a string to uppercase special for Greek comparison
    '''
    ar1 = u"αάΆΑβγδεέΈζηήΉθιίϊΊκλμνξοόΌπρσςτυύΎφχψωώΏ"
    ar2 = u"ΑΑΑΑΒΓΔΕΕΕΖΗΗΗΘΙΙΙΙΚΛΜΝΞΟΟΟΠΡΣΣΤΥΥΥΦΧΨΩΩΩ"
    ftxt = u''
    for letter in txtVal:
        if letter in ar1:
            ftxt += ar2[ar1.index(letter)]
        else:
            ftxt += letter.upper()
    return ftxt


class Open_sqlite:
    '''
    Context manager class
    Use it as:
    with Open_sqlite(dbfilename) as db:
        your code here ...
    '''
    def __init__(self, dbfile):
        self.db = dbfile
        self.active = False

    def __enter__(self):
        self.con = sqlite3.connect(self.db)
        self.con.create_function("grup", 1, grup)
        self.cur = self.con.cursor()
        self.active = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.active:
            self.cur.close()
            self.con.close()

    def script(self, sqlscript):
        self.con.executescript(sqlscript)
        return True

    def application_id(self):
        '''Get application_id from database file'''
        sql = 'PRAGMA application_id;'
        try:
            rws = self.select(sql)
            return rws[0][0]
        except:
            return -9

    def set_application_id(self, id):
        '''Set application_id to database file'''
        self.execute_script('PRAGMA application_id = %s;' % id)

    def user_version(self):
        '''Get user_version from database file'''
        sql = 'PRAGMA user_version;'
        try:
            rws = self.select(sql)
            return rws[0][0]
        except:
            return -9

    def set_user_version(self, version):
        '''Set user_version to database file'''
        self.execute_script('PRAGMA user_version = %s;' % version)

    def select(self, sql):
        '''Get a list of tuples with data'''
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows

    def select_with_names(self, sql):
        '''Get a tuple with column names and a list of tuples with data'''
        self.cur.execute(sql)
        column_names = tuple([t[0] for t in self.cur.description])
        rows = self.cur.fetchall()
        return column_names, rows

    def select_as_dict(self, sql):
        '''Get a list of dictionaries [{}, {}, ...]'''
        self.cur.execute(sql)
        column_names = [t[0] for t in self.cur.description]
        rows = self.cur.fetchall()
        arrayOfDictionaries = []
        for row in rows:
            dic = {}
            for i, col in enumerate(row):
                dic[column_names[i]] = col
            arrayOfDictionaries.append(dic)
        diclen = len(arrayOfDictionaries)
        if diclen > 0:
            return arrayOfDictionaries
        else:
            return [{}]

    def select_master_detail_as_dic(self,
                                    idv,
                                    tablemaster,
                                    tabledetail=None,
                                    id_at_end=True):
        '''
        Get a specific record from table tablemaster with id = idv
        If we pass a tabledetail value it gets detail records too
        idv : id value of record
        tablemaster : Master table name
        tabledetail : Detail table name
        id_at_end   : If True Foreign key is like <masterTable>_id
                      else is like id_<masterTable>
        '''
        if id_at_end:
            fkeytemplate = '%s_id'
        else:
            fkeytemplate = 'id_%s'

        id_field = fkeytemplate % tablemaster
        sql1 = "SELECT * FROM %s WHERE id='%s'" % (tablemaster, idv)
        sql2 = "SELECT * FROM %s WHERE %s='%s'" % (tabledetail, id_field, idv)
        dic = self.select_as_dict(sql1)[0]
        if len(dic) == 0:
            return dic
        if tabledetail:
            dic['zlines'] = self.select_as_dict(sql2)
            # Remove id_field key
            for el in dic['zlines']:
                del el[id_field]
        return dic


if __name__ == '__main__':
    dbpath = '/home/tedlaz/tedfiles/prj/2017/2017a.sql3'
    with Open_sqlite(dbpath) as db:
        print(db.select('select * from lmo limit 2;'))
        print(db.select_as_dict('select * from vtr_trd limit 10;'))
        print(db.select_with_names('select * from lmo limit 2;'))
        # print(db.script('PRAGMA application_id = 20170313;'))
        print(db.application_id())
        print(db.user_version())
        print(db.select_master_detail_as_dic(1, 'tr', 'trd', False))
        print(db.select_master_detail_as_dic(20, 'tr'))
        print(db.select_master_detail_as_dic(200000, 'tr'))
        print(db.select_master_detail_as_dic(200000, 'tr', 'trd', False))
