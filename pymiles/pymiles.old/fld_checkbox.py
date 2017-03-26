# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import fld__parameters as par


class CheckBox(QtGui.QCheckBox):
    """
    True or False field
    Gets / Sets two values : 0 for unchecked , 2 for checked
    """
    def __init__(self, pin, parent=None):
        super(CheckBox, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.parent = parent

        self.set(pin.get('val', False))
        self.isreq = pin.get('isRequired', False)
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
    dialog1 = CheckBox({'val': 1})
    dialog1.show()
    appobject = app.exec_()
    print(dialog1.get())
    sys.exit(appobject)
