# -*- coding: utf-8 -*-

import u_db_select as udbs


class Metadb():

    def __init__(self, db):
        self.opendb(db)

    @property
    def db(self):
        return self._db

    def flbl(self, fld):
        if len(fld) > 3:
            if fld[-3:] == '_id':
                return self.tlbl(fld[:-3])
        return self._flbl.get(fld, fld)

    def ftype(self, fld):
        if len(fld) > 3:
            if fld[-3:] == '_id':
                return 'INTEGER'
        return self._ftyp.get(fld, 'VARCHAR(30)')

    def fnot_null(self, fld):
        return self._fnnu.get(fld, 1)

    def tlbl(self, tbl):
        return self._tlbl.get(tbl, tbl)

    def tlbp(self, tbl):
        return self._tlbp.get(tbl, tbl)

    def trpr(self, tbl):
        return self._trpr.get(tbl, "SELECT id, 'error' as rpr FROM %s" % tbl)

    def pars(self, par):
        return self._pars.get(par, '')

    def opendb(self, db):
        self._db = db
        self._flbl = {}
        self._ftyp = {}  # field type
        self._fnnu = {}  # field not null (0, 1)
        self._tlbl = {}
        self._tlbp = {}
        self._trpr = {}
        self._pars = {}
        self.zt_exists = False
        self.zf_exists = False
        self.z_exists = False
        sqlf = "SELECT fld, flbl, typos, nonull FROM zf"
        sqlt = "SELECT tbl, tlbl, tlblp, rpr FROM zt"
        sqlz = "SELECT key, val FROM z"
        valsf = udbs.select(db, sqlf)
        valst = udbs.select(db, sqlt)
        keval = udbs.select(db, sqlz)
        if valsf:
            self.zf_exists = True
            for line in valsf['rows']:
                self._flbl[line['fld']] = line['flbl']
                self._ftyp[line['fld']] = line['typos']
                self._fnnu[line['fld']] = line['nonull']
        if valst:
            self.zt_exists = True
            for line in valst['rows']:
                self._tlbl[line['tbl']] = line['tlbl']
                self._tlbp[line['tbl']] = line['tlblp']
                self._trpr[line['tbl']] = line['rpr']
        if keval:
            self.z_exists = True
            for line in keval['rows']:
                self._pars[line['key']] = line['val']
