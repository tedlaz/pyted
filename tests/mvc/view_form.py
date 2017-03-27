# -*- coding: utf-8 -*-
# from PyQt4 import QtGui
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtWidgets as Qw


class ViewForm(Qw.QDialog):
    def __init__(self, idx, parent=None):
        # Qw.QDialog.__init__(self, parent)
        super().__init__(parent)
        self.setWindowTitle('ViewForm')
        self._dataMapper = Qw.QDataWidgetMapper()
        self._dataMapper.setSubmitPolicy(Qw.QDataWidgetMapper.ManualSubmit)
        layout = Qw.QVBoxLayout()
        self.setLayout(layout)
        self.flayout = Qw.QFormLayout()
        layout.addLayout(self.flayout)
        self.epo = Qw.QLineEdit()
        self.ono = Qw.QLineEdit()
        self.pat = Qw.QLineEdit()
        self.mit = Qw.QLineEdit()
        self.index = idx
        if parent:
            self.setModel(parent.model())
        hlayout = Qw.QHBoxLayout()
        self.bsave = Qw.QPushButton('save')
        self.bdel = Qw.QPushButton('Delete')
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
            self._widgets[i] = Qw.QLineEdit()
            self.flayout.addRow(Qw.QLabel(lbl), self._widgets[i])
            self._dataMapper.addMapping(self._widgets[i], i)
        self._widgets[0].setReadOnly(True)

    def makeConnections(self):
        self.bsave.clicked.connect(self.saveit)
        self.bdel.clicked.connect(self.delete)
        if self.index:
            self._dataMapper.setCurrentModelIndex(self.index)

    def saveit(self):
        idx = self._dataMapper.currentIndex()
        self._dataMapper.submit()
        sizw = self._model.isNull(idx)
        if int(sizw) == 0:
            print('sizw is zero', sizw)
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
            print('sizw is zero', sizw)
            self._model.removeRows(idx, 1)
            self.accept()
            return
        self._model.deleteFromDb(idx)
        self.accept()

    def closeEvent(self, event):
        self.saveit()
