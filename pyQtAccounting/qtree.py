# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys
#import icons_rc
import sqlite3
import decimal
import qtreedata as d
def isNum(value): # Einai to value arithmos, i den einai ?
    """ use: Returns False if value is not a number , True otherwise
        input parameters : 
            1.value : the value to check against.
        output: True or False
    """
    if not value:
        return False
    try: float(value)
    except ValueError: return False
    else: return True

def dec(poso , dekadika=2 ):
    """ 
    use : Given a number, it returns a decimal with a specific number of decimal digits
    input Parameters:
          1.poso     : The number for conversion in any format (e.g. string or int ..)
          2.dekadika : The number of decimals (default 2)
    output: A decimal number     
    """
    PLACES = decimal.Decimal(10) ** (-1 * dekadika)
    if isNum(poso):
        tmp = decimal.Decimal(str(poso))
    else:
        tmp = decimal.Decimal('0')
    return tmp.quantize(PLACES)

def makeDecimalFromString(strNumber):
    g = "".join(strNumber.split())
    return dec(g.replace(",","."))
def getData(sql,DB):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(sql)
    v1 = cur.fetchall()
    cur.close()
    con.close()
    return v1
    
class Node(object):
    def __init__(self, name, parent=None,vals=['','',dec(0),dec(0),dec(0)]):
        self._name = name
        self._vals = vals
        self._children = []
        self._parent = parent
        if parent is not None:
            parent.addChild(self)
            self.updateParent()
    def updateParent(self):
            a2= a3= a4 = 0
            for chi in self._parent._children:
                a2 += chi.val(2)
                a3 += chi.val(3)
                a4 += chi.val(4)
            self._parent.setVal(a2,2)
            self._parent.setVal(a3,3)
            self._parent.setVal(a4,4)
            #print self._name,'-->',self._parent._name,a2,a3
            if self._parent._parent is not None:
                self._parent.updateParent()
    def typeInfo(self):
        return "NODE"
    def addChild(self, child):
        self._children.append(child)
    def insertChild(self, position, child):
        if position < 0 or position > len(self._children):
            return False
        self._children.insert(position, child)
        child._parent = self
        return True
    def removeChild(self, position):
        if position < 0 or position > len(self._children):
            return False
        child = self._children.pop(position)
        child._parent = None
        return True
    def name(self):
        return self._name
    def setName(self, name):
        self._name = name
    def val(self,column):
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
    def log(self, tabLevel=-1):
        output     = u""
        tabLevel += 1
        for i in range(tabLevel):
            output += "\t"
        output += u"|--- %s\n" % self._name
        for child in self._children:
            output += child.log(tabLevel)
        tabLevel -= 1
        output += "\n"
        return output
    def __repr__(self):
        return self.log()

class TransformNode(Node):
    def __init__(self, name, parent=None):
        super(TransformNode, self).__init__(name, parent)
    def typeInfo(self):
        return "TRANSFORM"

class CameraNode(Node):
    def __init__(self, name, parent=None):
        super(CameraNode, self).__init__(name, parent)
    def typeInfo(self):
        return "CAMERA"

class LightNode(Node):
    def __init__(self, name, parent=None):
        super(LightNode, self).__init__(name, parent)
    def typeInfo(self):
        return "LIGHT"
    
