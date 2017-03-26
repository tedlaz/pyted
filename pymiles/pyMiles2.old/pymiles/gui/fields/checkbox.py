# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import parameters as par


class Checkbox(QtGui.QCheckBox):

    """
    True or False field
    Gets / Sets two values : 0 for unchecked , 2 for checked
    """

    def __init__(self, parent, val=False):
        super(Checkbox, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        # assert(parent is not None)
        self.set(val)

        self.setMinimumHeight(par.MIN_HEIGHT)

    def set(self, txtVal):
        if txtVal:
            self.setChecked(txtVal)
        else:
            self.setChecked(False)

    def get(self):
        return self.checkState()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dialog1 = Checkbox(None, 1)
    dialog1.show()
    appobject = app.exec_()
    print(dialog1.get())
    sys.exit(appobject)
