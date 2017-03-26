# -*- coding: utf-8 -*-


class Metadbz():

    def __init__(self):
        self._flbl = {}  # field labels
        self._flbl['id'] = u'No'
        self._ftyp = {}  # field types
        self._ftyp['id'] = 'INTEGER'
        self._fnnu = {}  # field not null (0, 1)
        self._fmax = {}
        '''
        fields = ['fld', 'flbl', 'zftyp_id', 'nonull', 'max',
                  'ftyp',
                  'tbl', 'zttyp_id', 'tlbl', 'tlblp',
                  'zt_id', 'zfld_id', 'uniq', 'tuniq', 'rpr',
                  'ttyp',
                  'key', 'val',
                  'vname', 'vsql']
        '''
        self._flbl['fld'] = 'Field'
        self._flbl['flbl'] = 'Field label'
        self._flbl['zftyp_id'] = 'SQL,QT Type'
        self._flbl['nonull'] = 'Not Null'
        self._flbl['max'] = 'Max Size'
        self._flbl['ftyp'] = 'SQL,Qt Type'
        self._flbl['tbl'] = 'Table'
        self._flbl['zttyp_id'] = 'Table or View'
        self._flbl['tlbl'] = 'Table Label'
        self._flbl['tlblp'] = 'Table Label Plural'
        self._flbl['rpr'] = 'in rpr'
        self._flbl['zt_id'] = 'Table'
        self._flbl['zfld_id'] = 'Field'
        self._flbl['uniq'] = 'is Unique'
        self._flbl['tuniq'] = 'is Table Unique'
        self._flbl['ttyp'] = 'Table or View'
        self._flbl['key'] = 'meta key'
        self._flbl['val'] = 'meta value'
        self._flbl['vname'] = 'View name'
        self._flbl['vsql'] = 'View SQL'

        self._ftyp['fld'] = 'VARCHAR'
        self._ftyp['flbl'] = 'VARCHAR'
        self._ftyp['zftyp_id'] = 'IDCOMBO'
        self._ftyp['nonull'] = 'YESNO'
        self._ftyp['max'] = 'INTEGER'
        self._ftyp['ftyp'] = 'VARCHAR'
        self._ftyp['tbl'] = 'VARCHAR'
        self._ftyp['zttyp_id'] = 'IDCOMBO'
        self._ftyp['tlbl'] = 'VARCHAR'
        self._ftyp['tlblp'] = 'VARCHAR'
        self._ftyp['zt_id'] = 'IDBUTTON'
        self._ftyp['zfld_id'] = 'IDBUTTON'
        self._ftyp['uniq'] = 'YESNO'
        self._ftyp['tuniq'] = 'YESNO'
        self._ftyp['rpr'] = 'YESNO'
        self._ftyp['ttyp'] = 'VARCHAR'
        self._ftyp['key'] = 'VARCHAR'
        self._ftyp['val'] = 'VARCHAR'
        self._ftyp['vname'] = 'VARCHAR'
        self._ftyp['vsql'] = 'TEXT'

        self._fnnu['fld'] = 1
        self._fnnu['flbl'] = 1
        self._fnnu['zftyp_id'] = 1
        self._fnnu['nonull'] = 1
        self._fnnu['max'] = 1
        self._fnnu['ftyp'] = 1
        self._fnnu['tbl'] = 1
        self._fnnu['zttyp_id'] = 1
        self._fnnu['tlbl'] = 1
        self._fnnu['tlblp'] = 1
        self._fnnu['zt_id'] = 1
        self._fnnu['zfld_id'] = 1
        self._fnnu['uniq'] = 1
        self._fnnu['tuniq'] = 1
        self._fnnu['rpr'] = 1
        self._fnnu['ttyp'] = 1
        self._fnnu['key'] = 1
        self._fnnu['val'] = 1
        self._fnnu['vname'] = 1
        self._fnnu['vsql'] = 1

        self._fmax['fld'] = 10
        self._fmax['flbl'] = 30
        self._fmax['zftyp_id'] = 10
        self._fmax['max'] = 10
        self._fmax['ftyp'] = 20
        self._fmax['tbl'] = 10
        self._fmax['zttyp_id'] = 10
        self._fmax['tlbl'] = 30
        self._fmax['tlblp'] = 30
        self._fmax['zt_id'] = 10
        self._fmax['zfld_id'] = 10
        self._fmax['uniq'] = 1
        self._fmax['tuniq'] = 1
        self._fmax['rpr'] = 1
        self._fmax['ttyp'] = 10
        self._fmax['key'] = 50
        self._fmax['val'] = 50
        self._fmax['vname'] = 30
        self._fmax['vsql'] = 500

        self._tables = ['zfld', 'zftyp', 'zt', 'zt_d', 'zttyp', 'zkv', 'zv']
        self._tlbl = {}  # table labels
        self._tlbp = {}  # table labels plural
        self._trpr = {}  # table rpr

        self._tlbl['zfld'] = 'Field'
        self._tlbl['zftyp'] = 'Sql, Qt type'
        self._tlbl['zt'] = 'Table'
        self._tlbl['zt_d'] = 'Field'
        self._tlbl['zttyp'] = 'Table or view'
        self._tlbl['zkv'] = 'Key-value'
        self._tlbl['zv'] = 'View'

        self._tlbp['zfld'] = 'Fields'
        self._tlbp['zftyp'] = 'Sql, Qt types'
        self._tlbp['zt'] = 'Tables'
        self._tlbp['zt_d'] = 'Tables-Fields'
        self._tlbp['zttyp'] = 'Tables or views'
        self._tlbp['zkv'] = 'Keys-Values'
        self._tlbp['zv'] = 'Views'

        self._trpr['zfld'] = ['fld']
        self._trpr['zftyp'] = ['ftyp']
        self._trpr['zt'] = ['tbl']
        self._trpr['zt_d'] = ['zt_id', 'zfld_id']
        self._trpr['zttyp'] = ['ttyp']
        self._trpr['zkv'] = ['key']
        self._trpr['zv'] = 'vname'

        self._tbl_flds = {}
        self._tbl_flds['zfld'] = ['id', 'fld', 'flbl', 'zftyp_id',
                                  'nonull', 'max']
        self._tbl_flds['zftyp'] = ['id', 'ftyp']
        self._tbl_flds['zt'] = ['id', 'tbl', 'zttyp_id', 'tlbl',
                                'tlblp']
        self._tbl_flds['zt_d'] = ['id', 'zt_id', 'zfld_id', 'uniq', 'tuniq',
                                  'rpr']
        self._tbl_flds['zttyp'] = ['id', 'ttyp']
        self._tbl_flds['zkv'] = ['id', 'key', 'val']
        self._tbl_flds['zv'] = ['id', 'vname', 'vsql']

    def table_fields(self, table):
        """
        Returns a list with table's fields
        """
        assert(table in self._tables)
        return self._tbl_flds[table]

    def tlabel(self, table, plural=False):
        """
        Returns table label
        """
        if plural:
            return self._tlbp.get(table, table)
        else:
            return self._tlbl.get(table, table)

    def flabel(self, field):
        return self._flbl.get(field, field)

    def ftype(self, field):
        return self._ftyp.get(field, 'VARCHAR')

    def labels_from_fields(self, fields):
        """
        Returns a list with field labels.
        """
        labels = []
        for field in fields:
            # if no label just return the field
            labels.append(self._flbl.get(field, field))
        return labels

    def rpr_field(self, table):
        rprf = self._trpr.get(table, '')
        return " || ' ' || ".join(rprf)

    def rpr(self, table):
        """
        RETURNs sql with id and representation data of field
        """
        rpr = self.rpr_field(table)
        sql = "SELECT id, %s as rpr FROM %s" % (rpr, table)
        return sql

    def _sql_arr_all(self, table):
        """
        given a table get all fields and replace foreign keys with actual
        fields from foreign table
        """
        fields = self._tbl_flds[table]
        final = []
        inner = []
        innertxt = 'INNER JOIN %s ON %s.id=%s.%s_id'
        for field in fields:
            tmptxt = '%s.%s' % (table, field)
            if field == 'id':
                tmptxt += " as %s_ID" % table
            final.append(tmptxt)
            if field.endswith('_id'):
                tabl = field[:-3]
                inner.append(innertxt % (tabl, tabl, table, tabl))
                fin, inn = self._sql_arr_all(tabl)
                final += fin
                inner += inn
        return final, inner

    def sql_all(self, table):
        """
        Returns sql with full foreign key analysis
        Looks for foreign keys and makes all required INNER JOINS
        """
        fields, inner = self._sql_arr_all(table)
        sql = "SELECT " + ', '.join(fields) + ('\nFROM %s\n' % table)
        sql += '\n'.join(inner)
        return sql

    def sql_rpr(self, table):
        fields = self._tbl_flds[table]
        innertxt = 'INNER JOIN %s ON %s.id=%s.%s_id'
        dflds = []
        inner = []
        for field in fields:
            tmpsql = '%s.%s' % (table, field)
            if field.endswith('_id'):
                tabl = field[:-3]
                inner.append(innertxt % (tabl, tabl, table, tabl))
                tmpsql = "%s as %s" % (self.rpr_field(tabl), field)
            dflds.append(tmpsql)
        sql = "SELECT " + ', '.join(dflds) + ('\nFROM %s\n' % table)
        sql += '\n'.join(inner)
        return sql

    def dic_for_menu(self):
        alist = []
        for table in self._tables:
            if table.endswith('_d'):
                continue
            adic = {'name': table,
                    'title': self.tlabel(table, True),
                    'typ': 'tbl'}
            alist.append(adic)
        return alist
