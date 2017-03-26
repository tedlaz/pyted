# -*- coding: utf-8 -*-
'''
Created on Nov 25, 2014

@author: tedlaz.
'''
from PyQt4 import QtGui, QtCore, Qt
import parameters as par
from pymiles.sqlite.db_select import select
from pymiles.gui.forms.find import Ffind


class Text_button(QtGui.QLineEdit):

    """Button text class """

    def __init__(self, parent, name, val=None):
        super(Text_button, self).__init__(parent)
        assert(parent is not None)
        assert(name.endswith('_id'))
        assert(len(name) > 3)

        self.button = QtGui.QToolButton(self)

        self.status = False

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

        self.name = name
        self.ptable = name[:-3]
        self.rpr = self.parent().meta.rpr(self.ptable)
        self.sql_id = "%s WHERE %s.id=" % (self.rpr, self.ptable)
        self.sql_id += '%s'
        self.db = self.parent().db
        self.meta = self.parent().meta
        self.set(val)

    def resizeEvent(self, event):
        button_size = self.button.sizeHint()
        f_width = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.button.move(
            self.rect().right() - f_width - button_size.width(),
            (self.rect().bottom() - button_size.height() + 1)/2)
        super(Text_button, self).resizeEvent(event)

    def set(self, val):
        if not val:
            self.setStatus(self.setErr())
            self.fld1v = None
            self.id = '0'
            return
        self.id = val
        result = select(self.db, self.sql_id % val)

        self.fld1v = result['rows'][0]['rpr']
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
        hf = 0
        if self.hasFocus():
            pytxt = u'%s' % self.text()  # Convert it to python text
            sqlw = self.rpr + (" WHERE grup(rpr) LIKE grup('%%%s%%')" % pytxt)
            data = select(self.db, sqlw, False)
            tmplbls = self.meta.labels_from_fields(['id', self.name])
        else:
            sqlw = 'SELECT * FROM %s' % self.ptable
            data = select(self.db, sqlw, False)
            flds = self.meta._tbl_flds[self.ptable]
            tmplbls = self.meta.labels_from_fields(flds)
            hf = 1

        data['labels'] = tmplbls
        data['table'] = self.ptable
        data['meta'] = self.meta
        data['db'] = self.db

        if data['rownum'] > 1 or hf == 1:
            data['tablelbl'] = self.meta._tlbp[self.ptable]
            a = Ffind(data, self)
            if a.exec_() == QtGui.QDialog.Accepted:
                self.set(str(a.array[0]))

        elif data['rownum'] == 1:
            self.checkChange = False
            self.set(data['rows'][0][0])
