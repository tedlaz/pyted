# -*- coding: utf-8 -*-
'''
Created on Oct 13, 2014

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore
import fld__parameters as par


class Integer(QtGui.QSpinBox):
    '''
    Integer values (eg 123)
    '''
    def __init__(self, pin, parent=None):
        super(Integer, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.parent = parent

        width = (4)*10 + 5
        self.setMinimumWidth(width)
        # self.setMaximumWidth(width)
        # self.width = 100

        self.setMinimum(0)
        self.setMaximum(999999999)
        self.setAlignment(QtCore.Qt.AlignRight |
                          QtCore.Qt.AlignTrailing |
                          QtCore.Qt.AlignVCenter)
        self.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

        self.set(pin.get('val', 0))
        self.setMinimumHeight(par.MIN_HEIGHT)

    def get(self):
        return '%s' % self.value()

    def set(self, val):
        if val:
            self.setValue(int(val))
        else:
            self.setValue(0)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dlg = Integer({'intVal': 123})
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)
