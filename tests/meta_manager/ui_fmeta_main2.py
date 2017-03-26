# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tedlaz/python_work/meta_manager/fmeta_main2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tab = QtGui.QTabWidget(self.centralwidget)
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tab_tables = QtGui.QWidget()
        self.tab_tables.setObjectName(_fromUtf8("tab_tables"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab_tables)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableView = QtGui.QTableView(self.tab_tables)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.tab.addTab(self.tab_tables, _fromUtf8(""))
        self.tab_queries = QtGui.QWidget()
        self.tab_queries.setObjectName(_fromUtf8("tab_queries"))
        self.tab.addTab(self.tab_queries, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tab)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionNew)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Meta Manager", None))
        self.tab.setTabText(self.tab.indexOf(self.tab_tables), _translate("MainWindow", "Πίνακες", None))
        self.tab.setTabText(self.tab.indexOf(self.tab_queries), _translate("MainWindow", "Queries", None))
        self.menuFile.setTitle(_translate("MainWindow", "file", None))
        self.actionOpen.setText(_translate("MainWindow", "open", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))

