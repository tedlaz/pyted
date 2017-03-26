# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from textline import Text_line


class Textline_numbers_only(Text_line):

    '''
    Text field with numeric chars only left aligned.
    '''

    def __init__(self, parent, val=''):
        super(Textline_numbers_only, self).__init__(parent, val)

        rval = QtCore.QRegExp('(\d*)([1-9])(\d*)')
        self.setValidator(QtGui.QRegExpValidator(rval))

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dlg = Textline_numbers_only('123456789')
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)

