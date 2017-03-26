# -*- coding: utf-8 -*-
'''
Created on Nov 25, 2014

@author: tedlaz.
'''
from PyQt4 import QtGui, QtCore, Qt
import fld__parameters as par
from frm_find import Ffind
import u_db_helper as dbh


class Button_text(QtGui.QLineEdit):

    """Button text class """

    def __init__(self, id_, name, parent=None):
        super(Button_text, self).__init__(parent)
        # self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        # Create visible controls
        self.button = QtGui.QToolButton(self)

        self.parent = parent
        self.status = False
        if parent:
            self.db = parent.db
        self.name = name
        self.ptable = self.name[:-3]  # parent_id minus _id = parent
        self.pfield = self.ptable + '_rp'
        self.psql = self.parent.tables[self.ptable]['rpr']

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
        self.set(id_)

    def resizeEvent(self, event):
        button_size = self.button.sizeHint()
        f_width = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.button.move(
            self.rect().right() - f_width - button_size.width(),
            (self.rect().bottom() - button_size.height() + 1)/2)
        super(Button_text, self).resizeEvent(event)

    def set(self, val):
        if not val:
            self.setStatus(self.setErr())
            self.fld1v = None
            self.id = '0'
            return
        self.id = val
        sql_parent = "%s WHERE id=%s" % (self.psql, val)
        result = dbh.select(self.db, sql_parent)

        self.fld1v = result['rows'][0][self.pfield]
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
        tmplbls = []
        metaparent = self.parent.tables[self.ptable]
        if self.hasFocus():
            pytxt = u'%s' % self.text()  # Convert it to python text
            data = dbh.sql_where(self.db, self.psql, {self.pfield: pytxt})
            tmplbls = [u'ΑΑ', metaparent["title"]]
        else:
            # sql = "SELECT * FROM %s" % self.name[:-3]
            data = dbh.table_vals(self.db, self.ptable, False)

            metaparent = self.parent.tables[self.ptable]
            metaparent['fields']['id'] = {'lbl': u'ΑΑ'}
            for field in metaparent['order']:
                tmplbls.append(metaparent['fields'][field].get('lbl', 'aa'))

        data['labels'] = tmplbls

        if data['rownum'] > 1:
            a = Ffind(data, self)
            if a.exec_() == QtGui.QDialog.Accepted:
                try:
                    # print('------>%s' % a.array[0])
                    self.set(a.array[0])
                except:
                    self.set(None)
        elif data['rownum'] == 1:
            self.checkChange = False
            self.set(data['rows'][0][0])
