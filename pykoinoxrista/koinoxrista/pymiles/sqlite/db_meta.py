 # -*- coding: utf-8 -*-

from pymiles.sqlite import db_select as dbs

sql_zfld = '''SELECT zfld.fld, zfld.flbl, zftyp.ftyp, zfld.nonull, zfld.max
FROM zfld
INNER JOIN zftyp ON zftyp.id=zfld.zftyp_id
'''
sql_zt = '''SELECT tbl, zttyp_id, tlbl, tlblp
FROM zt
ORDER BY tbl
'''
sql_ztf = '''SELECT zt.tbl as tabl, zfld.fld as field, zt_d.rpr as rpr
FROM zt
INNER JOIN zt_d ON zt.id=zt_d.zt_id
INNER JOIN zfld ON zfld.id=zt_d.zfld_id
ORDER BY zt.tbl, zt_d.id
'''
# , zt_d.rpr as rpr


class Metadb():

    def __init__(self, dbmeta='app.meta'):
        self._dbmeta = dbmeta

        self._flbl = {}  # field labels
        self._flbl['id'] = u'No'
        self._ftyp = {}  # field types
        self._ftyp['id'] = 'INTEGER'
        self._fnnu = {}  # field not null (0, 1)
        self._fmax = {}
        for row in dbs.select(dbmeta, sql_zfld)['rows']:
            self._flbl[row['fld']] = row['flbl']
            self._ftyp[row['fld']] = row['ftyp']
            self._fnnu[row['fld']] = row['nonull']
            self._fmax[row['fld']] = row['max']

        self._tables = []
        self._tlbl = {}  # table labels
        self._tlbp = {}  # table labels plural
        self._trpr = {}  # table rpr
        for row in dbs.select(dbmeta, sql_zt)['rows']:
            self._tables.append(row['tbl'])
            self._tlbl[row['tbl']] = row['tlbl']
            self._tlbp[row['tbl']] = row['tlblp']
            # self._trpr[row['tbl']] = row['rpr']

        self._tbl_flds = {}  # Table fields {'tbl1':['id', 'fld1', 'fld2' ], }
        for row in dbs.select(dbmeta, sql_ztf)['rows']:
            if row['tabl'] not in self._tbl_flds.keys():
                self._tbl_flds[row['tabl']] = ['id']
            self._tbl_flds[row['tabl']].append(row['field'])
            if row['rpr'] == 1:
                if row['tabl'] not in self._trpr.keys():
                    self._trpr[row['tabl']] = [row['field']]
                else:
                    self._trpr[row['tabl']].append(row['field'])

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
        rprf = " || ' ' || ".join(self._trpr.get(table, []))
        if rprf:
            return " || ' ' || ".join(self._trpr.get(table, []))
        else:
            return 'id'

    def _rpr_list(self, table):
        fields = self._trpr.get(table, [])
        rprv = []
        innerjoin = []
        innertxt = 'INNER JOIN %s ON %s.id=%s.%s_id'
        for field in fields:
            if field.endswith('_id'):
                tabl = field[:-3]
                innerjoin.append(innertxt % (tabl, tabl, table, tabl))
                rprt, innert = self._rpr_list(tabl)
                rprv += rprt
                innerjoin += innert
            else:
                rprv.append('%s.%s' % (table, field))
        return rprv, innerjoin

    def rpr(self, table):
        """
        RETURNs sql with id and representation data of field
        """
        flds, inns = self._rpr_list(table)
        sql = "SELECT %s.id, %s as rpr FROM %s\n%s"
        return sql % (table, " || ' ' || ".join(flds), table, '\n'.join(inns))

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
                tmpsql = "%s.%s as %s" % (tabl, self.rpr_field(tabl), field)
            dflds.append(tmpsql)
        sql = "SELECT " + ', '.join(dflds) + ('\nFROM %s\n' % table)
        sql += '\n'.join(inner)
        return sql

    def dic_for_menu(self):
        alist = []
        # {'name': 'erg', 'title': u'Εργαζόμενος', 'typ': 'tbl'}
        for table in self._tables:
            if table.endswith('_d'):
                continue
            adic = {'name': table,
                    'title': self.tlabel(table, True),
                    'typ': 'tbl'}
            alist.append(adic)
        return alist
