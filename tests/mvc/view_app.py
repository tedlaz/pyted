# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import view_grid as vgrid
import model_table_sqlite as model_table
import sqlite3


class Main(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.settings = QtCore.QSettings()

        self.db = '%s' % self.settings.value("db", defaultValue='').toString()
        frame = QtGui.QFrame(self)
        self.setCentralWidget(frame)
        main_layout = QtGui.QVBoxLayout(frame)
        hlayout = QtGui.QHBoxLayout()
        self.list = QtGui.QListWidget(self)
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
        sqlt = "SELECT name AS tname FROM sqlite_master WHERE type='table' "
        sqlt += "ORDER BY name"
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
        self.openAct = QtGui.QAction(u'Άνοιγμα αρχείου sqlite3', self)
        self.closeAct = QtGui.QAction(u'Κλείσιμο εφαρμογής', self)
        self.openAct.triggered.connect(self.open)
        self.closeAct.triggered.connect(self.close)
        self.fileMenu = self.menuBar().addMenu(u"Αρχείο")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.closeAct)

    def open(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, u'Επιλογή Αρχείου',
                                                  self.db, u"Αρχείο (*.*)")
        old_db = self.db
        if fname:
            self.db = '%s' % fname
            try:
                self.fill_list()
                self.settings.setValue("db", self.db)
            except:
                self.db = old_db
                self.fill_list()
        print('file open code here!!')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("tedlaz")
    app.setOrganizationDomain("tedlaz")
    app.setApplicationName("mvc")
    form = Main()
    form.show()
    sys.exit(app.exec_())
