# -*- coding: utf-8 -*-
'''
Created on Nov 25, 2014

@author: tedlaz
'''
from PyQt4 import QtGui, QtCore, Qt
import fld__parameters as par
from form_find import FormFind
from utils import sqlite3_methods as tu


class ButtonText2(QtGui.QWidget):
    def __init__(self, pin, parent=None):
        super(ButtonText2, self).__init__(parent)

        # Create visible controls
        self.button = QtGui.QToolButton(self)
        self.button.setMaximumSize(20, 20)
        self.button.setMinimumSize(20, 20)


        self.fld1 = QtGui.QLineEdit(self)
        self.fld1.setMaximumWidth(100)
        self.fld1.setMinimumWidth(80)

        self.fld2 = QtGui.QLineEdit(self)
        self.fld2.setMinimumWidth(100)
        self.setMinimumWidth(200)

        self.set(pin)

        layout = QtGui.QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setMargin(0)

        layout.addWidget(self.fld1)
        layout.addWidget(self.fld2)
        layout.addWidget(self.button)

        self.setStatus(self.id)
        self.fld1.textChanged.connect(self.edChanged)
        self.fld2.textChanged.connect(self.edChanged)

        self.button.clicked.connect(self.buttonClicked)
        self.checkChange = True
        self.setMinHeight(par.MIN_HEIGHT)

    def setMinHeight(self, val):
        self.fld1.setMinimumHeight(val)
        self.fld2.setMinimumHeight(val)
        self.button.setMinimumHeight(val)
        self.setMaximumHeight(val)

    def set(self, pin):
        self.id = pin.get('val', None)
        self.fld1v = pin.get('fld1', '')
        self.fld2v = pin.get('fld2', '')
        self.sql0 = pin.get('sql', None)
        self.sql1 = pin.get('sql1', None)
        self.sql2 = pin.get('sql2', None)
        self.db = pin.get('db', None)
        self.fld1.setText(self.fld1v)
        self.fld2.setText(self.fld2v)

    def get(self):
        return '%s' % self.id

    def edChanged(self):
        self.setErr()
        if self.fld1.hasFocus() and self.checkChange:
            self.fld2.setText('')
        elif self.fld2.hasFocus() and self.checkChange:
            self.fld1.setText('')

    def buttonClicked(self):
        self.button.setFocus()
        self.clicked()

    def setOk(self):
        self.button.setStyleSheet(
            'border: 0px; padding: 0px; background-color: rgba(0, 200, 0); '
            'color: rgb(255, 255, 255);')
        self.button.setText('..')
        self.status = True

    def setErr(self):
        self.button.setStyleSheet(
            'border: 0px; padding: 0px; background-color: rgba(200, 0, 0); '
            'color: rgb(255, 255, 255);')
        self.button.setText('o')
        self.status = False

    def setStatus(self, val):
        if val:
            self.setOk()
        else:
            self.setErr()

    def keyPressEvent(self, ev):
        if self.fld1.hasFocus() or self.fld2.hasFocus():
            if (self.fld1v != self.fld1.text()) or (self.fld2v != self.fld2.text()):
                self.setErr()
        if (ev.key() == QtCore.Qt.Key_Enter or ev.key() == QtCore.Qt.Key_Return):
            if self.fld1.hasFocus() or self.fld2.hasFocus():
                if (self.fld1v != self.fld1.text()) or (self.fld2v != self.fld2.text()):
                    self.clicked()
                else:
                    # move focus to next field
                    pass
        return QtGui.QWidget.keyPressEvent(self, ev)

    def clicked(self):
        if self.fld1.hasFocus():
            sql = self.sql1 % tu.grup('%s' % self.fld1.text())
        elif self.fld2.hasFocus():
            sql = self.sql2 % tu.grup('%s' % self.fld2.text())
        else:
            sql = self.sql0

        found = tu.dbRows({'sql': sql, 'db': self.db})

        if found['rowNumber'] > 1:
            a = FormFind({'rows': found['rows'],
                          'labels': found['columnNames']}, self)
            if a.exec_() == QtGui.QDialog.Accepted:
                try:
                    self.id = a.array[0]
                    self.fld1.setText(a.array[1])
                    self.fld2.setText(a.array[2])
                    self.setStatus(self.id)
                    self.fld1v = a.array[1]
                    self.fld2v = a.array[2]
                except:
                    self.id = None
                    self.fld1.setText('')
                    self.fld2.setText('')
                    self.setStatus(0)
                    self.code = ''
                    self.per = ''
        elif found['rowNumber'] == 1:
            print(found['rows'][0][2])
            self.checkChange = False
            self.id = found['rows'][0][0]
            self.fld1.setText(found['rows'][0][1])
            self.fld2.setText(found['rows'][0][2])
            self.setStatus(self.id)
            self.fld1v = found['rows'][0][1]
            self.fld2v = found['rows'][0][2]
            self.checkChange = True

if __name__ == '__main__':
    import sys
    import test_db as tdb
    tdb.create_tst_db()
    app = QtGui.QApplication([])
    dlg1 = ButtonText2(tdb.button_text_value)
    dlg1.show()
    s = app.exec_()
    print(dlg1.get())
    tdb.delete_tst_db()
    sys.exit(s)
