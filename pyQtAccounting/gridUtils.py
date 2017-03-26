#!/usr/bin/env python
#coding=utf-8
'''
Created on 10 Μαϊ 2011

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore
    
def setItems(val,type):
    if type == '0':
        return numItem(val)
    elif type == '9':
        return strItem(val)
    else:
        return None
            
def numItem(no):
    item = QtGui.QTableWidgetItem(QtCore.QString("%L1").arg(float(no),0,"f",2))
    item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
    return item

def strItem(str):
    item = QtGui.QTableWidgetItem(str)
    return item

if __name__ == "__main__":
    print 'test'