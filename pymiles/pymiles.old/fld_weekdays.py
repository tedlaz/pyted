# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore, Qt
import fld__parameters as par
MSG_SELECT_DAYS = u'Επιλέξτε τις Εργάσιμες ημέρες\nΜε δεξί κλικ μηδενίστε'
BLANK, GREEN = range(2)


class Weekdays(QtGui.QWidget):

    '''
    Weekdays selection ( [1,1,1,1,1,0,0] 7 values 0 or 1, one per weekday)
    '''

    def __init__(self, pin, parent=None):
        '''pin: {'name': xx, 'vals': [1,1,1,1,1,1,1], 'dayNames': []}'''
        super(Weekdays, self).__init__(parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)

        self.parent = parent
        self.setSizePolicy(
            QtGui.QSizePolicy(
                QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))

        self.set(pin.get('val', [1, 1, 1, 1, 1, 0, 0]))
        self.selected = [0, 0]
        self.dayNames = pin.get('dayNames',
                                [u'ΔΕ',
                                 u'ΤΡ',
                                 u'ΤΕ',
                                 u'ΠΕ',
                                 u'ΠΑ',
                                 u'ΣΑ',
                                 u'ΚΥ'])
        self.setMinimumSize(QtCore.QSize(170, 20))
        self.setMaximumSize(QtCore.QSize(170, 20))
        self.setToolTip(MSG_SELECT_DAYS)
        self.setMinimumHeight(par.MIN_HEIGHT)

    def sizeHint(self):
        return QtCore.QSize(170, 20)

    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.LeftButton:
            xOffset = self.width() / 7
            # yOffset = xOffset #self.height()
            if event.x() < xOffset:
                x = 0
            elif event.x() < 2 * xOffset:
                x = 1
            elif event.x() < 3 * xOffset:
                x = 2
            elif event.x() < 4 * xOffset:
                x = 3
            elif event.x() < 5 * xOffset:
                x = 4
            elif event.x() < 6 * xOffset:
                x = 5
            else:
                x = 6

            cell = self.grid[x]
            if cell == BLANK:
                cell = GREEN
            else:
                cell = BLANK
            self.grid[x] = cell
            self.selected = [x, 0]
            self.update()

        elif event.button() == Qt.Qt.RightButton:
            self.reset()

    def paintEvent(self, event=None):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        xOffset = self.width() / 7
        yOffset = self.height()
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        for x in range(7):
            cell = self.grid[x]
            rect = QtCore.QRectF(x * xOffset, 0, xOffset,
                                 yOffset).adjusted(0.1, 0.1, -0.1, -0.1)

            color = None
            painter.drawRect(rect.adjusted(2, 2, -2, -2))
            if cell == GREEN:
                color = Qt.Qt.green
            if color is not None:
                painter.save()
                painter.setPen(Qt.Qt.black)
                painter.setBrush(color)
                painter.drawRect(rect.adjusted(2, 2, -2, -2))
                color = Qt.Qt.black
                painter.restore()

            painter.setPen(Qt.Qt.black)
            painter.drawText(rect.adjusted(4, 3, -3, -3), self.dayNames[x])
            painter.drawRect(rect)

    def get(self, strVal=True):
        if strVal:
            st = '['
            for i in range(7):
                if i == 6:
                    st += '%s]' % self.grid[i]
                else:
                    st += '%s,' % self.grid[i]
            return st
        else:
            return self.grid

    def set(self, darr=[0, 0, 0, 0, 0, 0, 0]):
        # Set values to days vector. But first checks for
        # proper array length and type
        darr = '%s' % darr
        tmparr = eval(darr)
        if len(tmparr) == 7:
            self.grid = tmparr
        else:
            self.grid = [0, 0, 0, 0, 0, 0, 0]
        self.update()

    def reset(self):
        'Set everything to Null'
        self.set([0, 0, 0, 0, 0, 0, 0])

    def set5days(self):
        'Set Standard five days week'
        self.set([1, 1, 1, 1, 1, 0, 0])

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dlg = Weekdays({'val': [1, 1, 1, 1, 1, 0, 0]})
    dlg.show()
    s = app.exec_()
    print(dlg.get())
    sys.exit(s)
