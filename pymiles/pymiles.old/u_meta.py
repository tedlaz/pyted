# -*- coding: utf-8 -*-

from u_logger import log
import u_db_sqlparse as sqp


class Meta(object):

    """
    First we try to connect with database.
    Then we parse metadata with metadata parser
    """

    def __init__(self, dbpath):
        self.initdata(dbpath)

    def initdata(self, dbpath):
        self._dbpath = dbpath
        self._sqlmeta = {}
        self._tables = []
        self._field_lbl = {'id': u'AA'}
        self._field_qt = {}
        self._field_tp = {}  # field type
        self._field_notnull = {}
        self._table_lbl = {}
        self._table_lblp = {}
        self._sqlmeta = sqp.return_meta(self._dbpath)
        for table in self._sqlmeta.keys():
            for field in self._sqlmeta[table]:
                self._field_tp[field['fname']] = field['type']
                self._field_notnull[field['fname']] = field['notnull']

    def tables(self):
        return sorted(self._sqlmeta.keys())

    def fields(self):
        tmplist = []
        for table in self._sqlmeta.keys():
            for field in self._sqlmeta[table]:
                fldname = field['fname']
                if fldname not in tmplist:
                    tmplist.append(fldname)
        return sorted(tmplist)

    def table_fields(self, table):
        tmplist = []
        if table not in self.tables():
            return []
        for field in self._sqlmeta[table]:
            tmplist.append(field['fname'])
        return tmplist

    def field_lbl(self, field):
        return self._field_lbl.get(field, field)

    def field_qt(self, field):
        return self._field_qt.get(field, 'textline')

    def table_lbl(self, tablename):
        return self._table_lbl.get(tablename, tablename)

    def table_lblp(self, tablename):
        return self._table_lblp.get(tablename, tablename)
