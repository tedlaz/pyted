# -*- coding: utf-8 -*-

from PyQt4 import QtGui, Qt
from frm_seq import Fsequencial
from frm_grid import Fgrid
from u_db_sql import save_one_many as sql_many
from u_db_save import save_one_many as save_many


class Fmaster_detail(QtGui.QDialog):

    def __init__(self,
                 tables,
                 master,
                 detail,
                 id_=None,
                 parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setAttribute(Qt.Qt.WA_DeleteOnClose)
        self.setMinimumWidth(350)

        self.tblmaster = master
        self.tbldetail = detail
        self.id = id_

        if parent:
            self.db = parent.db
        else:
            self.db = 'tst.sql3'

        self.con_key = "%s_id" % master

        blayout = QtGui.QVBoxLayout()
        self.master = Fsequencial(tables,
                                  master,
                                  id_,
                                  'one',
                                  False,
                                  ['id'],
                                  self)

        self.detail = Fgrid(tables,
                            detail,
                            None,
                            'manywhere',
                            False,
                            ['id', self.con_key],
                            self,
                            [self.con_key, self.id]
                            )
        blayout.addWidget(self.master)
        blayout.addWidget(self.detail)
        self.setLayout(blayout)

        self.setWindowTitle('%s / %s' % (self.master.title, self.detail.title))

        # Add Buttons
        layout = QtGui.QHBoxLayout()
        b_ok_lbl = u'Αποθήκευση'

        self.b_ok = QtGui.QPushButton(b_ok_lbl)
        self.b_cancel = QtGui.QPushButton(u'Ακύρωση')
        self.b_add = QtGui.QPushButton(u'Νέα γραμμή')
        layout.addWidget(self.b_cancel)
        layout.addWidget(self.b_add)
        self.b_add.setFocusPolicy(0)
        self.b_cancel.setFocusPolicy(0)
        self.b_ok.setFocusPolicy(0)
        layout.addWidget(self.b_ok)
        blayout.addLayout(layout)
        self.b_ok.clicked.connect(self.saveit)
        self.b_add.clicked.connect(self.on_add_row)
        self.b_cancel.clicked.connect(self.close)

    def on_ok(self):
        self.master.saveit()
        self.detail.saveit()

    def on_add_row(self):
        self.detail.add_row()
        rowindex = self.detail.grid.rowCount() - 1
        self.detail.widgets[rowindex][self.con_key].set(self.id)

    def saveit(self):
        if self.id:
            self.on_ok()
            self.accept()
            return
        # To connect with action or button
        # Saves data or searches or ...
        fdicm = self.master.widget_to_dict()[0]  # {fld: value, ..}
        fdicd = self.detail.widget_to_dict()
        sql = sql_many(self.tblmaster, fdicm, self.tbldetail, fdicd)
        save_many(self.db, sql)
        self.close()
