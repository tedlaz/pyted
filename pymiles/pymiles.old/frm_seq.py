# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from frm_data import Fdata
from fld_selector import makefld


class Fsequencial(Fdata):

    def create_gui(self):
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        # Create Fields
        layout = QtGui.QFormLayout()
        self.widgets.append({})
        for fld in self.meta["order"]:
            # create widgets
            widg = self.meta["fields"][fld].get('qt', 'mala')
            self.widgets[0][fld] = makefld(widg, fld, self)
            # Create labels
            if fld not in self.invisible_fields:
                lblv = self.meta["fields"][fld]['lbl']
                # Add them to layout
                layout.addRow(QtGui.QLabel(lblv), self.widgets[0][fld])
            else:
                self.widgets[0][fld].setVisible(False)
            # Set ReadOnly True or False
            #self.widgets[0][fld].setReadOnly(self.readonly)
        # Special treatment for id (Mostly we don't want user interaction)
        self.widgets[0]['id'].setReadOnly(True)
        self.layout.addLayout(layout)



        # Create bottom buttons
        if not self.visible_buttons:
            return
        layout = QtGui.QHBoxLayout()
        b_ok_lbl = u'Αποθήκευση'
        '''
        if self.meta['mode'] == 'edit':
            b_ok_lbl = u'Αποθήκευση'
        elif self.meta['mode'] == 'search':
            b_ok_lbl = u'Αναζήτηση'
        else:
            b_ok_lbl = u'κενο'
        '''
        self.b_ok = QtGui.QPushButton(b_ok_lbl)
        self.b_cancel = QtGui.QPushButton(u'Ακύρωση')
        layout.addWidget(self.b_cancel)
        self.b_cancel.setFocusPolicy(0)
        self.b_ok.setFocusPolicy(0)
        layout.addWidget(self.b_ok)
        self.layout.addLayout(layout)
        self.b_ok.clicked.connect(self.saveit)
        self.b_cancel.clicked.connect(self.closeit)
