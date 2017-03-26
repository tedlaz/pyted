#!/usr/bin/env python
from PyQt4 import QtGui,QtCore
import sys
class TerminalViewer(QtGui.QWidget):
  def __init__(self,parent=None):
    QtGui.QWidget.__init__(self,parent)
    #self.Label = QtGui.QLabel("Waiting for Something",self)
    self.pb = QtGui.QProgressBar(self)
    self.pb.setValue(0)
    self.bu = QtGui.QPushButton("Go for it")
    self.str = "dokimi"
    layout  = QtGui.QVBoxLayout()
    layout.addWidget(self.pb)
    layout.addWidget(self.bu)
    self.setLayout(layout)
    self.DataCollector = TerminalX(self)
    self.connect(self.DataCollector,QtCore.SIGNAL("Activated1 ( QString ) "), self.Activated)
    self.connect(self.bu, QtCore.SIGNAL("clicked()"),self.run)
    
  def run(self):
    self.DataCollector.start()

  def Activated(self,newtext):
    self.pb.setValue(int(newtext))

  def closeEvent(self,e):
    e.accept()
    app.exit()

class TerminalX(QtCore.QThread):
  def __init__(self,parent=None):
    QtCore.QThread.__init__(self,parent)
    self.test = 0
    self.par = parent.str
  def run(self):
    print self.par
    print "Runing ..."
    self.test = 1
    while self.test < 50000:
      self.test += 1
      a = self.test * 100 / 50000
      self.emit(QtCore.SIGNAL("Activated1( QString )"),'%s' % a)

class TedEmit(QtCore.QThread):
  def __init__(self,parent=None):
    QtCore.QThread.__init__(self,parent)
    self.test = ''
  def run(self):
    while self.test != 'q':
      self.test = raw_input('enter data: ')
      self.emit(QtCore.SIGNAL("Activated( QString )"),self.test)
app = QtGui.QApplication(sys.argv)
qb = TerminalViewer()
qb.show()
sys.exit(app.exec_())

