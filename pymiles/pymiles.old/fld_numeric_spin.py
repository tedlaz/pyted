# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import fld__parameters as par


class Numeric_spin(QtGui.QDoubleSpinBox):

    '''
    Numeric (decimal 2 ) values (eg 999,99)
    '''

    def __init__(self, pin, parent=None):

        super(Numeric_spin, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.parent = parent

        self.setMinimum(-99999999999)
        self.setMaximum(99999999999)
        self.setAlignment(QtCore.Qt.AlignRight |
                          QtCore.Qt.AlignTrailing |
                          QtCore.Qt.AlignVCenter)
        self.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

        self.set(pin.get('val', 0))
        self.setMinimumHeight(par.MIN_HEIGHT)

    def get(self):
        val = '%s' % self.value()
        if val[-2:] == '.0':
            val = val[:-2]
        return val

    def set(self, val):
        if val:
            self.setValue(val)
        else:
            self.setValue(0)

    def mouseDoubleClickEvent(self, ev):
        print('test')

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dlg = Numeric_spin({'val': 123.32})
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)
