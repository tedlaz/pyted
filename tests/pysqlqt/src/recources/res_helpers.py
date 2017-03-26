# -*- coding: utf-8 -*-
# Ted Lazaros
from PyQt4 import QtCore


def readFromRes(resname):
    f = QtCore.QFile(resname)
    if f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
        stream = QtCore.QTextStream(f)
        stream.setCodec('utf-8')
        vstr = u''
        while not stream.atEnd():
            vstr += u'%s\n' % stream.readLine().__str__()
    f.close()
    return vstr
