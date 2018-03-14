# -*- coding: utf-8 -*-
'''
Created on 14 Ιαν 2013

@author: tedlaz
'''
from collections import OrderedDict
from PyQt4 import QtCore, QtGui
import minkat as mk
import f2
import sys

import decimal
import dbforms as dbf
import locale

locale.setlocale(locale.LC_ALL, '')


def isNum(value): # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters : 
            1.value : the value to check against.
        output: True or False
        """
    try: float(value)
    except ValueError: return False
    else: return True


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


def numOrEmptytext(val):
    if dbf.isNum(val):
        return val
    else:
        return ''


def addArrs(ar1, ar2):
    '''
    having ar1: [a1,a2,...,an] and ar2: [b1,b2,...,bn]
    addArrs(ar1,ar2) returns [a1+b1,a2+b2,...,an+bn]
    '''
    len1 = len(ar1)
    len2 = len(ar2)
    if len1 <> len2:
        print 'error , arrays have not the same length'
        return []
    far = []
    for i in range(len1):
        'If Numeric adds else appends empty string'
        if dbf.isNum(ar1[i]) and dbf.isNum(ar2[i]):
            far.append(dbf.dec(ar1[i])+dbf.dec(ar2[i]))
        else:
            far.append('')
    return far


def createSubtotalsFromOrderedVals(vals, depth):
    '''
    Having an ordered from left to right vals array [[a1,a2,...,an],[b1,b2,..bn],...[N1,N2,...,Nn]]
    uses columns from 0 to Depth to create subtotals on Numeric Values
    '''
    tots = OrderedDict()
    ar = []
    for val in vals:      
        stra = ''
        preval = '0'
        for col in range(depth):
            if stra == '': par = '0'
            else: par = stra
            stra += '%s' % val[col]
            ar.append(stra)
            if stra in tots:
                tots[stra] = [par, addArrs(tots[stra][1], val[depth:]), '%s' % val[col], preval]
            else:
                tots[stra] = [par, [numOrEmptytext(tim) for tim in val[depth:]], '%s'% val[col], preval]
            preval = '%s'% val[col]    
    farr = []
    for key in tots:
        farr.append([tots[key][2], tots[key][3], tots[key][1]])
    return farr

    
class Node():
    def __init__(self, name, parentn, vals):
        self._name = name
        self._vals = vals
        self._children = []
        self._parent = parentn
        if parentn is not None:
            parentn.addChild(self)
     
    def typeInfo(self):
        return "NODE"
        
    def addChild(self, child):
        self._children.append(child)
               
    def name(self):
        return self._name
        
    def setName(self, name):
        self._name = name
        
    def val(self,column):
        return self._vals[column]
        
    def valF(self,column):  
        if isNum(self._vals[column]):
            return locale.format("%0.2f", self._vals[column], grouping=True)
        else:
            return self._vals[column]
        
    def setVal(self,val,column):
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
        self._headers  = headers
        
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
                return node.valF(index.column()-1)
        if role == QtCore.Qt.TextAlignmentRole:
            if index.column() >= 1:
                return QtCore.Qt.AlignRight
        if role == 100:
            return node.name()

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
    
    
def makeModel(treenam=None, db=None, par=None):
    sqlModel = "SELECT * FROM tree WHERE tname='%s'" % treenam
    tnam, mname, tdepth, txtv, numv, sql = dbf.getDbOneRow(sqlModel, dbf.zdb)
    vals = head = []
    if sql:
        vals, head = dbf.getDbRows(sql,db)
        lbls = dbf.getLabels(head)[:-1]
        farr = createSubtotalsFromOrderedVals(vals,tdepth)
    else:
        pass

    en = {'0': Node(u'root', None, [0,])}  # {'0':Node(u'root',None,valAr2)}
    for el in farr:
        en[el[0]] = Node(el[0], en[el[1]], el[2])
    return treeModel(en['0'], [u'Ανάλυση'] + lbls[tdepth:], pare=par)

    
class TreeData(QtGui.QTreeView):
    def __init__(self, treenam=None, db=None, parent=None):
        super(TreeData, self).__init__(parent)
        self.db = db
        self.treenam = treenam
        self.parent = parent
        sql = "SELECT mname FROM tree WHERE tname=?" 
        self.mname= dbf.getDbSingleVal(sql, [treenam,], dbf.zdb)
        self.setModel(makeModel(self.treenam, self.db, self))
        self.setColumnWidth(0, 350)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(3, 80)
        self.setColumnWidth(4, 70)
        
    def contextMenuEvent(self, event):
        val = '%s' % self.currentIndex().data(100).toString()
        sqlmonth = "SELECT id, mip FROM mi"
        sqlQuart = "SELECT id, trp FROM tr"
        months ,b= dbf.getDbRows(sqlmonth, self.db)
        trims ,b= dbf.getDbRows(sqlQuart, self.db)
        mines = []
        fmines = {}
        trimina  = []
        ftrimina = {}
        menu = QtGui.QMenu(self)
        for el in months:
            mines.append(el[1])
            fmines[el[1]] = el[0]
            
        for el in trims:
            trimina.append(el[1])
            ftrimina[el[1]] = el[0]
        if val in mines:
            Action = menu.addAction(u"Κατάσταση εσόδων - εξόδων")
            Action.triggered.connect(self.openEsExMina)
            self.contextVal1 = '%s' % self.currentIndex().parent().parent().data(100).toString()
            self.contextVal2 = '%s' % fmines[val]
        elif val in trimina:
            Action = menu.addAction(u"ΦΠΑ Τριμήνου")
            Action.triggered.connect(self.openFpaTriminou)
            self.contextVal1 = '%s' % self.currentIndex().parent().data(100).toString()
            self.contextVal2 = '%s' % ftrimina[val]
        menu.exec_(event.globalPos())
        
    def openEsExMina(self):
        dlg = mk.PtextForm(self, self.contextVal1, self.contextVal2)
        self.parent.parent.addDialogOnStack(dlg)
        
    def openFpaTriminou(self):
        dlg = f2.PtextForm(self, self.contextVal1, self.contextVal2)
        self.parent.parent.addDialogOnStack(dlg)
        
    def edit(self, index, trigger, event):
        if trigger == QtGui.QAbstractItemView.DoubleClicked:
            dbf.dprint(u'DoubleClick Killed!')
            return False
        return QtGui.QTreeView.edit(self, index, trigger, event)
    

class TreeForm(QtGui.QDialog):
    def __init__(self, treenam=None, db=None, parent=None):
        super(TreeForm, self).__init__(parent)
        self.parent = parent
        layout = QtGui.QVBoxLayout()
        self.tr = TreeData(treenam,db,self)
        layout.addWidget(dbf.makeTitle(self.tr.mname))        
        layout.addWidget(self.tr)
        
        #self.bt = QtGui.QPushButton('test')
        #layout.addWidget(self.bt)
        self.setLayout(layout)
        #self.bt.clicked.connect(self.onClickbt)
    #def onClickbt(self):
    #    import tst
    #    ff=tst.PtextForm(tst.strFpa(tst.fpaCheck(tst.tstArr))) 
    #    if self.parent:
    #        self.parent.addDialogOnStack(ff)   
    def canAdd(self):
        return False  


if __name__ == '__main__':
    pass
