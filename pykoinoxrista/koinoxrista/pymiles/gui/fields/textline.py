# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import parameters as par


class Text_line(QtGui.QLineEdit):

    """Text Line Class"""

    def __init__(self, parent, val=''):
        super(Text_line, self).__init__(parent)

        self.set(val)

        self.setMinimumHeight(par.MIN_HEIGHT)

    def set(self, txt):
        if txt:
            ttxt = '%s' % txt
            self.setText(ttxt.strip())
        else:
            self.setText('')
        self.setCursorPosition(0)

    def get(self):
        tmp = '%s' % self.text()
        return tmp.strip()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])

    dlg = Text_line(None, 'sdfkj 123')
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)
