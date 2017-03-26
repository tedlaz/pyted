# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import view_form


class ViewGrid(QtGui.QDialog):

    def __init__(self, model, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setWindowTitle('ViewGrid')
        self.setMinimumWidth(500)
        layout = QtGui.QVBoxLayout()
        btnlayout = QtGui.QHBoxLayout()
        self.setLayout(layout)

        self.label = QtGui.QLabel(u'Δοκιμή ..')
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        layout.addWidget(self.label)

        self.tblView = QtGui.QTableView()
        self.tblView.setAlternatingRowColors(True)
        self.tblView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        # self.tblView.setSortingEnabled(True)

        layout.addWidget(self.tblView)
        layout.addLayout(btnlayout)
        self.badd = QtGui.QPushButton('Add New Record')
        btnlayout.addWidget(self.badd)
        self.tblView.setModel(model)
        self.tblView.doubleClicked.connect(self.showViewForm)
        self.badd.clicked.connect(self.addNewRecord)

    def addNewRecord(self):
        form = view_form.ViewForm(self)
        form.insertr()
        # self.tblView.clicked.connect(form.mi)
        form.show()

    def showViewForm(self):
        form = view_form.ViewForm(self)
        self.tblView.clicked.connect(form.mi)
        form.exec_()

    def model(self):
        return self.tblView.model()

    def setModel(self, model):
        self.tblView.setModel(model)
        self.label.setText(model._table)
        self.tblView.resizeColumnsToContents()
