# -*- coding: utf-8 -*-
'''
Created on 14 Ιαν 2013

@author: tedlaz
'''

# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys

from utils.tedutils import dec, isNum
from utils.dbutils import getDbRows 
   
class Node(object):
    def __init__(self, name, parent,vals):
        #def __init__(self, name, parent=None,vals=['','',dec(0),dec(0),dec(0),dec(0)]):
        self._name = name
        self._vals = vals
        self._children = []
        self._parent = parent
        if parent is not None:
            parent.addChild(self)
            self.updateParent()
            
    def updateParent(self):
        isnum = []
        tots  = []
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
                self._parent.setVal(tots[i],i)
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

 
class SceneGraphModel(QtCore.QAbstractItemModel):

    def __init__(self, root, headers, parent=None):
        super(SceneGraphModel, self).__init__(parent)
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
            elif index.column() >=2:
                return '%.2f' % node.val(index.column())
            else:
                return node.val(index.column())
        if role == QtCore.Qt.TextAlignmentRole:
            if index.column() >= 2:
                return QtCore.Qt.AlignRight

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                node = index.internalPointer()
                #node.setName(value)
                node.setVal(value,index.column())
                #node.setName('editingTed')
                return True
        return False
    
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            return self._headers[section]
            
    
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
    
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            childCount = parentNode.childCount()
            childNode = Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)
        self.endInsertRows()
        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            success = parentNode.removeChild(position)
        self.endRemoveRows()
        return success
        
sqla = '''
select  m12_xrisi.xrisi,'Μήνας ' || m12_period.id,m12_period.periodp || ' ' || m12_mist.mistp,m12_fpr.epon || ' ' || m12_fpr.onom as onomatep, m12_eid.eidp,
sum( case when mtyp_id=200 then val end) as apodoxes,
sum( case when mtyp_id=502 then val end) as ika,
sum( case when mtyp_id=900 then val end) as plir,
sum( case when mtyp_id=500 then val end) as ikaenos
from m12_misd
inner join m12_mis on m12_mis.id=m12_misd.mis_id
inner join m12_pro on  m12_pro.id=m12_misd.pro_id
inner join m12_fpr on m12_fpr.id=m12_pro.fpr_id  
inner join m12_eid on m12_eid.id=m12_pro.eid_id
inner join m12_xrisi on m12_xrisi.id=m12_mis.xrisi_id
inner join m12_period on m12_period.id=m12_mis.period_id
inner join m12_mist on m12_mist.id=m12_mis.mist_id
group by mis_id,pro_id
ORDER BY m12_xrisi.xrisi desc ,m12_period.id desc ,m12_mist.id
'''
sqlb = '''
SELECT m12_fpr.epon || ' ' || m12_fpr.onom,m12_xrisi.xrisi,'Μήνας ' || m12_period.id,m12_period.periodp || ' ' || m12_mist.mistp, m12_pro.prod,
sum( case when m12_misd.mtyp_id=200 then m12_misd.val end ) as totapod,
sum( case when m12_misd.mtyp_id=500 then m12_misd.val end ) as ikaEnos,
sum( case when m12_misd.mtyp_id=502 then m12_misd.val end ) as ika,
sum( case when m12_misd.mtyp_id=900 then m12_misd.val end ) as pliroteo
FROM m12_fpr
INNER JOIN m12_pro ON m12_pro.fpr_id=m12_fpr.id
INNER JOIN m12_misd ON m12_misd.pro_id=m12_pro.id
INNER JOIN m12_mis ON m12_mis.id=m12_misd.mis_id
INNER JOIN m12_xrisi ON m12_xrisi.id=m12_mis.xrisi_id
INNER JOIN m12_period ON m12_period.id=m12_mis.period_id
INNER JOIN m12_mist ON m12_mist.id=m12_mis.mist_id
GROUP BY  m12_fpr.epon, m12_mis.xrisi_id,m12_mis.period_id, m12_mis.mist_id
ORDER BY  m12_fpr.epon, m12_mis.xrisi_id,m12_mis.period_id, m12_mis.mist_id
'''
def makeModel(db=None):
    if not db:
        db = 'C:/ted/mis.sql3'
    
    arr = getDbRows(sqla,db)
    n0=n1=n2=''
    farr = [] 
    #arr = arr * 100 #Για δοκιμές με μεγάλες τιμές Array
    for el in arr:
        if n0 <> el[0]:
            farr.append([el[0],'0',['','',0,0,0,0]])
            n0 = el[0]
            n1 = ''
            n2 = ''
        if n1 <> el[1]:
            farr.append([el[1],el[0],['','',0,0,0,0]])
            n1 = el[1]
            n2 = ''
        if n2 <> el[2]:
            farr.append([el[2],el[1],['','',0,0,0,0]])
            n2 = el[2]
        farr.append([el[3],el[2],[el[3],el[4],el[5],el[6],el[7],el[8]]])
    e = {'0':Node(u'root',None,['','',dec(0),dec(0),dec(0),dec(0)])}
    for el in farr:
        e[el[0]] = Node(el[0],e[el[1]],el[2])
        
    return SceneGraphModel(e['0'],[u'Χρήση / Εργαζόμενος',u'Ειδικότητα',u'Αποδοχές',u'ΙΚΑ',u'Πληρωτέο',u'Ικα εργαζομένου'])

class TreeView1(QtGui.QTreeView):    
    def edit(self, index, trigger, event):
        if trigger == QtGui.QAbstractItemView.DoubleClicked:
            print 'DoubleClick Killed!',self.model().data(index,QtCore.Qt.DisplayRole)
            return False
        return QtGui.QTreeView.edit(self, index, trigger, event)
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    tarr = []
    model = makeModel()
    treeView = TreeView1()
    
    treeView.setModel(model)

    treeView.show()
    treeView.setColumnWidth(0,250)
    sys.exit(app.exec_())