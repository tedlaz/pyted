# -*- coding: utf-8 -*-
'''
Created on 14 Ιαν 2013

@author: tedlaz
'''

from PyQt4 import QtCore, QtGui
#import minkat as mk
#import f2
import sys

import dbutils as db
import num_txt_etc as nm
import locale

locale.setlocale(locale.LC_ALL, '')
    
class Node():
    def __init__(self, name, parentn,vals):
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
        if nm.isNum(self._vals[column]):
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
    
def makeModel(treenam=None,db=None,par=None):
    sqlModel = "SELECT * FROM tree WHERE tname='%s'" % treenam
    tnam,mname,tdepth,txtv,numv,sql = db.getDbOneRow(sqlModel,db.zdb)
    vals = head = []
    if sql:
        vals, head = db.getDbRows(sql,db)
        lbls = db.getLabels(head)[:-1]
        farr = nm.createSubtotalsFromOrderedVals(vals,tdepth)
    else:
        pass

    en = {'0':Node(u'root',None,[0,])}#{'0':Node(u'root',None,valAr2)}
    for el in farr:
        en[el[0]] = Node(el[0],en[el[1]],el[2])
    return treeModel(en['0'],[u'Ανάλυση']+lbls[tdepth:],pare=par)
    
class TreeData(QtGui.QTreeView):
    def __init__(self,treenam=None,db=None,parent=None):
        super(TreeData, self).__init__(parent)
        self.db = db
        self.treenam = treenam
        self.parent = parent
        sql = "SELECT mname FROM tree WHERE tname=?" 
        self.mname= db.getDbSingleVal(sql, [treenam,], db.zdb)
        self.setModel(makeModel(self.treenam,self.db,self))
        self.setColumnWidth(0,350)
        self.setColumnWidth(1,80)
        self.setColumnWidth(2,80)
        self.setColumnWidth(3,80)
        self.setColumnWidth(4,70)
        
    def contextMenuEvent(self, event):
        val = '%s' % self.currentIndex().data(100).toString()
        sqlmonth = "SELECT id, mip FROM mi"
        sqlQuart = "SELECT id, trp FROM tr"
        months ,b = db.getDbRows(sqlmonth, self.db)
        trims ,b = db.getDbRows(sqlQuart, self.db)
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
        #dlg = mk.PtextForm(self,self.contextVal1,self.contextVal2)
        #self.parent.parent.addDialogOnStack(dlg)
        pass
    
    def openFpaTriminou(self):
        #dlg = f2.PtextForm(self,self.contextVal1,self.contextVal2)
        #self.parent.parent.addDialogOnStack(dlg)
        pass
    
    def edit(self, index, trigger, event):
        if trigger == QtGui.QAbstractItemView.DoubleClicked:
            db.dprint(u'DoubleClick Killed!')
            return False
        return QtGui.QTreeView.edit(self, index, trigger, event)
    
class TreeForm(QtGui.QDialog):
    def __init__(self,treenam=None,db=None,parent=None):
        super(TreeForm, self).__init__(parent)
        self.parent = parent
        layout = QtGui.QVBoxLayout()
        self.tr = TreeData(treenam,db,self)
        layout.addWidget(db.makeTitle(self.tr.mname))        
        layout.addWidget(self.tr)

        self.setLayout(layout)

    def canAdd(self):
        return False  
if __name__ == '__main__':
    pass