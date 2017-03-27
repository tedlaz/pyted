# -*- coding: utf-8 -*-
# from PyQt4 import QtGui
# import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw
import view_form


class ViewGrid(Qw.QDialog):

    def __init__(self, model, parent=None):
        # Qw.QDialog.__init__(self, parent)
        super().__init__(parent)

        self.setWindowTitle('ViewGrid')
        self.setMinimumWidth(500)
        layout = Qw.QVBoxLayout()
        btnlayout = Qw.QHBoxLayout()
        self.setLayout(layout)

        self.label = Qw.QLabel(u'Δοκιμή ..')
        font = Qg.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        layout.addWidget(self.label)

        self.tblView = Qw.QTableView()
        self.tblView.setAlternatingRowColors(True)
        self.tblView.setSelectionMode(Qw.QAbstractItemView.SingleSelection)
        self.tblView.setSelectionBehavior(Qw.QAbstractItemView.SelectRows)
        self.tblView.setEditTriggers(Qw.QAbstractItemView.NoEditTriggers)
        # self.tblView.setSortingEnabled(True)

        layout.addWidget(self.tblView)
        layout.addLayout(btnlayout)
        self.badd = Qw.QPushButton('Add New Record')
        btnlayout.addWidget(self.badd)
        self.tblView.setModel(model)
        self.tblView.doubleClicked.connect(self.showViewForm)
        self.badd.clicked.connect(self.addNewRecord)

    def addNewRecord(self):
        form = view_form.ViewForm(None, self)
        form.insertr()
        form.show()

    def showViewForm(self):
        form = view_form.ViewForm(self.tblView.currentIndex(), self)
        form.exec_()

    def model(self):
        return self.tblView.model()

    def setModel(self, model):
        self.tblView.setModel(model)
        self.label.setText(model._table)
        self.tblView.resizeColumnsToContents()
