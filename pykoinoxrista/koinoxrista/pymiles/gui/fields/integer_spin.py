# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
import parameters as par


class Integer_spin(QtGui.QSpinBox):

    '''
    Integer values (eg 123)
    '''

    def __init__(self, parent, val=0):
        super(Integer_spin, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.set(val)

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
    dlg = Integer_spin(None)
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)
