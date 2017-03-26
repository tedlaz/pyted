 # -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import fld__parameters as par
import u_txt_num as dec


class Numeric(QtGui.QLineEdit):

    '''
    Text field with numeric chars only.
    '''

    insert_pressed = QtCore.pyqtSignal()

    def __init__(self, pin, parent=None):
        super(Numeric, self).__init__(parent)

        self.parent = pin.get('parent', None)
        self.isreq = pin.get('isRequired', False)
        self.set(pin.get('val', '0'))
        self.setMinimumHeight(par.MIN_HEIGHT)

        rval = QtCore.QRegExp('(\d*)([1-9,])(\d*)')
        self.setValidator(QtGui.QRegExpValidator(rval))
        self.setMinimumHeight(par.MIN_HEIGHT)
        self.setAlignment(QtCore.Qt.AlignRight)
        self.type = 0

    def keyPressEvent(self, ev):
        # Check if keypressed is '.'
        if ev.key() == 46:
            if ',' in self.text():
                pass
            else:
                self.setText(self.text() + ',')
        elif ev.key() == QtCore.Qt.Key_Insert:
            self.insert_pressed.emit()
        elif ev.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            self.set(self.get())
        QtGui.QLineEdit.keyPressEvent(self, ev)

    def focusOutEvent(self, ev):
        self.set(self.get())
        QtGui.QLineEdit.focusOutEvent(self, ev)

    def focusInEvent(self, ev):
        self.selectAll()

    def set(self, txt):
        if txt:
            self.setText(dec.strGrDec(txt))
        else:
            self.setText(dec.strGrDec(0))

    def get(self):
        greek_div = ','
        normal_div = '.'
        tmp = '%s' % self.text()
        tmp = tmp.replace(normal_div, '')
        tmp = tmp.replace(greek_div, normal_div)
        return dec.dec(tmp.strip())

    def set_type(self, type):
        self.type = type

    @QtCore.pyqtSlot(str, str, str)
    def updated_val(self, xr, pi, yp):
        if self.hasFocus():
            print(self.get())
            if self.get() == 0:
                dyp = dec.dec(yp)
                if dyp > 0:
                    if self.type == 2:
                        self.set(dyp)
                    else:
                        self.set(dyp * -1)
                else:
                    if self.type == 1:
                        self.set(dyp * -1)
                    else:
                        self.set(dyp)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dlg = Numeric({'val': '123.32'})
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)
