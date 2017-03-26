# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import fld__parameters as par


class TextLine(QtGui.QLineEdit):

    """Text Line Class"""

    def __init__(self, pin, parent=None):
        super(TextLine, self).__init__(parent)

        self.parent = pin.get('parent', None)
        self.isreq = pin.get('isRequired', False)
        self.set(pin.get('val', ''))
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


class TextLineMasked(TextLine):

    '''
    Text field with numeric chars only.
    '''

    def __init__(self, pin, parent=None):
        super(TextLineMasked, self).__init__(pin, parent)

        rval = QtCore.QRegExp('(\d*)([1-9])(\d*)')
        self.setValidator(QtGui.QRegExpValidator(rval))
        self.setMinimumHeight(par.MIN_HEIGHT)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dlg1 = TextLine({'val': 'Text Line'})
    dlg1.show()
    dlg = TextLineMasked({'val': '1234'})
    dlg.show()
    s = app.exec_()
    print(dlg1.get())
    print(dlg.get())
    sys.exit(s)
