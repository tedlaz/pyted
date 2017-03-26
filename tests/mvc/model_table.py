# -*- coding: utf-8 -*-
from PyQt4 import QtCore


class ModelTable(QtCore.QAbstractTableModel):

    def __init__(self, data=[[]], headers=[], parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__data = data
        self.__headers = headers

    def header(self, idx):
        if idx < len(self.__headers):
            return self.__headers[idx]
        else:
            return 'No Header'

    def saved(self, idx):
        print('Data saved to DB no %s' % idx)

    def rows(self):
        return len(self.__data)

    def cols(self):
        if self.__data:
            return len(self.__data[0])
        else:
            return 0

    def rowCount(self, parent):
        return len(self.__data)

    def columnCount(self, parent):
        if self.__data:
            return len(self.__data[0])
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
                self.__data[row][column] = value
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
                valn = section + 1
                return QtCore.QString("%1").arg(valn)

    # =====================================================#
    # INSERTING & REMOVING
    # =====================================================#
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
