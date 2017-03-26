# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from frm_data import Fdata
from fld_selector import makefld


class Fgrid(Fdata):

    def create_gui(self):
        self.setMinimumWidth(800)
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        self.grid = QtGui.QTableWidget(self)
        self.layout.addWidget(self.grid)

        # Get data dimensions (How many columns , rows)
        self.grid.setColumnCount(len(self.meta['fields']))

        # Set column titles
        labels = []
        for i, fld in enumerate(self.meta["order"]):
            labels.append(self.meta["fields"][fld]['lbl'])
            if fld in self.invisible_fields:
                self.grid.setColumnHidden(i, True)
        self.grid.setHorizontalHeaderLabels(labels)
        self.grid.setColumnWidth(0, 30)
        # Create widgets
        for i in range(len(self.data['rows'])):
            self.add_row()

        # Create bottom buttons
        if not self.visible_buttons:
            return
        layout = QtGui.QHBoxLayout()
        b_ok_lbl = u'Αποθήκευση'

        self.b_ok = QtGui.QPushButton(b_ok_lbl)
        self.b_cancel = QtGui.QPushButton(u'Ακύρωση')
        self.b_add = QtGui.QPushButton(u'Νέα εγγραφή')
        layout.addWidget(self.b_cancel)
        layout.addWidget(self.b_add)
        self.b_add.setFocusPolicy(0)
        self.b_cancel.setFocusPolicy(0)
        self.b_ok.setFocusPolicy(0)
        layout.addWidget(self.b_ok)
        self.layout.addLayout(layout)
        self.b_ok.clicked.connect(self.saveit)
        self.b_add.clicked.connect(self.add_row)
        self.b_cancel.clicked.connect(self.closeit)

    def add_row(self):
        trows = self.grid.rowCount()
        self.grid.setRowCount(trows + 1)
        self.widgets.append({})
        for j, fld in enumerate(self.meta["order"]):
            widg = self.meta["fields"][fld].get('qt', 'noval')
            self.widgets[trows][fld] = makefld(widg, fld, self)
            self.grid.setCellWidget(trows, j, self.widgets[trows][fld])
            if fld in self.invisible_fields:
                self.widgets[trows][fld].setVisible(False)
        self.grid.resizeColumnsToContents()
        # self.grid.setColumnWidth(0,50)