class SceneGraphModel(QtCore.QAbstractItemModel):
    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode = root
    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
        return parentNode.childCount()
    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent):
        return 5
    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.name()
            elif index.column() >=2:
                return '%.2f' % node.val(index.column())
            else:
                return node.val(index.column())
        if role == QtCore.Qt.TextAlignmentRole:
            if index.column() >= 2:
                return QtCore.Qt.AlignRight

    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                node = index.internalPointer()
                #node.setName(value)
                node.setVal(value,index.column())
                #node.setName('editingTed')
                return True
        return False
    
    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return u"Λογαριασμός"
            elif section == 1:
                return u"Περιγραφή"
            elif section == 2:
                return u"Χρέωση"
            elif section == 3:
                return u"Πίστωση"
            elif section == 4:
                return u"Υπόλοιπο"
            else:
                return u"Άγνωστο"
    
    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    """INPUTS: QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return the parent of the node with the given QModelIndex"""
    def parent(self, index):
        node = self.getNode(index)
        parentNode = node.parent()
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)
        
    """INPUTS: int, int, QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return a QModelIndex that corresponds to the given row, column and parent node"""
    def index(self, row, column, parent):
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()
    """CUSTOM"""
    """INPUTS: QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self._rootNode
    
    """INPUTS: int, int, QModelIndex"""
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            childCount = parentNode.childCount()
            childNode = Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)
        self.endInsertRows()
        return success
    
    def insertLights(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            childCount = parentNode.childCount()
            childNode = LightNode("light" + str(childCount))
            success = parentNode.insertChild(position, childNode)
        self.endInsertRows()
        return success

    """INPUTS: int, int, QModelIndex"""
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            success = parentNode.removeChild(position)
        self.endRemoveRows()
        return success
        
def parent(lmos,sep='.'):
    ''' Εδώ υπολογίζεται ο πατέρας του λογαριασμού lmos με διαχωριστικό βαθμίδων το sep
    '''
    lmosSize = len(lmos)
    lmosArr = lmos.split(sep)
    lmosDegree = len(lmosArr)
    par = ''
    if lmosDegree == 1:
        if lmosSize == 1:
            return '0'
        else:
            return lmos[0]
    for i in range(lmosDegree-1):
        if i == lmosDegree-2:
            par += lmosArr[i]
        else:
            par += lmosArr[i] + sep
    return par
def makeNode(lmos,e,sep='.'):
    ''' Δημιουργία ενός Node και μόνον.
    '''
    par = parent(lmos[0],sep)
    e[lmos[0]] = Node(lmos[0],e[par],lmos)
def makeTreeModel(isozygio,sep='.'):
    ''' To isozygio είναι array με τους λογαριασμούς 
    '''
    e = {'0':Node(u'root')}
    for lmos in isozygio:
        par = parent(lmos[0],sep)
        e[lmos[0]] = Node(lmos[0],e[par],lmos)
    return SceneGraphModel(e['0'])

class fTree(QtGui.QDialog):
    def __init__(self, args=None,parent=None):
        super(fTree, self).__init__(parent)
        self.parent = parent
        if self.parent:
            self.db = parent.db
        else:
            self.db =None
        
        sql = 'SELECT code,per, sum(xr), sum(pi) ,sum(xr)-sum(pi) as ypol FROM logistiki_tran_d inner join logistiki_lmo on logistiki_tran_d.lmos_id=logistiki_lmo.id group by lmos_id order by code'
        arr = getData(sql,self.db)
        trarr = []
        for el in d.arr:
            trarr.append(el)
        for el in arr:
            trarr.append([el[0],el[1],el[2],el[3],el[4]])
        model = makeTreeModel(trarr)
        treeView = QtGui.QTreeView()
        #treeView.show()
        treeView.setModel(model)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(treeView)
        treeView.setColumnWidth(0,160)
        treeView.setColumnWidth(1,400)
        treeView.setColumnWidth(2,80)
        treeView.setColumnWidth(3,80)
        treeView.setColumnWidth(4,80)
        self.setLayout(layout)
        self.setWindowTitle(u"Ισοζύγιο tree")
        self.setMinimumSize(900, 600)
if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    #app.setStyle("plastique")

    
    sql = 'SELECT code,per, sum(xr), sum(pi) ,sum(xr)-sum(pi) as ypol FROM logistiki_tran_d inner join logistiki_lmo on logistiki_tran_d.lmos_id=logistiki_lmo.id group by lmos_id order by code'
    arr = getData(sql,'db.sql3')
    for el in arr:
        d.arr.append([el[0],el[1],el[2],el[3],el[4]])
    model = makeTreeModel(d.arr)
    
    treeView = QtGui.QTreeView()
    treeView.show()
    
    treeView.setModel(model)

    sys.exit(app.exec_())