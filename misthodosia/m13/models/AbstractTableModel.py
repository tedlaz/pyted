# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import sys

class abTableModel(QtCore.QAbstractTableModel):

    def __init__(self, mdata = [[]], headers = [],parent=None):
        QtCore.QAbstractTableModel.__init__(self,parent)
        self.__mdata  = []
        for el in mdata:
            self.__mdata.append(list(el))
        self.__headers = headers
        
    def rowCount(self,parent): 
        return len(self.__mdata) 

    def columnCount(self,parent): 
        return len(self.__mdata[0])
        
    def headerData(self,section,orientation,role):
        
        if role == QtCore.Qt.TextAlignmentRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QVariant(int(QtCore.Qt.AlignCenter))
            return QtCore.QVariant(int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter))
    
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__headers[section]
            else:
                return QtCore.QString(u'%1').arg(section+1)
        
    def data(self,index,role):
    
        if role == QtCore.Qt.EditRole:
            return self.__mdata[index.row()][index.column()]
    
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            column = index.column()
            value = self.__mdata[row][column]
            return value
        '''    
        if role == QtCore.Qt.DecorationRole:
           
           value = self.__mdata[index.row()][index.column()]
           pixmap = QtGui.QPixmap(26,26)
           pixmap.fill(value)
           icon = QtGui.QIcon(pixmap)
           return icon
        '''
        if role == QtCore.Qt.ToolTipRole:
            return u'Δεδομένα : %s' % self.__mdata[index.row()][index.column()]
            
    def setData(self,index,value,role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            self.__mdata[index.row()][index.column()] = value
            self.dataChanged.emit(index,index)
            return True
        return False
        
    def flags(self,index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    tableView = QtGui.QTableView()
    tableView.show()
    
    cch = [u'Ονοματεπώνυμο',u'Ημ.Γέννησης',u'Τηλέφωνο']
    
    tdata = [[u'Λάζαρος Θεόδωρος','1963-02-10','2108660643'],[u'Μαυράκης Νικόλαος','1961-01-01','2108654713']]
    
    model = abTableModel(tdata,cch)
    
    tableView.setModel(model)
    
    sys.exit(app.exec_())