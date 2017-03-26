# -*- coding: utf-8 -*-
'''
Created on Nov 25, 2014

@author: tedlaz.
'''
from PyQt4 import QtGui, QtCore, Qt
import fld__parameters as par
from form_find import FormFind
from utils import sqlite3_methods as tu


class ButtonText(QtGui.QLineEdit):
    """Button text class """
    def __init__(self, pin, parent=None):
        super(ButtonText, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        # Create visible controls
        self.button = QtGui.QToolButton(self)

        self.parent = parent
        self.status = False
        self.set(pin)

        self.textChanged.connect(self.edChanged)

        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.setFocusPolicy(Qt.Qt.NoFocus)

        self.button.clicked.connect(self.buttonClicked)

        f_width = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        button_size = self.button.sizeHint()
        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' %
                           (button_size.width() + f_width + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(),
                                button_size.width() + f_width*2 + 2),
                            max(self.minimumSizeHint().height(),
                                button_size.height() + f_width*2 + 2))
        self.setMinimumHeight(par.MIN_HEIGHT)

    def resizeEvent(self, event):
        button_size = self.button.sizeHint()
        f_width = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.button.move(
            self.rect().right() - f_width - button_size.width(),
            (self.rect().bottom() - button_size.height() + 1)/2)
        super(ButtonText, self).resizeEvent(event)

    def set(self, pin):
        self.id = pin.get('val', None)
        self.fld1v = pin.get('fld1', '')
        self.sql0 = pin.get('sql', None)
        self.sql1 = pin.get('sql1', None)
        self.db = pin.get('db', None)
        self.setText(self.fld1v)
        self.setStatus(self.id)

    def get(self):
        return '%s' % self.id

    def edChanged(self):
        self.setErr()

    def buttonClicked(self):
        self.button.setFocus()
        self.clicked()

    def setOk(self):
        self.button.setStyleSheet(
            'border: 0px; padding: 0px; background-color: rgba(0, 150, 0); '
            'color: rgb(255, 255, 255);')
        self.button.setText('..')
        self.status = True

    def setErr(self):
        self.button.setStyleSheet(
            'border: 0px; padding: 0px; background-color: rgba(220, 50, 0); '
            'color: rgb(255, 255, 255);')
        self.button.setText('o')
        self.status = False

    def setStatus(self, val):
        if val:
            self.setOk()
        else:
            self.setErr()

    def keyPressEvent(self, ev):
        if self.fld1v != self.text():
            self.setErr()
        if ev.key() == QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return:
            if self.fld1v != self.text():
                self.clicked()
            else:
                # move focus to next field
                pass
        return QtGui.QLineEdit.keyPressEvent(self, ev)

    def clicked(self):
        if self.hasFocus():
            sql = self.sql1 % tu.grup('%s' % self.text())
        else:
            sql = self.sql0

        found = tu.dbRows({'sql': sql, 'db': self.db})
        if found['rowNumber'] > 1:
            a = FormFind({'rows': found['rows'],
                          'labels': found['columnNames']}, self)
            if a.exec_() == QtGui.QDialog.Accepted:
                try:
                    self.id = a.array[0]
                    self.setText(a.array[1])
                    self.setStatus(self.id)
                    self.fld1v = a.array[1]
                except:
                    self.id = None
                    self.setText('')
                    self.setStatus(0)
                    self.code = ''
                    self.per = ''
        elif found['rowNumber'] == 1:
            print(found['rows'][0][2])
            self.checkChange = False
            self.id = found['rows'][0][0]
            self.setText(found['rows'][0][1])
            self.setStatus(self.id)
            self.fld1v = found['rows'][0][1]


if __name__ == '__main__':
    import sys
    import test_db as tdb
    tdb.create_tst_db()
    app = QtGui.QApplication([])
    dlg1 = ButtonText(tdb.button_text_value)
    dlg1.show()
    s = app.exec_()
    print(dlg1.get())
    tdb.delete_tst_db()
    sys.exit(s)
