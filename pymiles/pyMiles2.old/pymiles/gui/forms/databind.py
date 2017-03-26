# -*- coding: utf-8 -*-
from pymiles.sqlite.db_select import select
from pymiles.sqlite.db_sql import save as sqlsave
from pymiles.sqlite.db_save import save as dbsave


class Databind():

    def __init__(self, parent, table, id_=None):
        assert(table is not None)
        assert(parent is not None)
        self.meta = self.parent().meta
        self.db = self.parent().db
        self.data = {}
        assert(self.db is not None)
        assert(table in self.meta._tables)
        self.table = table
        self.id = id_ or 0
        self.qtfields = {}
        self.last_inserted_id = None

    def populate(self, id_):
        sqlg = "SELECT * FROM %s WHERE id=%s" % (self.table, id_)
        dictdata = select(self.db, sqlg)
        assert(dictdata['rownum'] == 1)  # Must have one and only one record
        self.data = dictdata['rows'][0]
        for fld in self.meta.table_fields(self.table):
            self.qtfields[fld].set(self.data[fld])

    def save(self):
        fields = self._get_updated_fields()
        if not fields:
            self.accept()
            return
        if 'id' not in fields:
            fields.append('id')
        dicforsql = {}
        for field in fields:
            dicforsql[field] = self.qtfields[field].get()
        sqls = sqlsave(self.table, dicforsql)
        self.last_inserted_id = dbsave(self.db, [sqls, ])
        self.accept()

    def _get_updated_fields(self):
        if not self.data:
            return self.meta.table_fields(self.table)
        updated_fields = []
        for fld in self.meta.table_fields(self.table):
            # print(self.data[fld], self.qtfields[fld].get())
            vala = u'%s' % self.data[fld]
            valb = u'%s' % self.qtfields[fld].get()
            if vala != valb:
                updated_fields.append(fld)
        return updated_fields
