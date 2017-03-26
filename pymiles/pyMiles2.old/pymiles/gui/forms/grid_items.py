# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from pymiles.utils import txt_num as tu


class sortWidgetItem(QtGui.QTableWidgetItem):

    def __init__(self, text, sortKey):
        # call custom constructor with UserType item type
        QtGui.QTableWidgetItem.__init__(self,
                                        text,
                                        QtGui.QTableWidgetItem.UserType)
        self.sortKey = sortKey

    def __lt__(self, other):
        return self.sortKey < other.sortKey


def _intItem(num):
    # be sure that num is number or zero
    try:
        float(num)
    except:
        num = 0
    item = sortWidgetItem(str(num), int(num))
    item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    return item


def _numItem(num):
    item = sortWidgetItem(tu.strGrDec(num), num)
    item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    return item


def _strItem(strv):
    st = '%s' % strv
    if st == 'None':
        st = ''
    item = QtGui.QTableWidgetItem(st)
    return item


def _dateItem(strv):
    strv = '%s' % strv
    if len(strv) < 10:
        item = sortWidgetItem(strv, strv)
    else:
        y, m, d = strv.split('-')
        item = sortWidgetItem('%s/%s/%s' % (d, m, y), strv)
    return item


def tblitem(typ, val):
    '''
    Factory for fld classes.
    '''
    typo = typ.upper()
    if typo == 'BOOLEAN':
        return _strItem(val)
    elif typo == 'DATE':
        return _dateItem(val)
    elif typo == 'DATEN':
        return _dateItem(val)
    elif typo == 'INTEGER':
        return _intItem(val)
    elif typo == 'INTEGERS':
        return _strItem(val)
    elif typo == 'NUMERIC':
        return _numItem(val)
    elif typo == 'NUMERICS':
        return _numItem(val)
    elif typo == 'TEXT':
        return _strItem(val)
    elif typo == 'IDBUTTON':
        return _strItem(val)
    elif typo == 'IDCOMBO':
        return _strItem(val)
    elif typo == 'VARCHAR':
        return _strItem(val)
    elif typo == 'VARCHARN':
        return _strItem(val)
    elif typo == 'WEEKDAYS':
        return _strItem(val)
    elif typo == 'YESNO':
        if int(val):
            return _strItem('Yes')
        else:
            return _strItem('No')
    else:
        return _strItem(val)
