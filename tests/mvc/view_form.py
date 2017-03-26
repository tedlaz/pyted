# -*- coding: utf-8 -*-
from PyQt4 import QtGui


class ViewForm(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setWindowTitle('ViewForm')
        self._dataMapper = QtGui.QDataWidgetMapper()
        self._dataMapper.setSubmitPolicy(QtGui.QDataWidgetMapper.ManualSubmit)
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        self.flayout = QtGui.QFormLayout()
        layout.addLayout(self.flayout)
        self.epo = QtGui.QLineEdit()
        self.ono = QtGui.QLineEdit()
        self.pat = QtGui.QLineEdit()
        self.mit = QtGui.QLineEdit()
        if parent:
            self.setModel(parent.model())
        hlayout = QtGui.QHBoxLayout()
        self.bsave = QtGui.QPushButton('save')
        self.bdel = QtGui.QPushButton('Delete')
        hlayout.addWidget(self.bsave)
        hlayout.addWidget(self.bdel)
        layout.addLayout(hlayout)
        self.makeConnections()
        self.setMinimumWidth(300)

    def setModel(self, model):
        self._model = model
        self._dataMapper.setModel(model)
        self._widgets = {}
        for i in range(self._model.cols()):
            lbl = self._model.header(i)
            self._widgets[i] = QtGui.QLineEdit()
            self.flayout.addRow(QtGui.QLabel(lbl), self._widgets[i])
            self._dataMapper.addMapping(self._widgets[i], i)
        self._widgets[0].setReadOnly(True)

    def makeConnections(self):
        self.bsave.clicked.connect(self.saveit)
        self.bdel.clicked.connect(self.delete)
        self._dataMapper.setCurrentModelIndex(self._model.index(0, 0))

    def mi(self, idx):
        self._dataMapper.setCurrentModelIndex(idx)

    def saveit(self):
        idx = self._dataMapper.currentIndex()
        self._dataMapper.submit()
        sizw = self._model.isNull(idx)
        if int(sizw) == 0:
            print('edo', sizw)
            self._model.removeRows(idx, 1)
            self.accept()
            return
        print(self._model.save2db(idx))
        self.accept()

    def insertr(self):
        idx = self._model.rows()
        self._model.insertRows(idx, 1)
        self._dataMapper.setCurrentModelIndex(self._model.index(idx, 0))

    def delete(self):
        idx = self._dataMapper.currentIndex()
        sizw = self._model.isNull(idx)
        if int(sizw) == 0:
            print('edo', sizw)
            self._model.removeRows(idx, 1)
            self.accept()
            return
        self._model.deleteFromDb(idx)
        self.accept()

    def closeEvent(self, event):
        self.saveit()
