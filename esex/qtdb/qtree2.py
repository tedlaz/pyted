# -*- coding: utf-8 -*-
'''
Created on 14 Ιαν 2013

@author: tedlaz
'''

from PyQt4 import QtCore, QtGui
import sys

import decimal
import dbforms as dbf
import locale

locale.setlocale(locale.LC_ALL, '')

sqlv = '''
SELECT strftime('%Y',es.dat) as etos,tr.per as quarter,mi.per as minas,strftime('%d/%m/%Y',es.dat) as dt,sr.srp || ' ' || es.par || ' ' || syn.epon, et.etp,esd.val,esd.fpa, esd.val+esd.fpa as tot
from es
INNER JOIN sr ON sr.id=es.sr_id
INNER JOIN syn ON syn.id=es.syn_id
INNER JOIN esd ON es.id = esd.es_id
INNER JOIN et ON et.id = esd.et_id
INNER JOIN tr on tr.id = (cast(strftime('%m', es.dat) as integer) + 2) / 3
INNER JOIN mi on mi.id = strftime('%m',es.dat)
ORDER BY es.dat, es.sr_id,es.par
'''


def isNum(value):  # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters :
            1.value : the value to check against.
        output: True or False
        """
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


def dec(poso, dekadika=2):
    """ use : Given a number, it returns a decimal with a specific number of decimals
        input Parameters:
            1.poso : The number for conversion in any format (e.g. string or int ..)
            2.dekadika : The number of decimals (default 2)
        output: A decimal number
        """
    PLACES = decimal.Decimal(10) ** (-1 * dekadika)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)


class Node():
    def __init__(self, name, parentn, vals):
        self._name = name
        self._vals = vals
        self._children = []
        self._parent = parentn
        if parentn is not None:
            parentn.addChild(self)
            self.updateParentn()

    def updateParentn(self):
        isnum = []
        tots = []
        for el in self._vals:
            if isNum(el):
                isnum.append(True)
                tots.append(0)
            else:
                isnum.append(False)
                tots.append('')
        for chi in self._parent._children:

            for i in range(len(chi._vals)):
                if isnum[i]:
                    tots[i] += chi.val(i)
        for i in range(len(self._vals)):
            if isnum[i]:
                self._parent.setVal(tots[i], i)
        self._parent.setVal(tots[2], 2)
        if self._parent._parent is not None:
            self._parent.updateParentn()

    def typeInfo(self):
        return "NODE"

    def addChild(self, child):
        self._children.append(child)

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def val(self, column):
        return self._vals[column]

    def valF(self, column):

        if isNum(self._vals[column]):
            return locale.format("%0.2f", self._vals[column], grouping=True)
        else:
            return self._vals[column]

    def setVal(self, val, column):
        self._vals[column] = val

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def __repr__(self):
        return self._name


class treeModel(QtCore.QAbstractItemModel):

    def __init__(self, root, headers, pare=None):
        super(treeModel, self).__init__(pare)
        self._rootNode = root
        self._headers = headers

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
        return parentNode.childCount()

    def columnCount(self, parent):
        return len(self._headers)

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.name()
            else:
                return node.valF(index.column())
        if role == QtCore.Qt.TextAlignmentRole:
            if index.column() >= 1:
                return QtCore.Qt.AlignRight

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            return self._headers[section]
        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def parent(self, index):
        node = self.getNode(index)
        parentNode = node.parent()
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self._rootNode


def dataForModel(dbvals, treeDepth=5, txtv=1, numv=3):
    valArr = [''] * txtv + [0] * numv
    valAr2 = [''] * txtv + [dec(0)] * numv
    n = [''] * treeDepth
    farr = []
    for el in dbvals:
        for i in range(treeDepth):
            if n[i] != el[i]:
                if i == 0:
                    farr.append([el[i], '0', valArr])
                else:
                    farr.append([el[i], el[i - 1], valArr])
                n[i] = el[i]
                if i + 1 < treeDepth:
                    for k in range(i + 1, treeDepth):
                        n[k] = ''
        farr.append([el[treeDepth], el[treeDepth - 1], el[treeDepth:]])
    # Με αυτό τον τρόπο λύνω ένα παράξενο πρόβλημα χτυπήματος
    exec 'fval = %s' % farr
    return fval, valAr2


def makeModel(treenam=None, db=None, par=None):
    sqlModel = "SELECT * FROM tree WHERE tname='%s'" % treenam
    tnam, mname, tdepth, txtv, numv, sql = dbf.getDbOneRow(sqlModel, dbf.zdb)
    tnam
    vals = head = []
    if sql:
        vals, head = dbf.getDbRows(sql, db)
        farr, valAr2 = dataForModel(vals, tdepth, txtv, numv)
    else:
        pass
    en = {'0': Node(u'root', None, valAr2)}  # {'0':Node(u'root',None,valAr2)}
    for el in farr:
        en[el[0]] = Node(el[0], en[el[1]], el[2])
    return treeModel(en['0'],
                     [u'Χρήση/Μήνας/Τρίμηνο/ημνια/Παρκό',
                      u'Έσοδα',
                      u'ΦΠΑ',
                      u'Έξοδα',
                      u'ΦΠΑ'],
                     pare=par)


class TreeData(QtGui.QTreeView):
    def __init__(self, treenam=None, db=None, parent=None):
        super(TreeData, self).__init__(parent)
        self.db = db
        self.treenam = treenam
        self.setModel(makeModel(self.treenam, self.db, self))
        self.setColumnWidth(0, 350)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(3, 80)

    def edit(self, index, trigger, event):
        if trigger == QtGui.QAbstractItemView.DoubleClicked:
            print u'DoubleClick Killed!'
            return False
        return QtGui.QTreeView.edit(self, index, trigger, event)


class TreeForm(QtGui.QDialog):
    def __init__(self, treenam=None, db=None, parent=None):
        super(TreeForm, self).__init__(parent)
        self.parent = parent
        layout = QtGui.QVBoxLayout()
        layout.addWidget(dbf.makeTitle(u'Βιβλίο Εσόδων-Εξόδων'))
        self.tr = TreeData(treenam, db, self)
        layout.addWidget(self.tr)

        self.bt = QtGui.QPushButton('test')
        layout.addWidget(self.bt)
        self.setLayout(layout)
        self.bt.clicked.connect(self.onClickbt)

    def onClickbt(self):
        import tst
        ff = tst.PtextForm(tst.strFpa(tst.fpaCheck(tst.tstArr)))
        if self.parent:
            self.parent.addDialogOnStack(ff)

    def canAdd(self):
        return False


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    tarr = []
    treeView = TreeData()
    treeView.show()
    sys.exit(app.exec_())
