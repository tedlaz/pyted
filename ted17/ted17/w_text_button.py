# -*- coding: utf-8 -*-
'''
Created on Nov 25, 2014

@author: tedlaz.
'''
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
from .f_table import Form_find
from . import db as dbm
# from .grup import grup


class Text_button(Qw.QWidget):
    """Advanced control for foreign key fields

    :param val: the id value of foreign relation
    :param table: Table or View
    :param parent: The parent object

    .. warning:: Parent object must have db member

    """
    # SIGNALS HERE
    valNotFound = Qc.pyqtSignal(str)

    def __init__(self, val, table, parent):
        """Init"""
        super().__init__(parent)
        self.table = table  # the table or view name
        self.dbf = parent.dbf  # parent must have .dbf
        # create gui
        self.text = Qw.QLineEdit(self)
        self.button = Qw.QToolButton(self)
        self.button.setText('?')
        self.button.setFocusPolicy(Qc.Qt.NoFocus)
        layout = Qw.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.setLayout(layout)
        layout.addWidget(self.text)
        layout.addWidget(self.button)
        # connections
        self.text.textChanged.connect(self.text_changed)
        self.button.clicked.connect(self.button_clicked)
        # init gui as red and try to fill it with existing value from db
        self.red()
        self.set(val)

    def set(self, idv):
        self.val = dbm.find_by_id(self.dbf, idv, self.table, 'names-tuples')
        self.vap = self.txt_val()
        self.text.setText(self.vap)
        self.setToolTip(self.rpr_val())
        self.text.setCursorPosition(0)
        lval = len(self.val[1])
        if lval > 0:
            self.green()
        else:
            self.red()

    def txt_val(self):
        """[('id', 'fld1', ..), [(id0, f0, ...), ...]
        """
        atxt = []
        if self.val[1] == []:
            return ''
        for i, field in enumerate(self.val[0]):
            if field != 'id':
                atxt.append('%s' % self.val[1][0][i])
        return ' '.join(atxt)

    def rpr_val(self):
        """
        all fields: values of table mainly for tooltip use
        """
        atxt = ''
        if self.val[1] == []:
            return ''
        for i, field_name in enumerate(self.val[0]):
            atxt += '%s : %s\n' % (field_name, self.val[1][0][i])
        return atxt

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
        self.isGreen = True

    def red(self):
        self.button.setStyleSheet('background-color: rgba(239, 41, 41);')
        self.isGreen = False

    def keyPressEvent(self, ev):
        if ev.key() == Qc.Qt.Key_Enter or ev.key() == Qc.Qt.Key_Return:
            if self.vap != self.text.text():
                self.find(self.text.text())
        return Qw.QWidget.keyPressEvent(self, ev)

    def find(self, text):
        """
        :param text: text separated by space multi-search values 'va1 val2 ..'
        """
        oldvalue = self.get()
        vals = dbm.find(self.dbf, self.table, text, 'names-tuples')
        # print(vals)
        if len(vals[1]) == 1:
            # We assume that the first element of first tuple is id
            self.set(vals[1][0][0])
        elif len(vals[1]) > 1:
            ffind = Form_find(vals, u'Αναζήτηση', self)
            if ffind.exec_() == Qw.QDialog.Accepted:
                self.set(ffind.vals[0])
            else:
                if oldvalue == self.get():
                    pass
                else:
                    self.red()
        else:
            self.valNotFound.emit(self.text.text())
