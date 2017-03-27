# -*- coding: utf-8 -*-
"""view_app module"""
import sys
import PyQt5.QtCore as Qc
import PyQt5.QtWidgets as Qw
from PyQt5.QtWidgets import QAction as Qa
import view_grid as vgrid
import model_table_sqlite as model_table
import sqlite3


class Main(Qw.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = Qc.QSettings()
        self.db = self.settings.value("db", defaultValue='')
        frame = Qw.QFrame(self)
        self.setCentralWidget(frame)
        main_layout = Qw.QVBoxLayout(frame)
        hlayout = Qw.QHBoxLayout()
        self.list = Qw.QListWidget(self)
        self.list.setMaximumWidth(150)
        hlayout.addWidget(self.list)
        self.grid = vgrid.ViewGrid(None)
        hlayout.addWidget(self.grid)
        main_layout.addLayout(hlayout)
        # self.list.clicked.connect(self.list_clicked)
        self.list.currentRowChanged.connect(self.list_currentRowChanged)
        self.setMinimumHeight(600)
        self.createActions()
        self.fill_list()

    def list_currentRowChanged(self, idx):
        try:
            tbl = self.list.currentItem().text()
            self.model = model_table.ModelTable(self.db, tbl)
            self.grid.setModel(self.model)
        except:
            pass

    def fill_list(self):
        self.list.clear()
        sqlt = ("SELECT name AS tname FROM sqlite_master WHERE type='table' "
                "ORDER BY name")
        con = sqlite3.connect(self.db)
        # con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sqlt)
        tables = list(cur.fetchall())
        cur.close()
        con.close()
        tblarr = []
        for tabl in tables:
            tblarr.append(tabl[0])
        self.list.addItems(tblarr)
        self.setWindowTitle(self.db)

    def createActions(self):
        self.openAct = Qa(u'Άνοιγμα αρχείου sqlite3', self)
        self.closeAct = Qa(u'Έξοδος', self)
        self.openAct.triggered.connect(self.open)
        self.closeAct.triggered.connect(self.close)
        self.fileMenu = self.menuBar().addMenu(u"Αρχείο")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.closeAct)

    def open(self):
        fname = Qw.QFileDialog.getOpenFileName(self, u'Επιλογή Αρχείου',
                                               self.db, u"Αρχείο (*.*)")
        print(fname)
        old_db = self.db
        if fname[0] == self.db:
            # filename is the same. Do nothing.
            return
        elif fname[0] == '':
            return
        else:
            self.db = fname[0]
            try:
                self.fill_list()
                self.settings.setValue("db", self.db)
            except:
                self.db = old_db
                self.fill_list()
        print('file open code here!!')


if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    app.setOrganizationName("tedlaz")
    app.setOrganizationDomain("tedlaz")
    app.setApplicationName("mvc")
    form = Main()
    form.show()
    sys.exit(app.exec_())
