# -*- coding: utf-8 -*-
'''
Created on Nov 25, 2014

@author: tedlaz.
'''
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from .f_table import Form_find
from . import db as dbm

from .grup import grup


class Text_button(Qw.QWidget):
    """Button text class """
    # SIGNALS HERE
    valNotFound = Qc.pyqtSignal(str)

    def __init__(self, val, table, parent):
        '''
        val : The actual value
        '''
        super().__init__(parent)
        self.table = table
        self.dbm = dbm.SqliteManager(parent.db)
        self.text = Qw.QLineEdit(self)
        self.button = Qw.QToolButton(self)
        layout = Qw.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.setLayout(layout)
        layout.addWidget(self.text)
        layout.addWidget(self.button)
        self.red()  # We start with red Button
        self.text.textChanged.connect(self.text_changed)
        self.button.setFocusPolicy(Qc.Qt.NoFocus)
        self.button.clicked.connect(self.button_clicked)
        self.find_record(val)

    def _set(self, dic_from_db, isGreen):
        self.val = dic_from_db
        self.vap = self.txt_val()
        self.text.setText(self.vap)
        self.setToolTip(self.rpr_val())
        self.text.setCursorPosition(0)
        if isGreen:
            self.green()
        else:
            self.red()

    def txt_val(self):
        atxt = ''
        for i, field in enumerate(self.val[0]):
            if field != 'id':
                atxt += '%s ' % self.val[1][0][i]
        return atxt

    def rpr_val(self):
        atxt = ''
        for i, field_name in enumerate(self.val[0]):
            atxt += '%s : %s\n' % (field_name, self.val[1][0][i])
        return atxt

    def find_record(self, idval):
        """Find a record by its id value

        :param idval: id value of record
        """
        if not idval:
            self._set(None, False)
        else:
            dic_from_db = self.dbm.find_record_by_id(self.table,
                                                     idval,
                                                     'names-tuples')
            if dic_from_db:
                self._set(dic_from_db, True)
            else:
                # There is not an rpr from database
                self._set(None, False)

    def get(self):
        field_names, vals = self.val
        if 'id' not in field_names:
            return ''
        id_index = field_names.index('id')
        if self.isGreen:
            return '%s' % vals[0][id_index]
        else:
            return ''

    def text_changed(self):
        if self.vap != self.text.text():
            self.red()
        else:
            self.green()

    def button_clicked(self):
        self.button.setFocus()
        self.find('')

    def green(self):
        self.button.setStyleSheet('background-color: rgba(0, 180, 0);')
        self.button.setText('?')
        self.isGreen = True

    def red(self):
        self.button.setStyleSheet('background-color: rgba(239, 41, 41);')
        self.button.setText('?')
        self.isGreen = False

    def keyPressEvent(self, ev):
        if ev.key() == Qc.Qt.Key_Enter or ev.key() == Qc.Qt.Key_Return:
            if self.vap != self.text.text():
                self.find(self.text.text())
        return Qw.QWidget.keyPressEvent(self, ev)

    def find(self, text):
        oldvalue = self.get()
        vals = self.dbm.find_records(self.table, text, 'names-tuples')
        if len(vals[1]) == 1:
            self._set(vals, True)
        elif len(vals[1]) > 1:
            tf = Form_find(vals[0], vals[1], u'Αναζήτηση', self)
            if tf.exec_() == Qw.QDialog.Accepted:
                self.find_record(tf.vals[0])
            else:
                if oldvalue == self.get():
                    pass
                else:
                    self.red()
        else:
            self.valNotFound.emit(self.text.text())
