# -*- coding: utf-8 -*-
from PyQt4 import QtCore
import sqlite3
import os


class ModelTable(QtCore.QAbstractTableModel):

    def __init__(self, db, table, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        assert os.path.exists(db)
        self._db = db
        self._table = ''
        self.__data = [[]]
        self.__headers = []
        self.__fields = []
        self.getData(table)

    def sqltbl(self, table):
        fields, inner = self.sqlarr(table)
        sql = 'SELECT ' + ', '.join(fields)
        sql += '\nFROM %s\n' % table
        sql += ''.join(inner)
        return sql

    def sqlarr(self, table):
        fields = self.getfields(table)
        sqlflds = '%s.%s'  # table.fieldname
        sqlfldas = '%s.%s AS %s_%s'
        sqlinn = 'INNER JOIN %s ON %s.id=%s.%s\n'
        flds = []
        inner = []
        for field in fields:
            if field.startswith('id_'):
                tbl = field[3:]
                inner.append(sqlinn % (tbl, tbl, table, field))
                fl, inn = self.sqlarr(tbl)
                flds += fl
                inner += inn
            elif field.endswith('_id'):
                tbl = field[:-3]
                inner.append(sqlinn % (tbl, tbl, table, field))
                fl, inn = self.sqlarr(tbl)
                flds += fl
                inner += inn
            else:
                if field == 'id':

                    flds.append(sqlfldas % (table, field, table, field))
                else:
                    flds.append(sqlflds % (table, field))
        return flds, inner

    def getfields(self, table):
        sqlt = 'SELECT * FROM %s limit 0' % table
        con = sqlite3.connect(self._db)
        cur = con.cursor()
        cur.execute(sqlt)
        fields = [t[0] for t in cur.description]
        cur.close()
        con.close()
        return fields

    def getData(self, table):
        '''Select'''
        self._table = table
        sqlt = 'SELECT * FROM %s'
        con = sqlite3.connect(self._db)
        # con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sqlt % self._table)
        self.__headers = [t[0] for t in cur.description]
        self.__fields = [t[0] for t in cur.description]
        self.__data = list(cur.fetchall())
        cur.close()
        con.close()

    def header(self, idx):
        if idx < len(self.__headers):
            return self.__headers[idx]
        else:
            return 'No Header'

    def deleteFromDb(self, idx):
        rowid = self.var2string(idx)[0]
        if len(rowid) == 0:
            return
        sql = "DELETE FROM %s WHERE id='%s'" % (self._table, rowid)
        con = sqlite3.connect(self._db)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()
        self.removeRows(idx, 1)

    def isNull(self, idx):
        row = self.var2string(idx)
        fstr = u''
        for field in row:
            fstr += u'%s' % field
        return len(fstr.strip())

    def save2db(self, idx):
        # here we actually save data to db ...
        row = self.var2string(idx)
        flds = []
        vals = []
        vup = []
        si = u"INSERT INTO %s (%s) VALUES (%s);"
        su = u"UPDATE %s SET %s WHERE id='%s';"
        sql = u''

        for i, fld in enumerate(self.__fields):
            if i == 0:
                continue
            flds.append(fld)
            vals.append(u"'%s'" % row[i])
            vup.append("%s='%s'" % (fld, row[i]))
        if len(row[0]) > 0:
            # record already exists so do an update
            ', '.join(flds)
            self._update(su % (self._table, ', '.join(vup), row[0]))
            print('Record updated!!')
        else:
            # Insert a new record
            sql = si % (self._table, ', '.join(flds), ', '.join(vals))
            newid = self._insert(sql)
            self.__data[idx] = list(self.__data[idx])
            self.__data[idx][0] = newid
            self.__data[idx] = tuple(self.__data[idx])
            print('Record Saved !!!!')

    def _insert(self, sql):
        con = sqlite3.connect(self._db)
        cur = con.cursor()
        cur.execute(sql)
        insert_id = cur.lastrowid
        con.commit()
        cur.close()
        con.close()
        # post conditions
        assert insert_id > 0
        print(insert_id)
        return insert_id

    def _update(self, sql):
        con = sqlite3.connect(self._db)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()

    def var2string(self, idx):
        row = []
        for el in self.__data[idx]:
            try:
                row.append(u'%s' % el.toString())
            except:
                row.append(u'%s' % el)
        return row

    def saved(self, idx):
        print('Data saved to DB no %s' % idx)

    def rows(self):
        return len(self.__data)

    def cols(self):
        if self.__fields:
            return len(self.__fields)
        else:
            return 0

    def rowCount(self, parent):
        return len(self.__data)

    def columnCount(self, parent):
        if self.__fields:
            return len(self.__fields)
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | \
                    QtCore.Qt.ItemIsSelectable

    def data(self, index, role):

        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            return self.__data[row][column]

        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            column = index.column()
            return u"Τιμή: %s" % self.__data[row][column]

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__data[row][column]
            return value

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            if value:
                self.__data[row] = list(self.__data[row])
                # column 0 is probably the id column
                if column == 0:
                    return False
                av = value.toString().trimmed()
                self.__data[row][column] = av  # value
                self.__data[row] = tuple(self.__data[row])
                self.dataChanged.emit(index, index)
                return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "not implemented"
            else:
                # valn = section + 1
                # return QtCore.QString("%1").arg(valn)
                return ''

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            defaultValues = ['' for i in range(self.columnCount(None))]
            self.__data.insert(position, defaultValues)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.__data.pop(position)
        self.endRemoveRows()
        return True

if __name__ == '__main__':
    db = "sam2015.sql3"
    db2 = "mis.m13"
    model = ModelTable(db, 'trd')
    print(model.sqltbl('trd'))
